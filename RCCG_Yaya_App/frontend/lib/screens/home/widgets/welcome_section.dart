import 'package:flutter/material.dart';

class WelcomeSection extends StatelessWidget {
  const WelcomeSection({super.key});

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [

        Image.asset(
          "assets/images/rccg_yaya.png",
          height: 110,
        ),

        const SizedBox(height: 20),

        const Text(
          "Welcome to Our Church",
          textAlign: TextAlign.center,
          style: TextStyle(
            color: Colors.white,
            fontWeight: FontWeight.bold,
            fontSize: 34,
          ),
        ),

        const SizedBox(height: 10),

        const Padding(
          padding: EdgeInsets.symmetric(horizontal: 25),
          child: Text(
            "Connecting branches, sharing resources, and growing together.",
            textAlign: TextAlign.center,
            style: TextStyle(
              color: Colors.white70,
              fontSize: 17,
              height: 1.6,
            ),
          ),
        ),
      ],
    );
  }
}
