package com.example.mcontrol

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import com.example.mcontrol.databinding.ActivityConnectionsManagerBinding
class ConnectionsManagerActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        Log.d("AfterConnectionAct", "onCreate")
        super.onCreate(savedInstanceState)

        setContentView(R.layout.activity_connections_manager)

        val bindingClass = ActivityConnectionsManagerBinding.inflate(layoutInflater)
        setContentView(bindingClass.root)

        bindingClass.apply {
            tvConnectedServer.text = "Connected to ${SharedData.connector.host}: ${SharedData.connector.port}"
            tvDeviceIP.text = "Your device IP address: ${SharedData.deviceIP}"
        }


        // <!> pseudo code
        // if (button("Disconnect").WasPressed) { doDisconnectFromCurrentConnection() }
        // if (button("Add Connection").WasPressed) { addAnotherConn() }
        // if (button("Remote Controller").WasPressed) { openRemoteController }

        bindingClass.bDisconnect.setOnClickListener {
            SharedData.connector.disconnect()
//            val intent = Intent(this, MainActivity::class.java)
            finish()
        }

        // bindingClass.bAddConn.setOnClickListener {
        //     val intent = Intent(this, MainActivity::class.java)
        //     startActivity(intent)
        // }

        bindingClass.bRC.setOnClickListener {
            val intent = Intent(this, CommandControlActivity::class.java)
            startActivity(intent)
        }
    }
}