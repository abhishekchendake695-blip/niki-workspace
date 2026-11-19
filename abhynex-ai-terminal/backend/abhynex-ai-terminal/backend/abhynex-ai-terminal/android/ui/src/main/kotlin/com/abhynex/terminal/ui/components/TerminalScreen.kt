package com.abhynex.terminal.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material3.Text
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.abhynex.terminal.terminal.TerminalViewModel

@Composable
fun TerminalScreen(viewModel: TerminalViewModel) {
    val output by viewModel.output.collectAsState()
    var command by remember { mutableStateOf("") }

    Column(modifier = Modifier.fillMaxSize().background(Color.Black).padding(8.dp)) {
        LazyColumn(modifier = Modifier.weight(1f)) {
            item { Text(output, color = Color.Green, fontFamily = FontFamily.Monospace, fontSize = 12.sp) }
        }
        Row(modifier = Modifier.fillMaxWidth()) {
            Text("$ ", color = Color.Cyan, fontFamily = FontFamily.Monospace)
            BasicTextField(
                value = command,
                onValueChange = { command = it },
                textStyle = TextStyle(color = Color.White, fontFamily = FontFamily.Monospace),
                modifier = Modifier.fillMaxWidth(),
                keyboardOptions = KeyboardOptions(imeAction = ImeAction.Done),
                onKeyboardActions = androidx.compose.foundation.text.KeyboardActions(
                    onDone = {
                        if (command.isNotBlank()) {
                            viewModel.executeCommand(command)
                            command = ""
                        }
                    }
                )
            )
        }
    }
}