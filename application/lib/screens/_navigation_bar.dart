import 'package:application/screens/camera_screen.dart';
import 'package:application/screens/home_screen.dart';
import 'package:application/screens/report_screen.dart';
import 'package:application/screens/settings_screen.dart';
import 'package:flutter/material.dart';

class NavigationBarWidget extends StatefulWidget {
  @override
  _NavigationBarState createState() => _NavigationBarState();
}

class _NavigationBarState extends State<NavigationBarWidget> {
  int _selectedIndex = 0;

  final List<Widget> _screens = [
    const HomeScreen(),
    const CameraScreen(),
    const ReportScreen(),
    const SettingsScreen(),
  ];

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        NavigationRail(
          minWidth: 72.0,
          extended: false,
          selectedIndex: _selectedIndex,
          onDestinationSelected: (index) {
            setState(() {
              _selectedIndex = index;
            });
          },
          selectedIconTheme: IconThemeData(
            color: Colors.blue,
            size: 40.0, // Resizes the selected icon
          ),
          unselectedIconTheme: IconThemeData(
            color: Colors.grey,
            size: 32.0, // Resizes unselected icons
          ),
          labelType: NavigationRailLabelType.selected,
          destinations: const <NavigationRailDestination>[
            NavigationRailDestination(
              icon: Icon(Icons.home),
              label: Text('Home'),
            ),
            NavigationRailDestination(
              icon: Icon(Icons.camera_alt),
              label: Text('Camera'),
            ),
            NavigationRailDestination(
              icon: Icon(Icons.checklist),
              label: Text('Report'),
            ),
            NavigationRailDestination(
              icon: Icon(Icons.settings),
              label: Text('Settings'),
            ),
          ],
        ),
        Expanded(child: _screens[_selectedIndex]),
      ],
    );
  }
}
