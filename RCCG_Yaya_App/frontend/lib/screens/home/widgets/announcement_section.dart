import 'package:flutter/material.dart';

class AnnouncementSection extends StatelessWidget {
  const AnnouncementSection({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: Colors.orange.withOpacity(.15),
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: Colors.orange.shade300),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Row(
            children: [
              Icon(Icons.campaign, color: Colors.orange),

              SizedBox(width: 10),

              Text(
                "Latest Announcement",
                style: TextStyle(
                  color: Colors.white,
                  fontWeight: FontWeight.bold,
                  fontSize: 20,
                ),
              ),
            ],
          ),

          const SizedBox(height: 20),

          const Text(
            "YAYA Convention 2026",
            style: TextStyle(
              color: Colors.white,
              fontWeight: FontWeight.bold,
              fontSize: 18,
            ),
          ),

          const SizedBox(height: 8),

          const Text(
            "Registration is now open for all youth and young adults across RCCG.",
            style: TextStyle(color: Colors.white70, height: 1.5),
          ),

          const SizedBox(height: 20),

          TextButton(
            onPressed: () {},
            child: const Text(
              "Read More",
              style: TextStyle(color: Colors.amber),
            ),
          ),
        ],
      ),
    );
  }
}
