import pyttsx3  # For text-to-speech (TTS) conversion
import datetime # To get current date and time
import wikipedia # To fetch information from Wikipedia
import webbrowser # To open web browsers and URLs
import os       # For OS-level operations like clearing screen and path manipulation
import pyjokes  # To get random jokes
import shutil   # For high-level file operations, here used for terminal size
import speech_recognition as sr # For speech-to-text (STT) conversion

# --- Text-to-Speech Function ---
def speak(audio_text):
    """
    Converts the given text to speech using pyttsx3.
    It tries to initialize a TTS engine, select an English voice if available,
    and then speaks the text. Includes error handling.
    """
    engine = None
    try:
        # Initialize the TTS engine. pyttsx3 will try to find a suitable pre-installed engine.
        # Common engines: SAPI5 (Windows), NSSpeechSynthesizer (macOS), eSpeak (Linux).
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')

        if voices: # Check if any voices are available
            # Attempt to find an English voice.
            english_voice = next((v for v in voices if v.languages and 'en' in v.languages[0].lower()), None)
            if english_voice:
                engine.setProperty('voice', english_voice.id)
            else:
                # If no English voice is found, use the first available voice as a fallback.
                engine.setProperty('voice', voices[0].id)

        engine.say(audio_text)
        engine.runAndWait() # Blocks while processing all currently queued commands.
    except Exception as e:
        print(f"TTS Error: {e}")
        print("Please ensure a compatible TTS engine (e.g., eSpeak on Linux) is installed and configured.")
        # Fallback to printing the text if TTS fails.
        print(f"Assistant would say: {audio_text}")
    finally:
        # Ensure the engine's loop is properly terminated if it was started and an error occurred.
        if engine and hasattr(engine, '_inLoop') and engine._inLoop:
            engine.endLoop()


# --- Greeting Function ---
def wishMe():
    """
    Greets the user based on the current time of day.
    Also introduces the assistant by its name.
    """
    current_hour = int(datetime.datetime.now().hour)
    if 0 <= current_hour < 12:
        speak("Good Morning Sir!")
    elif 12 <= current_hour < 18:
        speak("Good Afternoon Sir!")
    else:
        speak("Good Evening Sir!")

    assistant_name = "Jarvis 2 point o" # Assistant's name, can be made configurable.
    speak("I am your Assistant")
    speak(assistant_name)


# --- User Name Handling Function ---
def usrname(recognizer_instance): # Parameter renamed for clarity
    """
    Asks for the user's name, captures it via speech, and greets them.
    Displays a welcome message on the console.
    """
    speak("What should I call you sir")
    user_name = takeCommand(recognizer_instance)
    if user_name and user_name != "None": # Check if a valid name was captured
        speak("Welcome Mister")
        speak(user_name)
        try:
            # Get terminal width for centered printing.
            columns = shutil.get_terminal_size().columns
            print("#####################".center(columns))
            print(f"Welcome Mr. {user_name}".center(columns))
            print("#####################".center(columns))
        except OSError: # shutil.get_terminal_size() can fail in non-terminal environments (e.g., some IDEs)
            print("#####################")
            print(f"Welcome Mr. {user_name}")
            print("#####################")

    speak("How can I Help you, Sir")


# --- Speech-to-Text Command Input Function ---
def takeCommand(recognizer_instance): # Parameter renamed for clarity
    """
    Listens for user's voice command using the microphone,
    recognizes it using Google Speech Recognition, and returns the command as text.
    Includes noise adjustment and error handling.
    """
    r = recognizer_instance # Use the passed recognizer instance

    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1 # Seconds of non-speaking audio before a phrase is considered complete.
        r.adjust_for_ambient_noise(source, duration=1) # Adjusts for ambient noise for better recognition.
        audio_data = None
        try:
            # Listen for audio input with timeouts to prevent indefinite blocking.
            audio_data = r.listen(source, timeout=5, phrase_time_limit=5)
        except sr.WaitTimeoutError:
            print("No speech detected within the time limit.")
            return "None" # Return "None" if no speech is detected

    recognized_query = "None" # Default return value
    if audio_data:
        try:
            print("Recognizing...")
            # Use Google's speech recognition.
            recognized_query = r.recognize_google(audio_data, language='en-in') # 'en-in' for Indian English
            print(f"User said: {recognized_query}")
        except sr.UnknownValueError:
            # This error means the speech was unintelligible.
            print("Google Speech Recognition could not understand the audio.")
            speak("I am sorry, I could not understand what you said.")
            recognized_query = "None"
        except sr.RequestError as e:
            # This error means there was an issue with the Google Speech Recognition service.
            print(f"Could not request results from Google Speech Recognition service; {e}")
            speak("I am having trouble connecting to the speech service.")
            recognized_query = "None"
        except Exception as e:
            # General exception during recognition.
            print(f"An unexpected error occurred during speech recognition: {e}")
            print("Unable to Recognize your voice.")
            recognized_query = "None"

    return recognized_query.lower() # Return the command in lowercase for easier processing.


# --- Screen Clearing Function ---
def clear_screen():
    """Clears the terminal screen in a cross-platform way."""
    # For Windows
    if os.name == 'nt':
        os.system('cls')
    # For Mac and Linux (os.name is 'posix')
    else:
        os.system('clear')


