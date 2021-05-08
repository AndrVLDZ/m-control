package com.example.mcontrol

import android.content.Context
import android.net.wifi.WifiManager
import android.os.Bundle
import android.os.StrictMode
import android.util.Log
import android.view.View
import android.widget.EditText
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import io.ktor.network.selector.*
import io.ktor.network.sockets.*
import io.ktor.util.cio.*
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.runBlocking
import java.net.InetSocketAddress
import java.net.Socket




//This function connects to the server
fun conn() {

    val client =  Socket("192.168.0.106", 9999)
    client.outputStream.write("EBATTT ONO RABOTAET!!!!".toByteArray())
//    client.close()
}

fun TLS_connect(host: String, port: Int ){
    runBlocking{
        val socket = aSocket(ActorSelectorManager(Dispatchers.IO)).tcp().connect(InetSocketAddress(host, port))
//            val input = socket.openReadChannel()
        val output = socket.openWriteChannel(autoFlush = false)
        output.write("Hi")
//            val response = input.readUTF8Line()
//            println("Server said: '$response'")
    }

}




fun ipToString(i: Int): String {
    return (i and 0xFF).toString() + "." +
            (i shr 8 and 0xFF) + "." +
            (i shr 16 and 0xFF) + "." +
            (i shr 24 and 0xFF)
}


class MainActivity : AppCompatActivity() {
    lateinit var etIP: EditText
    lateinit var etPort: EditText

    override fun onCreate(savedInstanceState: Bundle?) {
        Log.d("MyLogMAct", "onCreate")
        super.onCreate(savedInstanceState)
        val policy = StrictMode.ThreadPolicy.Builder().permitAll().build()
        StrictMode.setThreadPolicy(policy)
        setContentView(R.layout.activity_main)
        etIP = findViewById(R.id.etIP)
        etPort = findViewById(R.id.etPort)
        val tvDevIP = findViewById<TextView>(R.id.tvDevIP)
        val wifiManager = applicationContext.getSystemService(Context.WIFI_SERVICE) as WifiManager
        val ipAddress: String = ipToString(wifiManager.connectionInfo.ipAddress)
        tvDevIP.text = "Your Device IP Address: $ipAddress"
    }

    fun onClickConnect(view: View){

        TLS_connect(host = etIP.text.toString(), port = etPort.text.toString().toInt())

//        CoroutineScope(Dispatchers.Main).launch{
////            conn()
//
//        }
        val tvConn = findViewById<TextView>(R.id.tvConn)
        tvConn.text = "Connected"
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
        super.onDestroy()
        Log.d("MyLogMAct", "onDestroy")
    }

    override fun onRestart() {
        super.onRestart()
        Log.d("MyLogMAct", "onRestart")
    }



}


