package com.example.mcontrol

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.text.method.LinkMovementMethod
import android.widget.TextView

class AboutAppActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_about_app)

        var link = findViewById<TextView>(R.id.tvGitHubLink)
        link.movementMethod = LinkMovementMethod.getInstance()
    }
}