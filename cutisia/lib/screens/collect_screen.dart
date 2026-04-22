import 'dart:io';
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:image_picker/image_picker.dart';
import 'package:geolocator/geolocator.dart';
import 'package:intl/intl.dart';
import '../models/collection_entry.dart';
import '../services/collection_service.dart';
import '../services/cloud_api_service.dart';

class CollectScreen extends StatefulWidget {
  const CollectScreen({super.key});

  @override
  State<CollectScreen> createState() => _CollectScreenState();
}

class _CollectScreenState extends State<CollectScreen> {
  final _formKey = GlobalKey<FormState>();
  final _collectionService = CollectionService();
  final _cloudService = CloudApiService();
  final _picker = ImagePicker();

  // Form state
  XFile? _pickedImage;
  String _selectedLabel = 'Candidiase';
  String _selectedGender = 'Lahy';
  final _collectorController = TextEditingController();
  final _ageController = TextEditingController();
  final _nationalityController = TextEditingController();
  final _notesController = TextEditingController();
  final _locationController = TextEditingController();

  bool _isGettingLocation = false;
  bool _isSubmitting = false;
  double? _latitude;
  double? _longitude;

  static const List<String> _labels = [
    'Candidiase',
    'Leprosy',
    'Monkeypox',
    'Mélanomes',
    'Scabies',
    'Tinea',
  ];

  static const List<String> _genders = ['Lahy', 'Vavy'];

  @override
  void dispose() {
    _collectorController.dispose();
    _ageController.dispose();
    _nationalityController.dispose();
    _notesController.dispose();
    _locationController.dispose();
    super.dispose();
  }

  Future<void> _pickImage(ImageSource source) async {
    final image = await _picker.pickImage(source: source, imageQuality: 85);
    if (image != null) setState(() => _pickedImage = image);
  }

