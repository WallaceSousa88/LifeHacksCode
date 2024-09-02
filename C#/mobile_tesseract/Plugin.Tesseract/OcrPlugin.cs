using System;
using Plugin.Tesseract;

namespace Plugin.Tesseract
{
    public static class OcrPlugin
    {
        private static IOcrService? s_defaultImplementation;

        public static IOcrService Default
        {
            get
            {
                return s_defaultImplementation ??= new OcrImplementation();
            }
        }

        internal static void SetDefault(IOcrService? implementation) =>
            s_defaultImplementation = implementation;
    }
}
