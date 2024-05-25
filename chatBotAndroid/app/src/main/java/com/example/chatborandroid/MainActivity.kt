package com.example.chatborandroid

import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import com.example.chatborandroid.databinding.ActivityMainBinding
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import org.json.JSONObject
import java.io.OutputStreamWriter
import java.net.HttpURLConnection
import java.net.URL

class MainActivity : AppCompatActivity() {

    private lateinit var sendButton: Button
    private lateinit var messageEditText: EditText
    private lateinit var responseTextView: TextView
    private lateinit var binding: ActivityMainBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        sendButton = binding.sendButton
        messageEditText = binding.messageEditText
        responseTextView = binding.responseTextView

        sendButton.setOnClickListener {
            val message = messageEditText.text.toString()
            sendMessage(message)
        }
    }

    private fun sendMessage(message: String) {
        CoroutineScope(Dispatchers.IO).launch {
            val url = URL("http://192.168.0.103:5000/messages")
            val connection = url.openConnection() as HttpURLConnection
            connection.requestMethod = "POST"
            connection.setRequestProperty("Content-Type", "application/json")

            val requestBody = JSONObject().apply {
                put("message", message)
            }

            val outputStream = OutputStreamWriter(connection.outputStream)
            outputStream.write(requestBody.toString())
            outputStream.flush()

            val responseCode = connection.responseCode
            if (responseCode == HttpURLConnection.HTTP_OK) {
                val response = connection.inputStream.bufferedReader().readText()
                val jsonResponse = JSONObject(response)
                val answer = jsonResponse.getString("response")

                // Обновляем интерфейс в основном потоке
                withContext(Dispatchers.Main) {
                    responseTextView.text = answer
                }
            } else {
                // Обработка ошибок
                withContext(Dispatchers.Main) {
                    responseTextView.text = connection.responseMessage
                }
            }
            connection.disconnect()
        }
    }
}