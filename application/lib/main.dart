import 'dart:async';
import 'dart:io';
import 'package:cornseedapplication/screens/_navigation_bar.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:camera/camera.dart';
import 'package:window_manager/window_manager.dart';
import 'package:nativeapi/nativeapi.dart' hide TitleBarStyle;

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  bool isDesktop = !kIsWeb && (Platform.isWindows || Platform.isLinux || Platform.isMacOS);

  if(isDesktop) {
      await windowManager.ensureInitialized();

  WindowOptions windowOptions = WindowOptions(
    size: Size(780, 500),
    center: true,
    backgroundColor: Colors.transparent,
    skipTaskbar: false,
    titleBarStyle: TitleBarStyle.hidden,
  );
  windowManager.waitUntilReadyToShow(windowOptions, () async {
    await windowManager.show();
    await windowManager.focus();
  });
  }

  // final cameras = await availableCameras();

  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Corn Detection System',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
      ),
      debugShowCheckedModeBanner: false,

      builder: (context, child) {
        return Scaffold(
          body: Column(
            children: [
              const CustomTitleBar(),
              Expanded(child: child!),
            ],
          ),
        );
      },
      home: MyHomePage(),
    );
  }
}

class MyHomePage extends StatefulWidget {
  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  @override
  void initState() {
    super.initState();
    Timer(
      Duration(seconds: 3),
      () => Navigator.pushReplacement(
        context,
        MaterialPageRoute(builder: (context) => NavigationBarWidget()),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      color: Colors.white,
      child: FlutterLogo(size: MediaQuery.of(context).size.height),
    );
  }
}

class CustomTitleBar extends StatelessWidget {
  const CustomTitleBar({super.key});

  @override
  Widget build(BuildContext context) {
    return DragToMoveArea(
      child: Container(
        height: 32, // Standard compact title bar height
        decoration: BoxDecoration(
          color: Colors.deepPurple.shade900, // Matches your deepPurple theme
        ),
        child: Row(
          children: [
            // App Title
            const Padding(
              padding: EdgeInsets.symmetric(horizontal: 12.0),
              child: Text(
                'Corn Detection System',
                style: TextStyle(
                  color: Colors.white,
                  fontSize: 12,
                  fontWeight: FontWeight.w600,
                ),
              ),
            ),

            const Spacer(), // Pushes buttons to the right
            // Minimize Button
            IconButton(
              icon: const Icon(Icons.remove, color: Colors.white, size: 24),
              padding: EdgeInsets.zero,
              constraints: const BoxConstraints(),
              splashRadius: 16,
              hoverColor: Colors.deepPurple.shade700,
              onPressed: () async => await windowManager.minimize(),
            ),
            const SizedBox(width: 12),

            // Maximize / Restore Button
            IconButton(
              icon: const Icon(
                Icons.crop_square,
                color: Colors.white,
                size: 24,
              ),
              padding: EdgeInsets.zero,
              constraints: const BoxConstraints(),
              splashRadius: 16,
              hoverColor: Colors.deepPurple.shade700,
              onPressed: () async {
                if (await windowManager.isMaximized()) {
                  await windowManager.unmaximize();
                } else {
                  await windowManager.maximize();
                }
              },
            ),
            const SizedBox(width: 12),

            // Close Button
            IconButton(
              icon: const Icon(Icons.close, color: Colors.white, size: 24),
              padding: EdgeInsets.zero,
              constraints: const BoxConstraints(),
              splashRadius: 16,
              hoverColor: Colors.red, // Classic red hover for close
              onPressed: () async => await windowManager.close(),
            ),
            const SizedBox(width: 8),
          ],
        ),
      ),
    );
  }
}
