# ABHYNEX AI TERMINAL – NEXT GENERATION

## Overview
ABHYNEX AI TERMINAL is a production-ready Android AI application that combines a powerful AI reasoning engine with a real interactive terminal and autonomous agent capabilities.

## Features
- **Advanced AI Brain**: Integrated with Gemini and Groq APIs for multi-step reasoning.
- **Real Terminal**: Interactive shell execution with real-time output.
- **Autonomous Agent**: Plans, executes, and self-corrects tasks.
- **Coding Studio**: Create, edit, and debug code across multiple languages.
- **Premium UI**: AMOLED black theme with smooth Jetpack Compose animations.

## Project Structure
- `backend/`: Python FastAPI server for shell execution and AI orchestration.
- `android/`: Native Kotlin Android application with modular architecture.

## Setup Instructions

### Backend Setup
1. Navigate to the `backend` directory.
2. Install dependencies: `pip install -r requirements.txt`.
3. Set your API keys in environment variables or a `.env` file.
4. Run the server: `python main.py`.

### Android App Setup
1. Open the `android` folder in Android Studio.
2. Sync Gradle projects.
3. Update the `BASE_URL` in `NetworkModule.kt` to point to your backend IP.
4. Build and run the app on an Android device or emulator.

## Technology Stack
- **Android**: Kotlin, Jetpack Compose, Retrofit, WorkManager, SQLite.
- **Backend**: Python, FastAPI, Uvicorn.
- **AI**: Google Gemini API, Groq API.

## License
Proprietary - Created by ABHYNEX.