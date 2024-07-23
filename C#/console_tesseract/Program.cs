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

        var ocr = new TesseractEngine(@"./tessdata", "por", EngineMode.Default);

        foreach (var imagePath in imageFiles)
        {
            var pix = Pix.LoadFromFile(imagePath);
            var page = ocr.Process(pix);

            string text = page.GetText();
            Console.WriteLine("Texto Reconhecido para {0}: {1}", imagePath, text);

            string textFilePath = Path.ChangeExtension(imagePath, ".txt");

            File.WriteAllText(textFilePath, text);
        }
    }
}
