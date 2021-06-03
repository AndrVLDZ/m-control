package com.example.mcontrol

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import com.example.mcontrol.databinding.ActivityAfterConnectionBinding
import com.example.mcontrol.databinding.ActivityMainBinding

class AfterConnectionActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_after_connection)
        val bindingClass = ActivityAfterConnectionBinding.inflate(layoutInflater)
        setContentView(bindingClass.root)


        bindingClass.bRC.setOnClickListener {
            val intent = Intent(this, CommandControlActivity::class.java)
            startActivity(intent)


            //                        // UI changes here [!]
//                        imgConn.setImageResource(R.drawable.connected_p200)
//                        tvConn.text = "Connected"
//                        textView.textSize = 18F
//                        textView.text = "to: ${connector.host}"
//                        textView2.visibility = GONE
//                        bConnect.text = "Disconnect"
//                        etIP.visibility = GONE
//                        etPort.visibility = GONE
//                        bAddConn.visibility = VISIBLE
//                        bRC.visibility = VISIBLE




        }
    }
}