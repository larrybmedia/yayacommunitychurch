import 'package:flutter/material.dart';

class HeroBanner extends StatelessWidget {
  const HeroBanner({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.symmetric(horizontal: 20),
      padding: const EdgeInsets.all(25),
      decoration: BoxDecoration(
        color: Colors.white.withOpacity(0.12),
        borderRadius: BorderRadius.circular(25),
        border: Border.all(color: Colors.white24),
      ),
      child: Column(
        children: [
          Image.asset("assets/images/rccg_yaya.png", height: 90),

          const SizedBox(height: 20),

          const Text(
            "Welcome to Our Church",
            textAlign: TextAlign.center,
            style: TextStyle(
              fontSize: 30,
              fontWeight: FontWeight.bold,
              color: Colors.white,
            ),
          ),

          const SizedBox(height: 15),

          const Text(
            "Connecting branches, sharing resources, and growing together.",
            textAlign: TextAlign.center,
            style: TextStyle(color: Colors.white70, fontSize: 17, height: 1.6),
          ),

          const SizedBox(height: 25),

          ElevatedButton.icon(
            onPressed: () {},
            icon: const Icon(Icons.groups),
            label: const Text("Explore Community"),
            style: ElevatedButton.styleFrom(
              backgroundColor: const Color(0xFF0056D2),
              foregroundColor: Colors.white,
              padding: const EdgeInsets.symmetric(horizontal: 30, vertical: 15),
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(30),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
