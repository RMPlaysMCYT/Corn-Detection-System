import 'dart:async';
import 'package:flutter/material.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Column(
          children: [
            Container(
              padding: const EdgeInsets.all(16.0),
              child: Row(
                spacing: 12.0,
                children: [
                  Container(
                    padding: const EdgeInsets.only(left: 5.0),
                    width: 200.0,
                    height: 160.0,
                    color: Colors.blue,
                    child: Row(
                      children: [
                        Align(
                          alignment: Alignment.topLeft,
                          child: Text(
                            "Total Corn Detected",
                            style: TextStyle(
                              color: Colors.white,
                              shadows: [
                                Shadow(
                                  blurRadius: 5.0, // Softness of the shadow
                                  color: Colors.black.withAlpha(
                                    128,
                                  ), // Shadow color
                                  offset: Offset(
                                    4.0,
                                    4.0,
                                  ), // X and Y displacement
                                ),
                              ],
                              fontSize: 18,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                  Container(
                    padding: const EdgeInsets.only(left: 5.0),
                    width: 200.0,
                    height: 160.0,
                    color: Colors.blue,
                    child: Row(
                      children: [
                        Align(
                          alignment: Alignment.topLeft,
                          child: Text(
                            "Total Corn Passed",
                            style: TextStyle(
                              color: Colors.white,
                              shadows: [
                                Shadow(
                                  blurRadius: 5.0, // Softness of the shadow
                                  color: Colors.black.withAlpha(
                                    128,
                                  ), // Shadow color
                                  offset: Offset(
                                    4.0,
                                    4.0,
                                  ), // X and Y displacement
                                ),
                              ],
                              fontSize: 18,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                  Container(
                    padding: const EdgeInsets.only(left: 5.0),
                    width: 200.0,
                    height: 160.0,
                    color: Colors.blue,
                    child: Row(
                      children: [
                        Align(
                          alignment: Alignment.topLeft,
                          child: Text(
                            "Total Corn Defected",
                            style: TextStyle(
                              color: Colors.white,
                              shadows: [
                                Shadow(
                                  blurRadius: 5.0, // Softness of the shadow
                                  color: Colors.black.withAlpha(
                                    128,
                                  ), // Shadow color
                                  offset: Offset(
                                    4.0,
                                    4.0,
                                  ), // X and Y displacement
                                ),
                              ],
                              fontSize: 18,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                        ),
                      ],
                    ),
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
