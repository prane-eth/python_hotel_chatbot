import datetime
# import pyttsx3
import requests
import random
import os
import time
#from googletrans import Translator
#import playsound

# from gtts import gTTS      # Google TTS is slow
# import RPi.GPIO as GPIO    #  for bluetooth module and mic
# from pygame import mixer
# import speech_recognition as sr


'''
engine = pyttsx3.init()
engine.setProperty('rate', 160)  # 120 words per minute
engine.setProperty('volume', 5.0)
engine.setProperty('voice', 'en-scottish')'''
"""https://pypi.org/project/pyttsx3/"""
"""https://www.codementor.io/edwardzionsaji/simple-voice-enabled-chat-bot-in-python-kt2qi5oke"""
# change TTS engine and voice, language(if needed)

hlo = ['hello', 'hi', 'hey']
hru = ['how are you', 'how are you doing', 'how do you do']   # messages
ext = ['bye', 'exit', 'go away', 'quit', 'get out'] 
songs=['humsafar','main_yaha','majnu','morrakka','perfect','rozana','shape_of_you','taki','unity']
r_nam={000:'test_name', 101:'avl', 102:'avl', 103:'avl'} 
# name of person in room             # refresh every time from file
# a = available, f = full, avl=available
# store customer names with room number
# print( rooms['101']=='a')	# stores rooms in a file


my_reply="reply_error"


def outp(text2):
	my_reply= text2
	print("Bot : "+text2)
	# engine.say(text2)                      # giving output
	# engine.runAndWait()
	# tts = gTTS(text2)
	# tts.save('/home/praneeth/Desktop/Others/temp/msg.mp3')
	# os.system('mpg321 /home/praneeth/Desktop/Others/temp/msg.mp3')


"""
def lis():            # to listen to voice and return string-mes
	from pocketsphinx import LiveSpeech
	print('listening',end='')
	for phrase in LiveSpeech():
		return(phrase)"""


def call_human(text):
	import pyautogui
	pyautogui.click(93, 1064)
	time.sleep(3)
	pyautogui.hotkey('ctrl', 't')
	pyautogui.typewrite('https://www.messenger.com/t/vh.praneeth')
	pyautogui.press('enter')
	outp("Calling human.")
	time.sleep(10)
	pyautogui.click(850, 1002)
	pyautogui.typewrite(text)
	pyautogui.press('enter')
	pyautogui.hotkey('ctrl', 'w')


def get_wthr():
	try:
		url = "http://api.openweathermap.org/data/2.5/weather?appid=0c42f7f6b53b244c78a418f4f181282a&q=vijayawada"
		json_data = requests.get(url).json()           # get weather
		formatted_data = json_data['weather'][0]['main']
		tmp = int(json_data["main"]["temp"] - 273.15)
		return "Temperature is " + str(tmp) + " C. It is " + formatted_data.lower() + "y."
	except:
		return "Sorry. No internet connection."


def avail_rooms():
        avr=[]
        for room in r_nam:
                if r_nam[room]=='avl':
                        avr.append(room)
        return str(avr)


def wish():
	hr = datetime.datetime.now().hour
	mrng='morning'
	if hr>=12 and hr<=15:
		mrng='afternoon'    # wish good morning/afternoon/evening
	elif hr>=16:
		mrng='evening'
	return ("Good "+mrng+". How can I help you?")


def tim_now():
	time_fmt = "%I:%M %p"
	return time.strftime(time_fmt)


def dat_now():
	time_fmt = "%A, %b %d, %Y"
	return time.strftime(time_fmt)


