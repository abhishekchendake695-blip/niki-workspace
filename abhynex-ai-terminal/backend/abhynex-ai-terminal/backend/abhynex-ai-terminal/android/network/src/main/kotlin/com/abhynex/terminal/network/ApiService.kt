package com.abhynex.terminal.network

import retrofit2.http.Body
import retrofit2.http.POST
import retrofit2.http.GET
import retrofit2.http.Query

interface ApiService {
    @POST("chat")
    suspend fun chat(@Body request: ChatRequest): ChatResponse

    @POST("execute")
    suspend fun executeCommand(@Body request: CommandRequest): CommandResponse

    @GET("files")
    suspend fun listFiles(@Query("path") path: String): List<String>
}

data class ChatRequest(
    val message: String,
    val history: List<Map<String, String>> = emptyList(),
    val provider: String = "gemini",
    val api_key: String
)

data class ChatResponse(val response: String)

data class CommandRequest(val command: String, val cwd: String? = null)

data class CommandResponse(val stdout: String, val stderr: String, val returncode: Int)