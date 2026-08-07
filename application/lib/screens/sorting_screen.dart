import 'package:flutter/material.dart';

class SortingScreen extends StatefulWidget {
  const SortingScreen({super.key});

  @override
  _SortingScreenState createState() => _SortingScreenState();
}

class _SortingScreenState extends State<SortingScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Column(
                  children: [
                    Text('Status:', style: TextStyle(fontSize: 24)),
                    Text('Current: ', style: TextStyle(fontSize: 24)),
                    Text('Healthy: ', style: TextStyle(fontSize: 24)),
                    Text('Unhealthy: ', style: TextStyle(fontSize: 24)),
                    Text('System Status: ', style: TextStyle(fontSize: 24)),
                  ],
                ),
                
                Column(
                  children: [
                    Text('Status:', style: TextStyle(fontSize: 24)),
                    Text('Current: ', style: TextStyle(fontSize: 24)),
                    Text('Healthy: ', style: TextStyle(fontSize: 24)),
                    Text('Unhealthy: ', style: TextStyle(fontSize: 24)),
                    Text('System Status: ', style: TextStyle(fontSize: 24)),
                  ],
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
