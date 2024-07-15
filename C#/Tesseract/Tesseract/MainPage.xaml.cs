using System;
using Xamarin.Forms;

namespace Tesseract
{
    public partial class MainPage : ContentPage
    {
        public MainPage()
        {
            InitializeComponent();
        }

        private async void OnSelectImageClicked(object sender, EventArgs e)
        {
            // 1. Lógica para selecionar a imagem
            var file = await Plugin.Media.CrossMedia.Current.PickPhotoAsync(new Plugin.Media.Abstractions.PickMediaOptions
            {
                PhotoSize = Plugin.Media.Abstractions.PhotoSize.Medium
            });

            if (file == null)
                return;

            // 2. Integrar o Tesseract para extrair o texto
            // ** Certifique-se de instalar o pacote NuGet do Tesseract **
            // ** e configurar o Tesseract para sua plataforma **
            var recognizedText = await Tesseract.Ocr.Recognize(file.GetStream());

            // 3. Exibir o texto extraído no Editor
            var editor = this.FindByName<Editor>("TextoEditor"); // Substitua "TextoEditor" pelo nome do seu Editor no XAML
            editor.Text = recognizedText;
        }
    }
}