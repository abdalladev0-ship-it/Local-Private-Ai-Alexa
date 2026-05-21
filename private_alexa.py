import os
import time
import subprocess
import webbrowser
import asyncio
import threading
import speech_recognition as sr
import ollama
from gtts import gTTS
import websockets

PORT = 8000
WS_PORT = 8001
recognizer = sr.Recognizer()

# Keep track of active browser connections
CONNECTED_CLIENTS = set()

async def ws_handler(websocket):
    """Registers open browser tabs so Python can talk to them instantly."""
    CONNECTED_CLIENTS.add(websocket)
    try:
        await websocket.wait_closed()
    finally:
        CONNECTED_CLIENTS.remove(websocket)

def start_ws_server():
    """Runs the background network pipe for browser communication."""
    async def run():
        async with websockets.serve(ws_handler, "localhost", WS_PORT):
            await asyncio.Future()  # run forever
    asyncio.run(run())

def trigger_browser_animation(state):
    """Sends a fast text command to the open tab to start/stop moving."""
    async def send():
        if CONNECTED_CLIENTS:
            # Send 'talking' or 'listening' state to browser JavaScript
            await asyncio.gather(*[client.send(state) for client in CONNECTED_CLIENTS])
    
    # Safely handle the async call from inside standard Python loops
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    if loop.is_running():
        # If loop is busy, schedule it safely
        asyncio.run_coroutine_threadsafe(send(), loop)
    else:
        loop.run_until_complete(send())

def start_local_server():
    """Hosts the smart HTML page that listens for Python state changes."""
    import http.server
    import socketserver

    class CustomRouter(http.server.SimpleHTTPRequestHandler):
        def log_message(self, format, *args):
            pass # Keep terminal outputs clean

        def do_GET(self):
            if self.path == "/" or self.path == "/index.html":
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                
                # Intelligent single-page layout that reacts to network signals
                html_content = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <style>
                        body {{
                            margin: 0;
                            background-color: black;
                            overflow: hidden;
                            display: flex;
                            justify-content: center;
                            align-items: center;
                            height: 100vh;
                        }}
                        .alexa-ring {{
                            width: 35vw;
                            height: 35vw;
                            max-width: 400px;
                            max-height: 400px;
                            border: 15px solid transparent;
                            border-radius: 50%;
                            border-top: 15px solid #0044ff;
                            border-right: 15px solid #1a1a1a;
                            border-bottom: 15px solid #1a1a1a;
                            box-shadow: 0 0 20px #0044ff;
                            transition: all 0.5s ease;
                        }}
                        /* Active states managed dynamically by JavaScript */
                        .talking {{
                            border-top: 15px solid #00f0ff;
                            border-right: 15px solid #0044ff;
                            border-bottom: 15px solid #7000ff;
                            box-shadow: 0 0 60px #0044ff, 0 0 120px #00f0ff;
                            animation: spinAndPulse 1.2s infinite linear;
                        }}
                        .listening {{
                            border-top: 15px solid #00f0ff;
                            border-bottom: 15px solid #00f0ff;
                            box-shadow: 0 0 40px #00f0ff;
                            animation: pulseOnly 1.5s infinite ease-in-out alternate;
                        }}
                        @keyframes spinAndPulse {{
                            0% {{ transform: rotate(0deg) scale(0.95); filter: brightness(1); }}
                            50% {{ filter: brightness(1.4); }}
                            100% {{ transform: rotate(360deg) scale(0.95); filter: brightness(1); }}
                        }}
                        @keyframes pulseOnly {{
                            0% {{ transform: scale(0.95); opacity: 0.6; }}
                            100% {{ transform: scale(1.02); opacity: 1; }}
                        }}
                    </style>
                </head>
                <body>
                    <div id="ring" class="alexa-ring"></div>

                    <script>
                        // Open background data connection straight to Python script
                        const ws = new WebSocket('ws://localhost:{WS_PORT}');
                        const ring = document.getElementById('ring');

                        ws.onmessage = (event) => {{
                            const state = event.data;
                            ring.className = 'alexa-ring'; // Reset classes
                            
                            if (state === 'talking') {{
                                ring.classList.add('talking');
                            }} else if (state === 'listening') {{
                                ring.classList.add('listening');
                            }}
                        }};
                    </script>
                </body>
                </html>
                """
                self.wfile.write(html_content.encode('utf-8'))
            else:
                super().do_GET()

    socketserver.TCPServer.allow_reuse_address = True
    try:
        with socketserver.TCPServer(("", PORT), CustomRouter) as httpd:
            httpd.serve_forever()
    except Exception:
        pass

# Fire up Web server and WebSocket channels in background threads
threading.Thread(target=start_local_server, daemon=True).start()
threading.Thread(target=start_ws_server, daemon=True).start()

def speak_and_animate(text):
    """Signals open window to animate, plays the audio voice, then targets a calm state."""
    print(f"🤖 Alexa: {text}")
    try:
        tts = gTTS(text=text, lang='en')
        tts.save("alexa_voice.mp3")
        
        # Signal window to rapidly spin and pulse
        trigger_browser_animation("talking")
        
        # Stream audio text sequence
        subprocess.run(["mpg123", "alexa_voice.mp3"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        if os.path.exists("alexa_voice.mp3"):
            os.remove("alexa_voice.mp3")
            
        # Signal window to drop back down to standard state
        trigger_browser_animation("idle")
    except Exception as e:
        print(f"Audio Error: {e}")

def process_command(command):
    """Processes your private voice commands locally."""
    command = command.lower()
    
    if "time" in command:
        current_time = time.strftime("%I:%M %p")
        speak_and_animate(f"The current time is {current_time}.")
        
    elif "open youtube" in command:
        speak_and_animate("Opening YouTube.")
        webbrowser.open("https://youtube.com")
        
    elif "stop" in command or "goodbye" in command or "quit" in command:
        speak_and_animate("Goodbye.")
        return False
    else:
        print("🧠 Processing locally and privately...")
        try:
            response = ollama.chat(
                model='qwen2.5:0.5b',
                messages=[
                    {'role': 'system', 'content': 'You are private Alexa. Keep answers under 20 words.'},
                    {'role': 'user', 'content': command}
                ]
            )
            speak_and_animate(response['message']['content'].strip())
        except Exception:
            speak_and_animate("My local memory loop encountered a resource lag.")
            
    return True

# --- Launch Sequence ---
print("🚀 Initialising Private Voice Assistant...")
print("Opening application window canvas...")
webbrowser.open(f"http://localhost:{PORT}")
time.sleep(2) # Give browser a brief moment to connect its internal websocket pipeline

speak_and_animate("System online. Listening for local commands.")

running = True
while running:
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        
        # Change ring color to glowing cyan to signal it is listening for your microphone
        trigger_browser_animation("listening")
        print("\n🎤 Say a command...")
        
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            # Return to plain state while thinking
            trigger_browser_animation("idle")
            
            user_text = recognizer.recognize_google(audio)
            print(f"🗣️ You said: {user_text}")
            
            running = process_command(user_text)
            
        except sr.WaitTimeoutError:
            continue
        except sr.UnknownValueError:
            print("🔊 Listening standby...")
        except sr.RequestError as e:
            print(f"❌ Microphone error: {e}")
