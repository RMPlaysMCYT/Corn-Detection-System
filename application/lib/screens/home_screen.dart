import 'dart:async';
import 'package:cornseedapplication/utilities/dashboardCard.dart';
import 'package:flutter/material.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        child: Column(
          children: [
            Container(
              child: Wrap(
                spacing: 16.0, // Horizontal space between cards
                runSpacing: 16.0, // Vertical space when wrapping to a new line
                alignment: WrapAlignment.start,
                children: [
                  dashboardCard(
                    text: "Total Corn Detected",
                    value: "100",
                    backgroundColor: Colors.blue,
                  ),
                  dashboardCard(
                    text: "Total Corn Passed",
                    value: "80",
                    backgroundColor: Colors.green,
                  ),
                  dashboardCard(
                    value: "20",
                    text: "Total Corn Defected",
                    backgroundColor: Colors.red,
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
