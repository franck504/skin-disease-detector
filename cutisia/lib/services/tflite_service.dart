import 'dart:io';
import 'package:tflite_v2/tflite_v2.dart';
import 'package:logger/logger.dart';

class TFLiteService {
  final _logger = Logger();
  bool _isModelLoaded = false;

  /// Charge le modèle TFLite et les labels associés depuis les assets.
  Future<void> loadModel() async {
    try {
      String? res = await Tflite.loadModel(
        model: "assets/models/cutisia_mobile.tflite",
        labels: "assets/models/labels.txt",
        numThreads: 1, 
        isAsset: true,
        useGpuDelegate: false,
      );
      _logger.i("Modèle mobile chargé avec succès : $res");
      _isModelLoaded = true;
    } catch (e) {
      _logger.e("Erreur lors du chargement du modèle : $e");
    }
  }

  /// Exécute l'inférence sur une image locale.
  /// Renvoie une liste de résultats contenant le label et le score de confiance.
  Future<List?> classifyImage(String imagePath) async {
    if (!_isModelLoaded) {
      _logger.w("Tentative de classification alors que le modèle n'est pas chargé.");
      return null;
    }

    try {
      _logger.i("Analyse de l'image : $imagePath");
      final File imageFile = File(imagePath);
      if (!await imageFile.exists()) {
        _logger.e("Fichier introuvable : $imagePath");
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
      _logger.i("Résultats de l'inférence locale : $recognitions");
      return recognitions;
    } catch (e) {
      _logger.e("Échec de l'analyse TFLite : $e");
      return null;
    }
  }

  /// Libère les ressources du modèle pour économiser la mémoire.
  Future<void> close() async {
    await Tflite.close();
    _isModelLoaded = false;
  }
}
