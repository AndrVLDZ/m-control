package com.example.mcontrol

import android.os.Bundle
import android.os.StrictMode
import android.util.Log
import android.view.View
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.navigation.findNavController
import androidx.navigation.ui.AppBarConfiguration
import androidx.navigation.ui.setupActionBarWithNavController
import androidx.navigation.ui.setupWithNavController
import com.example.mcontrol.SharedData.connector
import com.example.mcontrol.databinding.ActivityCommandControlBinding
import com.google.android.material.bottomnavigation.BottomNavigationView
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

        val bindingClass: ActivityCommandControlBinding = ActivityCommandControlBinding.inflate(layoutInflater)
        setContentView(bindingClass.root)

        // val bottomNavigationView = findViewById<BottomNavigationView>(R.id.bottomNavigationView)
        // val navController = findNavController(R.id.controllerFragment)
        //
        // val appBarConfiguration = AppBarConfiguration(setOf(R.id.connectionsFragment, R.id.connectionsFragment, R.id.settingsFragment))
        // setupActionBarWithNavController(navController, appBarConfiguration)
        //
        // bottomNavigationView.setupWithNavController(navController)



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



//    override fun onBackPressed() {
//        // super.onBackPressed();
//        Toast.makeText(this@CommandControlActivity, "There is no back action!", Toast.LENGTH_LONG).show()
//        return
//    }
}
