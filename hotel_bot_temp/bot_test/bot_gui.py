
my_reply="reply"

import tkinter as tk

root = tk.Tk()
user_input = tk.Entry(root)
user_input.pack()


import datetime
import requests
import random
import os
from time import sleep
import time
from pygame import mixer
#from gtts import gTTS    # Google TTS
import pyautogui as pgui
from sys import path

my_pa = path[0]
my_path = my_pa+"/temp"

hlo = ['hello', 'hi', 'hey']
hru = ['how are you', 'how are you doing', 'how do you do']   # messages
ext = ['bye', 'exit', 'go away', 'quit', 'get out'] 


vo_work = False     # voice output testing at start
try:
        mixer.init()
except:
        print('-----Voice output error')
else:
        vo_work = True


# reloading room and name list from file
with open(my_path+"/avail_rooms.txt", 'r') as file:
        temp = file.readline()
available_rooms = temp.split(' ')
available_rooms.pop()
#
file = open(my_path+"/rooms_names.txt", 'r')
rooms_names = {}
while True:
        temp = file.readline()
        if temp == '' or temp=='\n':
                break
        temp = temp.split(' ')
        temp_num = temp[0]
        temp_name = temp[1][0:-1]
        rooms_names[temp_num] = temp_name
file.close()


def rewrite():
        av_r = ""
        for rn in available_rooms:
                av_r += rn+' '
        file1 = open(my_path+"/avail_rooms.txt", 'w')
        file1.write(av_r)
        file1.close()
        # rooms_names
        my_temp = ""
        for elem in rooms_names:
                my_temp += str(elem)+' '+rooms_names[elem]+'\n'
        file2 = open(my_path+"/rooms_names.txt", 'w')
        file2.write(my_temp)
        file2.close()



        
# --------------------------------------------------------
def outp(mtext):
        output = tk.Label(root, text=mtext)
        output.config(text=mtext)
        output.pack()
        return mtext

# -------

def inp(txt):
        msg = user_input.get()
        return msg

# --------------------------------------------------------





def call_human(txt):
    import smtplib, ssl
    sender_email = "gbswayam@gmail.com"
    password = "bot_pw#12"
    context = ssl.create_default_context()
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(sender_email, password)
        server.sendmail(sender_email, sender_email, txt)


def send_sms(ph_numb, msg_text):
        import way2sms
        q=way2sms.Sms('6302523157', 'C2484R')
        # q=way2sms.Sms('6301310434', 'K5928Q')
        q.send(ph_numb, msg_text)
        q.logout()


def verified_number():
        return outp("verified_number()")


def taxi_book():
        return outp('Thank You.Have a great Ride')


def get_wthr():
        return "get_wthr()"


def wish():
        hr = datetime.datetime.now().hour
        mrng = 'morning'
        if hr >= 16:
                mrng = 'evening'
        elif hr >= 12:
                mrng = 'afternoon'    # wish good morning/afternoon/evening
        return "Good "+mrng+". How can I help you?"


def time_now():
        return time.strftime("%I:%M %p")


def date_now():
        return time.strftime("%A, %b %d, %Y")


def book_room():
        my_reply = outp("Room booked.")
        return my_reply

def check_out():
        my_reply = outp("Check out completed for room ")
        return my_reply


def tourist_places():
        my_reply = outp("tourist_places()")
        return my_reply


def translate():
        my_reply = outp("The translated sentence is ")
        return my_reply


