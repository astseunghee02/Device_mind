package com.example.devicemind

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

class MainActivity: FlutterActivity() {
    private val CHANNEL = "com.example.devicemind/devicedata"

    override fun configureFlutterEngine(flutterEngine: FlutterEngine) {
        super.configureFlutterEngine(flutterEngine)
        MethodChannel(flutterEngine.dartExecutor.binaryMessenger, CHANNEL).setMethodCallHandler {
            call, result ->
            if (call.method == "getDeviceData") {
                if (!hasUsageStatsPermission()) {
                    startActivity(Intent(Settings.ACTION_USAGE_ACCESS_SETTINGS))
                    result.error("PERMISSION_DENIED", "Usage stats permission is not enabled.", null)
                } else {
                    val data = getDeviceData()
                    result.success(data)
                }
            } else {
                result.notImplemented()
            }
        }
    }

    private fun hasUsageStatsPermission(): Boolean {
        val appOps = getSystemService(Context.APP_OPS_SERVICE) as AppOpsManager
        val mode = appOps.checkOpNoThrow(AppOpsManager.OPSTR_GET_USAGE_STATS, Process.myUid(), packageName)
        return mode == AppOpsManager.MODE_ALLOWED
    }

    private fun getDeviceData(): Map<String, Any> {
        val batteryManager = getSystemService(Context.BATTERY_SERVICE) as BatteryManager
        val batteryLevel = batteryManager.getIntProperty(BatteryManager.BATTERY_PROPERTY_CAPACITY)

        val usageStatsManager = getSystemService(Context.USAGE_STATS_SERVICE) as UsageStatsManager
        val time = System.currentTimeMillis()
        val stats = usageStatsManager.queryUsageStats(UsageStatsManager.INTERVAL_DAILY, time - TimeUnit.DAYS.toMillis(1), time)

        val appUsage = stats.map {
            mapOf(
                "packageName" to it.packageName,
                "totalTimeInForeground" to it.totalTimeInForeground
            )
        }

        return mapOf(
            "batteryLevel" to batteryLevel,
            "appUsage" to appUsage
        )
    }
}
