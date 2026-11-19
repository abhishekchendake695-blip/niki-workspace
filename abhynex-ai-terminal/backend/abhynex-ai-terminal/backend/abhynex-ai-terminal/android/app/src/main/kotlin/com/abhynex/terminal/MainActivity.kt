package com.abhynex.terminal

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.abhynex.terminal.ui.components.TerminalScreen
import com.abhynex.terminal.ui.components.ChatScreen
import com.abhynex.terminal.terminal.TerminalViewModel
import com.abhynex.terminal.ai.ChatViewModel
import com.abhynex.terminal.network.NetworkModule

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState) 
        val apiService = NetworkModule.provideApiService("http://10.0.2.2:8000")
        val terminalViewModel = TerminalViewModel(apiService)
        val chatViewModel = ChatViewModel(apiService)

        setContent {
            val navController = rememberNavController()
            Scaffold(
                bottomBar = {
                    NavigationBar {
                        NavigationBarItem(selected = true, onClick = { navController.navigate("chat") }, icon = { Text("Chat") })
                        NavigationBarItem(selected = false, onClick = { navController.navigate("terminal") }, icon = { Text("Terminal") })
                    }
                }
            ) { innerPadding ->
                NavHost(navController, startDestination = "chat", modifier = Modifier.padding(innerPadding)) {
                    composable("chat") {
                        val messages by chatViewModel.messages.collectAsState()
                        val loading by chatViewModel.isLoading.collectAsState()
                        ChatScreen(messages, loading) { chatViewModel.sendMessage(it, "gemini", "YOUR_API_KEY") }
                    }
                    composable("terminal") {
                        val output by terminalViewModel.output.collectAsState()
                        TerminalScreen(output) { terminalViewModel.execute(it) }
                    }
                }
            }
        }
    }
}