  Future<void> _getLocation() async {
    setState(() => _isGettingLocation = true);
    try {
      bool serviceEnabled = await Geolocator.isLocationServiceEnabled();
      if (!serviceEnabled) {
        if (mounted) _showSnack('Tsy mandeha ny GPS (Location).');
        return;
      }

      LocationPermission permission = await Geolocator.checkPermission();
      if (permission == LocationPermission.denied) {
        permission = await Geolocator.requestPermission();
        if (permission == LocationPermission.denied) {
          if (mounted) _showSnack('Tsy nahazo alalana hampiasa GPS.');
          return;
        }
      }

      final pos = await Geolocator.getCurrentPosition(
        locationSettings: const LocationSettings(
          accuracy: LocationAccuracy.high,
        ),
      );

      setState(() {
        _latitude = pos.latitude;
        _longitude = pos.longitude;
        _locationController.text =
            '${pos.latitude.toStringAsFixed(4)}, ${pos.longitude.toStringAsFixed(4)}';
      });
    } catch (e) {
      if (mounted) _showSnack('Tsy nahazo ny toerana (GPS): $e');
    } finally {
      if (mounted) setState(() => _isGettingLocation = false);
    }
  }

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate()) return;
    if (_pickedImage == null) {
      _showSnack('Mifidiana sary aloha azafady.');
      return;
    }

    setState(() => _isSubmitting = true);
    try {
      final entry = CollectionEntry(
        imagePath: _pickedImage!.path,
        diseaseLabel: _selectedLabel,
        collectorName: _collectorController.text.trim(),
        patientAge: int.parse(_ageController.text.trim()),
        patientGender: _selectedGender,
        patientNationality: _nationalityController.text.trim(),
        patientNotes: _notesController.text.trim(),
        latitude: _latitude,
        longitude: _longitude,
        locationName: _locationController.text.trim(),
        collectedAt: DateFormat('yyyy-MM-dd HH:mm:ss').format(DateTime.now()),
      );

      await _collectionService.insertEntry(entry);

      // --- SYNC WITH CLOUD (New) ---
      bool cloudSyncSuccess = false;
      try {
        final isOnline = await _cloudService.checkHealth();
        if (isOnline) {
          cloudSyncSuccess = await _cloudService.submitCollection(
            _pickedImage!.path,
            entry.toMap(),
          );
        }
      } catch (e) {
        debugPrint("Cloud sync failed silently: $e");
      }

      if (mounted) {
        String msg = '✅ Tafiditra soa aman-tsara ny angon-drakitra!';
        if (cloudSyncSuccess) {
          msg += ' (Voalefa tany amin\'ny Cloud)';
        } else {
          msg += ' (Tahiry ato amin\'ny finday ihany)';
        }
        _showSnack(msg, isSuccess: true);
        _resetForm();
      }
    } catch (e) {
      if (mounted) _showSnack('Nisy fahadisoana teo am-pitahirizana: $e');
    } finally {
      if (mounted) setState(() => _isSubmitting = false);
    }
  }

  void _resetForm() {
    setState(() {
      _pickedImage = null;
      _selectedLabel = 'Candidiase';
      _selectedGender = 'Lahy';
      _latitude = null;
      _longitude = null;
    });
    _collectorController.clear();
    _ageController.clear();
    _nationalityController.clear();
    _notesController.clear();
    _locationController.clear();
  }

  void _showSnack(String msg, {bool isSuccess = false}) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(msg),
        backgroundColor: isSuccess ? Colors.green : Colors.red,
        behavior: SnackBarBehavior.floating,
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF5F7FB),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(20),
          child: Form(
            key: _formKey,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // Header
                Row(
                  children: [
                    Container(
                      padding: const EdgeInsets.all(10),
                      decoration: BoxDecoration(
                        gradient: const LinearGradient(
                          colors: [Color(0xFF2E5BFF), Color(0xFF5B8CFF)],
                        ),
                        borderRadius: BorderRadius.circular(14),
                      ),
                      child: const Icon(
                        Icons.add_a_photo,
                        color: Colors.white,
                        size: 26,
                      ),
                    ),
                    const SizedBox(width: 14),
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'Sary Vaovao',
                          style: GoogleFonts.outfit(
                            fontSize: 22,
                            fontWeight: FontWeight.bold,
                            color: const Color(0xFF1C2431),
                          ),
                        ),
                        Text(
                          'Fanangonana angon-drakitra ara-pahasalamana',
                          style: GoogleFonts.outfit(
                            fontSize: 13,
                            color: Colors.grey,
                          ),
                        ),
                      ],
                    ),
                  ],
                ),

                const SizedBox(height: 24),

                // --- IMAGE PICKER ---
                _buildSectionTitle('Sarin\'ny aretina *'),
                const SizedBox(height: 10),
                GestureDetector(
                  onTap: () => _showImageSourceDialog(),
                  child: Container(
                    height: 200,
                    width: double.infinity,
                    decoration: BoxDecoration(
                      color: Colors.white,
                      borderRadius: BorderRadius.circular(20),
                      border: Border.all(
                        color: _pickedImage != null
                            ? const Color(0xFF2E5BFF)
                            : Colors.grey.shade300,
                        width: 2,
                      ),
                    ),
                    child: _pickedImage != null
                        ? ClipRRect(
                            borderRadius: BorderRadius.circular(18),
                            child: Image.file(
                              File(_pickedImage!.path),
                              fit: BoxFit.cover,
                            ),
                          )
                        : Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Icon(
                                Icons.add_photo_alternate_outlined,
                                size: 52,
                                color: Colors.grey.shade400,
                              ),
                              const SizedBox(height: 10),
                              Text(
                                'Tsindrio raha haka sary na handefa',
                                style: GoogleFonts.outfit(color: Colors.grey),
                              ),
                            ],
                          ),
                  ),
                ),

                const SizedBox(height: 24),

                // --- DISEASE LABEL ---
                _buildSectionTitle('Karazan\'aretina *'),
                const SizedBox(height: 10),
                _buildDropdown(
                  value: _selectedLabel,
                  items: _labels,
                  onChanged: (v) => setState(() => _selectedLabel = v!),
                  icon: Icons.local_hospital,
                ),

                const SizedBox(height: 24),

                // --- COLLECTOR INFO ---
                _buildSectionTitle('Mombamomba ny mpanangona'),
                const SizedBox(height: 10),
                _buildTextField(
                  controller: _collectorController,
                  label: 'Anaran\'ny mpanangona *',
                  icon: Icons.badge,
                  validator: (v) => v!.isEmpty ? 'Tsy maintsy fenoina' : null,
                ),

                const SizedBox(height: 24),

                // --- PATIENT INFO ---
                _buildSectionTitle('Mombamomba ny marary'),
                const SizedBox(height: 10),
                Row(
                  children: [
                    Expanded(
                      child: _buildTextField(
                        controller: _ageController,
                        label: 'Taona *',
                        icon: Icons.cake,
                        keyboardType: TextInputType.number,
                        validator: (v) {
                          if (v!.isEmpty) return 'Tsy maintsy fenoina';
                          if (int.tryParse(v) == null) return 'Diso';
                          return null;
                        },
                      ),
                    ),
                    const SizedBox(width: 12),
                    Expanded(
                      child: _buildDropdown(
                        value: _selectedGender,
                        items: _genders,
                        onChanged: (v) => setState(() => _selectedGender = v!),
                        icon: Icons.person,
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 12),
                _buildTextField(
                  controller: _nationalityController,
                  label: 'Fizakà-manana (Nationalité) *',
                  icon: Icons.flag,
                  validator: (v) => v!.isEmpty ? 'Tsy maintsy fenoina' : null,
                ),
                const SizedBox(height: 12),
                _buildTextField(
                  controller: _notesController,
                  label: 'Fanamarihana momba ny aretina',
                  icon: Icons.notes,
                  maxLines: 3,
                ),

                const SizedBox(height: 24),

                // --- LOCATION ---
                _buildSectionTitle('Toerana (Localisation)'),
                const SizedBox(height: 10),
                Row(
                  children: [
                    Expanded(
                      child: _buildTextField(
                        controller: _locationController,
                        label: 'GPS (Coordonnées)',
                        icon: Icons.location_on,
                        readOnly: true,
                      ),
                    ),
                    const SizedBox(width: 10),
                    AnimatedSwitcher(
                      duration: const Duration(milliseconds: 300),
                      child: _isGettingLocation
                          ? const SizedBox(
                              width: 48,
                              height: 48,
                              child: CircularProgressIndicator(strokeWidth: 2),
                            )
                          : IconButton.filled(
                              icon: const Icon(Icons.my_location),
                              style: IconButton.styleFrom(
                                backgroundColor: const Color(0xFF2E5BFF),
                                foregroundColor: Colors.white,
                              ),
                              onPressed: _getLocation,
                            ),
                    ),
                  ],
                ),

                const SizedBox(height: 36),

                // --- SUBMIT BUTTON ---
                SizedBox(
                  width: double.infinity,
                  child: ElevatedButton.icon(
                    onPressed: _isSubmitting ? null : _submit,
                    icon: _isSubmitting
                        ? const SizedBox(
                            width: 18,
                            height: 18,
                            child: CircularProgressIndicator(
                              strokeWidth: 2,
                              color: Colors.white,
                            ),
                          )
                        : const Icon(Icons.upload_rounded),
                    label: Text(
                      _isSubmitting ? 'Andrasana...' : 'Handefa ny raharaha',
                      style: GoogleFonts.outfit(
                        fontWeight: FontWeight.bold,
                        fontSize: 16,
                      ),
                    ),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: const Color(0xFF2E5BFF),
                      foregroundColor: Colors.white,
                      padding: const EdgeInsets.symmetric(vertical: 18),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(18),
                      ),
                      disabledBackgroundColor: Colors.grey.shade300,
                    ),
                  ),
                ),
                const SizedBox(height: 20),
              ],
            ),
          ),
        ),
      ),
    );
  }

  void _showImageSourceDialog() {
    showModalBottomSheet(
      context: context,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(24)),
      ),
      builder: (_) => SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(20),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              ListTile(
                leading: const Icon(Icons.camera_alt, color: Color(0xFF2E5BFF)),
                title: Text('Haka sary', style: GoogleFonts.outfit()),
                onTap: () {
                  Navigator.pop(context);
                  _pickImage(ImageSource.camera);
                },
              ),
              ListTile(
                leading: const Icon(
                  Icons.photo_library,
                  color: Color(0xFF2E5BFF),
                ),
                title: Text(
                  'Hisafidy sary ato amin\'ny finday',
                  style: GoogleFonts.outfit(),
                ),
                onTap: () {
                  Navigator.pop(context);
                  _pickImage(ImageSource.gallery);
                },
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildSectionTitle(String title) => Text(
    title,
    style: GoogleFonts.outfit(
      fontWeight: FontWeight.bold,
      fontSize: 15,
      color: const Color(0xFF1C2431),
    ),
  );

  Widget _buildTextField({
    required TextEditingController controller,
    required String label,
    required IconData icon,
    TextInputType? keyboardType,
    String? Function(String?)? validator,
    int maxLines = 1,
    bool readOnly = false,
  }) {
    return TextFormField(
      controller: controller,
      keyboardType: keyboardType,
      validator: validator,
      maxLines: maxLines,
      readOnly: readOnly,
      style: GoogleFonts.outfit(),
      decoration: InputDecoration(
        labelText: label,
        labelStyle: GoogleFonts.outfit(color: Colors.grey),
        prefixIcon: Icon(icon, color: const Color(0xFF2E5BFF)),
        filled: true,
        fillColor: Colors.white,
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(14),
          borderSide: BorderSide.none,
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(14),
          borderSide: const BorderSide(color: Color(0xFF2E5BFF), width: 1.5),
        ),
      ),
    );
  }

  Widget _buildDropdown({
    required String value,
    required List<String> items,
    required ValueChanged<String?> onChanged,
    required IconData icon,
  }) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 4),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(14),
      ),
      child: DropdownButtonHideUnderline(
        child: DropdownButton<String>(
          value: value,
          isExpanded: true,
          icon: const Icon(Icons.keyboard_arrow_down),
          style: GoogleFonts.outfit(
            color: const Color(0xFF1C2431),
            fontSize: 14,
          ),
          items: items
              .map(
                (item) => DropdownMenuItem(
                  value: item,
                  child: Row(
                    children: [
                      Icon(icon, size: 18, color: const Color(0xFF2E5BFF)),
                      const SizedBox(width: 8),
                      Text(item),
                    ],
                  ),
                ),
              )
              .toList(),
          onChanged: onChanged,
        ),
      ),
    );
  }
}
