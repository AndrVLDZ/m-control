package com.example.mcontrol

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.Toast
import com.example.mcontrol.databinding.ActivityAfterConnectionBinding

class AfterConnectionActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
//        Log.d("AfterConnectionAct", "onCreate")
        super.onCreate(savedInstanceState)

        setContentView(R.layout.activity_after_connection)

        val bindingClass = ActivityAfterConnectionBinding.inflate(layoutInflater)
        setContentView(bindingClass.root)

        bindingClass.apply {
            tvConnectedServer.text = "${getString(R.string.Host_IP)}: ${SharedData.connector.host} ${getString(R.string.Port)}: ${SharedData.connector.port}"
            tvDeviceIP.text = "${getString(R.string.Your_device_IP_address)}: ${SharedData.deviceIP}"
        }

        // <!> pseudo code
        // if (button("Disconnect").WasPressed) { doDisconnectFromCurrentConnection() }
        // if (button("Add Connection").WasPressed) { addAnotherConn() }
        // if (button("Remote Controller").WasPressed) { openRemoteController }

        bindingClass.bDisconnect.setOnClickListener {
            try {
                SharedData.connector.disconnect()
                Toast.makeText(this@AfterConnectionActivity, "${getString(R.string.Disconnected)}: ${SharedData.connector.host}", Toast.LENGTH_SHORT).show()
                finish()
            }  catch (e: Exception) {
                Toast.makeText(this@AfterConnectionActivity, "${getString(R.string.Disconnect_failed)}!", Toast.LENGTH_SHORT).show()
            }
        }

        bindingClass.bRC.setOnClickListener {
            val intent = Intent(this, CommandControlActivity::class.java)
            startActivity(intent)
        }

        bindingClass.bAbout.setOnClickListener {
            val intent = Intent(this, AboutAppActivity::class.java)
            startActivity(intent)
        }
    }

    override fun onBackPressed() {
        Toast.makeText(this@AfterConnectionActivity, "${getString(R.string.There_is_no_back_action)}!", Toast.LENGTH_LONG).show()
        return
    }

    override fun onDestroy() {
        SharedData.connector.disconnect()
        super.onDestroy()
    }
}