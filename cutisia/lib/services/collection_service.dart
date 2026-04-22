import 'dart:io';
import 'package:path/path.dart';
import 'package:sqflite/sqflite.dart';
import 'package:path_provider/path_provider.dart';
import '../models/collection_entry.dart';

class CollectionService {
  static Database? _db;

  Future<Database> get database async {
    _db ??= await _initDb();
    return _db!;
  }

  Future<Database> _initDb() async {
    final dir = await getDatabasesPath();
    final path = join(dir, 'cutisia_collection.db');
    return await openDatabase(
      path,
      version: 1,
      onCreate: (db, version) async {
        await db.execute('''
          CREATE TABLE entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            imagePath TEXT NOT NULL,
            diseaseLabel TEXT NOT NULL,
            collectorName TEXT NOT NULL,
            patientAge INTEGER NOT NULL,
            patientGender TEXT NOT NULL,
            patientNationality TEXT NOT NULL,
            patientNotes TEXT,
            latitude REAL,
            longitude REAL,
            locationName TEXT,
            collectedAt TEXT NOT NULL
          )
        ''');
      },
    );
  }

  Future<int> insertEntry(CollectionEntry entry) async {
    final db = await database;
    return await db.insert('entries', entry.toMap());
  }

  Future<List<CollectionEntry>> getAllEntries() async {
    final db = await database;
    final maps = await db.query('entries', orderBy: 'id DESC');
    return maps.map((m) => CollectionEntry.fromMap(m)).toList();
  }

  Future<int> deleteEntry(int id) async {
    final db = await database;
    return await db.delete('entries', where: 'id = ?', whereArgs: [id]);
  }

  /// Exporte toutes les entrées sous forme de CSV et retourne le chemin du fichier
  Future<String> exportToCsv() async {
    final entries = await getAllEntries();
    final dir = await getApplicationDocumentsDirectory();
    final file = File('${dir.path}/cutisia_dataset_export.csv');

    final header = 'id,diseaseLabel,collectorName,patientAge,patientGender,'
        'patientNationality,patientNotes,latitude,longitude,locationName,'
        'collectedAt,imagePath\n';

    final rows = entries.map((e) {
      return '"${e.id}","${e.diseaseLabel}","${e.collectorName}",'
          '"${e.patientAge}","${e.patientGender}","${e.patientNationality}",'
          '"${e.patientNotes}","${e.latitude}","${e.longitude}",'
          '"${e.locationName}","${e.collectedAt}","${e.imagePath}"';
    }).join('\n');

    await file.writeAsString(header + rows);
    return file.path;
  }

  Future<int> countEntries() async {
    final db = await database;
    final result = await db.rawQuery('SELECT COUNT(*) FROM entries');
    return Sqflite.firstIntValue(result) ?? 0;
  }
}
