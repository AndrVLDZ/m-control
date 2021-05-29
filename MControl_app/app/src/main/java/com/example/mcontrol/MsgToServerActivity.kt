package com.example.mcontrol

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.os.StrictMode
import android.util.Log
import com.example.mcontrol.databinding.ActivityMainBinding
import com.example.mcontrol.databinding.ActivityMsgToServerBinding

class MsgToServerActivity : AppCompatActivity() {
    lateinit var bindingClass: ActivityMsgToServerBinding
    override fun onCreate(savedInstanceState: Bundle?) {
        Log.d("MyLogMAct", "onCreate")
        super.onCreate(savedInstanceState)
        val bindingClass: ActivityMsgToServerBinding = ActivityMsgToServerBinding.inflate(layoutInflater)
        val policy = StrictMode.ThreadPolicy.Builder().permitAll().build()
        StrictMode.setThreadPolicy(policy)
        setContentView(bindingClass.root)

        bindingClass.button1.setOnClickListener {
            val i = Intent()
            i.putExtra("cmd", bindingClass.button1.text.toString())
            setResult(RESULT_OK, i)
            finish()
        }

        bindingClass.bSend.setOnClickListener {
            val i = Intent()
            i.putExtra("cmd", bindingClass.etMsg.text.toString())
            setResult(RESULT_OK, i)
            finish()

        }

    }
}