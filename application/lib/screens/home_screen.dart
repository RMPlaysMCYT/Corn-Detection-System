import 'dart:async';
import 'package:cornseedapplication/utilities/dashboardCard.dart';
import 'package:cornseedapplication/utilities/texts.dart';
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
              child: Column(
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.start,
                    children: [
                      Padding(
                        padding: const EdgeInsets.all(16.0),
                        child: Text(
                          DashboardText,
                          style: TextStyle(
                            fontSize: 24,
                            fontWeight: FontWeight.normal,
                          ),
                        ),
                      ),
                    ],
                  ),
                  SizedBox(height: 8.0), // Space at the top
                  Wrap(
                    spacing: 16.0, // Horizontal space between cards
                    runSpacing:
                        16.0, // Vertical space when wrapping to a new line
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
                  SizedBox(height: 16.0), // Space at the bottom
                  Row(
                    mainAxisAlignment: MainAxisAlignment.start,
                    children: [
                      Padding(
                        padding: const EdgeInsets.all(16.0),
                        child: Text(
                          HistoryText,
                          style: TextStyle(
                            fontSize: 24,
                            fontWeight: FontWeight.normal,
                          ),
                        ),
                      ),
                    ],
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
