import 'package:flutter/material.dart';

class QuickActions extends StatelessWidget {
  const QuickActions({super.key});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 20),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            "Quick Access",
            style: TextStyle(
              color: Colors.white,
              fontSize: 22,
              fontWeight: FontWeight.bold,
            ),
          ),

          const SizedBox(height: 20),

          GridView.count(
            shrinkWrap: true,
            physics: const NeverScrollableScrollPhysics(),
            crossAxisCount: 3,
            crossAxisSpacing: 15,
            mainAxisSpacing: 15,
            childAspectRatio: .9,
            children: [
              _quickItem(Icons.people, "Community", Colors.blue),

              _quickItem(Icons.live_tv, "Live", Colors.red),

              _quickItem(Icons.event, "Events", Colors.orange),

              _quickItem(Icons.favorite, "Give", Colors.pink),

              _quickItem(Icons.volunteer_activism, "Prayer", Colors.green),

              _quickItem(Icons.article, "News", Colors.purple),
            ],
          ),
        ],
      ),
    );
  }

  Widget _quickItem(IconData icon, String title, Color color) {
    return Container(
      decoration: BoxDecoration(
        color: Colors.white.withOpacity(.12),

        borderRadius: BorderRadius.circular(20),
      ),

      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,

        children: [
          CircleAvatar(
            radius: 24,

            backgroundColor: color.withOpacity(.2),

            child: Icon(icon, color: color),
          ),

          const SizedBox(height: 12),

          Text(title, style: const TextStyle(color: Colors.white)),
        ],
      ),
    );
  }
}
