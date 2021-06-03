package com.example.mcontrol

import io.ktor.network.selector.*
import io.ktor.network.sockets.*
import io.ktor.util.*
import io.ktor.util.cio.*
import io.ktor.utils.io.*
import kotlinx.coroutines.Dispatchers
import java.net.InetSocketAddress


@KtorExperimentalAPI
class Connector(host: String, port: Int) {
    var host: String
    var port: Int

    private lateinit var socket: Socket
    private lateinit var input: ByteReadChannel
    private lateinit var output: ByteWriteChannel

    val isConnected: Boolean get() = ::socket.isInitialized && !socket.isClosed

    init {
        // TODO : Validation

        this.host = host
        this.port = port
    }

    suspend fun reset(newHost: String, newPort: Int) {
        // TODO : Validation
        if (isConnected) {
            disconnect()
        }

        host = newHost
        port = newPort
    }

    suspend fun send(msg: String) {
        output.write("$msg\r\n")
    }

    suspend fun connect() {
        // TODO: Try/Catch ?
        socket = aSocket(ActorSelectorManager(Dispatchers.IO)).tcp().connect(InetSocketAddress(host, port))
        input = socket.openReadChannel()
        output = socket.openWriteChannel(autoFlush = true)
    }

    fun disconnect() {
        output.close()
        socket.close()
    }
}
