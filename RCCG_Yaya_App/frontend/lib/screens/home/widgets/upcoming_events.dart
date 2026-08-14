import 'package:flutter/material.dart';

class UpcomingEvents extends StatelessWidget {
  const UpcomingEvents({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: Colors.white.withOpacity(.10),
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: Colors.white24),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [

          const Row(
            children: [

              Icon(
                Icons.event,
                color: Colors.orange,
              ),

              SizedBox(width: 10),

              Text(
                "Upcoming Events",
                style: TextStyle(
                  color: Colors.white,
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                ),
              ),

            ],
          ),

          const SizedBox(height: 20),

          _eventTile(
            "YAYA Convention 2026",
            "30 July 2026",
          ),

          const Divider(color: Colors.white24),

          _eventTile(
            "Leadership Summit",
            "12 August 2026",
          ),

          const SizedBox(height: 15),

          Align(
            alignment: Alignment.centerRight,
            child: TextButton(
              onPressed: () {},
              child: const Text("See All"),
            ),
          ),
        ],
      ),
    );
  }

  Widget _eventTile(String title, String date) {
    return ListTile(
      contentPadding: EdgeInsets.zero,
      leading: const CircleAvatar(
        backgroundColor: Colors.orange,
        child: Icon(
          Icons.calendar_month,
          color: Colors.white,
        ),
      ),
      title: Text(
        title,
        style: const TextStyle(
          color: Colors.white,
          fontWeight: FontWeight.bold,
        ),
      ),
      subtitle: Text(
        date,
        style: const TextStyle(
          color: Colors.white70,
        ),
      ),
    );
  }
}