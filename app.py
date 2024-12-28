import speech_recognition as sr
import pyttsx3
import datetime
from fuzzywuzzy import fuzz

# Initialize the recognizer and TTS engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Menu with Indian dishes and prices
menu = {
    "Starters": {
        "Paneer Tikka": 150.0,
        "Samosa": 20.0,
        "Pakora": 50.0
    },
    "Main Course": {
        "Butter Chicken": 350.0,
        "Paneer Butter Masala": 300.0,
        "Dal Makhani": 200.0,
        "Veg Biryani": 180.0,
        "Chicken Biryani": 220.0
    },
    "Breads": {
        "Tandoori Roti": 20.0,
        "Butter Naan": 30.0,
        "Stuffed Paratha": 50.0
    },
    "Desserts": {
        "Gulab Jamun": 40.0,
        "Rasgulla": 35.0,
        "Kheer": 60.0
    },
    "Drinks": {
        "Masala Chai": 15.0,
        "Lassi": 50.0,
        "Buttermilk": 20.0
    }
}

# Function to wish the user based on the time of day
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning! How can I help you today?")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon! What would you like to order?")
    else:
        speak("Good Evening! Hope you're doing well!")

# Function to listen to user input with Indian English accent
def listen():
    with sr.Microphone() as source:
        print("Listening for your command...")
        recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjust for ambient noise
        try:
            audio = recognizer.listen(source, timeout=5)  # Set timeout in seconds
            command = recognizer.recognize_google(audio, language="en-IN")  # Use Indian English
            print(f"You said: {command}")  # Print the recognized speech as text
            return command.lower()
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand that. Could you please repeat?")
            return None
        except sr.RequestError:
            print("Sorry, there was an issue with the speech recognition service.")
            return None
        except sr.WaitTimeoutError:
            print("Sorry, I couldn't hear anything.")
            return None

# Function to speak text back to the user
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to handle text-based command recognition with fuzzy matching
def recognize_command(command):
    if not command:
        speak("Sorry, I couldn't process your request. Please try again.")
        return False

    for category, items in menu.items():
        for item in items:
            if isinstance(item, str) and fuzz.partial_ratio(command, item.lower()) > 80:
                speak(f"Got it! {item} has been added to your order.")
                return True

    if "menu" in command:
        speak("Here is the menu for the restaurant. Take your time to decide!")
        for category, items in menu.items():
            speak(f"{category}:")
            for item in items:
                speak(f"  - {item}")
        return True

    if "price" in command:
        speak("Which item would you like to know the price for?")
        item = listen()
        if item:
            provide_price(item)
        return True

    if "cart" in command:
        speak("Your cart is currently empty. Would you like to add something?")
        return True

    if "exit" in command or "bye" in command:
        speak("Thank you for visiting! Have a great day!")
        return False

    speak("Sorry, I didn't understand that. Could you please repeat?")
    return True

# Function to provide the price of an item
def provide_price(item):
    for category, items in menu.items():
        if item in items:
            price = items[item]
            speak(f"The price for {item} is ₹{price}.")
            return
    speak(f"Sorry, {item} is not available in the menu.")

# Main function to interact with the user
def run_voice_assistant():
    wishMe()
    speak("Welcome to the restaurant! How can I assist you today?")
    while True:
        command = listen()
        if command:
            print(f"Recognized Command: {command}")
            continue_listening = recognize_command(command)
            if not continue_listening:
                break

if __name__ == "__main__":
    run_voice_assistant()
