package com.example.mcontrol
import android.app.Instrumentation
import android.content.Context
import android.content.Intent
import android.net.wifi.WifiManager
import android.os.Bundle
import android.os.StrictMode
import android.util.Log
import android.view.View.GONE
import android.view.View.VISIBLE
import androidx.activity.result.ActivityResult
import androidx.activity.result.ActivityResultLauncher
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AppCompatActivity
import com.example.mcontrol.databinding.ActivityMainBinding
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import java.net.Socket





lateinit var client: Socket
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

    private var launcher: ActivityResultLauncher<Intent>? = null

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

        launcher = registerForActivityResult(ActivityResultContracts.StartActivityForResult()){
            result: ActivityResult ->
            if(result.resultCode == RESULT_OK){
                val cmd = result.data?.getStringExtra("cmd")
//                bindingClass.textView.text = cmd
                if (cmd != null) {
//                    Log.d("MyLogMAct", cmd)
                    CoroutineScope(Dispatchers.Main).launch {
                        sendToSocket(cmd, client)

                    }
                }

            }
        }

        bindingClass.bRC.setOnClickListener {
            launcher?.launch(Intent(this, MsgToServerActivity::class.java))

        }


        // можно обойтись без флага - придумать другой механизм,
        // но нам за это не платят...
        var isConnected = false


        // да, client -- у нас shared resource... ну мир не идеален тоже!
        bindingClass.bConnect.setOnClickListener {
            // если уже подключены - выключаемся по нажатию
            if (isConnected) {
                CoroutineScope(Dispatchers.Main).launch {
                    sendToSocket("CLOSING", client)
                    isConnected = false
                }

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

            }


//            val cmd = intent.getCharArrayExtra(Constance.button).toString()
//            if(cmd != null) {
//                CoroutineScope(Dispatchers.Main).launch {
//                    sendToSocket(cmd, client)
//
//                }
//            }

            else {
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

                bindingClass.imgConn.setImageResource(R.drawable.connected_p200)
                bindingClass.tvConn.text = "Connected"
                bindingClass.textView.textSize = 18F
                bindingClass.textView.text = "to: $host"
                bindingClass.textView2.visibility = GONE
                bindingClass.bConnect.text = "Disconnect"
                bindingClass.etIP.visibility = GONE
                bindingClass.etPort.visibility = GONE
                bindingClass.bAddConn.visibility = VISIBLE
                bindingClass.bRC.visibility = VISIBLE
            }
        }


//        launcher = registerForActivityResult(ActivityResultContracts.StartActivityForResult()){
//                result: ActivityResult ->
//            if(result.resultCode == RESULT_OK){
//                val cmd = result.data?.getStringArrayExtra(Constance.button).toString()
//                bindingClass.textView.text = cmd
//                Log.d("MyLogMAct", cmd)
//
//                CoroutineScope(Dispatchers.Main).launch {
//                    sendToSocket(cmd, client)
//
//                }
//            }
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
    CoroutineScope(Dispatchers.Main).launch {
        sendToSocket("CLOSING", client)
    }
    Log.d("MyLogMAct", "onDestroy")
        super.onDestroy()


    }

    override fun onRestart() {
        super.onRestart()
        Log.d("MyLogMAct", "onRestart")
    }

}



