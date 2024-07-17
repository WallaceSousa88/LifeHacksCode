; ModuleID = 'obj\Debug\130\android\marshal_methods.x86_64.ll'
source_filename = "obj\Debug\130\android\marshal_methods.x86_64.ll"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-unknown-linux-android"


%struct.MonoImage = type opaque

%struct.MonoClass = type opaque

%struct.MarshalMethodsManagedClass = type {
	i32,; uint32_t token
	%struct.MonoClass*; MonoClass* klass
}

%struct.MarshalMethodName = type {
	i64,; uint64_t id
	i8*; char* name
}

%class._JNIEnv = type opaque

%class._jobject = type {
	i8; uint8_t b
}

%class._jclass = type {
	i8; uint8_t b
}

%class._jstring = type {
	i8; uint8_t b
}

%class._jthrowable = type {
	i8; uint8_t b
}

%class._jarray = type {
	i8; uint8_t b
}

%class._jobjectArray = type {
	i8; uint8_t b
}

%class._jbooleanArray = type {
	i8; uint8_t b
}

%class._jbyteArray = type {
	i8; uint8_t b
}

%class._jcharArray = type {
	i8; uint8_t b
}

%class._jshortArray = type {
	i8; uint8_t b
}

%class._jintArray = type {
	i8; uint8_t b
}

%class._jlongArray = type {
	i8; uint8_t b
}

%class._jfloatArray = type {
	i8; uint8_t b
}

%class._jdoubleArray = type {
	i8; uint8_t b
}

