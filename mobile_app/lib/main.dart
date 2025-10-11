import 'package.dart';
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
  String _deviceData = 'No data yet. Press a button to fetch data.';

  // 네이티브 코드를 호출하여 디바이스 데이터를 가져오는 함수
  // 이제 'interval' 파라미터를 받아서 네이티브에 전달합니다.
  Future<void> _getDeviceData(String interval) async {
    String deviceData;
    try {
      // invokeMethod를 호출할 때, 두 번째 인자로 파라미터를 Map 형태로 전달합니다.
      final result = await platform.invokeMethod('getDeviceData', {'interval': interval});
      // 결과 데이터를 예쁘게 포맷팅합니다.
      deviceData = _formatResult(result);
    } on PlatformException catch (e) {
      deviceData = "Failed to get device data: '${e.message}'.";
    }

    setState(() {
      _deviceData = deviceData;
    });
  }

  // 네이티브에서 받은 Map 데이터를 사람이 읽기 좋은 문자열로 변환합니다.
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

      // 사용 시간(ms)을 분 단위로 변환하고, 상위 5개 앱만 표시합니다.
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
          crossAxisAlignment: CrossAxisAlignment.start,
          children: <Widget>[
            const Text(
              'Device Data:',
              style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 10),
            // 데이터를 보여줄 스크롤 가능한 영역
            Expanded(
              child: SingleChildScrollView(
                child: Text(
                  _deviceData,
                  style: Theme.of(context).textTheme.bodyMedium,
                ),
              ),
            ),
            const SizedBox(height: 20),
            // 데이터 수집 기간을 선택하는 버튼들
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                ElevatedButton(
                  onPressed: () => _getDeviceData('daily'),
                  child: const Text('Daily'),
                ),
                ElevatedButton(
                  onPressed: () => _getDeviceData('weekly'),
                  child: const Text('Weekly'),
                ),
                ElevatedButton(
                  onPressed: () => _getDeviceData('monthly'),
                  child: const Text('Monthly'),
                ),
              ],
            )
          ],
        ),
      ),
    );
  }
}
