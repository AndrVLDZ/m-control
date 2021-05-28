package com.example.mcontrol

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.os.StrictMode
import android.util.Log
import com.example.mcontrol.databinding.ActivityMainBinding

class MsgToServerActivity : AppCompatActivity() {
    lateinit var bindingClass: ActivityMainBinding
    override fun onCreate(savedInstanceState: Bundle?) {
        Log.d("MyLogMAct", "onCreate")
        super.onCreate(savedInstanceState)
        val bindingClass: ActivityMainBinding = ActivityMainBinding.inflate(layoutInflater)
        val policy = StrictMode.ThreadPolicy.Builder().permitAll().build()
        StrictMode.setThreadPolicy(policy)
        setContentView(bindingClass.root)
    }
}