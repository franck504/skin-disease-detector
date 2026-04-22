import 'dart:io';
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:curved_navigation_bar/curved_navigation_bar.dart';
import 'screens/splash_screen.dart';
import 'screens/home_screen.dart';
import 'screens/collect_screen.dart';
import 'screens/collection_history_screen.dart';

import 'screens/scan_screen.dart';

class MyHttpOverrides extends HttpOverrides {
  @override
  HttpClient createHttpClient(SecurityContext? context) {
    return super.createHttpClient(context)
      ..badCertificateCallback =
          (X509Certificate cert, String host, int port) => true;
  }
}

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  HttpOverrides.global = MyHttpOverrides();
  runApp(const CutisiaApp());
}

class CutisiaApp extends StatelessWidget {
  const CutisiaApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Cutisia',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFF2E5BFF),
          primary: const Color(0xFF2E5BFF),
          secondary: const Color(0xFF00D09C),
          surface: const Color(0xFFF5F7FB),
        ),
        textTheme: GoogleFonts.outfitTextTheme(
          Theme.of(context).textTheme,
        ),
      ),
      initialRoute: '/',
      routes: {
        '/': (context) => const SplashScreen(),
        '/home': (context) => const MainShell(),
        '/scan': (context) => const ScanScreen(),
      },
    );
  }
}

/// Shell principal avec CurvedNavigationBar 3 onglets
class MainShell extends StatefulWidget {
  const MainShell({super.key});

  @override
  State<MainShell> createState() => _MainShellState();
}

class _MainShellState extends State<MainShell> {
  int _currentIndex = 0;

  final List<Widget> _screens = const [
    HomeScreen(),
    CollectScreen(),
    CollectionHistoryScreen(),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF5F7FB),
      extendBody: true,
      body: IndexedStack(
        index: _currentIndex,
        children: _screens,
      ),
      bottomNavigationBar: CurvedNavigationBar(
        index: _currentIndex,
        height: 65,
        backgroundColor: Colors.transparent,
        color: const Color(0xFF2E5BFF),
        buttonBackgroundColor: const Color(0xFF1A3BBF),
        animationDuration: const Duration(milliseconds: 350),
        animationCurve: Curves.easeInOut,
        items: const [
          Icon(Icons.home_rounded, color: Colors.white, size: 28), // Fandraisana
          Icon(Icons.add_a_photo_rounded, color: Colors.white, size: 28), // Fanangonana
          Icon(Icons.folder_special_rounded, color: Colors.white, size: 28), // Tahiry
        ],
        onTap: (index) => setState(() => _currentIndex = index),
      ),
    );
  }
}
