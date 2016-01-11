#!/usr/bin/etc python

import Backend

print("Initializing...please be patient...\n")

Backend.InitResource()

#dummo intro to get messy stuff out of the way
ans = Backend.get_response("initializing")

#Intro text
print("\n\nWelcome! Type below to have a conversation with TickTock. Make sure to put your input inside quotation marks. Type exit() to stop.\n")
print("TickTock: \"Hi! I'm TickTock. Ask me some questions.\"")

while(1):
    question = input('You: ')
    ans = Backend.get_response(question)
    print("TickTock: \"" + ans + "\"")
    
