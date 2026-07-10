import 'package:flutter/material.dart';

class dashboardCard extends StatelessWidget {
  final String text;
  final String value;

  final Color? backgroundColor;
  final Color? textColor;
  final IconData? icon;
  final double borderRadius;

  const dashboardCard({
    super.key,
    required this.text,
    required this.value,
    this.backgroundColor,
    this.textColor,
    this.icon,
    this.borderRadius = 8.0,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      // Cleaned up the padding to be uniform around the whole card
      padding: const EdgeInsets.all(16.0),
      width: 200.0,
      height: 160.0,
      decoration: BoxDecoration(
        color: backgroundColor ?? Colors.blue,
        borderRadius: BorderRadius.circular(borderRadius),
      ),
      // Swapped Row for Column to stack the title and the number vertically
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisAlignment:
            MainAxisAlignment.spaceBetween, // Pushes title up, number down
        children: [
          // 1. The Title
          Text(
            text,
            style: TextStyle(
              color: Colors.white,
              shadows: [
                Shadow(
                  blurRadius: 5.0,
                  color: Colors.black.withAlpha(128),
                  offset: const Offset(2.0, 2.0),
                ),
              ],
              fontSize: 18,
              fontWeight: FontWeight.bold,
            ),
          ),

          // 2. The Big Data Number
          Align(
            alignment: Alignment
                .bottomRight, // Puts the number in the bottom right corner
            child: Text(
              value,
              style: TextStyle(
                color: Colors.white,
                fontSize: 64, // Make the data massive and easy to read
                fontWeight: FontWeight.w900,
                shadows: [
                  Shadow(
                    blurRadius: 8.0,
                    color: Colors.black.withAlpha(128),
                    offset: const Offset(3.0, 3.0),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
