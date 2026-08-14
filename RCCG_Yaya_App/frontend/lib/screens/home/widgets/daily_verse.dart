import 'package:flutter/material.dart';

class DailyVerse extends StatelessWidget {
  const DailyVerse({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: Colors.white.withOpacity(0.12),
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: Colors.white24),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Row(
            children: [
              Icon(Icons.menu_book, color: Colors.amber),
              SizedBox(width: 10),
              Text(
                "Daily Bible Verse",
                style: TextStyle(
                  color: Colors.white,
                  fontWeight: FontWeight.bold,
                  fontSize: 20,
                ),
              ),
            ],
          ),

          const SizedBox(height: 15),

          const Text(
            "\"Trust in the Lord with all your heart and lean not on your own understanding.\"",
            style: TextStyle(
              color: Colors.white,
              fontSize: 16,
              height: 1.6,
              fontStyle: FontStyle.italic,
            ),
          ),

          const SizedBox(height: 15),

          const Align(
            alignment: Alignment.centerRight,
            child: Text(
              "Proverbs 3:5",
              style: TextStyle(
                color: Colors.white70,
                fontWeight: FontWeight.bold,
              ),
            ),
          ),

          const SizedBox(height: 15),

          SizedBox(
            width: double.infinity,
            child: ElevatedButton.icon(
              onPressed: () {
                // Later this will open the full devotional.
              },
              icon: const Icon(Icons.book),
              label: const Text("Read Devotional"),
            ),
          ),
        ],
      ),
    );
  }
}
