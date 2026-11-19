package com.abhynex.terminal.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

data class AgentStep(val id: String, val title: String, val status: String, val detail: String = "")

@Composable
fun AgentActivityPanel(steps: List<AgentStep>) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(Color(0xFF0A0A0A))
            .padding(16.dp)
    ) {
        Text(
            text = "AGENT ACTIVITY",
            style = MaterialTheme.typography.headlineSmall,
            color = Color.Cyan,
            modifier = Modifier.padding(bottom = 16.dp)
        )
        
        LazyColumn(verticalArrangement = Arrangement.spacedBy(8.dp)) {
            items(steps) { step ->
                AgentStepItem(step)
            }
        }
    }
}

@Composable
fun AgentStepItem(step: AgentStep) {
    Card(
        colors = CardDefaults.cardColors(containerColor = Color(0xFF1A1A1A)),
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(modifier = Modifier.padding(12.dp)) {
            Row(horizontalArrangement = Arrangement.SpaceBetween, modifier = Modifier.fillMaxWidth()) {
                Text(text = step.title, color = Color.White, fontSize = 14.sp)
                Text(
                    text = step.status.uppercase(),
                    color = when(step.status.lowercase()) {
                        "completed" -> Color.Green
                        "running" -> Color.Yellow
                        "failed" -> Color.Red
                        else -> Color.Gray
                    },
                    fontSize = 12.sp
                )
            }
            if (step.detail.isNotEmpty()) {
                Text(
                    text = step.detail,
                    color = Color.LightGray,
                    fontSize = 12.sp,
                    modifier = Modifier.padding(top = 4.dp)
                )
            }
        }
    }
}