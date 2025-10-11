import 'package.dart';
import 'dart:convert'; // JSON 인코딩을 위해 추가
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:http/http.dart' as http; // http 패키지 임포트

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
        textTheme: const TextTheme(
          bodyMedium: TextStyle(fontSize: 16),
          headlineMedium: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
        )
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
  
  // 수집된 데이터를 저장할 변수
  Map<String, dynamic>? _collectedData;
  String _statusText = 'No data yet. Press a button to fetch data.';

  // 네이티브 코드를 호출하여 디바이스 데이터를 가져오는 함수
  Future<void> _getDeviceData(String interval) async {
    try {
      final result = await platform.invokeMethod('getDeviceData', {'interval': interval});
      setState(() {
        _collectedData = Map<String, dynamic>.from(result);
        _statusText = _formatResult(_collectedData);
      });
    } on PlatformException catch (e) {
      setState(() {
        _statusText = "Failed to get device data: '${e.message}'.";
      });
    }
  }

  // 수집된 데이터를 서버로 업로드하는 함수
  Future<void> _uploadData() async {
    if (_collectedData == null) {
      setState(() {
        _statusText = 'No data to upload. Please fetch data first.';
      });
      return;
    }

    // 중요: 안드로이드 에뮬레이터에서 localhost(127.0.0.1)는 에뮬레이터 자신을 가리킵니다.
    //       개발용 PC의 localhost에 접속하려면 10.0.2.2를 사용해야 합니다.
    //       실제 디바이스에서 테스트하려면, PC의 실제 IP 주소를 입력하세요. (예: http://192.168.1.5:8000/data/)
    const serverUrl = 'http://10.0.2.2:8000/data/';

    setState(() {
      _statusText = 'Uploading data to server...';
    });

    try {
      final response = await http.post(
        Uri.parse(serverUrl),
        headers: {'Content-Type': 'application/json; charset=UTF-8'},
        body: jsonEncode(_collectedData), // 데이터를 JSON 문자열로 인코딩
      );

      if (response.statusCode == 200) {
        setState(() {
          _statusText = 'Upload successful!\nServer response: ${response.body}';
        });
      } else {
        setState(() {
          _statusText = 'Upload failed. Status code: ${response.statusCode}\nResponse: ${response.body}';
        });
      }
    } catch (e) {
      setState(() {
        _statusText = 'Error uploading data: $e';
      });
    }
  }

  // Map 데이터를 사람이 읽기 좋은 문자열로 변환합니다.
  String _formatResult(dynamic result) {
    if (result is Map) {
      final battery = result['batteryPerformance'];
      final usage = result['appUsage'] as List;

      final batteryInfo = '''
--- Battery Performance ---
- Level: ${battery['level'].toStringAsFixed(1)}%
- Health: ${battery['health']}
- Status: ${battery['status']}
- Temperature: ${battery['temperature']}°C
- Voltage: ${battery['voltage']}V
''';

      usage.sort((a, b) => b['totalTimeInForeground'].compareTo(a['totalTimeInForeground']));
      final top5Usage = usage.take(5);

      final usageInfo = top5Usage.map((app) {
        final minutes = (app['totalTimeInForeground'] / 60000).toStringAsFixed(1);
        return '- ${app['packageName']}: ${minutes} min';
      }).join('\n');

      return '$batteryInfo\n--- App Usage (Top 5) ---\n$usageInfo';
    }
    return result.toString();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('DeviceMind'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: <Widget>[
            const Text(
              'Device Data:',
              style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 10),
            Expanded(
              child: SingleChildScrollView(
                child: Text(
                  _statusText,
                  style: Theme.of(context).textTheme.bodyMedium,
                ),
              ),
            ),
            const SizedBox(height: 20),
            // 데이터 수집 기간을 선택하는 버튼들
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                ElevatedButton(onPressed: () => _getDeviceData('daily'), child: const Text('Daily')),
                ElevatedButton(onPressed: () => _getDeviceData('weekly'), child: const Text('Weekly')),
                ElevatedButton(onPressed: () => _getDeviceData('monthly'), child: const Text('Monthly')),
              ],
            ),
            const SizedBox(height: 10),
            // 서버로 데이터를 업로드하는 버튼
            ElevatedButton(
              onPressed: _uploadData, 
              style: ElevatedButton.styleFrom(backgroundColor: Colors.green),
              child: const Text('Upload to Server'),
            ),
          ],
        ),
      ),
    );
  }
}
