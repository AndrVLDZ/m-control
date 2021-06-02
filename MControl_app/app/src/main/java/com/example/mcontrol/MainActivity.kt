package com.example.mcontrol

import android.content.Context
import android.content.Intent
import android.net.wifi.WifiManager
import android.os.Bundle
import android.os.StrictMode
import android.util.Log
import android.view.View.GONE
import android.view.View.VISIBLE
import androidx.appcompat.app.AppCompatActivity
import com.example.mcontrol.SharedData.connector
import com.example.mcontrol.databinding.ActivityMainBinding
import io.ktor.util.*
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch


object SharedData {
    @KtorExperimentalAPI
    lateinit var connector: Connector
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
            val wifiManager = applicationContext.getSystemService(Context.WIFI_SERVICE) as WifiManager
            val ip = wifiManager.connectionInfo.ipAddress
            return "${ip and 0xFF}.${ip shr 8 and 0xFF}.${ip shr 16 and 0xFF}.${ip shr 24 and 0xFF}"
        }

        val ipAddress: String = getIpAddress()

        bindingClass.tvDevIP.text = "Your Device IP Address: $ipAddress"


        connector = Connector(
                host = bindingClass.etIP.text.toString(),
                port = bindingClass.etPort.text.toString().toInt(),
        )

        bindingClass.bConnect.setOnClickListener {
            if (connector.isConnected) {
                connector.disconnect()

                bindingClass.imgConn.setImageResource(R.drawable.disconnected_p200)
                bindingClass.tvConn.text = "No connection"
                bindingClass.bConnect.text = "Connect"
                bindingClass.textView.text = "Enter the host IP address"
                bindingClass.textView.textSize = 14F
                bindingClass.textView2.visibility = VISIBLE
                bindingClass.etIP.visibility = VISIBLE
                bindingClass.etPort.visibility = VISIBLE
                bindingClass.bAddConn.visibility = GONE
                bindingClass.bRC.visibility = GONE
            } else {
                CoroutineScope(Dispatchers.Main).launch {
                    /* TODO:
                        должен быть try - catch блок
                        и ещё предварительную валидацию
                        host, port строк неплохо бы...
                    */
                    connector.connect()
                }

                bindingClass.imgConn.setImageResource(R.drawable.connected_p200)
                bindingClass.tvConn.text = "Connected"
                bindingClass.textView.textSize = 18F
                bindingClass.textView.text = "to: ${connector.host}"
                bindingClass.textView2.visibility = GONE
                bindingClass.bConnect.text = "Disconnect"
                bindingClass.etIP.visibility = GONE
                bindingClass.etPort.visibility = GONE
                bindingClass.bAddConn.visibility = VISIBLE
                bindingClass.bRC.visibility = VISIBLE
            }
        }


        bindingClass.bRC.setOnClickListener {
            val intent = Intent(this, CommandControlActivity::class.java)
            startActivity(intent)
        }
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