# Responses
def resp(msg):     # for correct responses
        if 'hi' in msg or 'hello' in msg or 'hey' in msg:
                my_reply = outp(wish())
        elif 'how' in msg and 'you' in msg:
                my_reply = outp("I am fine. Thank you. What about you?")
        elif msg == "fine" or msg == "good" or msg == "well" or msg == 'no':
                my_reply = outp("Okay.")
        elif "kill" in msg or "destroy" in msg:
                my_reply = outp("I don't want to kill.")
        elif 'room' in msg and ('book' in msg or 'register' in msg):  # Booking
                book_room()
        elif ('avail' in msg or 'free' in msg) and 'room' in msg:
                num = len(available_rooms)
                if num == 0:
                        num = "Sorry. No"
                my_reply = outp(str(num)+" rooms are available.")
        elif msg == "check-out" or msg == "check out" or msg == "Leave room":
                check_out()                                  # Leaving
        elif "emergency" in msg or 'police' in msg or 'ambulance' in msg:
                my_reply = outp("Calling human.")
                call_human('emergency')
        elif 'call' in msg or 'human' in msg or 'help' in msg:
                my_reply = outp('Please enter your room number.')
                rr_no = inp('Room')
                call_human('Help '+rr_no)
        elif 'food' in msg:
                my_reply = outp('Please tell your room number.')
                r_numb = inp('Room')
                my_reply = outp('Which food do you want and how many?')
                fd = inp('Food')
                my_reply = outp('Sending '+fd)
                call_human('Food'+fd+' to room'+r_numb)
        elif 'taxi' in msg and 'book' in msg or 'organi' in msg or 'cab' in msg:
                taxi_book()
        elif 'sleep' in msg:
                my_reply = outp("Sleeping for 10 seconds...")
                sleep(10)
                my_reply = outp('Done.')
        elif msg in ext:
                my_reply = outp("Bye. See you soon.")
        elif 'thank' in msg or 'thanks' in msg:
                my_reply = outp("You are welcome.")
        elif "weather" in msg or 'temperature' in msg or 'rain' in msg or 'climate' in msg:
                my_reply = outp(get_wthr())
        elif "joke" in msg:
                my_reply = outp("What is the biggest lie in the entire universe? I have read and agree to the Terms & Conditions.")
        elif msg == 'lol' or msg == 'haha':
                my_reply = outp('I am glad that you found it funny.')
        elif 'tour' in msg or 'place' in msg or 'travel' in msg:
                tourist_places()
        elif 'time' in msg:
                my_reply = outp(time_now())
        elif 'date' in msg:
                date = date_now()
                my_reply = outp(date)
        elif "book" in msg:
                my_reply = outp('Please tell me what you want to book. Is it room or taxi or other?')
        elif msg == "" or msg == ' ':
                my_reply = outp("Please enter a message.")
        elif msg == "shutdown":
                my_reply = outp("Shutting down...")
                os.system('shutdown now')
        elif msg == "restart" or msg == "reboot":
                my_reply = outp("Restarting...")
                os.system('shutdown --reboot now')
        elif msg == "info" or msg == "hotel info" or msg == "hotel information":
                with open(my_path+"/info.txt", 'r') as file11:
                        my_reply = outp(file11.read())
        elif "music" in msg or 'song' in msg:
                fil_nam = random.choice(os.listdir(my_path+"/songs/"))
                if vo_work:
                        my_reply = outp("Playing music...")
                        mixer.music.load(my_path+'/songs/'+fil_nam)
                        mixer.music.play()
                else:
                        print('Error playing music.')
        elif 'translate' in msg:
                translate()
        elif 'ok' in msg or 'okay' in msg:
                my_reply = outp("Okay then.")
        elif "what can you" in msg:
                with open(my_path+"/what_can_do.txt", 'r') as file0:
                        my_reply = outp(file0.read())
        elif 'password' in msg or 'wifi' in msg or 'wi-fi' in msg:
                my_reply = outp("Wi-Fi password is hotel123. I repeat hotel123.")
        elif 'stop' in msg:
                if vo_work:
                        mixer.music.stop()
                else:
                        print('Unable to stop.')
        elif 'problem' in msg:
                my_reply = outp('Please enter the problem.')
                prob = str(inp('Problem'))
                call_human('Problem'+prob)
                add_data = open(my_path+"/feedback.txt", 'a')
                add_data.write("\n"+prob)          # Feedback
                add_data.close()
        elif 'clean' in msg:
                my_reply = outp('Do you want us to clean the room?')
                ab = inp('Yes/No')
                if 'y' in ab:
                        my_reply = outp('Please enter room number.')
                        rnu = inp('Room')
                        call_human('Clean room'+rnu)
                elif 'n' in ab:
                        my_reply = outp('It is okay.')
        elif 'feedback' in msg:
                my_reply = outp("Please give feedback now.")
                txt = inp('Feedback')
                add_data = open(my_path+"/feedback.txt", 'a')
                add_data.write("\n"+txt)    # Feedback
                add_data.close()
                my_reply = outp("Thank you for your valuable feedback.")
        elif 'extra' in msg:
                my_reply = outp('Please enter what you need extra')
                need = inp('Extra')
                my_reply = outp('Please enter your room number.')
                rnu = inp('Room')
                my_reply = outp('Sending Extra '+need+' to Room'+str(rnu))
                call_human('Extra : '+need+' Room : '+str(rnu))
        elif 'wake' in msg:
                my_reply = outp("Do you want a wakeup call?")
                response = inp("Yes/No")
                if 'y' in response:
                        my_reply = outp("Please enter your room number.")
                        rn = inp("Room")
                        my_reply = outp("Enter at what time you want.")
                        tm = inp("Time")
                        call_human("Wakeup call : "+rn+" "+tm)
                else:
                        my_reply = outp("Okay.")
        elif 'search' in msg:
                my_reply = outp("Please enter what you want to search for.")
                sea = inp("Search")
                url = "google.com/search?q="+sea
                pgui.click(69, 19)  # click on browser
                sleep(13)
                pgui.hotkey('ctrl', 't')
                pgui.typewrite(url)
                pgui.press('enter')
        elif msg == "err":
                my_reply = outp("I can't hear that.")
        else:
                my_reply = outp("Sorry. Please repeat.")
                add_data = open(my_path+"/newdata.txt", 'a')
                add_data.write("\n")
                add_data.write(msg)
                add_data.close()
        #
        return my_reply



def cb(event):
    user_text = inp('0').lower()
    resp(user_text)


outp("Hello there.")

cb('start')



'''
import random
import tkinter as tk

root = tk.Tk()
user_input = tk.Entry(root)
user_input.pack()


def cb(event):
    user_text = user_input.get()
    resp(user_text)
    output.config(text=my_reply)


user_input.bind("<Return>", cb)
output = tk.Label(root, text='')
output.pack()

tk.mainloop()
'''


