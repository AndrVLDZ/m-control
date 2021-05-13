package com.example.mcontrol

import android.content.Context
import android.net.wifi.WifiManager
import android.os.Bundle
import android.os.StrictMode
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.View.GONE
import android.view.View.VISIBLE
import android.widget.Button
import android.widget.EditText
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import com.example.mcontrol.databinding.ActivityMainBinding
import io.ktor.network.selector.*
import io.ktor.network.sockets.*
import io.ktor.util.cio.*
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.runBlocking
import java.net.InetSocketAddress
import java.net.Socket
import java.util.*

// эту функцию -- в карутину
fun sendToSocket(msg: String, client: Socket) {
    if (msg == "[close]")
        client.close()
    else
        client.outputStream.write(msg.toByteArray())
}

//fun TLS_connect(host: String, port: Int ){
//    runBlocking{
//        val socket = aSocket(ActorSelectorManager(Dispatchers.IO)).tcp().connect(InetSocketAddress(host, port))
////            val input = socket.openReadChannel()
//        val output = socket.openWriteChannel(autoFlush = false)
//        output.write("Hi".toByteArray().toString())
//        output.write("Hello")
////            val response = input.readUTF8Line()
////            println("Server said: '$response'")
//    }
//
//}

fun ipToString(i: Int): String {
    return (i and 0xFF).toString() + "." +
            (i shr 8 and 0xFF) + "." +
            (i shr 16 and 0xFF) + "." +
            (i shr 24 and 0xFF)
}

class MainActivity : AppCompatActivity() {
    lateinit var bindingClass: ActivityMainBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        Log.d("MyLogMAct", "onCreate")
        super.onCreate(savedInstanceState)
        val bindingClass: ActivityMainBinding = ActivityMainBinding.inflate(layoutInflater)
        val policy = StrictMode.ThreadPolicy.Builder().permitAll().build()
        StrictMode.setThreadPolicy(policy)
        setContentView(bindingClass.root)
        val wifiManager = applicationContext.getSystemService(Context.WIFI_SERVICE) as WifiManager
        val ipAddress: String = ipToString(wifiManager.connectionInfo.ipAddress)
        bindingClass.tvDevIP.text = "Your Device IP Address: $ipAddress"

        // получили данные
        val host = bindingClass.etIP.text.toString()
        val port = bindingClass.etPort.text.toString().toInt()

        // можно обойтись без флага - придумать другой механизм,
        // но нам за это не платят...
        var isConnected = false
        // да, client -- у нас shared resource... ну мир не идеален тоже!
        lateinit var client: Socket

        bindingClass.bConnect.setOnClickListener {
            // если уже подключены - выключаемся по нажатию
            if (isConnected) {
                CoroutineScope(Dispatchers.Main).launch {
                    client.close()
                    isConnected = false
                }

                bindingClass.tvConn.text = "No connection"
                bindingClass.bConnect.text = "Connect"
                bindingClass.textView.visibility = VISIBLE
                bindingClass.textView2.visibility = VISIBLE
                bindingClass.textView3.visibility = GONE
                bindingClass.etIP.visibility = VISIBLE
                bindingClass.etPort.visibility = VISIBLE
            } else {
                CoroutineScope(Dispatchers.Main).launch {
                    // подключение происходит тут!
                    /* TODO:
                        должен быть try - catch блок
                        и ещё предварительную валидацию
                        host, port строк неплохо бы...
                    */
                    client = Socket(host, port)
                    sendToSocket("Hi from client!", client)
                    isConnected = true
                }

                bindingClass.tvConn.text = "Connected"
                bindingClass.textView.visibility = GONE
                bindingClass.textView2.visibility = GONE
                bindingClass.textView3.visibility = VISIBLE
                bindingClass.textView3.text = "to: $host"
                bindingClass.bConnect.text = "Disconnect"
                bindingClass.etIP.visibility = GONE
                bindingClass.etPort.visibility = GONE
            }
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
        super.onDestroy()
        Log.d("MyLogMAct", "onDestroy")
    }

    override fun onRestart() {
        super.onRestart()
        Log.d("MyLogMAct", "onRestart")
    }
}


