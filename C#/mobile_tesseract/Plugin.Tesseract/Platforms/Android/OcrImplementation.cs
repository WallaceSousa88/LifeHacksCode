using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Threading;
using System.Threading.Tasks;
using Android.Gms.Tasks;
using Android.Graphics;
using Android.Util;
using Xamarin.Google.MLKit.Common;
using Xamarin.Google.MLKit.Vision.Common;
using Xamarin.Google.MLKit.Vision.Text;
using Xamarin.Google.MLKit.Vision.Text.Latin;
using static Plugin.Tesseract.OcrResult;
using Task = System.Threading.Tasks.Task;
using Plugin.Tesseract;

namespace Plugin.Tesseract
{
    public class OcrImplementation : IOcrService
    {
        private static readonly IReadOnlyCollection<string> s_supportedLanguages = new List<string>
        {
            "en", "pt"
        };

        public IReadOnlyCollection<string> SupportedLanguages => s_supportedLanguages;

        public event EventHandler<OcrCompletedEventArgs> RecognitionCompleted;

        public static OcrResult ProcessOcrResult(Java.Lang.Object result, OcrOptions? options = null)
        {
            var ocrResult = new OcrResult();
            var textResult = (Text)result;

            ocrResult.AllText = textResult.GetText();
            foreach (var block in textResult.TextBlocks)
            {
                foreach (var line in block.Lines)
                {
                    foreach (var element in line.Elements)
                    {
                        var ocrElement = new OcrElement
                        {
                            Text = element.Text,
                            Confidence = element.Confidence,
                        };
                        ocrResult.Elements.Add(ocrElement);
                    }
                }
            }

            if (options?.PatternConfigs != null)
            {
                foreach (var config in options.PatternConfigs)
                {
                    var match = OcrPatternMatcher.ExtractPattern(ocrResult.AllText, config);
                    if (!string.IsNullOrEmpty(match))
                    {
                        ocrResult.MatchedValues.Add(match);
                    }
                }
            }

            options?.CustomCallback?.Invoke(ocrResult.AllText);

            ocrResult.Success = true;
            return ocrResult;
        }

        public Task InitAsync(CancellationToken ct = default)
        {
            return Task.CompletedTask;
        }

        public async Task<OcrResult> RecognizeTextAsync(byte[] imageData, CancellationToken ct = default)
        {
            return await RecognizeTextAsync(imageData, new OcrOptions(), ct);
        }

        public async Task<OcrResult> RecognizeTextAsync(byte[] imageData, OcrOptions options, CancellationToken ct = default)
        {
            using var image = await BitmapFactory.DecodeByteArrayAsync(imageData, 0, imageData.Length);
            using var inputImage = InputImage.FromBitmap(image, 0);

            ITextRecognizer textScanner = TextRecognition.GetClient(TextRecognizerOptions.DefaultOptions);
            var result = await ToAwaitableTask(textScanner.Process(inputImage).AddOnSuccessListener(new OnSuccessListener()).AddOnFailureListener(new OnFailureListener()));
            return ProcessOcrResult(result, options);
        }

        private static Task<Java.Lang.Object> ToAwaitableTask(global::Android.Gms.Tasks.Task task)
        {
            var taskCompletionSource = new TaskCompletionSource<Java.Lang.Object>();
            var taskCompleteListener = new TaskCompleteListener(taskCompletionSource);
            task.AddOnCompleteListener(taskCompleteListener);

            return taskCompletionSource.Task;
        }

        public async Task StartRecognizeTextAsync(byte[] imageData, OcrOptions options, CancellationToken ct = default)
        {
            using var image = await BitmapFactory.DecodeByteArrayAsync(imageData, 0, imageData.Length);
            using var inputImage = InputImage.FromBitmap(image, 0);

            ITextRecognizer textScanner = TextRecognition.GetClient(TextRecognizerOptions.DefaultOptions);
            var result = ProcessOcrResult(await ToAwaitableTask(textScanner.Process(inputImage).AddOnSuccessListener(new OnSuccessListener()).AddOnFailureListener(new OnFailureListener())), options);
            RecognitionCompleted?.Invoke(this, new OcrCompletedEventArgs(result, null));
        }

        public class OnFailureListener : Java.Lang.Object, IOnFailureListener
        {
            public void OnFailure(Java.Lang.Exception e)
            {
                Log.Debug(nameof(OcrImplementation), e.ToString());
            }
        }

        public class OnSuccessListener : Java.Lang.Object, IOnSuccessListener
        {
            public void OnSuccess(Java.Lang.Object result)
            {
            }
        }

        internal class TaskCompleteListener(TaskCompletionSource<Java.Lang.Object> tcs) : Java.Lang.Object, IOnCompleteListener
        {
            private readonly TaskCompletionSource<Java.Lang.Object> _taskCompletionSource = tcs;

            public void OnComplete(global::Android.Gms.Tasks.Task task)
            {
                if (task.IsCanceled)
                {
                    _taskCompletionSource.SetCanceled();
                }
                else if (task.IsSuccessful)
                {
                    _taskCompletionSource.SetResult(task.Result);
                }
                else
                {
                    _taskCompletionSource.SetException(task.Exception);
                }
            }
        }
    }
}
