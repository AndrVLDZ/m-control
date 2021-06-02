package com.example.mcontrol

import android.os.Bundle
import android.os.StrictMode
import android.util.Log
import android.view.View
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import com.example.mcontrol.SharedData.connector
import com.example.mcontrol.databinding.ActivityMsgToServerBinding
import io.ktor.util.*
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch

class CommandControlActivity : AppCompatActivity() {

    @KtorExperimentalAPI
    override fun onCreate(savedInstanceState: Bundle?) {
        Log.d("MyLogMAct", "onCreate")

        super.onCreate(savedInstanceState)

        val policy = StrictMode.ThreadPolicy.Builder().permitAll().build()
        StrictMode.setThreadPolicy(policy)

        val bindingClass: ActivityMsgToServerBinding = ActivityMsgToServerBinding.inflate(layoutInflater)
        setContentView(bindingClass.root)


        // On Click Listeners

        val sendMsgOnClick: (View) -> Unit = {
            val msg = bindingClass.etMsg.text.toString()
            CoroutineScope(Dispatchers.Main).launch {
                connector.send(msg)
            }
        }

        val sendCmdOnClick: (View) -> Unit = { view ->
            if (view is TextView) {
                val cmd = view.text.toString()
                CoroutineScope(Dispatchers.Main).launch {
                    connector.send(cmd)
                }
            }
        }


        bindingClass.bSend.setOnClickListener(sendMsgOnClick)

        bindingClass.button1.setOnClickListener(sendCmdOnClick)
        bindingClass.button2.setOnClickListener(sendCmdOnClick)
        bindingClass.button3.setOnClickListener(sendCmdOnClick)
        bindingClass.button4.setOnClickListener(sendCmdOnClick)
        bindingClass.button5.setOnClickListener(sendCmdOnClick)
        bindingClass.button6.setOnClickListener(sendCmdOnClick)
        bindingClass.button7.setOnClickListener(sendCmdOnClick)
        bindingClass.button8.setOnClickListener(sendCmdOnClick)
        bindingClass.button9.setOnClickListener(sendCmdOnClick)
        bindingClass.button10.setOnClickListener(sendCmdOnClick)
        bindingClass.button11.setOnClickListener(sendCmdOnClick)
        bindingClass.button12.setOnClickListener(sendCmdOnClick)
    }
}
