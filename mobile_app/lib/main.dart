import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'DeviceMind',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: const MyHomePage(),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({Key? key}) : super(key: key);

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  static const platform = MethodChannel('com.example.devicemind/devicedata');
  String _deviceData = 'Unknown';

  Future<void> _getDeviceData() async {
    String deviceData;
    try {
      final result = await platform.invokeMethod('getDeviceData');
      deviceData = 'Device Data: $result';
    } on PlatformException catch (e) {
      deviceData = "Failed to get device data: '${e.message}'.";
    }

    setState(() {
      _deviceData = deviceData;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('DeviceMind'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            const Text(
              'Device Data:',
            ),
            Text(
              _deviceData,
              style: Theme.of(context).textTheme.headlineMedium,
            ),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _getDeviceData,
        tooltip: 'Get Data',
        child: const Icon(Icons.data_usage),
      ),
    );
  }
}