; assembly_image_cache
@assembly_image_cache = local_unnamed_addr global [0 x %struct.MonoImage*] zeroinitializer, align 8
; Each entry maps hash of an assembly name to an index into the `assembly_image_cache` array
@assembly_image_cache_hashes = local_unnamed_addr constant [288 x i64] [
	i64 24362543149721218, ; 0: Xamarin.AndroidX.DynamicAnimation => 0x568d9a9a43a682 => 76
	i64 98382396393917666, ; 1: Microsoft.Extensions.Primitives.dll => 0x15d8644ad360ce2 => 24
	i64 120698629574877762, ; 2: Mono.Android => 0x1accec39cafe242 => 26
	i64 210515253464952879, ; 3: Xamarin.AndroidX.Collection.dll => 0x2ebe681f694702f => 65
	i64 232391251801502327, ; 4: Xamarin.AndroidX.SavedState.dll => 0x3399e9cbc897277 => 103
	i64 295915112840604065, ; 5: Xamarin.AndroidX.SlidingPaneLayout => 0x41b4d3a3088a9a1 => 104
	i64 316157742385208084, ; 6: Xamarin.AndroidX.Core.Core.Ktx.dll => 0x46337caa7dc1b14 => 70
	i64 502670939551102150, ; 7: System.Management.dll => 0x6f9d88e66daf4c6 => 40
	i64 634308326490598313, ; 8: Xamarin.AndroidX.Lifecycle.Runtime.dll => 0x8cd840fee8b6ba9 => 88
	i64 648449422406355874, ; 9: Microsoft.Extensions.Configuration.FileExtensions.dll => 0x8ffc15065568ba2 => 18
	i64 668723562677762733, ; 10: Microsoft.Extensions.Configuration.Binder.dll => 0x947c88986577aad => 16
	i64 670107554435801057, ; 11: SkiaSharp.Extended.Svg.dll => 0x94cb34537739fe1 => 33
	i64 702024105029695270, ; 12: System.Drawing.Common => 0x9be17343c0e7726 => 131
	i64 710500338161506772, ; 13: SixLabors.Fonts.dll => 0x9dc344b0ce959d4 => 29
	i64 720058930071658100, ; 14: Xamarin.AndroidX.Legacy.Support.Core.UI => 0x9fe29c82844de74 => 81
	i64 872800313462103108, ; 15: Xamarin.AndroidX.DrawerLayout => 0xc1ccf42c3c21c44 => 75
	i64 940822596282819491, ; 16: System.Transactions => 0xd0e792aa81923a3 => 129
	i64 996343623809489702, ; 17: Xamarin.Forms.Platform => 0xdd3b93f3b63db26 => 117
	i64 1000557547492888992, ; 18: Mono.Security.dll => 0xde2b1c9cba651a0 => 143
	i64 1010800728818218806, ; 19: Microsoft.Bcl.HashCode.dll => 0xe0715e84bea7736 => 14
	i64 1120440138749646132, ; 20: Xamarin.Google.Android.Material.dll => 0xf8c9a5eae431534 => 119
	i64 1315114680217950157, ; 21: Xamarin.AndroidX.Arch.Core.Common.dll => 0x124039d5794ad7cd => 60
	i64 1425944114962822056, ; 22: System.Runtime.Serialization.dll => 0x13c9f89e19eaf3a8 => 3
	i64 1624659445732251991, ; 23: Xamarin.AndroidX.AppCompat.AppCompatResources.dll => 0x168bf32877da9957 => 58
	i64 1628611045998245443, ; 24: Xamarin.AndroidX.Lifecycle.ViewModelSavedState.dll => 0x1699fd1e1a00b643 => 90
	i64 1636321030536304333, ; 25: Xamarin.AndroidX.Legacy.Support.Core.Utils.dll => 0x16b5614ec39e16cd => 82
	i64 1743969030606105336, ; 26: System.Memory.dll => 0x1833d297e88f2af8 => 42
	i64 1795316252682057001, ; 27: Xamarin.AndroidX.AppCompat.dll => 0x18ea3e9eac997529 => 59
	i64 1836611346387731153, ; 28: Xamarin.AndroidX.SavedState => 0x197cf449ebe482d1 => 103
	i64 1865037103900624886, ; 29: Microsoft.Bcl.AsyncInterfaces => 0x19e1f15d56eb87f6 => 13
	i64 1875917498431009007, ; 30: Xamarin.AndroidX.Annotation.dll => 0x1a08990699eb70ef => 56
	i64 1981742497975770890, ; 31: Xamarin.AndroidX.Lifecycle.ViewModel.dll => 0x1b80904d5c241f0a => 89
	i64 2040001226662520565, ; 32: System.Threading.Tasks.Extensions.dll => 0x1c4f8a4ea894a6f5 => 138
	i64 2064708342624596306, ; 33: Xamarin.Kotlin.StdLib.Jdk7.dll => 0x1ca7514c5eecb152 => 124
	i64 2136356949452311481, ; 34: Xamarin.AndroidX.MultiDex.dll => 0x1da5dd539d8acbb9 => 94
	i64 2165725771938924357, ; 35: Xamarin.AndroidX.Browser => 0x1e0e341d75540745 => 63
	i64 2262844636196693701, ; 36: Xamarin.AndroidX.DrawerLayout.dll => 0x1f673d352266e6c5 => 75
	i64 2284400282711631002, ; 37: System.Web.Services => 0x1fb3d1f42fd4249a => 135
	i64 2304837677853103545, ; 38: Xamarin.AndroidX.ResourceInspection.Annotation.dll => 0x1ffc6da80d5ed5b9 => 102
	i64 2329709569556905518, ; 39: Xamarin.AndroidX.Lifecycle.LiveData.Core.dll => 0x2054ca829b447e2e => 85
	i64 2335503487726329082, ; 40: System.Text.Encodings.Web => 0x2069600c4d9d1cfa => 50
	i64 2337758774805907496, ; 41: System.Runtime.CompilerServices.Unsafe => 0x207163383edbc828 => 45
	i64 2470498323731680442, ; 42: Xamarin.AndroidX.CoordinatorLayout => 0x2248f922dc398cba => 69
	i64 2479423007379663237, ; 43: Xamarin.AndroidX.VectorDrawable.Animated.dll => 0x2268ae16b2cba985 => 109
	i64 2497223385847772520, ; 44: System.Runtime => 0x22a7eb7046413568 => 46
	i64 2547086958574651984, ; 45: Xamarin.AndroidX.Activity.dll => 0x2359121801df4a50 => 55
	i64 2592350477072141967, ; 46: System.Xml.dll => 0x23f9e10627330e8f => 52
	i64 2624866290265602282, ; 47: mscorlib.dll => 0x246d65fbde2db8ea => 27
	i64 2694427813909235223, ; 48: Xamarin.AndroidX.Preference.dll => 0x256487d230fe0617 => 98
	i64 2783046991838674048, ; 49: System.Runtime.CompilerServices.Unsafe.dll => 0x269f5e7e6dc37c80 => 45
	i64 2787234703088983483, ; 50: Xamarin.AndroidX.Startup.StartupRuntime => 0x26ae3f31ef429dbb => 105
	i64 2815524396660695947, ; 51: System.Security.AccessControl => 0x2712c0857f68238b => 47
	i64 2851879596360956261, ; 52: System.Configuration.ConfigurationManager => 0x2793e9620b477965 => 36
	i64 2894542791763525065, ; 53: IronSoftware.Shared.dll => 0x282b7b554a3b7dc9 => 11
	i64 2960931600190307745, ; 54: Xamarin.Forms.Core => 0x2917579a49927da1 => 115
	i64 3017704767998173186, ; 55: Xamarin.Google.Android.Material => 0x29e10a7f7d88a002 => 119
	i64 3183889606213293070, ; 56: IronSoftware.Abstractions => 0x2c2f72ba5666d40e => 8
	i64 3289520064315143713, ; 57: Xamarin.AndroidX.Lifecycle.Common => 0x2da6b911e3063621 => 84
	i64 3303437397778967116, ; 58: Xamarin.AndroidX.Annotation.Experimental => 0x2dd82acf985b2a4c => 57
	i64 3311221304742556517, ; 59: System.Numerics.Vectors.dll => 0x2df3d23ba9e2b365 => 44
	i64 3344514922410554693, ; 60: Xamarin.KotlinX.Coroutines.Core.Jvm => 0x2e6a1a9a18463545 => 127
	i64 3396143930648122816, ; 61: Microsoft.Extensions.FileProviders.Abstractions => 0x2f2186e9506155c0 => 20
	i64 3493805808809882663, ; 62: Xamarin.AndroidX.Tracing.Tracing.dll => 0x307c7ddf444f3427 => 107
	i64 3494946837667399002, ; 63: Microsoft.Extensions.Configuration => 0x30808ba1c00a455a => 17
	i64 3522470458906976663, ; 64: Xamarin.AndroidX.SwipeRefreshLayout => 0x30e2543832f52197 => 106
	i64 3531994851595924923, ; 65: System.Numerics => 0x31042a9aade235bb => 43
	i64 3571415421602489686, ; 66: System.Runtime.dll => 0x319037675df7e556 => 46
	i64 3638003163729360188, ; 67: Microsoft.Extensions.Configuration.Abstractions => 0x327cc89a39d5f53c => 15
	i64 3655542548057982301, ; 68: Microsoft.Extensions.Configuration.dll => 0x32bb18945e52855d => 17
	i64 3716579019761409177, ; 69: netstandard.dll => 0x3393f0ed5c8c5c99 => 1
	i64 3727469159507183293, ; 70: Xamarin.AndroidX.RecyclerView => 0x33baa1739ba646bd => 101
	i64 3772598417116884899, ; 71: Xamarin.AndroidX.DynamicAnimation.dll => 0x345af645b473efa3 => 76
	i64 3889433610606858880, ; 72: Microsoft.Extensions.FileProviders.Physical.dll => 0x35fa0b4301afd280 => 21
	i64 3966267475168208030, ; 73: System.Memory => 0x370b03412596249e => 42
	i64 4195379201529348725, ; 74: Tesseract.Android => 0x3a38fb27dd380275 => 0
	i64 4201423742386704971, ; 75: Xamarin.AndroidX.Core.Core.Ktx => 0x3a4e74a233da124b => 70
	i64 4525561845656915374, ; 76: System.ServiceModel.Internals => 0x3ece06856b710dae => 136
	i64 4636684751163556186, ; 77: Xamarin.AndroidX.VersionedParcelable.dll => 0x4058d0370893015a => 111
	i64 4759461199762736555, ; 78: Xamarin.AndroidX.Lifecycle.Process.dll => 0x420d00be961cc5ab => 87
	i64 4782108999019072045, ; 79: Xamarin.AndroidX.AsyncLayoutInflater.dll => 0x425d76cc43bb0a2d => 62
	i64 4794310189461587505, ; 80: Xamarin.AndroidX.Activity => 0x4288cfb749e4c631 => 55
	i64 4795410492532947900, ; 81: Xamarin.AndroidX.SwipeRefreshLayout.dll => 0x428cb86f8f9b7bbc => 106
	i64 5142919913060024034, ; 82: Xamarin.Forms.Platform.Android.dll => 0x475f52699e39bee2 => 116
	i64 5202753749449073649, ; 83: Plugin.Media => 0x4833e4f841be63f1 => 28
	i64 5203618020066742981, ; 84: Xamarin.Essentials => 0x4836f704f0e652c5 => 114
	i64 5205316157927637098, ; 85: Xamarin.AndroidX.LocalBroadcastManager => 0x483cff7778e0c06a => 92
	i64 5348796042099802469, ; 86: Xamarin.AndroidX.Media => 0x4a3abda9415fc165 => 93
	i64 5376510917114486089, ; 87: Xamarin.AndroidX.VectorDrawable.Animated => 0x4a9d3431719e5d49 => 109
	i64 5408338804355907810, ; 88: Xamarin.AndroidX.Transition => 0x4b0e477cea9840e2 => 108
	i64 5451019430259338467, ; 89: Xamarin.AndroidX.ConstraintLayout.dll => 0x4ba5e94a845c2ce3 => 68
	i64 5507995362134886206, ; 90: System.Core.dll => 0x4c705499688c873e => 37
	i64 5624375662354994915, ; 91: SixLabors.ImageSharp.dll => 0x4e0dcbdd9e0596e3 => 30
	i64 5692067934154308417, ; 92: Xamarin.AndroidX.ViewPager2.dll => 0x4efe49a0d4a8bb41 => 113
	i64 5757522595884336624, ; 93: Xamarin.AndroidX.Concurrent.Futures.dll => 0x4fe6d44bd9f885f0 => 66
	i64 5814345312393086621, ; 94: Xamarin.AndroidX.Preference => 0x50b0b44182a5c69d => 98
	i64 5896680224035167651, ; 95: Xamarin.AndroidX.Lifecycle.LiveData.dll => 0x51d5376bfbafdda3 => 86
	i64 6085203216496545422, ; 96: Xamarin.Forms.Platform.dll => 0x5472fc15a9574e8e => 117
	i64 6086316965293125504, ; 97: FormsViewGroup.dll => 0x5476f10882baef80 => 6
	i64 6222399776351216807, ; 98: System.Text.Json.dll => 0x565a67a0ffe264a7 => 51
	i64 6284145129771520194, ; 99: System.Reflection.Emit.ILGeneration => 0x5735c4b3610850c2 => 139
	i64 6319713645133255417, ; 100: Xamarin.AndroidX.Lifecycle.Runtime => 0x57b42213b45b52f9 => 88
	i64 6401687960814735282, ; 101: Xamarin.AndroidX.Lifecycle.LiveData.Core => 0x58d75d486341cfb2 => 85
	i64 6504860066809920875, ; 102: Xamarin.AndroidX.Browser.dll => 0x5a45e7c43bd43d6b => 63
	i64 6514236370858598888, ; 103: IronSoftware.Drawing.Common => 0x5a67377723f4e1e8 => 9
	i64 6548213210057960872, ; 104: Xamarin.AndroidX.CustomView.dll => 0x5adfed387b066da8 => 73
	i64 6583230273628745597, ; 105: IronOcr => 0x5b5c550dee3d2f7d => 7
	i64 6591024623626361694, ; 106: System.Web.Services.dll => 0x5b7805f9751a1b5e => 135
	i64 6617685658146568858, ; 107: System.Text.Encoding.CodePages => 0x5bd6be0b4905fa9a => 137
	i64 6659513131007730089, ; 108: Xamarin.AndroidX.Legacy.Support.Core.UI.dll => 0x5c6b57e8b6c3e1a9 => 81
	i64 6671798237668743565, ; 109: SkiaSharp => 0x5c96fd260152998d => 32
	i64 6876862101832370452, ; 110: System.Xml.Linq => 0x5f6f85a57d108914 => 53
	i64 6894844156784520562, ; 111: System.Numerics.Vectors => 0x5faf683aead1ad72 => 44
	i64 6939043805913733614, ; 112: Tesseract.dll => 0x604c6f93ac5cd9ee => 54
	i64 6987056692196838363, ; 113: System.Management => 0x60f7030ae3e88bdb => 40
	i64 7036436454368433159, ; 114: Xamarin.AndroidX.Legacy.Support.V4.dll => 0x61a671acb33d5407 => 83
	i64 7103753931438454322, ; 115: Xamarin.AndroidX.Interpolator.dll => 0x62959a90372c7632 => 80
	i64 7348123982286201829, ; 116: System.Memory.Data.dll => 0x65f9c7d471b2a3e5 => 41
	i64 7488575175965059935, ; 117: System.Xml.Linq.dll => 0x67ecc3724534ab5f => 53
	i64 7635363394907363464, ; 118: Xamarin.Forms.Core.dll => 0x69f6428dc4795888 => 115
	i64 7637365915383206639, ; 119: Xamarin.Essentials.dll => 0x69fd5fd5e61792ef => 114
	i64 7654504624184590948, ; 120: System.Net.Http => 0x6a3a4366801b8264 => 2
	i64 7735352534559001595, ; 121: Xamarin.Kotlin.StdLib.dll => 0x6b597e2582ce8bfb => 123
	i64 7820441508502274321, ; 122: System.Data => 0x6c87ca1e14ff8111 => 128
	i64 7836164640616011524, ; 123: Xamarin.AndroidX.AppCompat.AppCompatResources => 0x6cbfa6390d64d704 => 58
	i64 7932306995570506601, ; 124: BitMiracle.LibTiff.NET => 0x6e15372f70537b69 => 4
	i64 7957977418052424808, ; 125: SixLabors.ImageSharp.Drawing => 0x6e706a4c6d985468 => 31
	i64 8044118961405839122, ; 126: System.ComponentModel.Composition => 0x6fa2739369944712 => 134
	i64 8083354569033831015, ; 127: Xamarin.AndroidX.Lifecycle.Common.dll => 0x702dd82730cad267 => 84
	i64 8087206902342787202, ; 128: System.Diagnostics.DiagnosticSource => 0x703b87d46f3aa082 => 38
	i64 8103644804370223335, ; 129: System.Data.DataSetExtensions.dll => 0x7075ee03be6d50e7 => 130
	i64 8167236081217502503, ; 130: Java.Interop.dll => 0x7157d9f1a9b8fd27 => 12
	i64 8187640529827139739, ; 131: Xamarin.KotlinX.Coroutines.Android => 0x71a057ae90f0109b => 126
	i64 8246048515196606205, ; 132: Microsoft.Maui.Graphics.dll => 0x726fd96f64ee56fd => 25
	i64 8398329775253868912, ; 133: Xamarin.AndroidX.ConstraintLayout.Core.dll => 0x748cdc6f3097d170 => 67
	i64 8400357532724379117, ; 134: Xamarin.AndroidX.Navigation.UI.dll => 0x749410ab44503ded => 97
	i64 8410671156615598628, ; 135: System.Reflection.Emit.Lightweight.dll => 0x74b8b4daf4b25224 => 140
	i64 8426919725312979251, ; 136: Xamarin.AndroidX.Lifecycle.Process => 0x74f26ed7aa033133 => 87
	i64 8476857680833348370, ; 137: System.Security.Permissions.dll => 0x75a3d925fd9d0312 => 48
	i64 8598790081731763592, ; 138: Xamarin.AndroidX.Emoji2.ViewsHelper.dll => 0x77550a055fc61d88 => 78
	i64 8601935802264776013, ; 139: Xamarin.AndroidX.Transition.dll => 0x7760370982b4ed4d => 108
	i64 8611085854550231972, ; 140: IronSoftware.Abstractions.dll => 0x7780b8f612db8ba4 => 8
	i64 8626175481042262068, ; 141: Java.Interop => 0x77b654e585b55834 => 12
	i64 8639588376636138208, ; 142: Xamarin.AndroidX.Navigation.Runtime => 0x77e5fbdaa2fda2e0 => 96
	i64 8684531736582871431, ; 143: System.IO.Compression.FileSystem => 0x7885a79a0fa0d987 => 133
	i64 8725526185868997716, ; 144: System.Diagnostics.DiagnosticSource.dll => 0x79174bd613173454 => 38
	i64 8853378295825400934, ; 145: Xamarin.Kotlin.StdLib.Common.dll => 0x7add84a720d38466 => 122
	i64 8951477988056063522, ; 146: Xamarin.AndroidX.ProfileInstaller.ProfileInstaller => 0x7c3a09cd9ccf5e22 => 100
	i64 9041985878101337471, ; 147: BouncyCastle.Crypto => 0x7d7b963fe854257f => 5
	i64 9262312476707878147, ; 148: IronSoftware.Drawing.Common.dll => 0x808a581facd77503 => 9
	i64 9312692141327339315, ; 149: Xamarin.AndroidX.ViewPager2 => 0x813d54296a634f33 => 113
	i64 9324707631942237306, ; 150: Xamarin.AndroidX.AppCompat => 0x8168042fd44a7c7a => 59
	i64 9342122023452561803, ; 151: SixLabors.ImageSharp => 0x81a5e27bd03e518b => 30
	i64 9650158550865574924, ; 152: Microsoft.Extensions.Configuration.Json => 0x85ec4012c28a7c0c => 19
	i64 9662334977499516867, ; 153: System.Numerics.dll => 0x8617827802b0cfc3 => 43
	i64 9678050649315576968, ; 154: Xamarin.AndroidX.CoordinatorLayout.dll => 0x864f57c9feb18c88 => 69
	i64 9711637524876806384, ; 155: Xamarin.AndroidX.Media.dll => 0x86c6aadfd9a2c8f0 => 93
	i64 9808709177481450983, ; 156: Mono.Android.dll => 0x881f890734e555e7 => 26
	i64 9825649861376906464, ; 157: Xamarin.AndroidX.Concurrent.Futures => 0x885bb87d8abc94e0 => 66
	i64 9834056768316610435, ; 158: System.Transactions.dll => 0x8879968718899783 => 129
	i64 9907349773706910547, ; 159: Xamarin.AndroidX.Emoji2.ViewsHelper => 0x897dfa20b758db53 => 78
	i64 9959489431142554298, ; 160: System.CodeDom => 0x8a3736deb7825aba => 35
	i64 9998632235833408227, ; 161: Mono.Security => 0x8ac2470b209ebae3 => 143
	i64 10038780035334861115, ; 162: System.Net.Http.dll => 0x8b50e941206af13b => 2
	i64 10205853378024263619, ; 163: Microsoft.Extensions.Configuration.Binder => 0x8da279930adb4fc3 => 16
	i64 10226222362177979215, ; 164: Xamarin.Kotlin.StdLib.Jdk7 => 0x8dead70ebbc6434f => 124
	i64 10229024438826829339, ; 165: Xamarin.AndroidX.CustomView => 0x8df4cb880b10061b => 73
	i64 10245369515835430794, ; 166: System.Reflection.Emit.Lightweight => 0x8e2edd4ad7fc978a => 140
	i64 10321854143672141184, ; 167: Xamarin.Jetbrains.Annotations.dll => 0x8f3e97a7f8f8c580 => 121
	i64 10364469296367737616, ; 168: System.Reflection.Emit.ILGeneration.dll => 0x8fd5fde967711b10 => 139
	i64 10376576884623852283, ; 169: Xamarin.AndroidX.Tracing.Tracing => 0x900101b2f888c2fb => 107
	i64 10385971460532963787, ; 170: IronSoftware.Logger.dll => 0x90226204206989cb => 10
	i64 10406448008575299332, ; 171: Xamarin.KotlinX.Coroutines.Core.Jvm.dll => 0x906b2153fcb3af04 => 127
	i64 10430153318873392755, ; 172: Xamarin.AndroidX.Core => 0x90bf592ea44f6673 => 71
	i64 10447083246144586668, ; 173: Microsoft.Bcl.AsyncInterfaces.dll => 0x90fb7edc816203ac => 13
	i64 10592024858677642023, ; 174: IronOcr.dll => 0x92fe6e7d71968327 => 7
	i64 10847732767863316357, ; 175: Xamarin.AndroidX.Arch.Core.Common => 0x968ae37a86db9f85 => 60
	i64 11002576679268595294, ; 176: Microsoft.Extensions.Logging.Abstractions => 0x98b1013215cd365e => 23
	i64 11023048688141570732, ; 177: System.Core => 0x98f9bc61168392ac => 37
	i64 11037814507248023548, ; 178: System.Xml => 0x992e31d0412bf7fc => 52
	i64 11044929383126564683, ; 179: Tesseract => 0x994778c162887f4b => 54
	i64 11162124722117608902, ; 180: Xamarin.AndroidX.ViewPager => 0x9ae7d54b986d05c6 => 112
	i64 11340910727871153756, ; 181: Xamarin.AndroidX.CursorAdapter => 0x9d630238642d465c => 72
	i64 11341245327015630248, ; 182: System.Configuration.ConfigurationManager.dll => 0x9d643289535355a8 => 36
	i64 11392833485892708388, ; 183: Xamarin.AndroidX.Print.dll => 0x9e1b79b18fcf6824 => 99
	i64 11529969570048099689, ; 184: Xamarin.AndroidX.ViewPager.dll => 0xa002ae3c4dc7c569 => 112
	i64 11578238080964724296, ; 185: Xamarin.AndroidX.Legacy.Support.V4 => 0xa0ae2a30c4cd8648 => 83
	i64 11580057168383206117, ; 186: Xamarin.AndroidX.Annotation => 0xa0b4a0a4103262e5 => 56
	i64 11591352189662810718, ; 187: Xamarin.AndroidX.Startup.StartupRuntime.dll => 0xa0dcc167234c525e => 105
	i64 11597940890313164233, ; 188: netstandard => 0xa0f429ca8d1805c9 => 1
	i64 11672361001936329215, ; 189: Xamarin.AndroidX.Interpolator => 0xa1fc8e7d0a8999ff => 80
	i64 12011556116648931059, ; 190: System.Security.Cryptography.ProtectedData => 0xa6b19ea5ec87aef3 => 141
	i64 12048689113179125827, ; 191: Microsoft.Extensions.FileProviders.Physical => 0xa7358ae968287843 => 21
	i64 12058074296353848905, ; 192: Microsoft.Extensions.FileSystemGlobbing.dll => 0xa756e2afa5707e49 => 22
	i64 12063623837170009990, ; 193: System.Security => 0xa76a99f6ce740786 => 142
	i64 12102847907131387746, ; 194: System.Buffers => 0xa7f5f40c43256f62 => 34
	i64 12137774235383566651, ; 195: Xamarin.AndroidX.VectorDrawable => 0xa872095bbfed113b => 110
	i64 12145679461940342714, ; 196: System.Text.Json => 0xa88e1f1ebcb62fba => 51
	i64 12292916162294916721, ; 197: IronSoftware.Logger => 0xaa99361e733f2671 => 10
	i64 12451044538927396471, ; 198: Xamarin.AndroidX.Fragment.dll => 0xaccaff0a2955b677 => 79
	i64 12463625692235400003, ; 199: BitMiracle.LibTiff.NET.dll => 0xacf7b1882f1f8343 => 4
	i64 12466513435562512481, ; 200: Xamarin.AndroidX.Loader.dll => 0xad01f3eb52569061 => 91
	i64 12487638416075308985, ; 201: Xamarin.AndroidX.DocumentFile.dll => 0xad4d00fa21b0bfb9 => 74
	i64 12538491095302438457, ; 202: Xamarin.AndroidX.CardView.dll => 0xae01ab382ae67e39 => 64
	i64 12550732019250633519, ; 203: System.IO.Compression => 0xae2d28465e8e1b2f => 132
	i64 12700543734426720211, ; 204: Xamarin.AndroidX.Collection => 0xb041653c70d157d3 => 65
	i64 12828192437253469131, ; 205: Xamarin.Kotlin.StdLib.Jdk8.dll => 0xb206e50e14d873cb => 125
	i64 12843321153144804894, ; 206: Microsoft.Extensions.Primitives => 0xb23ca48abd74d61e => 24
	i64 12963446364377008305, ; 207: System.Drawing.Common.dll => 0xb3e769c8fd8548b1 => 131
	i64 13081516019875753442, ; 208: BouncyCastle.Crypto.dll => 0xb58ae182e046ade2 => 5
	i64 13109727801987935684, ; 209: SixLabors.Fonts => 0xb5ef1bfa438dadc4 => 29
	i64 13129914918964716986, ; 210: Xamarin.AndroidX.Emoji2.dll => 0xb636d40db3fe65ba => 77
	i64 13162471042547327635, ; 211: System.Security.Permissions => 0xb6aa7dace9662293 => 48
	i64 13370592475155966277, ; 212: System.Runtime.Serialization => 0xb98de304062ea945 => 3
	i64 13401370062847626945, ; 213: Xamarin.AndroidX.VectorDrawable.dll => 0xb9fb3b1193964ec1 => 110
	i64 13404347523447273790, ; 214: Xamarin.AndroidX.ConstraintLayout.Core => 0xba05cf0da4f6393e => 67
	i64 13454009404024712428, ; 215: Xamarin.Google.Guava.ListenableFuture => 0xbab63e4543a86cec => 120
	i64 13465488254036897740, ; 216: Xamarin.Kotlin.StdLib => 0xbadf06394d106fcc => 123
	i64 13491513212026656886, ; 217: Xamarin.AndroidX.Arch.Core.Runtime.dll => 0xbb3b7bc905569876 => 61
	i64 13550417756503177631, ; 218: Microsoft.Extensions.FileProviders.Abstractions.dll => 0xbc0cc1280684799f => 20
	i64 13572454107664307259, ; 219: Xamarin.AndroidX.RecyclerView.dll => 0xbc5b0b19d99f543b => 101
	i64 13643785327914841093, ; 220: Plugin.Media.dll => 0xbd587677c60cf405 => 28
	i64 13647894001087880694, ; 221: System.Data.dll => 0xbd670f48cb071df6 => 128
	i64 13710614125866346983, ; 222: System.Security.AccessControl.dll => 0xbe45e2e7d0b769e7 => 47
	i64 13793664977988262628, ; 223: IronSoftware.Shared => 0xbf6cf1372bbc9ae4 => 11
	i64 13818328264475132956, ; 224: Microsoft.Bcl.HashCode => 0xbfc4905809c7c41c => 14
	i64 13828521679616088467, ; 225: Xamarin.Kotlin.StdLib.Common => 0xbfe8c733724e1993 => 122
	i64 13959074834287824816, ; 226: Xamarin.AndroidX.Fragment => 0xc1b8989a7ad20fb0 => 79
	i64 13967638549803255703, ; 227: Xamarin.Forms.Platform.Android => 0xc1d70541e0134797 => 116
	i64 14124974489674258913, ; 228: Xamarin.AndroidX.CardView => 0xc405fd76067d19e1 => 64
	i64 14172845254133543601, ; 229: Xamarin.AndroidX.MultiDex => 0xc4b00faaed35f2b1 => 94
	i64 14261073672896646636, ; 230: Xamarin.AndroidX.Print => 0xc5e982f274ae0dec => 99
	i64 14486659737292545672, ; 231: Xamarin.AndroidX.Lifecycle.LiveData => 0xc90af44707469e88 => 86
	i64 14495724990987328804, ; 232: Xamarin.AndroidX.ResourceInspection.Annotation => 0xc92b2913e18d5d24 => 102
	i64 14551742072151931844, ; 233: System.Text.Encodings.Web.dll => 0xc9f22c50f1b8fbc4 => 50
	i64 14620159896233883483, ; 234: SixLabors.ImageSharp.Drawing.dll => 0xcae53df6f66eb75b => 31
	i64 14644440854989303794, ; 235: Xamarin.AndroidX.LocalBroadcastManager.dll => 0xcb3b815e37daeff2 => 92
	i64 14792063746108907174, ; 236: Xamarin.Google.Guava.ListenableFuture.dll => 0xcd47f79af9c15ea6 => 120
	i64 14852515768018889994, ; 237: Xamarin.AndroidX.CursorAdapter.dll => 0xce1ebc6625a76d0a => 72
	i64 14912225920358050525, ; 238: System.Security.Principal.Windows => 0xcef2de7759506add => 49
	i64 14935719434541007538, ; 239: System.Text.Encoding.CodePages.dll => 0xcf4655b160b702b2 => 137
	i64 14987728460634540364, ; 240: System.IO.Compression.dll => 0xcfff1ba06622494c => 132
	i64 14988210264188246988, ; 241: Xamarin.AndroidX.DocumentFile => 0xd000d1d307cddbcc => 74
	i64 15150743910298169673, ; 242: Xamarin.AndroidX.ProfileInstaller.ProfileInstaller.dll => 0xd2424150783c3149 => 100
	i64 15227001540531775957, ; 243: Microsoft.Extensions.Configuration.Abstractions.dll => 0xd3512d3999b8e9d5 => 15
	i64 15279429628684179188, ; 244: Xamarin.KotlinX.Coroutines.Android.dll => 0xd40b704b1c4c96f4 => 126
	i64 15370334346939861994, ; 245: Xamarin.AndroidX.Core.dll => 0xd54e65a72c560bea => 71
	i64 15383240894167415497, ; 246: System.Memory.Data => 0xd57c4016df1c7ac9 => 41
	i64 15582737692548360875, ; 247: Xamarin.AndroidX.Lifecycle.ViewModelSavedState => 0xd841015ed86f6aab => 90
	i64 15609085926864131306, ; 248: System.dll => 0xd89e9cf3334914ea => 39
	i64 15777549416145007739, ; 249: Xamarin.AndroidX.SlidingPaneLayout.dll => 0xdaf51d99d77eb47b => 104
	i64 15810740023422282496, ; 250: Xamarin.Forms.Xaml => 0xdb6b08484c22eb00 => 118
	i64 15827202283623377193, ; 251: Microsoft.Extensions.Configuration.Json.dll => 0xdba5849eef9f6929 => 19
	i64 15963349826457351533, ; 252: System.Threading.Tasks.Extensions => 0xdd893616f748b56d => 138
	i64 16154507427712707110, ; 253: System => 0xe03056ea4e39aa26 => 39
	i64 16321164108206115771, ; 254: Microsoft.Extensions.Logging.Abstractions.dll => 0xe2806c487e7b0bbb => 23
	i64 16324796876805858114, ; 255: SkiaSharp.dll => 0xe28d5444586b6342 => 32
	i64 16337011941688632206, ; 256: System.Security.Principal.Windows.dll => 0xe2b8b9cdc3aa638e => 49
	i64 16423015068819898779, ; 257: Xamarin.Kotlin.StdLib.Jdk8 => 0xe3ea453135e5c19b => 125
	i64 16565028646146589191, ; 258: System.ComponentModel.Composition.dll => 0xe5e2cdc9d3bcc207 => 134
	i64 16621146507174665210, ; 259: Xamarin.AndroidX.ConstraintLayout => 0xe6aa2caf87dedbfa => 68
	i64 16649148416072044166, ; 260: Microsoft.Maui.Graphics => 0xe70da84600bb4e86 => 25
	i64 16677317093839702854, ; 261: Xamarin.AndroidX.Navigation.UI => 0xe771bb8960dd8b46 => 97
	i64 16822611501064131242, ; 262: System.Data.DataSetExtensions => 0xe975ec07bb5412aa => 130
	i64 16833383113903931215, ; 263: mscorlib => 0xe99c30c1484d7f4f => 27
	i64 17024911836938395553, ; 264: Xamarin.AndroidX.Annotation.Experimental.dll => 0xec44a31d250e5fa1 => 57
	i64 17031351772568316411, ; 265: Xamarin.AndroidX.Navigation.Common.dll => 0xec5b843380a769fb => 95
	i64 17037200463775726619, ; 266: Xamarin.AndroidX.Legacy.Support.Core.Utils => 0xec704b8e0a78fc1b => 82
	i64 17047433665992082296, ; 267: Microsoft.Extensions.Configuration.FileExtensions => 0xec94a699197e4378 => 18
	i64 17089166281881057141, ; 268: SkiaSharp.Extended.Svg => 0xed28ea30eb1a7775 => 33
	i64 17205988430934219272, ; 269: Microsoft.Extensions.FileSystemGlobbing => 0xeec7f35113509a08 => 22
	i64 17221578629025613250, ; 270: Tesseract.Android.dll => 0xeeff5684ee87c5c2 => 0
	i64 17523946658117960076, ; 271: System.Security.Cryptography.ProtectedData.dll => 0xf33190a3c403c18c => 141
	i64 17544493274320527064, ; 272: Xamarin.AndroidX.AsyncLayoutInflater => 0xf37a8fada41aded8 => 62
	i64 17704177640604968747, ; 273: Xamarin.AndroidX.Loader => 0xf5b1dfc36cac272b => 91
	i64 17710060891934109755, ; 274: Xamarin.AndroidX.Lifecycle.ViewModel => 0xf5c6c68c9e45303b => 89
	i64 17743407583038752114, ; 275: System.CodeDom.dll => 0xf63d3f302bff4572 => 35
	i64 17838668724098252521, ; 276: System.Buffers.dll => 0xf78faeb0f5bf3ee9 => 34
	i64 17882897186074144999, ; 277: FormsViewGroup => 0xf82cd03e3ac830e7 => 6
	i64 17891337867145587222, ; 278: Xamarin.Jetbrains.Annotations => 0xf84accff6fb52a16 => 121
	i64 17892495832318972303, ; 279: Xamarin.Forms.Xaml.dll => 0xf84eea293687918f => 118
	i64 17928294245072900555, ; 280: System.IO.Compression.FileSystem.dll => 0xf8ce18a0b24011cb => 133
	i64 18116111925905154859, ; 281: Xamarin.AndroidX.Arch.Core.Runtime => 0xfb695bd036cb632b => 61
	i64 18121036031235206392, ; 282: Xamarin.AndroidX.Navigation.Common => 0xfb7ada42d3d42cf8 => 95
	i64 18129453464017766560, ; 283: System.ServiceModel.Internals.dll => 0xfb98c1df1ec108a0 => 136
	i64 18260797123374478311, ; 284: Xamarin.AndroidX.Emoji2 => 0xfd6b623bde35f3e7 => 77
	i64 18305135509493619199, ; 285: Xamarin.AndroidX.Navigation.Runtime.dll => 0xfe08e7c2d8c199ff => 96
	i64 18318849532986632368, ; 286: System.Security.dll => 0xfe39a097c37fa8b0 => 142
	i64 18380184030268848184 ; 287: Xamarin.AndroidX.VersionedParcelable => 0xff1387fe3e7b7838 => 111
], align 16
@assembly_image_cache_indices = local_unnamed_addr constant [288 x i32] [
	i32 76, i32 24, i32 26, i32 65, i32 103, i32 104, i32 70, i32 40, ; 0..7
	i32 88, i32 18, i32 16, i32 33, i32 131, i32 29, i32 81, i32 75, ; 8..15
	i32 129, i32 117, i32 143, i32 14, i32 119, i32 60, i32 3, i32 58, ; 16..23
	i32 90, i32 82, i32 42, i32 59, i32 103, i32 13, i32 56, i32 89, ; 24..31
	i32 138, i32 124, i32 94, i32 63, i32 75, i32 135, i32 102, i32 85, ; 32..39
	i32 50, i32 45, i32 69, i32 109, i32 46, i32 55, i32 52, i32 27, ; 40..47
	i32 98, i32 45, i32 105, i32 47, i32 36, i32 11, i32 115, i32 119, ; 48..55
	i32 8, i32 84, i32 57, i32 44, i32 127, i32 20, i32 107, i32 17, ; 56..63
	i32 106, i32 43, i32 46, i32 15, i32 17, i32 1, i32 101, i32 76, ; 64..71
	i32 21, i32 42, i32 0, i32 70, i32 136, i32 111, i32 87, i32 62, ; 72..79
	i32 55, i32 106, i32 116, i32 28, i32 114, i32 92, i32 93, i32 109, ; 80..87
	i32 108, i32 68, i32 37, i32 30, i32 113, i32 66, i32 98, i32 86, ; 88..95
	i32 117, i32 6, i32 51, i32 139, i32 88, i32 85, i32 63, i32 9, ; 96..103
	i32 73, i32 7, i32 135, i32 137, i32 81, i32 32, i32 53, i32 44, ; 104..111
	i32 54, i32 40, i32 83, i32 80, i32 41, i32 53, i32 115, i32 114, ; 112..119
	i32 2, i32 123, i32 128, i32 58, i32 4, i32 31, i32 134, i32 84, ; 120..127
	i32 38, i32 130, i32 12, i32 126, i32 25, i32 67, i32 97, i32 140, ; 128..135
	i32 87, i32 48, i32 78, i32 108, i32 8, i32 12, i32 96, i32 133, ; 136..143
	i32 38, i32 122, i32 100, i32 5, i32 9, i32 113, i32 59, i32 30, ; 144..151
	i32 19, i32 43, i32 69, i32 93, i32 26, i32 66, i32 129, i32 78, ; 152..159
	i32 35, i32 143, i32 2, i32 16, i32 124, i32 73, i32 140, i32 121, ; 160..167
	i32 139, i32 107, i32 10, i32 127, i32 71, i32 13, i32 7, i32 60, ; 168..175
	i32 23, i32 37, i32 52, i32 54, i32 112, i32 72, i32 36, i32 99, ; 176..183
	i32 112, i32 83, i32 56, i32 105, i32 1, i32 80, i32 141, i32 21, ; 184..191
	i32 22, i32 142, i32 34, i32 110, i32 51, i32 10, i32 79, i32 4, ; 192..199
	i32 91, i32 74, i32 64, i32 132, i32 65, i32 125, i32 24, i32 131, ; 200..207
	i32 5, i32 29, i32 77, i32 48, i32 3, i32 110, i32 67, i32 120, ; 208..215
	i32 123, i32 61, i32 20, i32 101, i32 28, i32 128, i32 47, i32 11, ; 216..223
	i32 14, i32 122, i32 79, i32 116, i32 64, i32 94, i32 99, i32 86, ; 224..231
	i32 102, i32 50, i32 31, i32 92, i32 120, i32 72, i32 49, i32 137, ; 232..239
	i32 132, i32 74, i32 100, i32 15, i32 126, i32 71, i32 41, i32 90, ; 240..247
	i32 39, i32 104, i32 118, i32 19, i32 138, i32 39, i32 23, i32 32, ; 248..255
	i32 49, i32 125, i32 134, i32 68, i32 25, i32 97, i32 130, i32 27, ; 256..263
	i32 57, i32 95, i32 82, i32 18, i32 33, i32 22, i32 0, i32 141, ; 264..271
	i32 62, i32 91, i32 89, i32 35, i32 34, i32 6, i32 121, i32 118, ; 272..279
	i32 133, i32 61, i32 95, i32 136, i32 77, i32 96, i32 142, i32 111 ; 288..287
], align 16

