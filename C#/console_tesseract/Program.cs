using System;
using Tesseract;

namespace ConsoleTesseract
{
    class Program
    {
        static void Main(string[] args)
        {
            if (args.Length == 0)
            {
                Console.WriteLine("Informe o caminho da imagem como argumento.");
                return;
            }

            string caminhoImagem = args[0];

            try
            {
                string texto = ExtrairTexto(caminhoImagem);
                Console.WriteLine("Texto reconhecido:");
                Console.WriteLine(texto);
            }
            catch (Exception ex)
            {
                Console.WriteLine("Erro ao processar a imagem: " + ex.Message);
            }
        }

        static string ExtrairTexto(string caminhoImagem)
        {
            using var engine = new TesseractEngine(@"./tessdata", "eng", EngineMode.Default);
            using var img = Pix.LoadFromFile(caminhoImagem);
            using var page = engine.Process(img);
            return page.GetText();
        }
    }
}