def book_room():
	outp("That seems good. Which type of room do you want? \n 1. Non-AC room. \n 2. AC room. \n 3. Deluxe room.")
	rm_input1=input('Room type : ')
	rm_input=rm_input1.lower()
	if 'non' in rm_input or 'na' in rm_input:
		rm_type='na'
	elif 'ac' in rm_input or 'ac' in rm_input:
		rm_type='ac'
	elif 'del' in rm_input:
		rm_type='de'
	outp("How many people are you?")
	mem=int(input('Members : '))
	outp(rm_input1+" room is registered with "+str(mem)+" people.")
	outp("Please tell the type of room required.")
	option4=("Family room (max. 4 persons).")
	option2=("Double bedded room(max. 2 persons)")
	option1=("Single bedded room(max. 1 person)")
	options=""
	if mem==1:
		options+="\n "+option1
	if mem<=2:
		options+="\n "+option2
	if mem<=4:
		options+="\n "+option4
	outp(options)
	rm_cp=1
	rate=1000
	rm_cap=input('Type : ')
	if "sin" in rm_cap or "one" in rm_cap or "1" in rm_cap:
		rm_cp=1
	elif "dou" in rm_cap or "two" in rm_cap or "2" in rm_cap:
		rm_cp=2
	elif "fam" in rm_cap or "4" in rm_cap or "four" in rm_cap:
		rm_cp=4
	if rm_cp==1:
		if rm_type=='na':
			rate=1000
		elif rm_type=='ac':
			rate=1500
		elif rm_type=='del':
			rate=1900
	elif rm_cp==2:
		if rm_type=='na':
			rate=1700
		elif rm_type=='ac':
			rate=2200
		elif rm_type=='del':
			rate=2800
	elif rm_cp==4:
		if rm_type=='na':
			rate=2500
		elif rm_type=='ac':
			rate=3200
		elif rm_type=='del':
			rate=4000
	outp("How many "+rm_cap+" rooms do you want?")
	nr=int(input('Rooms : '))
	ratef=rate*nr
	outp("How many days do you want to be in that room?")
	days=int(input('Days : '))
	tot=ratef*days
	#outp("Your cost per day will be Rs."+rate+"/-.")
	outp("Please tell names of "+str(mem)+" people.")
	names=[]
	i=1
	while i<=mem:
		names.append(input(str(i)+'. '))
		i+=1
	outp("Please tell your contact number.")
	ph_no=int(input('Contact : '))
	i=0
	while True:
		if len(str(ph_no))==10:
			break
		outp("Invalid phone number. Please tell again.")
		ph_no=input('Contact : ')
		i+=1
		if i==3:
			outp("Phone number invalid.")
			call_human("Phone number invalid.")
			break
	outp("Phone number is "+str(ph_no)+".")
	outp("Please tell your Aadhar number.")
	adh=str(input('Aadhar : '))
	i=0
	while True:
		if len(str(adh))==16:
			break
		outp("Invalid Aadhar number. Please tell again.")
		adh=str(input('Aadhar : '))
		i+=1
		if i==3:
			outp("Aadhar number invalid.")
			call_human("Aadhar number invalid.")
			break
	outp("These are the details that you have registered.")
	outp("Names : ")
	for name in names:
		outp(name)
	outp("Room type : "+rm_input1)
	outp("Phone number : "+str(ph_no))
	outp("Aadhar ID : "+adh)
	outp("Number of people : "+ str(mem) )
	outp("Total amount to be paid : "+str(tot))
	outp("The amount can be given to the cash reciever.")
	time.sleep(10)
	outp("Cash is recieved.")
	outp("Thank you for booking.")
	rnum=random.choice(rooms)
	outp("The room number is : "+str(rnum))
	name=names[0]
	u_file = "/home/praneeth/Desktop/Others/temp/guest/" + name + ".txt"
	cmd = "touch " + u_file
	os.system(cmd)
	x = datetime.datetime.now()
	add_dta = open(u_file, 'a')
	add_dta.write("in "+'str(num)'+" " +"\nRoom type : "+rm_input1+"\nPhone number : "+str(ph_no)+"\nAadhar ID : "+adh+"\nNumber of people : "+"\nNames : "+str(names)+ str(mem)+"\nTotal amount to be paid : "+str(tot)  )
	add_dta.close()
	r_nam[rnum]=names[0]
	call_human('booking '+str(rnum))


def check_out():
	outp("Please tell your room number.")
	num = input('Room : ')
	#outp("Please tell your name.")
	name = room_nam[num]
	u_file = "/home/praneeth/Desktop/Others/temp/guest/" + name + ".txt"
	file = open(u_file, 'r')
	#st = file.readline()                   # for leaving the room
	file.close()     # add feature- remove user file after check out
	# calculate bill during check out
	outp("Check out completed for room "+str(num)+".")
	outp("Thank you. Visit again.")
	r_nam[num]='avl'
	# send_human("check-out "+num)


def trans(msg):
	translator = Translator()
	ar=msg.split(' ')             # translate message and return output
	translations = translator.translate( ar[1], dest=ar[3][0:2].lower() )
	return ("The word "+ar[1]+" translated to "+ar[3]+" is "+translations.text)


