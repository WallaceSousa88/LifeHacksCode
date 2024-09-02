using System;
using System.Collections.Generic;
using System.Text.RegularExpressions;
using System.Threading;
using System.Threading.Tasks;
using Plugin.Tesseract;

namespace Plugin.Tesseract;

public delegate bool CustomOcrValidationCallback(string extractedText);

public interface IOcrService
{
    event EventHandler<OcrCompletedEventArgs> RecognitionCompleted;

    IReadOnlyCollection<string> SupportedLanguages { get; }

    Task InitAsync(CancellationToken ct = default);

    Task<OcrResult> RecognizeTextAsync(byte[] imageData, CancellationToken ct = default);

    Task<OcrResult> RecognizeTextAsync(byte[] imageData, OcrOptions options, CancellationToken ct = default);

    Task StartRecognizeTextAsync(byte[] imageData, OcrOptions options, CancellationToken ct = default);
}

public static class OcrPatternMatcher
{
    public static string? ExtractPattern(string input, OcrPatternConfig config)
    {
        var regex = new Regex(config.RegexPattern);
        var match = regex.Match(input);

        if (match.Success && (config.ValidationFunction == null || config.ValidationFunction(match.Value)))
        {
            return match.Value;
        }
        return null;
    }
}

public class OcrCompletedEventArgs(OcrResult? result, string? errorMessage = null) : EventArgs
{
    public string ErrorMessage { get; } = errorMessage ?? string.Empty;

    public bool IsSuccessful => Result?.Success ?? false;

    public OcrResult? Result { get; } = result;
}

public class OcrOptions
{
    public OcrOptions(string? language = null, List<OcrPatternConfig>? patternConfigs = null, CustomOcrValidationCallback? customCallback = null)
    {
        Language = language;
        PatternConfigs = patternConfigs;
        CustomCallback = customCallback;
    }

    public OcrOptions(string? language = null, OcrPatternConfig? patternConfig = null, CustomOcrValidationCallback? customCallback = null)
    {
        Language = language;
        PatternConfigs = new List<OcrPatternConfig> { patternConfig };
        CustomCallback = customCallback;
    }

    public CustomOcrValidationCallback? CustomCallback { get; set; }

    public string? Language { get; set; }

    public List<OcrPatternConfig>? PatternConfigs { get; set; }
}

public class OcrPatternConfig
{
    public OcrPatternConfig(string regexPattern, Func<string, bool> validationFunction = null)
    {
        RegexPattern = regexPattern;
        ValidationFunction = validationFunction;
    }

    public string RegexPattern { get; set; }

    public Func<string, bool> ValidationFunction { get; set; }
}

public class OcrResult
{
    public string AllText { get; set; }

    public IList<OcrElement> Elements { get; set; } = new List<OcrElement>();

    public IList<string> MatchedValues { get; set; } = new List<string>();

    public bool Success { get; set; }

    public class OcrElement
    {
        public float Confidence { get; set; }

        public string Text { get; set; }
    }
}
