package com.abhynex.terminal.terminal

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.abhynex.terminal.network.ApiService
import com.abhynex.terminal.core.CommandRequest
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

class TerminalViewModel(private val apiService: ApiService) : ViewModel() {
    private val _output = MutableStateFlow("Welcome to ABHYNEX AI Terminal\n")
    val output: StateFlow<String> = _output

    fun executeCommand(command: String) {
        viewModelScope.launch {
            _output.value += "$ ${command}\n"
            try {
                val response = apiService.executeCommand(CommandRequest(command))
                _output.value += response.stdout
                if (response.stderr.isNotEmpty()) {
                    _output.value += "Error: ${response.stderr}\n"
                }
            } catch (e: Exception) {
                _output.value += "Failed to execute: ${e.message}\n"
            }
        }
    }
}