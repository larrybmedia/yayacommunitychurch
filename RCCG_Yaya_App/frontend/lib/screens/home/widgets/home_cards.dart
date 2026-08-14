import 'package:flutter/material.dart';

import '../../../widgets/feature_card.dart';

class HomeCards extends StatelessWidget {
  const HomeCards({super.key});

  @override
  Widget build(BuildContext context) {
    return ListView(
      padding: const EdgeInsets.symmetric(horizontal: 20),
      children: [
        FeatureCard(
          icon: Icons.people,
          iconColor: Colors.blue,
          title: "Our Community",
          subtitle: "Join our vibrant network of branches nationwide.",
          onTap: () {
            // Navigate to Community Screen
          },
        ),

        const SizedBox(height: 20),

        FeatureCard(
          icon: Icons.live_tv,
          iconColor: Colors.red,
          title: "Live Streams",
          subtitle: "Watch our services live from anywhere in the world.",
          onTap: () {
            // Navigate to Live Stream
          },
        ),

        const SizedBox(height: 20),

        FeatureCard(
          icon: Icons.menu_book,
          iconColor: Colors.green,
          title: "Resource Library",
          subtitle: "Access manuals, teachings and spiritual materials.",
          onTap: () {
            // Navigate to Resource Library
          },
        ),

        const SizedBox(height: 20),

        FeatureCard(
          icon: Icons.event,
          iconColor: Colors.orange,
          title: "Events",
          subtitle: "View upcoming programmes and conferences.",
          onTap: () {
            // Navigate to Events
          },
        ),

        const SizedBox(height: 30),
      ],
    );
  }
}