@marshal_methods_number_of_classes = local_unnamed_addr constant i32 0, align 4

; marshal_methods_class_cache
@marshal_methods_class_cache = global [0 x %struct.MarshalMethodsManagedClass] [
], align 8; end of 'marshal_methods_class_cache' array


@get_function_pointer = internal unnamed_addr global void (i32, i32, i32, i8**)* null, align 8

; Function attributes: "frame-pointer"="none" "min-legal-vector-width"="0" mustprogress nofree norecurse nosync "no-trapping-math"="true" nounwind sspstrong "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx16,+cx8,+fxsr,+mmx,+popcnt,+sse,+sse2,+sse3,+sse4.1,+sse4.2,+ssse3,+x87" "tune-cpu"="generic" uwtable willreturn writeonly
define void @xamarin_app_init (void (i32, i32, i32, i8**)* %fn) local_unnamed_addr #0
{
	store void (i32, i32, i32, i8**)* %fn, void (i32, i32, i32, i8**)** @get_function_pointer, align 8
	ret void
}

; Names of classes in which marshal methods reside
@mm_class_names = local_unnamed_addr constant [0 x i8*] zeroinitializer, align 8
@__MarshalMethodName_name.0 = internal constant [1 x i8] c"\00", align 1

; mm_method_names
@mm_method_names = local_unnamed_addr constant [1 x %struct.MarshalMethodName] [
	; 0
	%struct.MarshalMethodName {
		i64 0, ; id 0x0; name: 
		i8* getelementptr inbounds ([1 x i8], [1 x i8]* @__MarshalMethodName_name.0, i32 0, i32 0); name
	}
], align 16; end of 'mm_method_names' array


