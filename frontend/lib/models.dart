class PlanetPosition {
  final String name;
  final String sign;
  final double? degree;
  final int? house;

  PlanetPosition({
    required this.name,
    required this.sign,
    this.degree,
    this.house,
  });

  factory PlanetPosition.fromJson(Map<String, dynamic> json) {
    return PlanetPosition(
      name: json['name'] ?? '',
      sign: json['sign'] ?? '',
      degree: json['degree'] != null ? (json['degree'] as num).toDouble() : null,
      house: json['house'],
    );
  }
}

class UserProfile {
  final int id;
  final String name;
  final String? gender;
  final String birthDate;
  final String birthTime;
  final String birthCity;

  final String? sunSign;
  final String? moonSign;
  final String? mercurySign;
  final String? venusSign;
  final String? marsSign;
  final String? jupiterSign;
  final String? saturnSign;
  final String? ascendant;
  final String? ascendantSign;

  final List<PlanetPosition> planetaryPositions;

  UserProfile({
    required this.id,
    required this.name,
    required this.gender,
    required this.birthDate,
    required this.birthTime,
    required this.birthCity,
    required this.sunSign,
    required this.moonSign,
    required this.mercurySign,
    required this.venusSign,
    required this.marsSign,
    required this.jupiterSign,
    required this.saturnSign,
    required this.ascendant,
    required this.ascendantSign,
    required this.planetaryPositions,
  });

  factory UserProfile.fromJson(Map<String, dynamic> json) {
    final positions = (json['planetary_positions'] as List?)
            ?.map((e) => PlanetPosition.fromJson(e))
            .toList() ??
        [];

    return UserProfile(
      id: json['id'],
      name: json['name'] ?? '',
      gender: json['gender'],
      birthDate: json['birth_date'] ?? '',
      birthTime: json['birth_time'] ?? '',
      birthCity: json['birth_city'] ?? '',
      sunSign: json['sun_sign'],
      moonSign: json['moon_sign'],
      mercurySign: json['mercury_sign'],
      venusSign: json['venus_sign'],
      marsSign: json['mars_sign'],
      jupiterSign: json['jupiter_sign'],
      saturnSign: json['saturn_sign'],
      ascendant: json['ascendant'],
      ascendantSign: json['ascendant_sign'],
      planetaryPositions: positions,
    );
  }
}

class MatchDetails {
  final double overallScore;
  final String matchLabel;
  final String category;
  final String reportText;
  final List<String> extraNotes;
  final List<String> compatiblePlanets;
  final List<String> incompatiblePlanets;
  final List<String> missingPlanets;

  MatchDetails({
    required this.overallScore,
    required this.matchLabel,
    required this.category,
    required this.reportText,
    required this.extraNotes,
    required this.compatiblePlanets,
    required this.incompatiblePlanets,
    required this.missingPlanets,
  });

  factory MatchDetails.fromJson(Map<String, dynamic> json) {
    return MatchDetails(
      overallScore: (json['overall_score'] as num).toDouble(),
      matchLabel: json['match_label'] ?? '',
      category: json['category'] ?? '',
      reportText: json['report_text'] ?? '',
      extraNotes: List<String>.from(json['extra_notes'] ?? []),
      compatiblePlanets: List<String>.from(json['compatible_planets'] ?? []),
      incompatiblePlanets: List<String>.from(json['incompatible_planets'] ?? []),
      missingPlanets: List<String>.from(json['missing_planets'] ?? []),
    );
  }
}

class MatchResult {
  final int userId;
  final String name;
  final double compatibilityScore;
  final String matchLabel;
  final MatchDetails details;

  MatchResult({
    required this.userId,
    required this.name,
    required this.compatibilityScore,
    required this.matchLabel,
    required this.details,
  });

  factory MatchResult.fromJson(Map<String, dynamic> json) {
    return MatchResult(
      userId: json['user_id'],
      name: json['name'] ?? '',
      compatibilityScore: (json['compatibility_score'] as num).toDouble(),
      matchLabel: json['match_label'] ?? '',
      details: MatchDetails.fromJson(json['details']),
    );
  }
}