#!/usr/bin/env python
import random
import json

import torch

from model import NeuralNet
from nltk_utils import bag_of_words, tokenize
from gtts import gTTS
import gtts_token
import os
import pygame
from io import BytesIO
import sounddevice as sd



import speech_recognition as sr



device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('intents.json', 'r') as json_data:
    intents = json.load(json_data)

FILE = "data.pth"
data = torch.load(FILE)

user_info = open("user_info.txt","w+")
english = 'en'


input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "Quin"

greeting = "Hi, I'm Quin!"
print("Hi, I'm Quin!")
#speak = gTTS(text=greeting, lang=english, slow=False)
#speak.save("voice.mp3")
#os.system("afplay voice.mp3")
r = sr.Recognizer()
#pygame.mixer.init()
fp = BytesIO()


with sr.Microphone() as source:
    while True:
        r.adjust_for_ambient_noise(source)
        print("You: ")
        audio = r.listen(source)
        sentence = "default sentence"
        try:
            #print("You said: : " + r.recognize_google(audio))
            sentence = r.recognize_google(audio)
        except Exception as e:
            print("Error: " + str(e))
        
        #sentence = input("You: ")
        if sentence == "goodbye":
            break
        input_string = ''.join([str(elem) for elem in sentence])
        sentence = tokenize(sentence)
        X = bag_of_words(sentence, all_words)
        X = X.reshape(1, X.shape[0])
        X = torch.from_numpy(X).to(device)

        output = model(X)
        _, predicted = torch.max(output, dim=1)

        tag = tags[predicted.item()]
        print("tag: " + str(tag))
        

        probs = torch.softmax(output, dim=1)
        prob = probs[0][predicted.item()]
        if prob.item() > 0.75:
            for intent in intents['intents']:
                if tag == intent["tag"]:
                    words = f"{random.choice(intent['responses'])}"
                    print(f"{bot_name}: " + words)
                    user_info.write(tag + ": " + input_string + "\n")
                    try:
                        voice = gTTS(words)
                        voice.save("voice.mp3")
                    except Exception as e:
                        print(e)
                    #os.system("afplay voice.mp3")

                    os.system("afplay voice.mp3")


        else:
            print(f"{bot_name}: Sorry, I'm still learning, I don't quite understand what you said...")
