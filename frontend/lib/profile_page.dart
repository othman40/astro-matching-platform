import 'package:flutter/material.dart';
import 'api_service.dart';
import 'models.dart';
import 'search_page.dart';

class ProfilePage extends StatelessWidget {
  final UserProfile profile;

  const ProfilePage({super.key, required this.profile});

  Widget _signTile(String title, String? value) {
    return ListTile(
      title: Text(title),
      subtitle: Text(value ?? 'Unknown'),
    );
  }

  @override
  Widget build(BuildContext context) {
    final api = ApiService();

    return Scaffold(
      appBar: AppBar(
        title: Text(profile.name),
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Text(
            profile.name,
            style: Theme.of(context).textTheme.headlineMedium,
          ),
          const SizedBox(height: 8),
          Text('Gender: ${profile.gender ?? "Unknown"}'),
          Text('Birth Date: ${profile.birthDate}'),
          Text('Birth Time: ${profile.birthTime}'),
          Text('Birth City: ${profile.birthCity}'),
          const SizedBox(height: 20),
          const Text(
            'Astrology Data',
            style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 12),
          _signTile('Sun', profile.sunSign),
          _signTile('Moon', profile.moonSign),
          _signTile('Mercury', profile.mercurySign),
          _signTile('Venus', profile.venusSign),
          _signTile('Mars', profile.marsSign),
          _signTile('Jupiter', profile.jupiterSign),
          _signTile('Saturn', profile.saturnSign),
          _signTile('Ascendant', profile.ascendant),
          const SizedBox(height: 20),
          ElevatedButton(
            onPressed: () async {
              final refreshed = await api.getProfile(profile.id);
              if (!context.mounted) return;

              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (_) => SearchPage(currentProfile: refreshed),
                ),
              );
            },
            child: const Text('Find Matches'),
          ),
        ],
      ),
    );
  }
}