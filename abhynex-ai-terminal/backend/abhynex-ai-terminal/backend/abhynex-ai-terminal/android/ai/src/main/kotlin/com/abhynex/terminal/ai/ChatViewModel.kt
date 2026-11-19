package com.abhynex.terminal.ai

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.abhynex.terminal.core.ChatMessage
import com.abhynex.terminal.network.ApiService
import com.abhynex.terminal.network.ChatRequest
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

class ChatViewModel(private val apiService: ApiService) : ViewModel() {
    private val _messages = MutableStateFlow<List<ChatMessage>>(emptyList())
    val messages: StateFlow<List<ChatMessage>> = _messages

    private val _isLoading = MutableStateFlow(false)
    val isLoading: StateFlow<Boolean> = _isLoading

    fun sendMessage(text: String, provider: String, apiKey: String) {
        if (text.isBlank()) return

        val userMsg = ChatMessage(role = "user", content = text)
        _messages.value = _messages.value + userMsg

        viewModelScope.launch {
            _isLoading.value = true
            try {
                val history = _messages.value.dropLast(1).map { mapOf("role" to it.role, "content" to it.content) }
                val response = apiService.chat(ChatRequest(text, history, provider, apiKey))
                val aiMsg = ChatMessage(role = "assistant", content = response.response)
                _messages.value = _messages.value + aiMsg
            } catch (e: Exception) {
                _messages.value = _messages.value + ChatMessage(role = "assistant", content = "Error: ${e.message}")
            } finally {
                _isLoading.value = false
            }
        }
    }
}