package com.example.mcontrol

import android.content.Context
import android.net.wifi.WifiManager
import android.os.Bundle
import android.os.StrictMode
import android.util.Log
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
    var defaultIp: String = "192.168.0.106"
    var defaultPort: Int = 9999
}


@KtorExperimentalAPI
class MainActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        Log.d("MyLogMAct", "onCreate")

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
                if (etIP.text.isNullOrBlank()) etIP.error = "You need to specify host ip"
                if (etPort.text.isNullOrBlank()) etPort.error = "You need to specify port"
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
        bindingClass.tvDeviceIP.text = "Your Device IP Address: ${SharedData.deviceIP}"

        bindingClass.bConnect.setOnClickListener {
//            val intent = Intent(this, AfterConnectionActivity::class.java)
//            startActivity(intent)

            bindingClass.apply {
                // get data and validation status
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

                // case: connected now -> need to disconnect
                if (connector.isConnected) {
                    connector.disconnect()

//                    // UI changes here [!]
//                    bindingClass.imgConn.setImageResource(R.drawable.disconnected_p200)
//                    bindingClass.tvConn.text = "No connection"
//                    bindingClass.bConnect.text = "Connect"
//                    bindingClass.textView.text = "Enter the host IP address"
//                    bindingClass.textView.textSize = 14F
//                    bindingClass.textView2.visibility = VISIBLE
//                    bindingClass.etIP.visibility = VISIBLE
//                    bindingClass.etPort.visibility = VISIBLE
//                    bindingClass.bAddConn.visibility = GONE
//                    bindingClass.bRC.visibility = GONE
                }
                // case:
                // 1) connected before then disconnected    -> need to get valid ip, port
                // 2) never connected                       -> need to get valid ip, port
                else {
                    val (isValid, newIp, newPort) = getFieldsData(
                        defaultIp = SharedData.defaultIp,
                        defaultPort = SharedData.defaultPort
                    )

                    if (isValid) {
                        CoroutineScope(Dispatchers.Main).launch {
                            connector.reset(newIp, newPort)
                            connector.connect()
                        }


//                        // UI changes here [!]
//                        imgConn.setImageResource(R.drawable.connected_p200)
//                        tvConn.text = "Connected"
//                        textView.textSize = 18F
//                        textView.text = "to: ${connector.host}"
//                        textView2.visibility = GONE
//                        bConnect.text = "Disconnect"
//                        etIP.visibility = GONE
//                        etPort.visibility = GONE
//                        bAddConn.visibility = VISIBLE
//                        bRC.visibility = VISIBLE
                    }
                }
            }
        }

//        bindingClass.bRC.setOnClickListener {
//            val intent = Intent(this, CommandControlActivity::class.java)
//            startActivity(intent)
//        }
    }


    override fun onResume() {
        super.onResume()
        Log.d("MyLogMAct", "onResume")
    }

    override fun onStart() {
        super.onStart()
        Log.d("MyLogMAct", "onStart")
    }

    override fun onPause() {
        super.onPause()
        Log.d("MyLogMAct", "onPause")
    }

    override fun onStop() {
        super.onStop()
        Log.d("MyLogMAct", "onStop")
    }

    override fun onDestroy() {
        connector.disconnect()
        Log.d("MyLogMAct", "onDestroy")
        super.onDestroy()
    }

    override fun onRestart() {
        super.onRestart()
        Log.d("MyLogMAct", "onRestart")
    }
}
