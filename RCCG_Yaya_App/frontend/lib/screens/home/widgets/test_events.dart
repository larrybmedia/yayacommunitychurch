import 'package:flutter/material.dart';

import '../../../services/event_service.dart';
import '../../../models/event_model.dart';

class TestEvents extends StatefulWidget {
  const TestEvents({super.key});

  @override
  State<TestEvents> createState() => _TestEventsState();
}

class _TestEventsState extends State<TestEvents> {
  final EventService _eventService = EventService();

  bool loading = true;
  String? error;
  List<EventModel> events = [];

  @override
  void initState() {
    super.initState();
    loadEvents();
  }

  Future<void> loadEvents() async {
    try {
      final result = await _eventService.getEvents();

      setState(() {
        events = result;
        loading = false;
      });
    } catch (e) {
      setState(() {
        error = e.toString();
        loading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    if (loading) {
      return const Center(child: CircularProgressIndicator());
    }

    if (error != null) {
      return Padding(
        padding: const EdgeInsets.all(20),
        child: Text('Error: $error', style: const TextStyle(color: Colors.red)),
      );
    }

    if (events.isEmpty) {
      return const Padding(
        padding: EdgeInsets.all(20),
        child: Text(
          'No events available.',
          style: TextStyle(color: Colors.white),
        ),
      );
    }

    return Column(
      children: events.map((event) {
        return ListTile(
          title: Text(event.title, style: const TextStyle(color: Colors.white)),
          subtitle: Text(
            event.date,
            style: const TextStyle(color: Colors.white70),
          ),
        );
      }).toList(),
    );
  }
}
