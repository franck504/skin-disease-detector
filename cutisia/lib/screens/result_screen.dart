import 'dart:io';
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:percent_indicator/percent_indicator.dart';
import '../services/tflite_service.dart';
import '../services/cloud_api_service.dart';
import '../widgets/scanner_animation.dart';

class ResultScreen extends StatefulWidget {
  final String imagePath;
  final bool isCloudMode;

  const ResultScreen({
    super.key,
    required this.imagePath,
    required this.isCloudMode,
  });

  @override
  State<ResultScreen> createState() => _ResultScreenState();
}

class _ResultScreenState extends State<ResultScreen> {
  final _tfliteService = TFLiteService();
  final _cloudService = CloudApiService();
  
  bool _isLoading = true;
  List? _results;
  String? _errorMessage;

  @override
  void initState() {
    super.initState();
    _startAnalysis();
  }

  @override
  void dispose() {
    _tfliteService.close();
    super.dispose();
  }

  Future<void> _startAnalysis() async {
    try {
      List? results;
      if (widget.isCloudMode) {
        final cloudData = await _cloudService.predictImage(widget.imagePath);
        if (cloudData != null) {
          results = [{
            'label': cloudData['class'],
            'confidence': cloudData['confidence'],
          }];
        }
      } else {
        await _tfliteService.loadModel();
        results = await _tfliteService.classifyImage(widget.imagePath);
      }

      if (mounted) {
        setState(() {
          _results = results;
          _isLoading = false;
          if (results == null || results.isEmpty) {
            _errorMessage = "Analysis failed. Please try again.";
          }
        });
      }
    } catch (e) {
      if (mounted) {
        setState(() {
          _isLoading = false;
          _errorMessage = "Error: $e";
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Analysis Result', style: GoogleFonts.outfit(fontWeight: FontWeight.bold)),
      ),
      body: SingleChildScrollView(
        child: Column(
          children: [
            // Image section + Scanner overlay
            Container(
              height: 300,
              width: double.infinity,
              margin: const EdgeInsets.all(16),
              child: ClipRRect(
                borderRadius: BorderRadius.circular(24),
                child: Stack(
                  fit: StackFit.expand,
                  children: [
                    Image.file(
                      File(widget.imagePath),
                      fit: BoxFit.cover,
                    ),
                    ScannerAnimation(visible: _isLoading),
                  ],
                ),
              ),
            ),
            
            Padding(
              padding: const EdgeInsets.all(24),
              child: _buildResultContent(),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildResultContent() {
    if (_isLoading) {
      return _buildLoadingState();
    }

    if (_errorMessage != null) {
      return _buildErrorState();
    }

    if (_results == null || _results!.isEmpty) {
      return const Text("No results found.");
    }

    final topResult = _results![0];
    final label = topResult['label'].toString().replaceAll('_', ' ');
    final confidence = topResult['confidence'] as double;

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'Fahamarinana (Probability)',
                    style: GoogleFonts.outfit(color: Colors.grey),
                  ),
                  Text(
                    label,
                    style: GoogleFonts.outfit(
                      fontSize: 28,
                      fontWeight: FontWeight.bold,
                      color: const Color(0xFF1C2431),
                    ),
                  ),
                ],
              ),
            ),
            CircularPercentIndicator(
              radius: 40.0,
              lineWidth: 8.0,
              percent: confidence,
              animation: true,
              animationDuration: 1000,
              center: Text(
                "${(confidence * 100).toStringAsFixed(1)}%",
                style: GoogleFonts.outfit(fontWeight: FontWeight.bold),
              ),
              progressColor: _getColor(confidence),
              backgroundColor: _getColor(confidence).withValues(alpha: 0.1),
              circularStrokeCap: CircularStrokeCap.round,
            ),
          ],
        ),
        const SizedBox(height: 30),
        const Divider(),
        const SizedBox(height: 20),
        _buildSectionTitle('What is this?'),
        _buildSectionTitle('Inona ity?'),
        const SizedBox(height: 10),
        Text(
          _getDescription(label),
          style: GoogleFonts.outfit(fontSize: 16, height: 1.5),
        ),
        const SizedBox(height: 30),
        _buildSectionTitle('Fitsaboana sy Torohevitra'),
        const SizedBox(height: 12),
        ..._getTreatments(label).map((t) => Padding(
          padding: const EdgeInsets.only(bottom: 10),
          child: _buildTreatmentCard(t['icon'] as IconData, t['title'] as String, t['detail'] as String, t['color'] as Color),
        )),
        const SizedBox(height: 16),
        _buildRecommendationCard(
          Icons.medical_services,
          'Manatona Dokotera',
          'Torohevitra fotsiny ihany ity fandalinana ity. Manatona dokotera mpitsabo hoditra azafady.',
        ),
        const SizedBox(height: 40),
        _buildBackButton(),
      ],
    );
  }

