package com.abhynex.terminal.core

data class ChatMessage(
    val role: String,
    val content: String
)

data class CommandResult(
    val stdout: String,
    val stderr: String,
    val returncode: int
)

data class FileItem(
    val name: String,
    val is_dir: Boolean,
    val size: Long,
    val path: String
)