package com.abhynex.terminal.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import com.abhynex.terminal.core.ChatMessage

@Composable
fun ChatScreen(messages: List<ChatMessage>, isLoading: Boolean, onSendMessage: (String) -> Unit) {
    var text by remember { mutableStateOf("") }

    Column(modifier = Modifier.fillMaxSize().background(Color(0xFF0A0A0A))) {
        LazyColumn(modifier = Modifier.weight(1f).padding(8.dp)) {
            items(messages) { msg ->
                val isUser = msg.role == "user"
                Box(modifier = Modifier.fillMaxWidth(), contentAlignment = if (isUser) Alignment.CenterEnd else Alignment.CenterStart) {
                    Card(
                        colors = CardDefaults.cardColors(containerColor = if (isUser) Color(0xFF007ACC) else Color(0xFF1E1E1E)),
                        shape = RoundedCornerShape(12.dp),
                        modifier = Modifier.padding(vertical = 4.dp).widthIn(max = 300.dp)
                    ) {
                        Text(text = msg.content, color = Color.White, modifier = Modifier.padding(12.dp))
                    }
                }
            }
            if (isLoading) {
                item { CircularProgressIndicator(modifier = Modifier.size(24.dp).padding(8.dp), color = Color.Cyan) }
            }
        }

        Row(modifier = Modifier.padding(8.dp).fillMaxWidth(), verticalAlignment = Alignment.CenterVertically) {
            TextField(
                value = text,
                onValueChange = { text = it },
                modifier = Modifier.weight(1f),
                placeholder = { Text("Ask ABHYNEX AI...") },
                colors = TextFieldDefaults.colors(focusedContainerColor = Color(0xFF1A1A1A), unfocusedContainerColor = Color(0xFF1A1A1A))
            )
            Button(onClick = { onSendMessage(text); text = "" }, modifier = Modifier.padding(start = 8.dp)) {
                Text("Send")
            }
        }
    }
}