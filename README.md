# AI Voice Assistant - Sara

A modern, interactive AI voice assistant built with Python and PySide6, featuring speech recognition, text-to-speech synthesis, and AI-powered conversations.

## Features

- 🎤 **Voice Recognition**: Real-time speech-to-text using Google's Speech Recognition API
- 🤖 **AI Conversations**: Powered by OpenRouter's meta-llama/llama-4-maverick model
- 🔊 **Text-to-Speech**: High-quality voice synthesis using Windows SAPI
- 🎨 **Modern UI**: Beautiful PySide6-based interface with animated GIF
- 💬 **Dual Input**: Support for both voice and text input
- 📝 **Conversation History**: Maintains context across interactions
- 🎯 **Customizable Voice**: Configurable speech rate and volume

## Screenshots

The application features a clean, modern interface with:
- Animated GIF display
- Real-time chat display
- Text input field
- Clickable microphone button for voice input

## Installation

### Prerequisites

- Python 3.8 or higher
- Windows OS (for SAPI text-to-speech)
- Microphone for voice input
- OpenRouter API key

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ai-voice-assistant.git
   cd ai-voice-assistant
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   Create a `.env` file in the project root:
   ```
   OPENROUTE_API_KEY=your_openrouter_api_key_here
   ```

4. **Get your OpenRouter API key**
   - Visit [OpenRouter](https://openrouter.ai/)
   - Sign up for an account
   - Generate an API key
   - Add it to your `.env` file

## Usage

### Running the Application

```bash
python main.py
```

### How to Use

1. **Text Input**: Type your message in the text field and press Enter
2. **Voice Input**: Click the microphone icon and speak your message
3. **Conversation**: The assistant will respond using AI-generated text and voice synthesis

### Voice Commands

- Ask questions: "What is the weather today?"
- Get information: "Tell me about artificial intelligence"
- Have conversations: "Let's talk about movies"
- Ask about the assistant: "What is your name?" or "Who are you?"

## Configuration

### Voice Settings

The application automatically configures:
- **Voice**: Microsoft Zira (female voice)
- **Speech Rate**: 150 words per minute
- **Volume**: 90%

You can modify these settings in the `main.py` file:

```python
# Set speaking rate and volume
self.tts_engine.setProperty('rate', 150)    # Speed of speech
self.tts_engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)
```

### AI Model

The application uses OpenRouter's `meta-llama/llama-4-maverick` model. You can change this in the `process_with_ai` method:

```python
data = {
    "model": "meta-llama/llama-4-maverick",  # Change this to use different models
    "messages": self.conversation_history,
    "temperature": 0.7,
    "max_tokens": 1000,
    "stream": False
}
```

## Project Structure

```
ai-voice-assistant/
├── main.py                 # Main application file
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
├── .gitignore             # Git ignore rules
├── .env                   # Environment variables (not in repo)
├── sara_gif.gif          # Animated GIF for UI
├── 326557_mic_icon.png   # Microphone icon
└── 326552_mic_off_icon.png # Microphone off icon
```

## Dependencies

- **PySide6**: Modern Qt-based GUI framework
- **SpeechRecognition**: Speech-to-text functionality
- **pyttsx3**: Text-to-speech synthesis
- **requests**: HTTP requests for API calls
- **python-dotenv**: Environment variable management

## API Integration

### OpenRouter

The application integrates with OpenRouter for AI-powered conversations:
- **Model**: meta-llama/llama-4-maverick
- **Features**: Context-aware conversations, natural language processing
- **Rate Limits**: Subject to OpenRouter's pricing and limits

### Google Speech Recognition

Voice input is processed using Google's Speech Recognition API:
- **Features**: Real-time speech-to-text conversion
- **Languages**: Supports multiple languages
- **Accuracy**: High accuracy with proper microphone setup

## Troubleshooting

### Common Issues

1. **Microphone not working**
   - Check microphone permissions
   - Ensure microphone is properly connected
   - Test microphone in Windows settings

2. **API errors**
   - Verify your OpenRouter API key is correct
   - Check your internet connection
   - Ensure you have sufficient API credits

3. **Voice synthesis issues**
   - Verify Windows SAPI is working
   - Check if Zira voice is installed
   - Try different voice settings

### Error Messages

- **"Error speaking: run loop already started"**: This is a known pyttsx3 issue and doesn't affect functionality
- **"API Error"**: Check your OpenRouter API key and internet connection
- **"Microphone Error"**: Verify microphone setup and permissions

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- OpenRouter for providing AI model access
- Google for Speech Recognition API
- PySide6 team for the excellent GUI framework
- The open-source community for various dependencies

## Support

If you encounter any issues or have questions:
1. Check the troubleshooting section
2. Search existing issues
3. Create a new issue with detailed information

## Future Enhancements

- [ ] Support for custom voice models
- [ ] Multi-language support
- [ ] Voice command shortcuts
- [ ] Conversation export functionality
- [ ] Plugin system for additional features
- [ ] Cross-platform compatibility 