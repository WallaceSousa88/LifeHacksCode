using System;
using System.IO;
using System.Threading.Tasks;
using Xamarin.Forms;
using Xamarin.Essentials;
using Tesseract;
using System.Drawing;

namespace MobileTesseract
{
    public partial class MainPage : ContentPage
    {
        public MainPage()
        {
            InitializeComponent();
        }

        private async void OnPickImageClicked(object sender, EventArgs e)
        {
            try
            {
                var result = await MediaPicker.PickPhotoAsync(new MediaPickerOptions
                {
                    Title = "Selecione uma Imagem"
                });

                if (result != null)
                {
                    using (var stream = await result.OpenReadAsync())
                    {
                        byte[] imageBytes;
                        using (var memoryStream = new MemoryStream())
                        {
                            await stream.CopyToAsync(memoryStream);
                            imageBytes = memoryStream.ToArray();
                        }

                        ImagePreview.Source = ImageSource.FromStream(() => new MemoryStream(imageBytes));

                        await RecognizeTextFromBytes(imageBytes);
                    }
                }
            }
            catch (Exception ex)
            {
                await DisplayAlert("Erro", $"Erro ao selecionar imagem: {ex.Message}", "OK");
            }
        }

        private async Task RecognizeTextFromBytes(byte[] imageBytes)
        {
            await Task.Run(async () =>
            {
                try
                {
                    var assetsManager = DependencyService.Get<IAssetsManager>();
                    string tessdataPath = assetsManager.GetAssetsPath();

                    using (var engine = new TesseractEngine(tessdataPath, "por", EngineMode.Default))
                    {
                        using (var image = Pix.LoadFromMemory(imageBytes))
                        {
                            using (var page = engine.Process(image))
                            {
                                var recognizedText = page.GetText();

                                Device.BeginInvokeOnMainThread(async () =>
                                {
                                    await SaveTextToFile(recognizedText);
                                    await DisplayAlert("Texto Reconhecido", recognizedText, "OK");
                                });
                            }
                        }
                    }
                }
                catch (Exception ex)
                {
                    Device.BeginInvokeOnMainThread(async () =>
                    {
                        await DisplayAlert("Erro", $"Erro ao reconhecer texto: {ex.Message}", "OK");
                    });
                }
            });
        }

        private async Task SaveTextToFile(string text)
        {
            try
            {
                var fileName = $"recognized_text_{DateTime.Now:yyyyMMdd_HHmmss}.txt";
                var folderPath = Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments);
                var filePath = Path.Combine(folderPath, fileName);

                using (var writer = new StreamWriter(filePath, true))
                {
                    await writer.WriteLineAsync(text);
                }

                await DisplayAlert("Sucesso", $"Texto salvo em: {filePath}", "OK");
            }
            catch (Exception ex)
            {
                await DisplayAlert("Erro", $"Erro ao salvar texto: {ex.Message}", "OK");
            }
        }
    }

    public interface IAssetsManager
    {
        string GetAssetsPath();
        Stream GetAssetStream(string filename);
    }
}