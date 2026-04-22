# TensorFlow Lite
-keep class org.tensorflow.lite.** { *; }
-keep class com.tflite.tflite_v2.** { *; }

# Ignore GPU delegate warnings (we use CPU by default)
-dontwarn org.tensorflow.lite.gpu.**

# Ignore Play Store split install warnings (not used in this app)
-dontwarn com.google.android.play.core.**

# Flutter and other dependencies
-keep class io.flutter.app.** { *; }
-keep class io.flutter.plugin.** { *; }
-keep class io.flutter.util.** { *; }
-keep class io.flutter.view.** { *; }
-keep class io.flutter.** { *; }
-keep class io.flutter.plugins.** { *; }
