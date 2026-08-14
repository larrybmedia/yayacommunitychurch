import 'package:flutter/material.dart';
import 'screens/splash/splash_screen.dart';
import 'config/app_theme.dart';

void main() {
  runApp(const RCCGYayaApp());
}

class RCCGYayaApp extends StatelessWidget {
  const RCCGYayaApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'RCCG YAYA',
      debugShowCheckedModeBanner: false,
      theme: AppTheme.lightTheme,
      home: const SplashScreen(),
    );
  }
}
