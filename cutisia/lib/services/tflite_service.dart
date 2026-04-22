import 'dart:io';
import 'package:tflite_v2/tflite_v2.dart';
import 'package:logger/logger.dart';

class TFLiteService {
  final _logger = Logger();
  bool _isModelLoaded = false;

  Future<void> loadModel() async {
    try {
      String? res = await Tflite.loadModel(
        model: "assets/models/cutisia_mobile.tflite",
        labels: "assets/models/labels.txt",
        numThreads: 1, 
        isAsset: true,
        useGpuDelegate: false,
      );
      _logger.i("Model Elite Mobile loaded: $res");
      _isModelLoaded = true;
    } catch (e) {
      _logger.e("Error loading model: $e");
    }
  }

  Future<List?> classifyImage(String imagePath) async {
    if (!_isModelLoaded) {
      _logger.w("Model not loaded yet");
      return null;
    }

    try {
      _logger.i("Starting classification for image at: $imagePath");
      final File imageFile = File(imagePath);
      if (!await imageFile.exists()) {
        _logger.e("File does not exist: $imagePath");
        return null;
      }

      var recognitions = await Tflite.runModelOnImage(
        path: imagePath,
        imageMean: 0.0,
        imageStd: 255.0,
        numResults: 3,
        threshold: 0.1,
        asynch: true,
      );
      _logger.i("Recognition raw result: $recognitions");
      return recognitions;
    } catch (e) {
      _logger.e("Error during runModelOnImage: $e");
      return null;
    }
  }

  Future<void> close() async {
    await Tflite.close();
    _isModelLoaded = false;
  }
}