# Responses
def resp(msg):                      # for correct responses
	if msg in hlo:
		outp(wish())
	elif msg in hru:
		outp("I am fine. Thank you. What about you?")
	elif msg == "fine" or msg == "good" or msg == "well" or msg  == 'no':
		outp("Okay.")
	elif "kill" in msg:
		outp("I don't want to kill anything, humans or animals.")
	elif 'room' in msg and 'book' in msg:           #Booking
		book_room()
	elif ('avail' in msg or 'free' in msg) and 'room' in msg:
		outp(avail_rooms())
	elif msg == "check-out" or msg == "check out" or msg == "Leave room":
		check_out()                                  #Leaving
	elif "emergency" in msg or 'police' in msg or 'ambulance' in msg:
		call_human('emergency')
	elif 'call' in msg or 'human' in msg or 'help' in msg:
		call_human('help')
	elif 'food' in msg:
		outp("Please tell your room number")
		r_numb=input('Room : ')
		outp('Which food do you want?')
		fd=input('Food : ')
		outp('Sending '+fd)
		call_human('Food : '+fd+' Room : '+r_numb)
	elif 'taxi' in msg:
		outp("Travel charges for taxi are 10 rupees per km or 9 rupees per hour, whichever is higher.")
		outp("Which place do you want to travel to?")
		place=input('Place : ')
		outp("Please enter your room number.")
		rr_num=input('Room : ')
		outp("Booking taxi to "+place)
		call_human('Taxi : '+place+' for room : '+rr_num)
	elif 'sleep' in msg:
		outp("Sleeping for 10 seconds...")
		time.sleep(10)
		outp('Done.')
	elif msg in ext:
		outp("Bye. See you soon.")
	elif 'thank' in msg or 'thanks' in msg:
		outp("You are welcome.")
	elif "weather" in msg or 'temperature' in msg or 'rain' in msg or 'climate' in msg:
		outp(get_wthr())
	elif "joke" in msg:
		outp("What is the biggest lie in the entire universe? I have read and agree to the Terms & Conditions.")
	elif msg == 'lol' or msg == 'haha':
		outp('I am glad that you found it funny.')
	elif 'time' in msg:
		outp(tim_now())
	elif 'date' in msg:
		date = dat_now()
		outp(date)
	elif "book" in msg:
		outp('Please tell me what you want to book. Is it room or taxi or other?')
	elif msg == "" or msg == ' ':
		outp("Please enter a message.")
	elif msg == "shutdown":
		outp("Shutting down...")
		os.system('shutdown now')
	elif msg == "restart" or msg == "reboot":
		outp("Restarting...")
		os.system('shutdown --reboot now')
	elif msg == "new terminal":
		outp("Opening new terminal window.")
		os.system('gnome-terminal & disown')
	elif msg == "info" or msg == "hotel info" or msg == "hotel information":
		file = open("/home/praneeth/Desktop/Others/temp/info.txt", 'r')
		outp(file.read())
		file.close()
	elif "music" in msg:
		fil_nam=random.choice(songs)
		outp("Playing music...")
		playsound.playsound('/home/praneeth/Desktop/Others/temp/songs/'+fil_nam+'.mp3', True)
	elif 'translate' in msg:
		outp(trans(msg))
	elif 'ok' in msg or 'okay' in msg:
		outp("Okay then.")
	elif msg == "what can you do":
		file = open("/home/praneeth/Desktop/Others/temp/what_can_do.txt", 'r')
		outp(file.read())                        # What can you do
		file.close()
	elif 'password' in msg or 'wifi' in msg or 'wi-fi' in msg:
		outp("Wi-Fi password is hotel123. I repeat hotel123.")
	elif 'problem' in msg:
		outp('Please enter the problem.')
		prob=str(input('Problem : '))
		call_human('Problem : '+prob)
		add_data = open("/home/praneeth/Desktop/Others/temp/feedback.txt", 'a')
		add_data.write("\n"+txt)          # Feedback
		add_data.close()
	elif msg=='q':
		return
	elif 'feedback' in msg:
		outp("Please give feedback now.")
		txt = input('Feedback : ')
		add_data = open("/home/praneeth/Desktop/Others/temp/feedback.txt", 'a')
		add_data.write("\n"+txt)          # Feedback
		add_data.close()
		outp("Thank you for your valuable feedback.")
	else:
		outp("Sorry. Please repeat.")
		add_data = open("/home/praneeth/Desktop/Others/temp/newdata.txt", 'a')
		add_data.write("\n")
		add_data.write(msg)
		add_data.close()

	'''elif 'calc' in msg:
		outp('Please enter the calculation.')
		cal=input('Calculation : ')
		if '+' in cal:
			op='+'
		if '-' in cal:
			op='-'
		if '*' in cal:
			op='*'
		if '/' in cal:
			op='/'
		prev=''
		for ch in cal:
			if ch != '+' or '-' or
			prev=prev+ch'''


# chat program starts here

print("-----------------------------------------")   
# outp(wish())
                                 # Uncomment 2 lines before release
# playsound.playsound('/home/praneeth/Desktop/Others/temp/short.mp3', True)
# outp("Welcome to our hotel. How may I help you?")"""
'''
while True:
	mesg = input("You : ").lower()
	#print('You : ',end="")
	#mesg = lis()
	if mesg == "q":
		break
	resp(mesg)'''

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
output = tk.Label(root, text='started')
output.pack()

#tk.mainloop()




