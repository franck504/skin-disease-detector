import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:logger/logger.dart';

class CloudApiService {
  final _logger = Logger();

  // URL de base de votre serveur Ngrok (à mettre à jour par l'utilisateur)
  String baseUrl = "https://chalazian-nonfissile-dian.ngrok-free.dev";

  Future<Map<String, dynamic>?> predictImage(String imagePath) async {
    try {
      final url = Uri.parse("$baseUrl/predict");
      _logger.i("Sending request to Cloud API: $url");

      var request = http.MultipartRequest('POST', url);
      request.files.add(await http.MultipartFile.fromPath('file', imagePath));

      var streamedResponse = await request.send().timeout(
        const Duration(seconds: 30),
      );
      var response = await http.Response.fromStream(streamedResponse);

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        _logger.i(
          "Cloud Prediction Success: ${data['class']} (${data['confidence']})",
        );
        return data;
      } else {
        _logger.e("Cloud API Error: ${response.statusCode} - ${response.body}");
        return null;
      }
    } catch (e) {
      _logger.e("Cloud API Connection Exception: $e");
      return null;
    }
  }

  Future<bool> submitCollection(String imagePath, Map<String, dynamic> metadata) async {
    try {
      final url = Uri.parse("$baseUrl/collect");
      _logger.i("Sending collection data to Cloud API: $url");

      var request = http.MultipartRequest('POST', url);
      request.files.add(await http.MultipartFile.fromPath('file', imagePath));
      request.fields['metadata'] = json.encode(metadata);

      var streamedResponse = await request.send().timeout(
        const Duration(seconds: 30),
      );
      
      if (streamedResponse.statusCode == 200) {
        _logger.i("Collection data submitted successfully to Cloud");
        return true;
      } else {
        _logger.e("Cloud Collection Error: ${streamedResponse.statusCode}");
        return false;
      }
    } catch (e) {
      _logger.e("Cloud Collection Exception: $e");
      return false;
    }
  }

  // Vérifier si le serveur est en ligne
  Future<bool> checkHealth() async {
    try {
      final response = await http
          .get(Uri.parse(baseUrl))
          .timeout(const Duration(seconds: 5));
      return response.statusCode == 200;
    } catch (_) {
      return false;
    }
  }
}
