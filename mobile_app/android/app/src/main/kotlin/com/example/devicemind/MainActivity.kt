// 패키지 이름 선언
package com.example.devicemind

// 안드로이드 및 Flutter와 통신하는 데 필요한 클래스들을 임포트합니다.
import android.app.AppOpsManager
import android.app.usage.UsageStatsManager
import android.content.Context
import android.content.Intent
import android.os.BatteryManager
import android.os.Process
import android.provider.Settings
import io.flutter.embedding.android.FlutterActivity
import io.flutter.embedding.engine.FlutterEngine
import io.flutter.plugin.common.MethodChannel
import java.util.concurrent.TimeUnit


// Flutter 앱을 호스팅하는 메인 액티비티 클래스입니다.
class MainActivity: FlutterActivity() {
    // Flutter와 네이티브 코드 간의 통신 채널 이름입니다. 이 이름이 같아야 서로 통신할 수 있습니다.
    private val CHANNEL = "com.example.devicemind/devicedata"

    // Flutter 엔진이 설정될 때 호출되는 함수입니다. 여기서 MethodChannel을 설정합니다.
    override fun configureFlutterEngine(flutterEngine: FlutterEngine) {
        super.configureFlutterEngine(flutterEngine)
        
        // MethodChannel을 생성하고, Flutter로부터 오는 메시지를 처리할 핸들러를 설정합니다.
        MethodChannel(flutterEngine.dartExecutor.binaryMessenger, CHANNEL).setMethodCallHandler {
            call, result ->
            // Flutter에서 호출한 메소드 이름이 "getDeviceData"인지 확인합니다.
            if (call.method == "getDeviceData") {
                // 앱 사용 기록 접근 권한이 있는지 확인합니다.
                if (!hasUsageStatsPermission()) {
                    // 권한이 없으면, 사용자가 직접 권한을 설정할 수 있도록 시스템 설정 화면으로 안내합니다.
                    startActivity(Intent(Settings.ACTION_USAGE_ACCESS_SETTINGS))
                    // Flutter에 권한이 없다는 에러를 보냅니다.
                    result.error("PERMISSION_DENIED", "Usage stats permission is not enabled.", null)
                } else {
                    // 권한이 있으면, 디바이스 데이터를 수집하는 함수를 호출합니다.
                    val data = getDeviceData()
                    // 수집된 데이터를 Flutter에 성공적으로 전달합니다.
                    result.success(data)
                }
            } else {
                // 호출된 메소드가 구현되지 않았을 경우, 'notImplemented' 상태를 반환합니다.
                result.notImplemented()
            }
        }
    }

    // 앱 사용 기록 접근 권한이 있는지 확인하는 내부 함수입니다.
    private fun hasUsageStatsPermission(): Boolean {
        // AppOpsManager를 통해 현재 앱의 권한 상태를 확인합니다.
        val appOps = getSystemService(Context.APP_OPS_SERVICE) as AppOpsManager
        val mode = appOps.checkOpNoThrow(AppOpsManager.OPSTR_GET_USAGE_STATS, Process.myUid(), packageName)
        // 권한이 허용(MODE_ALLOWED) 상태인지 여부를 반환합니다.
        return mode == AppOpsManager.MODE_ALLOWED
    }

    // 실제 디바이스 데이터를 수집하는 내부 함수입니다.
    private fun getDeviceData(): Map<String, Any> {
        // 1. 배터리 종합 성능 데이터 수집
        val batteryPerformance = getBatteryPerformanceData()

        // 2. 앱 사용 기록 수집
        // USAGE_STATS_SERVICE를 통해 UsageStatsManager 인스턴스를 가져옵니다.
        val usageStatsManager = getSystemService(Context.USAGE_STATS_SERVICE) as UsageStatsManager
        val time = System.currentTimeMillis()
        // 지난 24시간 동안의 앱 사용 통계를 쿼리합니다.
        val stats = usageStatsManager.queryUsageStats(UsageStatsManager.INTERVAL_DAILY, time - TimeUnit.DAYS.toMillis(1), time)

        // 수집된 통계 데이터를 Flutter로 보내기 좋은 형태로 가공합니다.
        // 사용 시간이 0보다 큰 앱들만 필터링합니다.
        val appUsage = stats?.filter { it.totalTimeInForeground > 0 }?.map {
            // 각 앱에 대해 패키지 이름과 총 사용 시간(Foreground)을 맵으로 만듭니다.
            mapOf(
                "packageName" to it.packageName,
                "totalTimeInForeground" to it.totalTimeInForeground
            )
        }

        // 최종적으로 수집된 모든 데이터를 하나의 맵으로 묶어서 반환합니다.
        return mapOf(
            "batteryPerformance" to batteryPerformance,
            "appUsage" to (appUsage ?: emptyList()) // 앱 사용 기록이 null일 경우 빈 리스트를 보냅니다.
        )
    }

    // 배터리 관련 데이터를 수집하는 상세 함수입니다.
    private fun getBatteryPerformanceData(): Map<String, Any> {
        val intentFilter = android.content.IntentFilter(Intent.ACTION_BATTERY_CHANGED)
        val batteryStatus = context.registerReceiver(null, intentFilter)

        val health = batteryStatus?.getIntExtra(BatteryManager.EXTRA_HEALTH, -1) ?: -1
        val healthString = when (health) {
            BatteryManager.BATTERY_HEALTH_GOOD -> "Good"
            BatteryManager.BATTERY_HEALTH_OVERHEAT -> "Overheat"
            BatteryManager.BATTERY_HEALTH_DEAD -> "Dead"
            BatteryManager.BATTERY_HEALTH_OVER_VOLTAGE -> "Over Voltage"
            BatteryManager.BATTERY_HEALTH_UNSPECIFIED_FAILURE -> "Unspecified Failure"
            else -> "Unknown"
        }

        val status = batteryStatus?.getIntExtra(BatteryManager.EXTRA_STATUS, -1) ?: -1
        val statusString = when (status) {
            BatteryManager.BATTERY_STATUS_CHARGING -> "Charging"
            BatteryManager.BATTERY_STATUS_DISCHARGING -> "Discharging"
            BatteryManager.BATTERY_STATUS_FULL -> "Full"
            BatteryManager.BATTERY_STATUS_NOT_CHARGING -> "Not Charging"
            else -> "Unknown"
        }

        val level = batteryStatus?.getIntExtra(BatteryManager.EXTRA_LEVEL, -1) ?: -1
        val scale = batteryStatus?.getIntExtra(BatteryManager.EXTRA_SCALE, -1) ?: -1
        val batteryPct = if (level != -1 && scale != -1) (level * 100 / scale.toFloat()) else -1f

        return mapOf(
            "level" to batteryPct, // 현재 배터리 잔량 (%)
            "health" to healthString, // 건강 상태
            "status" to statusString, // 충전 상태
            "temperature" to (batteryStatus?.getIntExtra(BatteryManager.EXTRA_TEMPERATURE, -1)?.div(10.0) ?: -1.0), // 온도 (섭씨)
            "voltage" to (batteryStatus?.getIntExtra(BatteryManager.EXTRA_VOLTAGE, -1)?.div(1000.0) ?: -1.0) // 전압 (V)
        )
    }
}
