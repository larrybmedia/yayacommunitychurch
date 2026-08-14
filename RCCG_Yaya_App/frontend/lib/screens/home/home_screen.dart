import 'package:flutter/material.dart';

import '../../widgets/app_header.dart';
import '../../widgets/feature_card.dart';
import '../../widgets/app_drawer.dart';
import '../../widgets/bottom_navigation.dart';

import 'widgets/hero_banner.dart';
import 'widgets/quick_actions.dart';
import 'widgets/daily_verse.dart';
import 'widgets/announcement_section.dart';
import 'widgets/upcoming_events.dart';
import 'widgets/live_stream_card.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      drawer: const AppDrawer(),
      bottomNavigationBar: const BottomNavigation(),

      body: Stack(
        children: [
          // ============================================================
          // BACKGROUND IMAGE
          // ============================================================
          Positioned.fill(
            child: Image.asset(
              'assets/images/rccg_ycc.jpg',
              fit: BoxFit.cover,
            ),
          ),

          // ============================================================
          // DARK OVERLAY
          // ============================================================
          Positioned.fill(
            child: Container(
              color: Colors.black54,
            ),
          ),

          // ============================================================
          // PAGE CONTENT
          // ============================================================
          SafeArea(
            child: SingleChildScrollView(
              physics: const BouncingScrollPhysics(),
              child: Column(
                children: [
                  // ======================================================
                  // HEADER
                  // ======================================================
                  const AppHeader(),

                  const SizedBox(height: 20),

                  // ======================================================
                  // HERO BANNER
                  // ======================================================
                  const HeroBanner(),

                  const SizedBox(height: 20),

                  // ======================================================
                  // DAILY VERSE
                  // ======================================================
                  const DailyVerse(),

                  const SizedBox(height: 20),

                  // ======================================================
                  // QUICK ACTIONS
                  // ======================================================
                  const QuickActions(),

                  const SizedBox(height: 25),

                  // ======================================================
                  // ANNOUNCEMENTS
                  // ======================================================
                  const AnnouncementSection(),

                  const SizedBox(height: 20),

                  // ======================================================
                  // UPCOMING EVENTS
                  // ======================================================
                  const UpcomingEvents(),

                  const SizedBox(height: 20),

                  // ======================================================
                  // LIVE STREAM
                  // ======================================================
                  const LiveStreamCard(),

                  const SizedBox(height: 30),

                  // ======================================================
                  // FOOTER
                  // ======================================================
                  const Padding(
                    padding: EdgeInsets.symmetric(horizontal: 20),
                    child: Column(
                      children: [
                        Text(
                          'RCCG YAYA COMMUNITY CHURCH',
                          textAlign: TextAlign.center,
                          style: TextStyle(
                            color: Colors.white,
                            fontWeight: FontWeight.bold,
                            fontSize: 15,
                          ),
                        ),

                        SizedBox(height: 8),

                        Text(
                          '© 2026 RCCG Youth and Young Adults.',
                          textAlign: TextAlign.center,
                          style: TextStyle(
                            color: Colors.white70,
                            fontSize: 13,
                          ),
                        ),

                        SizedBox(height: 25),

                        Text(
                          'Connecting branches, sharing resources, and growing together.',
                          textAlign: TextAlign.center,
                          style: TextStyle(
                            color: Colors.white54,
                            fontSize: 12,
                          ),
                        ),
                      ],
                    ),
                  ),

                  const SizedBox(height: 40),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