# --- Main Orchestration Function ---
def orchestrate():
    """
    Main function to orchestrate the assistant's operations.
    Initializes, greets, and then enters a loop to listen for and process commands.
    """
    recognizer = sr.Recognizer() # Create a single Recognizer instance for efficiency.
    wishMe()
    usrname(recognizer) # Pass the recognizer instance.

    assistant_name_local = "Jarvis 2 point o" # Local variable for the assistant's name, can be changed.

    # Main command loop
    while True:
        query = takeCommand(recognizer) # Get command from user, pass recognizer instance.

        if query == "None": # If command recognition failed or no command was given, loop again.
            continue

        # --- Command Processing ---

        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            search_query = query.replace("wikipedia", "").strip()
            if not search_query: # If "wikipedia" was said alone, ask for search term.
                speak("What would you like to search on Wikipedia?")
                search_query = takeCommand(recognizer)
                if search_query == "None" or not search_query:
                    speak("No search term provided for Wikipedia.")
                    continue
            try:
                # Fetch summary from Wikipedia (first 3 sentences).
                results = wikipedia.summary(search_query, sentences=3)
                speak("According to Wikipedia")
                print(results)
                speak(results)
            except wikipedia.exceptions.DisambiguationError as e:
                # Handle cases where the search term is ambiguous.
                speak(f"Your query '{search_query}' led to multiple results like {e.options[:3]}. Please be more specific.")
                print(f"DisambiguationError for '{search_query}': {e}")
            except wikipedia.exceptions.PageError:
                # Handle cases where no Wikipedia page is found.
                speak(f"Sorry, I could not find a Wikipedia page for {search_query}.")
                print(f"PageError for query: {search_query}")
            except Exception as e:
                # General error during Wikipedia search.
                speak("Sorry, an error occurred while searching Wikipedia.")
                print(f"Wikipedia search error: {e}")

        elif 'open youtube' in query:
            speak("Opening Youtube in your web browser.")
            # Using https://www.youtube.com as a placeholder, direct link is better.
            webbrowser.open("https://www.youtube.com")

        elif 'open google' in query:
            speak("Opening Google in your web browser.")
            webbrowser.open("https://www.google.com")

        elif 'open stackoverflow' in query or 'open stack overflow' in query:
            speak("Opening Stack Overflow. Happy coding!")
            webbrowser.open("https://stackoverflow.com")

        elif 'what`s the time' in query or "what is the time" in query:
            # Get current time and format it (e.g., 02:30 PM).
            current_time_str = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"Sir, the time is {current_time_str}")

        elif 'how are you' in query:
            speak("I am functioning optimally, Thank you for asking.")

        elif 'fine' in query or "good" in query or "i am good" in query or "i am fine" in query:
            speak("It's good to know that you are fine.")

        elif "change my name to" in query: # Refers to changing the assistant's name.
            new_name = query.replace("change my name to", "").strip()
            if new_name:
                assistant_name_local = new_name
                speak(f"Okay, you can call me {assistant_name_local} from now on.")
            else:
                speak("Please specify a name.")

        elif "what's your name" in query or "what is your name" in query:
            speak(f"My name is {assistant_name_local}.")

        elif 'exit' in query or 'quit' in query or 'goodbye' in query:
            speak("Thanks for your time. Goodbye Sir!")
            break # Exit the main loop, terminating the program.

        elif "who made you" in query or "who created you" in query:
            # Generic response about creation.
            speak("I am a virtual assistant, a result of programming and algorithms. I was conceptually developed based on a project by Group Number 49, under the guidance of Professor Gauraw Jumnake sir.")

        elif 'joke' in query or 'tell me a joke' in query :
            try:
                joke = pyjokes.get_joke()
                print(joke)
                speak(joke)
            except Exception as e:
                speak("I couldn't fetch a joke right now.")
                print(f"Error getting joke: {e}")

        elif "who i am" in query:
            speak("If you are talking, you are most likely a human.")

        elif "why you came to this world" in query or "why were you created" in query:
            speak("I was created to assist with tasks and provide information. My development was inspired by a project from Group Number 49.")

        elif 'what is love' in query:
            # A philosophical or dictionary-style answer.
            speak("Love is a complex set of emotions, behaviors, and beliefs associated with strong feelings of affection, protectiveness, warmth, and respect for another person. It can also be a feeling of deep affection for or pleasure in something.")

        elif "who are you" in query:
            speak(f"I am {assistant_name_local}, your virtual assistant, inspired by a project from Group Number 49.")

        elif 'what is the reason for you to be here' in query or 'your purpose' in query:
            speak("My purpose is to assist you with tasks, answer questions, and make your interaction with technology smoother. I was inspired by a Minor project by Group Number 49.")

        elif 'lock window' in query or 'lock device' in query or 'lock screen' in query:
            # Locking the screen is OS-specific and cannot be done generically by this script.
            speak("Locking the device is an operating system specific function.")
            speak("I cannot perform this action in a generic way. You may need to use your system's shortcut to lock the screen.")
            # Providing info about common shortcuts.
            print("INFO: Screen lock is OS-specific. Common shortcuts:")
            print("- Windows: Win + L")
            print("- macOS: Control + Command + Q")
            print("- Linux (varies): Often Ctrl + Alt + L")

        else:
            # This block handles queries that are recognized by STT but not matched by any command.
            # It avoids responding to very short or likely erroneous recognitions.
            if query and query != "None" and len(query.split()) > 2 :
                # You could add a generic "I don't understand" response here if desired.
                # speak(f"I'm not sure how to handle '{query}'. Can you try a different command?")
                pass # Currently does nothing for unrecognized (but captured) commands.
