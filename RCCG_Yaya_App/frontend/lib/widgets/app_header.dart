import 'package:flutter/material.dart';

class AppHeader extends StatelessWidget {
  const AppHeader({super.key});

  @override
  Widget build(BuildContext context) {
    return Builder(
      builder: (context) {
        return Padding(
          padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 15),
          child: Row(
            children: [
              CircleAvatar(
                radius: 22,
                backgroundColor: Colors.white24,
                child: IconButton(
                  icon: const Icon(Icons.menu, color: Colors.white),
                  onPressed: () {
                    Scaffold.of(context).openDrawer();
                  },
                ),
              ),

              const SizedBox(width: 15),

              Expanded(
                child: Row(
                  children: [
                    Image.asset("assets/images/rccg_yaya.png", height: 40),

                    const SizedBox(width: 10),

                    const Expanded(
                      child: Text(
                        "YAYA Church Community",
                        style: TextStyle(
                          color: Colors.white,
                          fontWeight: FontWeight.bold,
                          fontSize: 18,
                        ),
                      ),
                    ),
                  ],
                ),
              ),

              CircleAvatar(
                radius: 22,
                backgroundColor: Colors.white24,
                child: IconButton(
                  icon: const Icon(
                    Icons.notifications_none,
                    color: Colors.white,
                  ),
                  onPressed: () {},
                ),
              ),
            ],
          ),
        );
      },
    );
  }
}
