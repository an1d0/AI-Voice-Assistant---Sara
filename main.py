import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton, QLabel, QHBoxLayout
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QMovie, QImage, QPixmap
import speech_recognition as sr
import pyttsx3
from dotenv import load_dotenv
import requests
import json

# Load environment variables
load_dotenv()

# Configure OpenRouter API
OPENROUTE_API_KEY = os.getenv('OPENROUTE_API_KEY')
OPENROUTE_API_URL = "https://openrouter.ai/api/v1/chat/completions"

class VoiceAssistant(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Voice Assistant")
        self.setGeometry(100, 100, 800, 600)
        
        # Initialize text-to-speech engine with Windows SAPI
        self.tts_engine = pyttsx3.init()
        voices = self.tts_engine.getProperty('voices')
        
        # Print available voices
        print("\nAvailable voices:")
        for voice in voices:
            print(f"Voice: {voice.name}")
        
        # Try to set a female voice
        for voice in voices:
            if "Zira" in voice.name:  # Zira is a female voice
                self.tts_engine.setProperty('voice', voice.id)
                print(f"Successfully set voice to: {voice.name}")
                break
        
        # Set speaking rate and volume
        self.tts_engine.setProperty('rate', 150)    # Speed of speech
        self.tts_engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Add GIF animation
        self.gif_label = QLabel()
        self.movie = QMovie("sara_gif.gif")
        self.gif_label.setMovie(self.movie)
        self.movie.start()
        layout.addWidget(self.gif_label)
        
        # Add chat display
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        layout.addWidget(self.chat_display)
        
        # Create horizontal layout for text input and microphone button
        input_layout = QHBoxLayout()
        
        # Add text input
        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText("Type your message here...")
        self.text_input.returnPressed.connect(self.process_text_input)
        input_layout.addWidget(self.text_input)
        
        # Add microphone image button
        self.microphone_label = QLabel()
        self.set_microphone_icon("326557_mic_icon.png")
        self.microphone_label.setCursor(Qt.PointingHandCursor)
        self.microphone_label.mousePressEvent = lambda event: self.toggle_recording()
        input_layout.addWidget(self.microphone_label)
        
        # Add input layout to main layout
        layout.addLayout(input_layout)
        
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.is_recording = False
        self.recording_thread = None
        
        # Initialize conversation history
        self.conversation_history = []
        
    def set_microphone_icon(self, icon_path):
        pixmap = QPixmap(icon_path)
        self.microphone_label.setPixmap(pixmap.scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def toggle_recording(self):
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()
            
    def start_recording(self):
        self.is_recording = True
        self.set_microphone_icon("326552_mic_off_icon.png")
        self.recording_thread = RecordingThread(self.recognizer)
        self.recording_thread.text_recognized.connect(self.process_voice_input)
        self.recording_thread.start()
        
    def stop_recording(self):
        self.is_recording = False
        self.set_microphone_icon("326557_mic_icon.png")
        if self.recording_thread:
            self.recording_thread.stop()
            
    def process_voice_input(self, text):
        if text:
            self.chat_display.append(f"You: {text}")
            self.process_with_ai(text)
            
    def process_text_input(self):
        text = self.text_input.text()
        if text:
            self.chat_display.append(f"You: {text}")
            self.text_input.clear()
            self.process_with_ai(text)
            
    def process_with_ai(self, text):
        # Check for specific queries about the assistant's name
        if "what is your name" in text.lower() or "who are you" in text.lower():
            ai_response = "Hi, I am Sara."
            self.chat_display.append(f"Assistant: {ai_response}")
            self.speak_text(ai_response)
            return

        try:
            # Add user message to conversation history
            self.conversation_history.append({"role": "user", "content": text})
            
            # Prepare the API request for OpenRouter
            headers = {
                "Authorization": f"Bearer {OPENROUTE_API_KEY}",
                "HTTP-Referer": "http://localhost:3000",
                "X-Title": "AI Voice Assistant",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "meta-llama/llama-4-maverick",
                "messages": self.conversation_history,
                "temperature": 0.7,
                "max_tokens": 1000,
                "stream": False
            }
            
            # Make the API request
            response = requests.post(OPENROUTE_API_URL, headers=headers, json=data)
            response.raise_for_status()
            
            # Extract the AI's response
            ai_response = response.json()["choices"][0]["message"]["content"]
            
            # Add AI response to conversation history
            self.conversation_history.append({"role": "assistant", "content": ai_response})
            
            # Display and speak the response
            self.chat_display.append(f"Assistant: {ai_response}")
            self.speak_text(ai_response)
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            self.chat_display.append(f"Assistant: {error_msg}")
            self.speak_text("I encountered an error. Please try again.")
            
    def speak_text(self, text):
        try:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            print(f"Error speaking: {str(e)}")

class RecordingThread(QThread):
    text_recognized = Signal(str)
    
    def __init__(self, recognizer):
        super().__init__()
        self.recognizer = recognizer
        self.is_running = True
        
    def run(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            while self.is_running:
                try:
                    audio = self.recognizer.listen(source, timeout=5)
                    text = self.recognizer.recognize_google(audio)
                    self.text_recognized.emit(text)
                except sr.WaitTimeoutError:
                    continue
                except sr.UnknownValueError:
                    continue
                except Exception as e:
                    print(f"Error in recording thread: {str(e)}")
                    
    def stop(self):
        self.is_running = False

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VoiceAssistant()
    window.show()
    sys.exit(app.exec()) 