  Widget _buildLoadingState() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const _LoadingPlaceholder(width: 80, height: 15),
                  const SizedBox(height: 10),
                  const _LoadingPlaceholder(width: 180, height: 35),
                ],
              ),
            ),
            CircularPercentIndicator(
              radius: 40.0,
              lineWidth: 8.0,
              percent: 0.0,
              center: const CircularProgressIndicator(strokeWidth: 2),
              progressColor: Colors.grey.shade300,
              backgroundColor: Colors.grey.shade100,
            ),
          ],
        ),
        const SizedBox(height: 30),
        const Divider(),
        const SizedBox(height: 20),
        _buildSectionTitle('Inona ity?'),
        const SizedBox(height: 10),
        const _LoadingPlaceholder(width: double.infinity, height: 15),
        const SizedBox(height: 8),
        const _LoadingPlaceholder(width: double.infinity, height: 15),
        const SizedBox(height: 8),
        const _LoadingPlaceholder(width: 200, height: 15),
      ],
    );
  }

  Widget _buildErrorState() {
    return Center(
      child: Column(
        children: [
          const Icon(Icons.error_outline, color: Colors.red, size: 60),
          const SizedBox(height: 16),
          Text(
            _errorMessage!,
            style: GoogleFonts.outfit(color: Colors.red, fontWeight: FontWeight.bold),
            textAlign: TextAlign.center,
          ),
          const SizedBox(height: 24),
          _buildBackButton(),
        ],
      ),
    );
  }

  Widget _buildBackButton() {
    return SizedBox(
      width: double.infinity,
      child: ElevatedButton(
        onPressed: () => Navigator.popUntil(context, (route) => route.isFirst),
        style: ElevatedButton.styleFrom(
          backgroundColor: const Color(0xFF2E5BFF),
          padding: const EdgeInsets.symmetric(vertical: 20),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(16),
          ),
        ),
        child: Text(
          'Hiverina amin\'ny fandraisana',
          style: GoogleFonts.outfit(color: Colors.white, fontWeight: FontWeight.bold),
        ),
      ),
    );
  }

  Color _getColor(double confidence) {
    if (confidence > 0.7) return Colors.green;
    if (confidence > 0.4) return Colors.orange;
    return Colors.red;
  }

  Widget _buildSectionTitle(String title) {
    return Text(
      title,
      style: GoogleFonts.outfit(
        fontSize: 20,
        fontWeight: FontWeight.bold,
        color: const Color(0xFF1C2431),
      ),
    );
  }

  Widget _buildRecommendationCard(IconData icon, String title, String subtitle) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.red.withValues(alpha: 0.05),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: Colors.red.withValues(alpha: 0.1)),
      ),
      child: Row(
        children: [
          Icon(icon, color: Colors.red),
          const SizedBox(width: 15),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(title, style: GoogleFonts.outfit(fontWeight: FontWeight.bold, color: Colors.red)),
                Text(subtitle, style: GoogleFonts.outfit(fontSize: 12, color: Colors.red.withValues(alpha: 0.8))),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildTreatmentCard(IconData icon, String title, String detail, Color color) {
    return Container(
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: color.withValues(alpha: 0.07),
        borderRadius: BorderRadius.circular(14),
        border: Border.all(color: color.withValues(alpha: 0.2)),
      ),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Icon(icon, color: color, size: 22),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(title, style: GoogleFonts.outfit(
                  fontWeight: FontWeight.bold, color: color, fontSize: 14)),
                const SizedBox(height: 2),
                Text(detail, style: GoogleFonts.outfit(
                  fontSize: 12, color: color.withValues(alpha: 0.85), height: 1.4)),
              ],
            ),
          ),
        ],
      ),
    );
  }

  String _getDescription(String label) {
    final l = label.toLowerCase();
    if (l.contains('candidiase') || l.contains('candidiasis')) {
      return 'Candidiasis is a fungal infection caused by Candida yeasts. On the skin, it appears as a red, itchy rash, often in warm and moist areas. It is common but treatable.';
    }
    if (l.contains('leprosy') || l.contains('lepre')) {
      return 'Leprosy (Hansen disease) is a chronic bacterial infection caused by Mycobacterium leprae. It affects skin, nerves, and mucous membranes, causing discolored skin patches and numbness.';
    }
    if (l.contains('m\u00e9lanome') || l.contains('melanoma') || l.contains('melanome')) {
      return 'Melanoma is the most dangerous form of skin cancer, developing from pigment-producing cells. It appears as an irregular mole or dark spot that changes shape, size or color over time.';
    }
    if (l.contains('monkeypox')) {
      return 'Monkeypox is a viral zoonosis caused by the monkeypox virus. It causes fever, swollen lymph nodes, and a characteristic rash with raised, fluid-filled lesions that can spread over the body.';
    }
    if (l.contains('scabies') || l.contains('gale')) {
      return 'Scabies is a contagious skin infestation by the mite Sarcoptes scabiei. It causes intense itching and a pimple-like rash, especially at night. It spreads through prolonged skin-to-skin contact.';
    }
    if (l.contains('tinea')) {
      return 'Tinea is a superficial fungal infection of the skin. Depending on its location, it can manifest as ringworm (body), athlete\'s foot, or nail infection. It causes scaling, itching and redness.';
    }
    return 'Detailed medical information is being updated. Please consult a qualified dermatologist for a precise diagnosis and treatment plan.';
  }

  List<Map<String, dynamic>> _getTreatments(String label) {
    final l = label.toLowerCase();
    if (l.contains('candidiase') || l.contains('candidiasis')) {
      return [
        {'icon': Icons.medication, 'title': 'Antifungal Cream', 'detail': 'Apply clotrimazole or miconazole cream to the affected area 2x daily for 2 weeks.', 'color': Colors.teal},
        {'icon': Icons.air, 'title': 'Keep Area Dry', 'detail': 'Wear breathable clothing and keep the affected area clean and dry to prevent spreading.', 'color': Colors.blue},
        {'icon': Icons.no_meals, 'title': 'Reduce Sugar Intake', 'detail': 'A diet low in refined sugars may help prevent recurrent candida infections.', 'color': Colors.orange},
      ];
    }
    if (l.contains('leprosy') || l.contains('lepre')) {
      return [
        {'icon': Icons.medication, 'title': 'Multi-Drug Therapy (MDT)', 'detail': 'WHO-recommended treatment combining Dapsone, Rifampicin, and Clofazimine for 6-12 months.', 'color': Colors.red},
        {'icon': Icons.people_alt, 'title': 'Contact Tracing', 'detail': 'All close contacts should be examined and monitored regularly for signs of infection.', 'color': Colors.purple},
        {'icon': Icons.healing, 'title': 'Wound Care', 'detail': 'Regular care of numb areas to prevent injuries and infections due to loss of sensation.', 'color': Colors.brown},
      ];
    }
    if (l.contains('m\u00e9lanome') || l.contains('melanoma') || l.contains('melanome')) {
      return [
        {'icon': Icons.content_cut, 'title': 'Surgical Excision', 'detail': 'Primary treatment involves surgical removal of the melanoma with clear margins.', 'color': Colors.red},
        {'icon': Icons.biotech, 'title': 'Immunotherapy', 'detail': 'Checkpoint inhibitors (PD-1/CTLA-4) may be used for advanced or metastatic melanoma.', 'color': Colors.indigo},
        {'icon': Icons.wb_sunny, 'title': 'Strict Sun Protection', 'detail': 'Apply SPF 50+ sunscreen daily, wear protective clothing and avoid direct sun exposure.', 'color': Colors.amber},
      ];
    }
    if (l.contains('monkeypox')) {
      return [
        {'icon': Icons.home, 'title': 'Isolation & Rest', 'detail': 'Isolate at home until all lesions have crusted over. Rest and stay well-hydrated.', 'color': Colors.orange},
        {'icon': Icons.medication, 'title': 'Antiviral Treatment', 'detail': 'Tecovirimat (TPOXX) may be prescribed for severe or high-risk cases by a physician.', 'color': Colors.red},
        {'icon': Icons.clean_hands, 'title': 'Strict Hygiene', 'detail': 'Wash hands frequently, disinfect surfaces and avoid sharing personal items or bedding.', 'color': Colors.teal},
      ];
    }
    if (l.contains('scabies') || l.contains('gale')) {
      return [
        {'icon': Icons.medication, 'title': 'Permethrin 5% Cream', 'detail': 'Apply from neck to toes and leave for 8-14 hours before washing off. Repeat after 1 week.', 'color': Colors.green},
        {'icon': Icons.local_laundry_service, 'title': 'Wash All Clothing', 'detail': 'Machine-wash all bedding, clothing and towels in hot water (60°C+) to kill mites.', 'color': Colors.blue},
        {'icon': Icons.family_restroom, 'title': 'Treat Close Contacts', 'detail': 'All household members and close contacts should be treated simultaneously to prevent re-infestation.', 'color': Colors.purple},
      ];
    }
    if (l.contains('tinea')) {
      return [
        {'icon': Icons.medication, 'title': 'Antifungal Medication', 'detail': 'Topical terbinafine or clotrimazole for mild cases. Oral antifungals for extensive infections.', 'color': Colors.teal},
        {'icon': Icons.shower, 'title': 'Good Hygiene', 'detail': 'Keep the skin dry and clean. Change socks daily and wear breathable footwear.', 'color': Colors.blue},
        {'icon': Icons.do_not_touch, 'title': 'Avoid Sharing Items', 'detail': 'Do not share shoes, towels or nail clippers. Tinea is highly contagious through contact.', 'color': Colors.orange},
      ];
    }
    return [
      {'icon': Icons.medical_services, 'title': 'Professional Diagnosis', 'detail': 'Consult a certified dermatologist for a precise diagnosis and a tailored treatment plan.', 'color': Colors.grey},
    ];
  }
}

class _LoadingPlaceholder extends StatelessWidget {
  final double width;
  final double height;
  const _LoadingPlaceholder({required this.width, required this.height});

  @override
  Widget build(BuildContext context) {
    return Container(
      width: width,
      height: height,
      decoration: BoxDecoration(
        color: Colors.grey.shade200,
        borderRadius: BorderRadius.circular(height / 2),
      ),
    );
  }
}
