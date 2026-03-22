import 'package:flutter/material.dart';
import 'api_service.dart';
import 'models.dart';

class SearchPage extends StatefulWidget {
  final UserProfile currentProfile;

  const SearchPage({super.key, required this.currentProfile});

  @override
  State<SearchPage> createState() => _SearchPageState();
}

class _SearchPageState extends State<SearchPage> {
  final _api = ApiService();
  bool _isLoading = true;
  List<MatchResult> _matches = [];

  @override
  void initState() {
    super.initState();
    _loadMatches();
  }

  Future<void> _loadMatches() async {
    try {
      final results = await _api.getMatches(widget.currentProfile.id);
      setState(() {
        _matches = results;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _isLoading = false;
      });

      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Failed to load matches: $e')),
      );
    }
  }

  String _titleFromLabel(String label) {
    switch (label) {
      case 'soulmate_match':
        return 'Soulmate Match';
      case 'strong_incomplete_love':
        return 'Strong Incomplete Love';
      case 'strong_emotional_union':
        return 'Strong Emotional Union';
      case 'very_good_compatibility':
        return 'Very Good Compatibility';
      case 'good_compatibility':
        return 'Good Compatibility';
      case 'good_similarity':
        return 'Good Similarity';
      case 'moderate_compatibility':
        return 'Moderate Compatibility';
      case 'mixed_compatibility':
        return 'Mixed Compatibility';
      default:
        return 'Difficult Relationship';
    }
  }

  void _showMatchDetails(MatchResult match) {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      builder: (_) {
        return Padding(
          padding: const EdgeInsets.all(16),
          child: ListView(
            shrinkWrap: true,
            children: [
              Text(
                match.name,
                style: Theme.of(context).textTheme.headlineSmall,
              ),
              const SizedBox(height: 8),
              Text('Compatibility: ${match.compatibilityScore.toStringAsFixed(0)}%'),
              Text(_titleFromLabel(match.matchLabel)),
              const SizedBox(height: 16),
              Text(
                match.details.reportText,
                style: const TextStyle(fontSize: 16),
              ),
              const SizedBox(height: 16),
              if (match.details.extraNotes.isNotEmpty) ...[
                const Text(
                  'Extra Notes',
                  style: TextStyle(fontWeight: FontWeight.bold),
                ),
                const SizedBox(height: 8),
                ...match.details.extraNotes.map((e) => Text('• $e')),
                const SizedBox(height: 16),
              ],
              if (match.details.compatiblePlanets.isNotEmpty) ...[
                const Text(
                  'Compatible Planets',
                  style: TextStyle(fontWeight: FontWeight.bold),
                ),
                const SizedBox(height: 8),
                Text(match.details.compatiblePlanets.join(', ')),
                const SizedBox(height: 16),
              ],
              if (match.details.incompatiblePlanets.isNotEmpty) ...[
                const Text(
                  'Incompatible Planets',
                  style: TextStyle(fontWeight: FontWeight.bold),
                ),
                const SizedBox(height: 8),
                Text(match.details.incompatiblePlanets.join(', ')),
              ],
            ],
          ),
        );
      },
    );
  }

  Widget _buildCard(MatchResult match) {
    return Card(
      child: ListTile(
        title: Text(match.name),
        subtitle: Text(
          '${_titleFromLabel(match.matchLabel)} - ${match.compatibilityScore.toStringAsFixed(0)}%',
        ),
        trailing: const Icon(Icons.chevron_right),
        onTap: () => _showMatchDetails(match),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Matches'),
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : _matches.isEmpty
              ? const Center(child: Text('No matches found'))
              : ListView.builder(
                  padding: const EdgeInsets.all(12),
                  itemCount: _matches.length,
                  itemBuilder: (_, index) => _buildCard(_matches[index]),
                ),
    );
  }
}