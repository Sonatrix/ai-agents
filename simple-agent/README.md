# Simple AI Agent

A lightweight and extensible AI agent framework built with Python that enables autonomous task execution and decision making.

## Features

- 🤖 Modular agent architecture
- 🧠 Memory and state management
- 🗣️ Command-line interface for interactive chat
- 🔌 Connects to OpenAI-compatible APIs (e.g., Ollama)

## Project Overview

This project provides a basic framework for a chat-based AI agent. It consists of:

*   **`main.py`**: The entry point of the application. It sets up the agent and handles the user interaction loop in the command line. It loads necessary configurations, such as API endpoints, from environment variables.
*   **`src/agent.py`**: Defines the `Agent` class, which is responsible for:
    *   Initializing with a system message.
    *   Managing the conversation history (user and assistant messages).
    *   Connecting to an OpenAI-compatible API (like a local Ollama instance) using the `openai` library.
    *   Sending user messages to the AI model and retrieving responses.

The agent maintains a list of messages to provide context for the conversation. It's designed to be simple and extensible.

## Installation
uv sync