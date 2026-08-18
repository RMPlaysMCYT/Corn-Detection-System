import 'package:cornseedapplication/screens/home_screen.dart';
import 'package:flutter/material.dart';

class SortingScreenFinished extends StatefulWidget {
  const SortingScreenFinished({super.key});

  @override
  _SortingScreenFinishedState createState() => _SortingScreenFinishedState();
}

class _SortingScreenFinishedState extends State<SortingScreenFinished> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Container(
          child: Row(
            children: [
              Text('Sorting Screen Finished'),
              Text('Total Seeds Sorted: '),
              Text('Sorting Healthy Seeds: '),
              Text('Sorting Unhealthy Seeds: '),
              Column(
                children: [
                  ElevatedButton(onPressed: (){
                    Navigator.push(
                      context,
                      MaterialPageRoute(builder: (context) => const HomeScreen()),
                    );
                  }, child: const Text("Exit"))
                ],
              )
            ],
          )
        ),
      ),
    );
  }
}