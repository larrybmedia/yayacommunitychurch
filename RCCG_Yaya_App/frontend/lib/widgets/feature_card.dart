import 'package:flutter/material.dart';
import 'glass_container.dart';

class FeatureCard extends StatelessWidget {
  final IconData icon;
  final Color iconColor;
  final String title;
  final String subtitle;
  final VoidCallback onTap;

  const FeatureCard({
    super.key,
    required this.icon,
    required this.iconColor,
    required this.title,
    required this.subtitle,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return InkWell(
      borderRadius: BorderRadius.circular(20),

      onTap: onTap,

      child: GlassContainer(
        child: Padding(
          padding: const EdgeInsets.all(25),

          child: Row(
            children: [
              CircleAvatar(
                radius: 30,

                backgroundColor: iconColor.withOpacity(.2),

                child: Icon(icon, size: 32, color: iconColor),
              ),

              const SizedBox(width: 20),

              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,

                  children: [
                    Text(
                      title,
                      style: const TextStyle(
                        color: Colors.white,
                        fontWeight: FontWeight.bold,
                        fontSize: 20,
                      ),
                    ),

                    const SizedBox(height: 8),

                    Text(
                      subtitle,
                      style: const TextStyle(color: Colors.white70),
                    ),
                  ],
                ),
              ),

              const Icon(Icons.arrow_forward_ios, color: Colors.white70),
            ],
          ),
        ),
      ),
    );
  }
}
