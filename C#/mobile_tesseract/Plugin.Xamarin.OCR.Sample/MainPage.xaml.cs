using System;
using System.IO;
using System.Threading.Tasks;
using Xamarin.Essentials;
using Xamarin.Forms;
using System.Text.RegularExpressions;
using System.Collections.Generic;

namespace Plugin.Xamarin.OCR.Sample
{
    public partial class MainPage : ContentPage
    {
        private OcrResult _resultadoOCR;
        private int _larguraReal;
        private int _alturaReal;

        private readonly IOcrService _ocr;

        public MainPage() : this(DependencyService.Get<IOcrService>())
        {
        }

        public MainPage(IOcrService? ocr)
        {
            InitializeComponent();
            _ocr = ocr ?? OcrPlugin.Default;
        }

        protected override async void OnAppearing()
        {
            base.OnAppearing();
            await _ocr.InitAsync();
        }

        private void LimparBtn_Clicked(object sender, EventArgs e)
        {
            ResultadoLbl.Text = string.Empty;
            LimparBtn.IsEnabled = false;
            CopiarBtn.IsEnabled = false;
            ImagemSelecionada.Source = null;
        }

        private async void AbrirDaCameraBtn_Clicked(object sender, EventArgs e)
        {
            if (MediaPicker.IsCaptureSupported)
            {
                var foto = await MediaPicker.CapturePhotoAsync();

                if (foto != null)
                {
                    var resultado = await ProcessarFoto(foto);
                    LimparBtn.IsEnabled = true;
                    CopiarBtn.IsEnabled = true;
                }
            }
            else
            {
                await DisplayAlert("Erro", "A captura de imagem não é suportada neste dispositivo.", "OK");
            }
        }

        private async void AbrirDoArquivoBtn_Clicked(object sender, EventArgs e)
        {
            var foto = await MediaPicker.PickPhotoAsync();

            if (foto != null)
            {
                var resultado = await ProcessarFoto(foto);
                LimparBtn.IsEnabled = true;
                CopiarBtn.IsEnabled = true;
            }
        }

        private async void CopiarBtn_Clicked(object sender, EventArgs e)
        {
            await Clipboard.SetTextAsync(ResultadoLbl.Text);
        }

        private async Task<OcrResult> ProcessarFoto(FileResult foto)
        {
            using var fluxoFonte = await foto.OpenReadAsync();
            var dadosImagem = new byte[fluxoFonte.Length];
            await fluxoFonte.ReadAsync(dadosImagem, 0, dadosImagem.Length);

            var fonteImagem = ImageSource.FromStream(() => new MemoryStream(dadosImagem));
            ImagemSelecionada.Source = fonteImagem;

            var resultadoOCR = await _ocr.RecognizeTextAsync(dadosImagem, false);

            if (resultadoOCR.AllText.Length == 0)
            {
                ResultadoLbl.Text = "Erro: Nenhum texto encontrado na imagem.";
                return resultadoOCR;
            }

            var regex = new Regex(@"\b\d{5}\b");
            var matches = regex.Matches(resultadoOCR.AllText);

            if (matches.Count == 0)
            {
                ResultadoLbl.Text = "Erro: Nenhum número de 5 dígitos encontrado.";
                return resultadoOCR;
            }

            List<string> numerosCincoDigitos = new List<string>();
            foreach (Match match in matches)
            {
                numerosCincoDigitos.Add(match.Value);
            }

            ResultadoLbl.Text = string.Join(", ", numerosCincoDigitos);

            _resultadoOCR = resultadoOCR;
            return resultadoOCR;
        }

        private double ConverterParaPixels(double unidadesXamarinForms)
        {
            var densidadeTela = DeviceDisplay.MainDisplayInfo.Density;
            return unidadesXamarinForms * densidadeTela;
        }
    }
}