package com.example.mcontrol

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import android.widget.Toast
import com.example.mcontrol.databinding.ActivityAfterConnectionBinding

class AfterConnectionActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        Log.d("AfterConnectionAct", "onCreate")
        super.onCreate(savedInstanceState)

        setContentView(R.layout.activity_after_connection)

        val bindingClass = ActivityAfterConnectionBinding.inflate(layoutInflater)
        setContentView(bindingClass.root)

        bindingClass.apply {
            tvConnectedServer.text = "to: ${SharedData.connector.host} Port: ${SharedData.connector.port}"
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

        bindingClass.bAbout.setOnClickListener {
            val intent = Intent(this, SettingsActivity::class.java)
            startActivity(intent)
        }
    }

    override fun onBackPressed() {
        // super.onBackPressed();
        Toast.makeText(this@AfterConnectionActivity, "There is no back action!", Toast.LENGTH_LONG).show()
        return
    }
}