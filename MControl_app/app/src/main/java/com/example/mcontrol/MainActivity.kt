package com.example.mcontrol

import android.content.Context
import android.content.Intent
import android.net.wifi.WifiManager
import android.os.Bundle
import android.os.StrictMode
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.example.mcontrol.SharedData.connector
import com.example.mcontrol.databinding.ActivityMainBinding
import io.ktor.util.*
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch


object SharedData {
    lateinit var deviceIP: String

    @KtorExperimentalAPI
    lateinit var connector: Connector

    // default credentials values
    var defaultIp: String = "192.168.0.0"
    var defaultPort: Int = 9999
}


@KtorExperimentalAPI
class MainActivity : AppCompatActivity() {
    
    override fun onCreate(savedInstanceState: Bundle?) {
//        Log.d("MyLogMainAct", "onCreate")
        super.onCreate(savedInstanceState)

        val policy = StrictMode.ThreadPolicy.Builder().permitAll().build()
        StrictMode.setThreadPolicy(policy)

        val bindingClass = ActivityMainBinding.inflate(layoutInflater)
        setContentView(bindingClass.root)


        fun getIpAddress(): String {
            val wifiManager =
                applicationContext.getSystemService(Context.WIFI_SERVICE) as WifiManager
            val ip = wifiManager.connectionInfo.ipAddress
            return "${ip and 0xFF}.${ip shr 8 and 0xFF}.${ip shr 16 and 0xFF}.${ip shr 24 and 0xFF}"
        }

        fun isFieldsEmpty(): Boolean {
            bindingClass.apply {
                if (etIP.text.isNullOrBlank()) etIP.error = getString(R.string.You_need_to_specify_host_ip)
                if (etPort.text.isNullOrBlank()) etPort.error = getString(R.string.You_need_to_specify_port)
                return etIP.text.isNullOrBlank() || etPort.text.isNullOrBlank()
            }
        }

        fun getFieldsData(defaultIp: String, defaultPort: Int): Triple<Boolean, String, Int> {
            bindingClass.apply {
                val hostIp = if (etIP.text.isNullOrBlank()) defaultIp else etIP.text.toString()
                val portNumber =
                    if (etPort.text.isNullOrBlank()) defaultPort else etPort.text.toString().toInt()
                val isValid = !isFieldsEmpty()
                return Triple(isValid, hostIp, portNumber)
            }
        }

        SharedData.deviceIP = getIpAddress()
        bindingClass.tvDeviceIP.text = "${getString(R.string.Your_device_IP_address)}: ${SharedData.deviceIP}"

        bindingClass.bConnect.setOnClickListener {
            // get validated data from fields
            val (isValid, hostIp, portNumber) = getFieldsData(
                    defaultIp = SharedData.defaultIp,
                    defaultPort = SharedData.defaultPort
            )

            // exit if user is an asshole
            if (!isValid) return@setOnClickListener

            // set connector instance
            connector = Connector(
                    host = hostIp,
                    port = portNumber,
            )

            CoroutineScope(Dispatchers.Main).launch {
                try {
                    connector.connect()
                    Toast.makeText(this@MainActivity, "${getString(R.string.Connected_to)}: ${SharedData.connector.host}", Toast.LENGTH_SHORT).show()
                    val intent = Intent(this@MainActivity, AfterConnectionActivity::class.java)
                    startActivity(intent)
                }  catch (e: Exception) {
                    Toast.makeText(this@MainActivity, "${getString(R.string.Could_not_connect)}!", Toast.LENGTH_SHORT).show()
                }

            }

        }
    }

    override fun onDestroy() {
        connector.disconnect()
        super.onDestroy()
    }
}



//        Log.d("MyLogMAct", "onDestroy")


// override fun onResume() {
//     super.onResume()
//     Log.d("MyLogMAct", "onResume")
// }
//
// override fun onStart() {
//     super.onStart()
//     Log.d("MyLogMAct", "onStart")
// }
//
// override fun onPause() {
//     super.onPause()
//     Log.d("MyLogMAct", "onPause")
// }
//
// override fun onStop() {
//     super.onStop()
//     Log.d("MyLogMAct", "onStop")
// }



// override fun onRestart() {
//     super.onRestart()
//     Log.d("MyLogMAct", "onRestart")
// }