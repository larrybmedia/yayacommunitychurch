import 'package:flutter/material.dart';

class LiveStreamCard extends StatelessWidget {
  const LiveStreamCard({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: Colors.red.withOpacity(.15),
        borderRadius: BorderRadius.circular(20),
        border: Border.all(
          color: Colors.redAccent,
        ),
      ),
      child: Column(
        children: [

          const Row(
            children: [

              Icon(
                Icons.live_tv,
                color: Colors.red,
              ),

              SizedBox(width: 10),

              Text(
                "LIVE NOW",
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
            "Sunday Worship Service",
            style: TextStyle(
              color: Colors.white,
              fontWeight: FontWeight.bold,
              fontSize: 18,
            ),
          ),

          const SizedBox(height: 8),

          const Text(
            "Join believers around the world in today's live service.",
            textAlign: TextAlign.center,
            style: TextStyle(
              color: Colors.white70,
            ),
          ),

          const SizedBox(height: 20),

          ElevatedButton.icon(
            onPressed: () {},
            icon: const Icon(Icons.play_arrow),
            label: const Text("Watch Live"),
          ),
        ],
      ),
    );
  }
}