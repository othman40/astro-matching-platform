import 'package:flutter/material.dart';
import 'birth_data_form.dart';

void main() {
  runApp(const AstroMatchingApp());
}

class AstroMatchingApp extends StatelessWidget {
  const AstroMatchingApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Astro Matching Platform',
      debugShowCheckedModeBanner: false,
      theme: ThemeData.dark(),
      home: const BirthDataFormPage(),
    );
  }
}