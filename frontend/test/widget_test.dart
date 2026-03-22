import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:astro_matching_platform/main.dart';

void main() {
  testWidgets('App starts and shows create profile screen', (WidgetTester tester) async {
    await tester.pumpWidget(const AstroMatchingApp());

    expect(find.text('Create Astro Profile'), findsOneWidget);
    expect(find.byType(MaterialApp), findsOneWidget);
    expect(find.byType(ElevatedButton), findsOneWidget);
  });
}