attributes #0 = { "min-legal-vector-width"="0" mustprogress nofree norecurse nosync "no-trapping-math"="true" nounwind sspstrong "stack-protector-buffer-size"="8" uwtable willreturn writeonly "frame-pointer"="none" "target-cpu"="x86-64" "target-features"="+cx16,+cx8,+fxsr,+mmx,+popcnt,+sse,+sse2,+sse3,+sse4.1,+sse4.2,+ssse3,+x87" "tune-cpu"="generic" }
attributes #1 = { "min-legal-vector-width"="0" mustprogress "no-trapping-math"="true" nounwind sspstrong "stack-protector-buffer-size"="8" uwtable "frame-pointer"="none" "target-cpu"="x86-64" "target-features"="+cx16,+cx8,+fxsr,+mmx,+popcnt,+sse,+sse2,+sse3,+sse4.1,+sse4.2,+ssse3,+x87" "tune-cpu"="generic" }
attributes #2 = { nounwind }

!llvm.module.flags = !{!0, !1}
!llvm.ident = !{!2}
!0 = !{i32 1, !"wchar_size", i32 4}
!1 = !{i32 7, !"PIC Level", i32 2}
!2 = !{!"Xamarin.Android remotes/origin/d17-5 @ 45b0e144f73b2c8747d8b5ec8cbd3b55beca67f0"}
!llvm.linker.options = !{}
