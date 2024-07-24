using System;
using System.IO;
using System.Linq;
using Tesseract;

class Program
{
    static void Main()
    {
        string directoryPath = @"C:\x";
        var allFiles = Directory.GetFiles(directoryPath);

        var imageFiles = allFiles.Where(file => file.EndsWith(".jpg") || file.EndsWith(".jpeg") || file.EndsWith(".png")).ToArray();

        var ocr = new TesseractEngine(@"C:\x\tessdata", "por", EngineMode.Default);

        foreach (var imagePath in imageFiles)
        {
            try
            {
                Console.WriteLine($"Processando imagem: {imagePath}");

                using (var pix = Pix.LoadFromFile(imagePath))
                {
                    using (var page = ocr.Process(pix))
                    {
                        string text = page.GetText();

                        string textFilePath = Path.ChangeExtension(imagePath, ".txt");
                        File.WriteAllText(textFilePath, text);

                        Console.WriteLine($"Texto salvo em: {textFilePath}");
                    }
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Erro ao processar {imagePath}: {ex.Message}");
            }
        }

        Console.WriteLine("Processamento concluído.");
    }
}