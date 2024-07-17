using System;
using Xamarin.Forms;
using IronOcr;
using Plugin.Media.Abstractions;

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
            try
            {
                var file = await Plugin.Media.CrossMedia.Current.PickPhotoAsync(new PickMediaOptions
                {
                    PhotoSize = PhotoSize.Medium
                });

                if (file == null)
                    return;

                var ocr = new IronTesseract();
                using (var input = new OcrInput(file.GetStream()))
                {
                    var result = ocr.Read(input);
                    var recognizedText = result.Text;

                    var editor = this.FindByName<Editor>("ResultadoOCR");
                    editor.Text = recognizedText;
                }
            }
            catch (Exception ex)
            {
                await DisplayAlert("Erro", $"Ocorreu um erro: {ex.Message}", "OK");
            }
        }
    }
}