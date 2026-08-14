import 'package:flutter/material.dart';

class AppDrawer extends StatelessWidget {
  const AppDrawer({super.key});

  @override
  Widget build(BuildContext context) {
    return Drawer(
      child: ListView(
        padding: EdgeInsets.zero,
        children: [
          const DrawerHeader(
            decoration: BoxDecoration(
              color: Color(0xFF0056D2),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                CircleAvatar(
                  radius: 30,
                  backgroundImage: AssetImage("assets/images/rccg_yaya.png"),
                ),
                SizedBox(height: 12),
                Text(
                  "RCCG YAYA",
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 22,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                Text(
                  "Youth and Young Adults",
                  style: TextStyle(color: Colors.white70),
                ),
              ],
            ),
          ),

          _drawerItem(Icons.home, "Home"),
          _drawerItem(Icons.info, "About"),
          _drawerItem(Icons.live_tv, "Live Stream"),
          _drawerItem(Icons.event, "Events"),
          _drawerItem(Icons.article, "News"),
          _drawerItem(Icons.menu_book, "Manuals"),
          _drawerItem(Icons.work, "Jobs"),
          _drawerItem(Icons.favorite, "Give"),
          _drawerItem(Icons.volunteer_activism, "Prayer"),
          _drawerItem(Icons.record_voice_over, "Testimonies"),
          _drawerItem(Icons.badge, "Membership"),
          const Divider(),
          _drawerItem(Icons.admin_panel_settings, "Admin Login"),
        ],
      ),
    );
  }

  static Widget _drawerItem(IconData icon, String title) {
    return ListTile(
      leading: Icon(icon),
      title: Text(title),
      onTap: () {
        // Navigation will be added later.
      },
    );
  }
}
