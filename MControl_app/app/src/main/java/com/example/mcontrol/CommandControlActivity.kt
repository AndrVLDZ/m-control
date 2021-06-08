package com.example.mcontrol

import android.os.Bundle
import android.os.StrictMode
import android.view.View
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.example.mcontrol.SharedData.connector
import com.example.mcontrol.databinding.ActivityCommandControlBinding
import io.ktor.util.*
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch

class CommandControlActivity : AppCompatActivity() {

    @KtorExperimentalAPI
    override fun onCreate(savedInstanceState: Bundle?) {

        super.onCreate(savedInstanceState)

        val policy = StrictMode.ThreadPolicy.Builder().permitAll().build()
        StrictMode.setThreadPolicy(policy)

        val bindingClass: ActivityCommandControlBinding = ActivityCommandControlBinding.inflate(layoutInflater)
        setContentView(bindingClass.root)


        // On Click Listeners
        val sendMsgOnClick: (View) -> Unit = {
            val msg = bindingClass.etMsg.text.toString()
            CoroutineScope(Dispatchers.Main).launch {

                try {
                    connector.send(msg)
                    Toast.makeText(this@CommandControlActivity, R.string.Message_sent, Toast.LENGTH_SHORT).show()
                }  catch (e: Exception) {
                    Toast.makeText(this@CommandControlActivity, R.string.Failed_to_send, Toast.LENGTH_SHORT).show()
                }
            }
        }

        val sendCmdOnClick: (View) -> Unit = { view ->
            if (view is TextView) {
                val cmd = view.text.toString()
                CoroutineScope(Dispatchers.Main).launch {

                    try {
                        connector.send(cmd)
                        Toast.makeText(this@CommandControlActivity, R.string.Command_sent, Toast.LENGTH_SHORT).show()
                    }  catch (e: Exception) {
                        Toast.makeText(this@CommandControlActivity, R.string.Failed_to_send, Toast.LENGTH_SHORT).show()
                    }
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
