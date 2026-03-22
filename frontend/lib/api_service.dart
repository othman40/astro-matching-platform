import 'dart:convert';
import 'package:http/http.dart' as http;
import 'models.dart';

class ApiService {
  static const String baseUrl = 'http://127.0.0.1:8000';

  Future<UserProfile> createProfile({
    required String name,
    required String? gender,
    required String birthDate,
    required String birthTime,
    required String birthCity,
  }) async {
    final response = await http.post(
      Uri.parse('$baseUrl/create-profile'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'name': name,
        'gender': gender,
        'birth_date': birthDate,
        'birth_time': birthTime,
        'birth_city': birthCity,
      }),
    );

    if (response.statusCode != 200) {
      throw Exception('Failed to create profile: ${response.body}');
    }

    return UserProfile.fromJson(jsonDecode(response.body));
  }

  Future<List<UserProfile>> getProfiles() async {
    final response = await http.get(Uri.parse('$baseUrl/profiles'));

    if (response.statusCode != 200) {
      throw Exception('Failed to load profiles');
    }

    final List<dynamic> data = jsonDecode(response.body);
    return data.map((e) => UserProfile.fromJson(e)).toList();
  }

  Future<UserProfile> getProfile(int id) async {
    final response = await http.get(Uri.parse('$baseUrl/profiles/$id'));

    if (response.statusCode != 200) {
      throw Exception('Failed to load profile');
    }

    return UserProfile.fromJson(jsonDecode(response.body));
  }

  Future<List<MatchResult>> getMatches(int profileId) async {
    final response = await http.get(Uri.parse('$baseUrl/match/$profileId'));

    if (response.statusCode != 200) {
      throw Exception('Failed to load matches');
    }

    final List<dynamic> data = jsonDecode(response.body);
    return data.map((e) => MatchResult.fromJson(e)).toList();
  }
}