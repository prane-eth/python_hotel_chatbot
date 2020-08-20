import random
import tkinter as tk
import sys

import pyttsx3
engine = pyttsx3.init()

root = tk.Tk()
user_input = tk.Entry(root)
user_input.pack()

def my_pack(txt):
    output = tk.Label(root, text=txt)
    output.pack()
    #print(txt)

my_resp = {
        'hi': 'hi there',
        'hello': 'hello there',
        'hey': 'hey there',
        'bye': 'bye there',
        'ok' : 'okay then',
        
        '': 'Please enter a message'
    }

def outp(txt):
    my_pack('Bot : '+txt)
    engine.say(txt)
    engine.runAndWait()


def resp(msg):
    my_pack("You : "+msg)
    if msg in my_resp:
        outp(my_resp[msg])
    elif 'exit' in msg:
        root.destroy()
    else:
        outp("I cant understand")

def cb(event):
    user_text = user_input.get()
    resp(user_text)

tk.Canvas(root, height=100).pack()
user_input.bind("<Return>", cb)
output = tk.Label(root)
my_pack('----Started----')
tk.mainloop()

