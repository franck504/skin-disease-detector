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
            _errorMessage = "Tsy nahomby ny fanadihadiana. Manandrama indray azafady.";
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
        title: Text('Vokatry ny fanadihadiana', style: GoogleFonts.outfit(fontWeight: FontWeight.bold)),
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
      return const Text("Tsy misy valiny hita.");
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
                    'Fahamarinana',
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
        const SizedBox(height: 30),
        _buildSectionTitle('Fitsaboana sy Torohevitra'),
        const SizedBox(height: 12),
        const _LoadingPlaceholder(width: double.infinity, height: 80),
        const SizedBox(height: 10),
        const _LoadingPlaceholder(width: double.infinity, height: 80),
        const SizedBox(height: 10),
        const _LoadingPlaceholder(width: double.infinity, height: 80),
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
      return 'Ny "Candidiase" dia aretina vokatry ny holatra (yeasts). Miseho ho mena sy mangidihidy amin\'ny faritra mando amin\'ny hoditra. Aretina mahazatra izy io nefa azo tsaboina tsara.';
    }
    if (l.contains('leprosy') || l.contains('lepre')) {
      return 'Ny "Leprosy" (aretin\'i Hansen) dia aretina maharitra vokatry ny bakteria. Manimba ny hoditra sy ny hozatra, ary miteraka pentina tsy mahatsapa fanaintainana.';
    }
    if (l.contains('m\u00e9lanome') || l.contains('melanoma') || l.contains('melanome')) {
      return 'Ny "Mélanome" dia karazana homamiadan\'ny hoditra mampidi-doza indrindra. Miseho ho pentina mainty tsy mitovy endrika ary miovaova loko na habe rehefa mandeha ny fotoana.';
    }
    if (l.contains('monkeypox')) {
      return 'Ny "Monkeypox" dia aretina vokatry ny viriosy. Miteraka tazo, fivontosan\'ny tany ary vay misy rano amin\'ny vatana.';
    }
    if (l.contains('scabies') || l.contains('gale')) {
      return 'Ny "Scabies" (Gale) dia aretina mifindra vokatry ny parasy kely anaty hoditra. Mangidihidy mafy indrindra rehefa alina. Mifindra amin\'ny alalan\'ny fifampikasokasohana amin\'ny olona marary.';
    }
    if (l.contains('tinea')) {
      return 'Ny "Tinea" dia aretina vokatry ny holatra eo amin\'ny hoditra. Miteraka faribolana mena sy mangidihidy ary mety hiparitaka amin\'ny faritra hafa.';
    }
    return 'Mbola eo am-panavaozana ny mombamomba ity aretina ity izahay. Manatona dokotera mpitsabo hoditra azafady mba hahazoana ny tena marina.';
  }

  List<Map<String, dynamic>> _getTreatments(String label) {
    final l = label.toLowerCase();
    if (l.contains('candidiase') || l.contains('candidiasis')) {
      return [
        {'icon': Icons.medication, 'title': 'Menaka famonoana holatra', 'detail': 'Mampiasà menaka clotrimazole na miconazole in-2 isan\'andro mandritra ny 2 herinandro.', 'color': Colors.teal},
        {'icon': Icons.air, 'title': 'Ataovy maina foana', 'detail': 'Mampiasà akanjo tsy mampitsemboka ary ataovy maina foana ny faritra marary.', 'color': Colors.blue},
        {'icon': Icons.no_meals, 'title': 'Ahena ny siramamy', 'detail': 'Ny fampihenana ny siramamy dia manampy amin\'ny fisorohana ny aretina vokatry ny holatra.', 'color': Colors.orange},
      ];
    }
    if (l.contains('leprosy') || l.contains('lepre')) {
      return [
        {'icon': Icons.medication, 'title': 'Fitsaboana MDT', 'detail': 'Fitsaboana mitambatra (Dapsone, Rifampicin, Clofazimine) mandritra ny 6-12 volana.', 'color': Colors.red},
        {'icon': Icons.people_alt, 'title': 'Fanamarihana ny olona nifaneraserana', 'detail': 'Tokony hojerena koa ny olona rehetra nifampikasokasoka tamin\'ny marary.', 'color': Colors.purple},
        {'icon': Icons.healing, 'title': 'Fikarakarana ny ratra', 'detail': 'Fikarakarana manokana ny faritra tsy mahatsapa fanaintainana mba hisorohana ny ratra.', 'color': Colors.brown},
      ];
    }
    if (l.contains('m\u00e9lanome') || l.contains('melanoma') || l.contains('melanome')) {
      return [
        {'icon': Icons.content_cut, 'title': 'Fandidiana', 'detail': 'Ny fandidiana hanalana ny aretina no dingana voalohany indrindra.', 'color': Colors.red},
        {'icon': Icons.biotech, 'title': 'Immunothérapie', 'detail': 'Fitsaboana mampitombo hery fiarovana raha efa miparitaka ny aretina.', 'color': Colors.indigo},
        {'icon': Icons.wb_sunny, 'title': 'Fiarovana amin\'ny masoandro', 'detail': 'Mampiasà sunscreen SPF 50+ ary aza mitanika masoandro loatra.', 'color': Colors.amber},
      ];
    }
    if (l.contains('monkeypox')) {
      return [
        {'icon': Icons.home, 'title': 'Fitokanana sy fitsaharana', 'detail': 'Mitokana ao an-trano mandra-pahasitran\'ny vay rehetra. Mitsahatra ary misotro rano betsaka.', 'color': Colors.orange},
        {'icon': Icons.medication, 'title': 'Fanafody viriosy', 'detail': 'Mety hanome fanafody manokana (Tecovirimat) ny dokotera raha mafy ny aretina.', 'color': Colors.red},
        {'icon': Icons.clean_hands, 'title': 'Fahadiovana mafy', 'detail': 'Sasao matetika ny tanana ary aza mifampizara zavatra amin\'ny olon-kafa.', 'color': Colors.teal},
      ];
    }
    if (l.contains('scabies') || l.contains('gale')) {
      return [
        {'icon': Icons.medication, 'title': 'Menaka Permethrin 5%', 'detail': 'Ahosotra amin\'ny vatana manontolo ary avela mandritra ny 8-14 ora vao sasana.', 'color': Colors.green},
        {'icon': Icons.local_laundry_service, 'title': 'Sasao ny fitafiana', 'detail': 'Sasao amin\'ny rano mafana (60°C+) ny fitafiana sy ny lamba rehetra ampiasaina.', 'color': Colors.blue},
        {'icon': Icons.family_restroom, 'title': 'Tsaboy ny mpianakavy', 'detail': 'Tokony hotsaboina miaraka ny olona rehetra ao an-trano mba tsy hifindraindray ny aretina.', 'color': Colors.purple},
      ];
    }
    if (l.contains('tinea')) {
      return [
        {'icon': Icons.medication, 'title': 'Fanafody famonoana holatra', 'detail': 'Menaka famonoana holatra na fanafody fihina raha efa miparitaka be.', 'color': Colors.teal},
        {'icon': Icons.shower, 'title': 'Fahadiovana tsara', 'detail': 'Ataovy madio sy maina foana ny hoditra. Manova ba kiraro isan\'andro.', 'color': Colors.blue},
        {'icon': Icons.do_not_touch, 'title': 'Aza mifampizara zavatra', 'detail': 'Aza mifampizara kiraro, lamba na mpanety hoho. Mifindra mora foana ity aretina ity.', 'color': Colors.orange},
      ];
    }
    return [
      {'icon': Icons.medical_services, 'title': 'Manatona dokotera', 'detail': 'Manatona dokotera mpitsabo hoditra mba hahazoana ny fitsaboana tena sahaza anao.', 'color': Colors.grey},
    ];
  }
}

class _LoadingPlaceholder extends StatelessWidget {
  final double width;
  final double height;
  final double borderRadius;

  const _LoadingPlaceholder({
    required this.width,
    required this.height,
    this.borderRadius = 12,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      width: width,
      height: height,
      decoration: BoxDecoration(
        color: Colors.grey.shade200,
        borderRadius: BorderRadius.circular(borderRadius),
      ),
    );
  }
}
