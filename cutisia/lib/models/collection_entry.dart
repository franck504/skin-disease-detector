class CollectionEntry {
  final int? id;
  final String imagePath;
  final String diseaseLabel;
  final String collectorName;
  final int patientAge;
  final String patientGender;
  final String patientNationality;
  final String patientNotes;
  final double? latitude;
  final double? longitude;
  final String locationName;
  final String collectedAt;

  CollectionEntry({
    this.id,
    required this.imagePath,
    required this.diseaseLabel,
    required this.collectorName,
    required this.patientAge,
    required this.patientGender,
    required this.patientNationality,
    required this.patientNotes,
    this.latitude,
    this.longitude,
    required this.locationName,
    required this.collectedAt,
  });

  Map<String, dynamic> toMap() => {
    if (id != null) 'id': id,
    'imagePath': imagePath,
    'diseaseLabel': diseaseLabel,
    'collectorName': collectorName,
    'patientAge': patientAge,
    'patientGender': patientGender,
    'patientNationality': patientNationality,
    'patientNotes': patientNotes,
    'latitude': latitude,
    'longitude': longitude,
    'locationName': locationName,
    'collectedAt': collectedAt,
  };

  factory CollectionEntry.fromMap(Map<String, dynamic> map) => CollectionEntry(
    id: map['id'],
    imagePath: map['imagePath'],
    diseaseLabel: map['diseaseLabel'],
    collectorName: map['collectorName'],
    patientAge: map['patientAge'],
    patientGender: map['patientGender'],
    patientNationality: map['patientNationality'],
    patientNotes: map['patientNotes'],
    latitude: map['latitude'],
    longitude: map['longitude'],
    locationName: map['locationName'],
    collectedAt: map['collectedAt'],
  );
}
