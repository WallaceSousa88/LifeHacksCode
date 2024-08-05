using Foundation;
using MobileTesseract;
using System.IO;

namespace MobileTesseract.iOS.Services
{
    public class MyAssetsManager : IAssetsManager
    {
        public string GetAssetsPath()
        {
            return NSBundle.MainBundle.PathForResource("tessdata", null);
        }

        public Stream GetAssetStream(string filename)
        {
            string path = Path.Combine(GetAssetsPath(), filename);
            return File.Open(path, FileMode.Open);
        }
    }
}