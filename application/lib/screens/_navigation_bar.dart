import 'package:application/screens/camera_screen.dart';
import 'package:application/screens/home_screen.dart';
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
    const SettingsScreen(),
  ];

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        NavigationRail(
          selectedIndex: _selectedIndex,
          onDestinationSelected: (index) {
            setState(() {
              _selectedIndex = index;
            });
          },
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
