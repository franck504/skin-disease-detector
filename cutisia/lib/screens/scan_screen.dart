import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:google_fonts/google_fonts.dart';
import 'result_screen.dart';

class ScanScreen extends StatefulWidget {
  const ScanScreen({super.key});

  @override
  State<ScanScreen> createState() => _ScanScreenState();
}

class _ScanScreenState extends State<ScanScreen> {
  final _picker = ImagePicker();
  
  bool _isLoading = false;
  bool _isPickerActive = false;
  bool _isCloudMode = false; // Par défaut : Local (Vitesse)

  @override
  void initState() {
    super.initState();
    _checkLostData();
  }

  Future<void> _checkLostData() async {
    final LostDataResponse response = await _picker.retrieveLostData();
    if (response.isEmpty) return;
    if (response.file != null) {
      _processImage(response.file!);
    }
  }

  @override
  void dispose() {
    super.dispose();
  }

  Future<void> _pickImage(ImageSource source) async {
    if (_isPickerActive || _isLoading) return;
    
    setState(() => _isPickerActive = true);
    
    try {
      final XFile? image = await _picker.pickImage(source: source);
      setState(() => _isPickerActive = false);
      
      if (image == null) return;
      await _processImage(image);
    } catch (e) {
      setState(() {
        _isPickerActive = false;
        _isLoading = false;
      });
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error picking image: $e')),
        );
      }
    }
  }

  Future<void> _processImage(XFile image) async {
    if (!mounted) return;

    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => ResultScreen(
          imagePath: image.path,
          isCloudMode: _isCloudMode,
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('New Scan', style: GoogleFonts.outfit(fontWeight: FontWeight.bold)),
        backgroundColor: Colors.transparent,
        elevation: 0,
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            // --- TOGGLE CLOUD MODE ---
            Container(
              width: 300,
              margin: const EdgeInsets.only(bottom: 30),
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
              decoration: BoxDecoration(
                color: _isCloudMode 
                    ? Colors.blue.withValues(alpha: 0.1) 
                    : Colors.grey.withValues(alpha: 0.1),
                borderRadius: BorderRadius.circular(16),
              ),
              child: SwitchListTile(
                title: Text('High Precision', 
                  style: GoogleFonts.outfit(fontWeight: FontWeight.bold, fontSize: 16)),
                subtitle: Text('Uses Cloud Elite AI', style: GoogleFonts.outfit(fontSize: 12)),
                secondary: Icon(Icons.cloud_done, color: _isCloudMode ? Colors.blue : Colors.grey),
                value: _isCloudMode,
                onChanged: (val) => setState(() => _isCloudMode = val),
                activeThumbColor: const Color(0xFF2E5BFF),
              ),
            ),
            
            _buildActionCard(
              'Take Photo',
              'Use your camera to scan.',
              Icons.camera_alt,
              () => _pickImage(ImageSource.camera),
            ),
            const SizedBox(height: 20),
            _buildActionCard(
              'Upload from Gallery',
              'Choose an existing photo.',
              Icons.photo_library,
              () => _pickImage(ImageSource.gallery),
            ),
            const SizedBox(height: 40),
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 40),
              child: Text(
                'Ensure the area is well-lit and the image is clear for better accuracy.',
                textAlign: TextAlign.center,
                style: GoogleFonts.outfit(
                  color: Colors.grey,
                  fontSize: 14,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildActionCard(String title, String subtitle, IconData icon, VoidCallback onTap) {
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(24),
      child: Container(
        width: 300,
        padding: const EdgeInsets.all(24),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(24),
          boxShadow: [
            BoxShadow(
              color: Colors.black.withValues(alpha: 0.05),
              blurRadius: 10,
              offset: const Offset(0, 4),
            ),
          ],
        ),
        child: Column(
          children: [
            Icon(icon, size: 48, color: const Color(0xFF2E5BFF)),
            const SizedBox(height: 16),
            Text(
              title,
              style: GoogleFonts.outfit(
                fontSize: 20,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 4),
            Text(
              subtitle,
              style: GoogleFonts.outfit(
                fontSize: 14,
                color: Colors.grey,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
