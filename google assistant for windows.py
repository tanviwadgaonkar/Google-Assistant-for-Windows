#!/usr/bin/env python
# coding: utf-8

# In[1]:


import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import requests
import playsound
from gtts import gTTS
import os
import wolframalpha
from selenium import webdriver

# Function to capture and return voice input
def get_voice_input():
    input_recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        audio = input_recognizer.listen(source)
        try:
            input_text = input_recognizer.recognize_google(audio)
            print(f"Your input is: {input_text}")
            return input_text
        except sr.UnknownValueError:
            print("Sorry, I could not understand your input. Please try again.")
            return None

# Function to synthesize and play a response
def speak_response(response_text):
    response = gTTS(text=response_text, lang='en')
    response_filename = "response.mp3"
    response.save(response_filename)
    playsound.playsound(response_filename, True)
    os.remove(response_filename)

# Main function to handle voice input and provide appropriate response
def handle_input(input_text):
    input_text = input_text.lower()
    
    # Exit the program if the input contains "stop," "exit," or "bye"
    if "stop" in input_text or "exit" in input_text or "bye" in input_text:
        speak_response("Ok, bye and take care.")
        return False
    
    # Search Wikipedia and provide a summary if the input contains "wikipedia"
    if 'wikipedia' in input_text:
        input_text = input_text.replace("wikipedia", "")
        wikipedia_summary = wikipedia.summary(input_text, sentences=3)
        speak_response(f"According to Wikipedia, {wikipedia_summary}")
        return True
    
    # Provide the current time if the input contains "time"
    if 'time' in input_text:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        speak_response(f"The current time is {current_time}.")
        return True
    
    # Perform a search if the input contains "search"
    if 'search' in input_text:
        input_text = input_text.replace("search", "")
        webbrowser.open_new_tab(input_text)
        speak_response(f"Searching for {input_text}.")
        return True
    
    # Use Wolfram Alpha to answer a math or science question if the input contains "calculate" or "what is"
    if "calculate" in input_text or "what is" in input_text:
        app_id = "YOUR_API_KEY_HERE"
        client = wolframalpha.Client(app_id)
        result = client.query(input_text)
        answer = next(result.results).text
        speak_response(f"The answer is {answer}.")
        return True
    
    # Open the Google homepage if the input contains
# Open the Google homepage if the input contains "open google"
    if 'open google' in input_text:
        webbrowser.open_new_tab("https://www.google.com")
        speak_response("Google is open.")
        return True
    
    # Search YouTube for the specified topic if the input contains "youtube"
    if 'youtube' in input_text:
        driver = webdriver.Chrome(r"YOUR_WEBDRIVER_LOCATION_HERE")
        driver.implicitly_wait(1)
        driver.maximize_window()
        input_text = input_text.replace("youtube", "")
        driver.get(f"http://www.youtube.com/results?search_query={input_text}")
        speak_response(f"Opening YouTube search results for {input_text}.")
        return True
    
    # Open Microsoft Word if the input contains "open word"
    if 'open word' in input_text:
        speak_response("Opening Microsoft Word.")
        os.startfile(r"YOUR_WORD_LOCATION_HERE")
        return True
    
    # Provide an error message if no appropriate action was found
    speak_response("Sorry, I am unable to perform that action.")
    return True

# Main program loop
def main():
    speak_response("Hi, I am tinku your personal desktop assistant.")
    while True:
        speak_response("How can I help you?")
        input_text = get_voice_input()
        if input_text is None:
            continue
        if not handle_input(input_text):
            break

if __name__ == '__main__':
    main()


# In[ ]:




