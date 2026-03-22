import 'package:flutter/material.dart';
import 'api_service.dart';
import 'models.dart';
import 'profile_page.dart';

class BirthDataFormPage extends StatefulWidget {
  const BirthDataFormPage({super.key});

  @override
  State<BirthDataFormPage> createState() => _BirthDataFormPageState();
}

class _BirthDataFormPageState extends State<BirthDataFormPage> {
  final _formKey = GlobalKey<FormState>();
  final _api = ApiService();

  final _nameController = TextEditingController();
  final _birthDateController = TextEditingController();
  final _birthTimeController = TextEditingController();
  final _birthCityController = TextEditingController();

  String? _selectedGender;
  bool _isLoading = false;

  Future<void> _createProfile() async {
    if (!_formKey.currentState!.validate()) return;

    setState(() {
      _isLoading = true;
    });

    try {
      final UserProfile profile = await _api.createProfile(
        name: _nameController.text.trim(),
        gender: _selectedGender,
        birthDate: _birthDateController.text.trim(),
        birthTime: _birthTimeController.text.trim(),
        birthCity: _birthCityController.text.trim(),
      );

      if (!mounted) return;

      Navigator.push(
        context,
        MaterialPageRoute(
          builder: (_) => ProfilePage(profile: profile),
        ),
      );
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error: $e')),
      );
    }

    if (mounted) {
      setState(() {
        _isLoading = false;
      });
    }
  }

  InputDecoration _decoration(String label) {
    return InputDecoration(
      labelText: label,
      border: const OutlineInputBorder(),
    );
  }

  @override
  void dispose() {
    _nameController.dispose();
    _birthDateController.dispose();
    _birthTimeController.dispose();
    _birthCityController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Create Astro Profile'),
      ),
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Form(
            key: _formKey,
            child: ListView(
              children: [
                TextFormField(
                  controller: _nameController,
                  decoration: _decoration('Name'),
                  validator: (value) =>
                      value == null || value.trim().isEmpty ? 'Enter your name' : null,
                ),
                const SizedBox(height: 16),
                DropdownButtonFormField<String>(
                  value: _selectedGender,
                  decoration: _decoration('Gender'),
                  items: const [
                    DropdownMenuItem(value: 'male', child: Text('Male')),
                    DropdownMenuItem(value: 'female', child: Text('Female')),
                  ],
                  onChanged: (value) {
                    setState(() {
                      _selectedGender = value;
                    });
                  },
                ),
                const SizedBox(height: 16),
                TextFormField(
                  controller: _birthDateController,
                  decoration: _decoration('Birth Date (YYYY-MM-DD)'),
                  validator: (value) => value == null || value.trim().isEmpty
                      ? 'Enter birth date'
                      : null,
                ),
                const SizedBox(height: 16),
                TextFormField(
                  controller: _birthTimeController,
                  decoration: _decoration('Birth Time (HH:MM)'),
                  validator: (value) => value == null || value.trim().isEmpty
                      ? 'Enter birth time'
                      : null,
                ),
                const SizedBox(height: 16),
                TextFormField(
                  controller: _birthCityController,
                  decoration: _decoration('Birth City'),
                  validator: (value) => value == null || value.trim().isEmpty
                      ? 'Enter birth city'
                      : null,
                ),
                const SizedBox(height: 24),
                ElevatedButton(
                  onPressed: _isLoading ? null : _createProfile,
                  child: _isLoading
                      ? const Padding(
                          padding: EdgeInsets.all(8),
                          child: CircularProgressIndicator(),
                        )
                      : const Text('Create Profile'),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}