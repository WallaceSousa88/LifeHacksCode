using System;
using Xamarin.Forms;
using Xamarin.Forms.Xaml;

#if __IOS__
[assembly: Dependency(typeof(MobileTesseract.iOS.Services.MyAssetsManager))] 
#endif

namespace MobileTesseract
{
    public partial class App : Application
    {
        public App()
        {
            InitializeComponent();

            MainPage = new MainPage();
        }

        protected override void OnStart()
        {
        }

        protected override void OnSleep()
        {
        }

        protected override void OnResume()
        {
        }
    }
}