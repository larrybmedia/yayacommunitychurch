import 'package:flutter/material.dart';

class HomeBackground extends StatelessWidget {
  const HomeBackground({super.key});

  @override
  Widget build(BuildContext context) {
    return Stack(
      children: [

        Positioned.fill(
          child: Image.asset(
            "assets/images/rccg_ycc.jpg",
            fit: BoxFit.cover,
          ),
        ),

        Positioned.fill(
          child: Container(
            decoration: BoxDecoration(
              gradient: LinearGradient(
                begin: Alignment.topCenter,
                end: Alignment.bottomCenter,
                colors: [
                  Colors.black.withOpacity(.45),
                  Colors.black.withOpacity(.65),
                ],
              ),
            ),
          ),
        ),
      ],
    );
  }
}
