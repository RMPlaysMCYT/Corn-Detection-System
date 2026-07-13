import 'dart:async';
import 'package:cornseedapplication/utilities/reportsvariable.dart';
import 'package:cornseedapplication/utilities/texts.dart';
import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/material.dart';

class ReportScreen extends StatelessWidget {
  const ReportScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        child: Column(
          children: [
            // Header row
            Row(
              mainAxisAlignment: MainAxisAlignment.start,
              children: [
                const Padding(padding: EdgeInsets.all(16.0)),
                Text(ReportsPage, style: const TextStyle(fontSize: 24.0, fontWeight: FontWeight.normal)), // Make sure ReportsPage is defined
              ],
            ),
            const SizedBox(height: 8.0), // Space at the top
            // Bar chart
            Padding(
              padding: const EdgeInsets.all(16.0),
              child: SizedBox(
                height: 300, // Set a fixed height for the chart
                width: double.infinity, // Make the chart take full width
                child: BarChart(
                  BarChartData(
                    maxY: 100, // Maximum value on the Y axis
                    minY: 0, // Minimum value on the Y axis
                    gridData: const FlGridData(
                      show: false,
                    ), // Hide background grid lines
                    borderData: FlBorderData(show: false), // Hide outer borders
                    titlesData: FlTitlesData(
                      show: true,
                      topTitles: const AxisTitles(
                        sideTitles: SideTitles(showTitles: false),
                      ),
                      rightTitles: const AxisTitles(
                        sideTitles: SideTitles(showTitles: false),
                      ),
                      bottomTitles: AxisTitles(
                        sideTitles: SideTitles(
                          showTitles: true,
                          getTitlesWidget: (value, meta) {
                            // Map X-axis indexes to custom labels
                            switch (value.toInt()) {
                              case 0:
                                return const Text('M');
                              case 1:
                                return const Text('T');
                              case 2:
                                return const Text('W');
                              case 3:
                                return const Text('T');
                              case 4:
                                return const Text('F');
                              case 5:
                                return const Text('S');
                              case 6:
                                return const Text('S');
                              default:
                                return const Text('');
                            }
                          },
                        ),
                      ),
                    ),
                    // Map the data list into individual bar groups
                    barGroups: List.generate(7, (index) {
                      return BarChartGroupData(
                        x: index,
                        barRods: [
                          // First dataset (weeklySummary)
                          BarChartRodData(
                            toY: weeklySummary[index],
                            color: Colors.blue,
                            width: 8,
                            borderRadius: BorderRadius.circular(4),
                          ),
                          // Second dataset (weeklySummary2)
                          BarChartRodData(
                            toY: weeklySummary2[index],
                            color: Colors.orange,
                            width: 8,
                            borderRadius: BorderRadius.circular(4),
                          ),
                        ],
                      );
                    }),
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
