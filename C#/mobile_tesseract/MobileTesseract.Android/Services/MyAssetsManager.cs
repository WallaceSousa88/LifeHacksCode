using Android.Content.Res;
using MobileTesseract;
using MobileTesseract.Droid.Services;
using System.IO;
using System.Reflection;

[assembly: Xamarin.Forms.Dependency(typeof(MyAssetsManager))]
namespace MobileTesseract.Droid.Services
{
    public class MyAssetsManager : IAssetsManager
    {
        public string GetAssetsPath()
        {
            return "tessdata";
        }

        public Stream GetAssetStream(string filename)
        {
            AssetManager assets = Android.App.Application.Context.Assets;
            return assets.Open(filename);
        }
    }
}