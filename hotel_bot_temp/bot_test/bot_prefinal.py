import datetime

import random
import os
import time
from pygame import mixer # voice output
from gtts import gTTS    # Google TTS

"""
# https://pypi.org/project/pyttsx3/
# https://www.codementor.io/edwardzionsaji/simple-voice-enabled-chat-bot-in-python-kt2qi5oke
# change TTS engine and voice, language(if needed)
"""

hlo = ['hello', 'hi', 'hey']
hru = ['how are you', 'how are you doing', 'how do you do']   # messages
ext = ['bye', 'exit', 'go away', 'quit', 'get out'] 

r_nam={101:'avl', 102:'avl', 103:'avl'} # room number to name
avr=[101,102,103]      #available rooms

# name of person in room             # refresh every time from file
# a = available, f = full, avl=available
# store customer names with room number

vo_work=False
try:
	mixer.init()
except:
	print('-----Voice error')
else:
	vo_work=True


from sys import path; my_pa=path[0];
my_path=my_pa+"/temp"
my_songs=os.listdir(my_path+"/songs/")

# reloading room and name list from file
file = open(my_path+"/avail_rooms.txt", 'r')
avr=[]
temp=file.readline()
temp1=temp.split(' ')
for rnu in temp1:
        avr.append(int(rnu))
file.close()
#
file = open(my_path+"/rooms_names.txt", 'r')
r_nam={}
while True:
        temp=file.readline()
        if temp=='':
                break
        temp1=temp.split(' ')
        temp_num=int(temp1[0])
        temp_name=temp1[1]
        if temp_name=='avl\n':
                temp_name='avl'
        r_nam[temp_num]=temp_name
file.close()


def rewrite():
        av_r=""
        for rn in avr:
                av_r +=str(rn)+' '
        file = open(my_path+"/avail_rooms.txt", 'w')
        file.write(av_r)
        file.close()
        # r_nam
        my_temp=""
        for elem in r_nam:
                my_temp+=str(elem)+' '+r_nam[elem]+'\n'
        file = open(my_path+"/rooms_names.txt", 'w')
        file.write(my_temp)
        file.close()
        

def outp(text):	
	print("Bot :",text)
	if vo_work:
		tts = gTTS(text)
		tts.save(my_path+'/msg.mp3')
		mixer.music.load(my_path+'/msg.mp3')
		mixer.music.play()


def lis():
	import speech_recognition as spreg
	#Setup the sampling rate and the data size
	sample_rate = 48000
	data_size = 8192
	recog = spreg.Recognizer()
	text="err"
	with spreg.Microphone(sample_rate = sample_rate, chunk_size = data_size) as source:
	   recog.adjust_for_ambient_noise(source)
	   speech = recog.listen(source)
	   try:
	      text = recog.recognize_google(speech)
	      print('You : ' + text)
	   except :
	      text=input('You : ')
	return text


def inp(txt):
	msg=lis()
	if msg=="err":
		msg=input(txt+" : ")
	return msg


def call_human(text):
	import pyautogui
	#pyautogui.click(69, 19) # click on browser
	#time.sleep(13)
	#pyautogui.hotkey('ctrl', 't')
	import webbrowser
	webbrowser.open('https://www.messenger.com/t/vh.praneeth')
	time.sleep(13)
	#pyautogui.typewrite('https://www.messenger.com/t/vh.praneeth')
	#pyautogui.press('enter')
	outp("Calling human."); time.sleep(3)
	#time.sleep(20)
	#pyautogui.click(263, 357)
	pyautogui.typewrite(text)
	pyautogui.press('enter')
	time.sleep(2)
	#pyautogui.hotkey('ctrl', 'w')
	pyautogui.hotkey('ctrl', 'w')


def taxi_book():
        outp("That will be no problem.Can you please tell me your room number?")
        num = inp('Room')
        outp('For your information the taxi will be provided by the hotel at reasonable rates.')
        time.sleep(3)
        outp("So For how many members you woud like to book the taxi ")
        n_o_p=int(inp('Members'))
        outp('At what time would you like to book the taxi for today')
        time.sleep(3)
        outp("Please give the input in 24 HOUR format ")
        time_h=int(inp('Hours'))
        time_m=int(inp('Minutes'))
        outp('Your Taxi is booked at :- '+str(time_h)+':'+str(time_m))
        time.sleep(3)
        outp('A message will be sent to you 15 minutes prior to notify that the taxi is ready')
        time.sleep(3)
        outp('Would you like me to book the taxi for your return')
        y_n=inp('Yes/No')
        if y_n=='yes' or y_n=='okay':
            outp('Well Great!The taxi is also booked for the Return.')
        elif y_n=='no':
            outp('No problem. ')
        time.sleep(3)
        outp('Your Taxi is booked and the details will be sent to your mobile number')
        time.sleep(3)
        '''add_data = open(my_path+"/newdata.txt", 'a')
        add_data.write("\n")
        add_data.write(msg)
        add_data.close()'''
        outp('Thank You.Have a great Ride')


def get_wthr():
	try:
		url = "http://api.openweathermap.org/data/2.5/weather?appid=0c42f7f6b53b244c78a418f4f181282a&q=vijayawada"
		json_data = requests.get(url).json()           # get weather
		formatted_data = json_data['weather'][0]['main']
		tmp = int(json_data["main"]["temp"] - 273.15)
		my_str=formatted_data.lower()
		if 'clou' in my_str:
			my_str='cloudy'
		elif 'mist' in my_str:
			my_str='misty'
		elif 'sun' in my_str:
			my_str='sunny'
		elif 'rain' in my_str:
			my_str='raining'
		elif 'haz' in my_str:
			my_str='hazy'
		elif 'clea' in my_str:
			my_str='clear'
		else:
			my_str=my_str+'y'
		return "Temperature is " + str(tmp) + " C. It is " + my_str + "."
	except:
		return "Sorry. No internet connection."


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
	rm_inp1=inp('Room type')
	rm_inp=rm_inp1.lower()
	if 'non' in rm_inp or 'na' in rm_inp:
		rm_type='na'
	elif 'ac' in rm_inp or 'ac' in rm_inp:
		rm_type='ac'
	elif 'del' in rm_inp:
		rm_type='de'
	outp("How many people are you?")
	mem=int(inp('Members'))
	outp(rm_inp1+" room is registered with "+str(mem)+" people.")
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
	rm_cap=inp('Type')
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
	nr=int(inp('Rooms'))
	ratef=rate*nr
	outp("How many days do you want to be in that room?")
	days=int(inp('Days'))
	tot=ratef*days
	#outp("Your cost per day will be Rs."+rate+"/-.")
	outp("Please tell names of "+str(mem)+" people.")
	names=[]
	for i in range(mem):
		names.append(inp(str(i+1)))
	outp("Please tell your contact number.")
	ph_no=int(inp('Contact'))
	i=0
	while True:
		if len(str(ph_no))==10:
			break
		outp("Invalid phone number. Please tell again.")
		ph_no=inp('Contact')
		i+=1
		if i==3:
			outp("Phone number invalid.")
			call_human("Phone number invalid.")
			break
	outp("Phone number is "+str(ph_no)+".")
	outp("Please tell your Aadhar number.")
	adh=str(inp('Aadhar'))
	i=0
	while True:
		if len(str(adh))==12:
			break
		outp("Invalid Aadhar number. Please tell again.")
		adh=str(inp('Aadhar'))
		i+=1
		if i==3:
			outp("Aadhar number invalid.")
			call_human("Aadhar number invalid.")
			break
	outp("These are the details that you have registered.")
	outp("Names : ")
	for name in names:
		outp(name)
	outp("Room type : "+rm_inp1)
	outp("Phone number : "+str(ph_no))
	outp("Aadhar ID : "+adh)
	outp("Number of people : "+ str(mem) )
	outp("Total amount to be paid : "+str(tot))
	outp("The amount can be given to the cash reciever.")
	time.sleep(10)
	outp("Cash is recieved.")
	outp("Thank you for booking.")
	rnum=random.choice(avr)
	outp("The room number is "+str(rnum))
	name=names[0]
	u_file = my_path+"/guest/" + name + ".txt"
	cmd = "touch " + u_file
	os.system(cmd)
	x = datetime.datetime.now()
	add_dta = open(u_file, 'a')
	add_dta.write("in : "+str(rnum)+" " +"\nRoom type : "+rm_inp1+"\nPhone  : "+str(ph_no)+"\nAadhar ID : "+adh+"\nNumber of people : "+"\nNames : "+str(names)+ str(mem)+"\nTotal amount to be paid : "+str(tot)  )
	add_dta.close()
	r_nam[rnum]=names[0]
	avr.remove(rnum)
	call_human('Booking : '+str(rnum))
	rewrite()


def check_out():
	outp("Please tell your room number.")
	num = inp('Room')
	#outp("Please tell your name.")
	name = room_nam[num]
	u_file = my_path+"/guest/" + name + ".txt"
	file = open(u_file, 'r')
	#st = file.readline()                   # for leaving the room
	file.close()     # add feature- remove user file after check out
	# calculate bill during check out
	outp("Check out completed for room "+str(num)+".")
	outp("Thank you. Visit again.")
	r_nam[num]='avl'
	avr.append(num)
	os.system('rm '+u_file)
	call_human("check-out"+num)
	rewrite()


def tourist_places():
        outp("These are the famous tourist places in Vijayawada.About which place do you want to know? \n 1. Sri Durga Malleswara Swamy Varla Davasthanam \n 2. Prakasham Barrage \n 3. Undavali Caves \n 4. Bhavani Island \n 5. Paritala Anjaneya Swami temple \n 6. Amaravati Museum \n 7. Gunadala Matha Shrine \n 8. Gandhi Hill \n 9. Lenin Statue \n 10. Mogalarajapuram Caves ")
        outp("Packages are available for trip. \n 11. Package A contains 1,2,4,9,10. Package A price-Rs 1800 per person (inclusive of the entry tickets for the places in Package A) \n 12. Package B contains 3,5,6,7,8. Package B price-Rs 2200 per person (inclusive of the entry tickets for the places in Package B) \n  You can select your package by choosing the respective no.s (for package A-11,for package B-12) for packages")
        print('------')
        tp_inp1=inp('Enter an option')
        if tp_inp1=='1':
            outp('It is known as Kanaka Durga Temple. It is one of famous temple of Goddess Durga located on the banks of Krishna River.')
        elif tp_inp1=='2':
            outp('It is a 1223.5 m barrage connecting Krishna River and Guntur District. It has 76 pillars in total.')
        elif tp_inp1=='3':
            outp('These caves are found in 7th century. It is formed of a single large block of stone and one of finest Indian rock-cut architecture.')
        elif '4' in tp_inp1:    
            outp('It is one of the largest river island in India with an area of 133 acres.It is situated in middle of Krishna River.')
        elif '5' in tp_inp1:
            outp('It is a temple residing the worlds tallest lord Hanuman Statue. It is 41 metres tall.')
        elif '6' in tp_inp1:
            outp('It is a treasure house of historical information,more about Buddha. It also has a giant magnificent Buddha Statue.')
        elif '7' in tp_inp1:
            outp('It is a holy church for christians with a divine atmosphere and brings spiritual consciousness in people.')
        elif '8' in tp_inp1:
            outp('It has a spot to take a whole view of Vijayawada.Morever this place relaxes and leave everyone in the historical thoughts.')
        elif '9' in tp_inp1:
            outp('It is symbol for communism and its ideologies. Though it is built in 1990 until now it is one of the main trading centre in Vijayawada.')
        elif '10' in tp_inp1:
            outp('The cave has a unique look with fine sculptures. Morever, you can find time to relax in greenery and resturants.')
        elif '11' in tp_inp1:
            outp(' These are the timings for Package A \n A. 8:00 AM-10:00 AM-Sri Durga Malleswara Swamy Varla Davasthanam \n B. 10:00 AM-12:30 PM-Bhavani Island \n C. 12:30 PM-2:00 PM-Lunch Break \n D. 2:00 PM-4:00 PM-Lenin Statue \n E. 4:30 PM-6:00 PM-Mogalarajapuram Caves \n F. 6:00 PM-8:00 PM-Prakasham Barrage')
        elif '12' in tp_inp1:
            outp(' These are the timings for Package B \n A. 8:00 AM-10:00 AM - Amaravati Museum \n B. 10:00 AM-12:30 PM - Undavali Caves \n C. 12:30 PM-2:00 PM - Lunch Break \n D. 2:00 PM-4:00 PM - Paritala Anjaneya Swami temple \n E. 4:30 PM-6:00 PM - Gandhi Hill \n F. 6:00 PM-8:00 PM - Gunadala Matha Shrine')
        else:
            outp('Invalid option')
        print('------')
        outp('Do you want to book any Package?')
        rep=inp('Yes/No')
        if 'y' in rep:
            outp('Which Package do you want to book?')
            pkg_inp=inp('Package ')
            outp("For how many people you want to book travel to tourist places?")
            tp_inp=inp('No. of persons')
            if 'A' or 'a' in pkg_inp:
                outp('A. 8:00 AM-10:00 AM-Sri Durga Malleswara Swamy Varla Davasthanam \n B. 10:00 AM-12:30 PM-Bhavani Island \n C. 12:30 PM-2:00 PM-Lunch Break \n D. 2:00 PM-4:00 PM-Lenin Statue \n E. 4:30 PM-6:00 PM-Mogalarajapuram Caves \n F. 6:00 PM-8:00 PM-Prakasham Barrage \n Package A is selected for you.')
                price=1800*int(tp_inp)
                outp('Your Package cost is '+str(price))
            elif 'B' or 'b' in pkg_inp:
                outp('A. 8:00 AM-10:00 AM - Amaravati Museum \n B. 10:00 AM-12:30 PM - Undavali Caves \n C. 12:30 PM-2:00 PM - Lunch Break \n D. 2:00 PM-4:00 PM - Paritala Anjaneya Swami temple \n E. 4:30 PM-6:00 PM - Gandhi Hill \n F. 6:00 PM-8:00 PM - Gunadala Matha Shrine \n Package B is selected for you.')
                price=2200*int(tp_inp)
                outp('Your Package cost is '+str(price))
        outp('Do you want to repeat the process?')
        rep=inp('Yes/No')
        if 'y' in rep:
            tourist_places()


def trans():
	from googletrans import Translator
	outp("Which language do you want to translate to?")
	lan=inp("Language")
	la=lan[0:2].lower()	
	outp("Enter the text.")
	txt=inp("Text")
	outp("The translated sentence is "+translator.translate(txt, dest=la))
	outp("Do you want to repeat the process?")
	rep=inp("Yes/No")
	if 'y' in rep or 'Y' in inp:
		trans()
	else:
		outp("Okay.")


# Responses
def resp(msg):           # for correct responses
	if msg in hlo:
		outp(wish())
	elif msg in hru:
		outp("I am fine. Thank you. What about you?")
	elif msg == "fine" or msg == "good" or msg == "well" or msg  == 'no':
		outp("Okay.")
	elif "kill" in msg:
		outp("I don't want to kill anything, humans or animals.")
	elif 'room' in msg and ('book' in msg or 'register' in msg):           #Booking
		book_room()
	elif ('avail' in msg or 'free' in msg) and 'room' in msg:
		num=len(avr)
		if num==0:
			num="Sorry. No"
		st=str(num)+" rooms are available."
		outp(st)
	elif msg == "check-out" or msg == "check out" or msg == "Leave room":
		check_out()                                  #Leaving
	elif "emergency" in msg or 'police' in msg or 'ambulance' in msg:
		call_human('emergency')
	elif 'call' in msg or 'human' in msg or 'help' in msg:
		outp('Please enter your room number.')
		rr_no=inp('Room')
		call_human(' '+rr_no)
	elif 'food' in msg:
		outp('Please tell your room number.')
		r_numb=inp('Room')
		outp('Which food do you want and how many?')
		fd=inp('Food')
		outp('Sending '+fd)
		call_human('Food'+fd+' to room'+r_numb)
	elif 'taxi' in msg and 'book' in msg or 'organi' in msg or 'cab' in msg:
		taxi_book()
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
	elif 'tour' in msg or 'place' in msg or 'travel' in msg:
		tourist_places()
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
	elif msg == "info" or msg == "hotel info" or msg == "hotel information":
		file = open(my_path+"/info.txt", 'r')
		outp(file.read())
		file.close()
	elif "music" in msg or 'song' in msg:
		fil_nam=random.choice(my_songs)
		if vo_work:
			outp("Playing music...")
			mixer.music.load(my_path+'/songs/'+fil_nam)
			mixer.music.play()
		else:
			print('Error playing music.')
	elif 'translate' in msg:
		trans()
	elif 'ok' in msg or 'okay' in msg:
		outp("Okay then.")
	elif msg == "what can you do":
		file = open(my_path+"/what_can_do.txt", 'r')
		outp(file.read())                        # What can you do
		file.close()
	elif 'password' in msg or 'wifi' in msg or 'wi-fi' in msg:
		outp("Wi-Fi password is hotel123. I repeat hotel123.")
	elif 'stop' in msg:
		if vo_work:
			mixer.music.stop()
		else:
			print('Unable to stop.')
	elif 'problem' in msg:
		outp('Please enter the problem.')
		prob=str(inp('Problem'))
		call_human('Problem'+prob)
		add_data = open(my_path+"/feedback.txt", 'a')
		add_data.write("\n"+txt)          # Feedback
		add_data.close()
	elif 'clean' in msg:
		outp('Do you want us to clean the room?')
		ab=inp('Yes/No')
		if 'y' in ab:
			outp('Please enter room number.')
			rnu=inp('Room')
			call_human('Clean room'+rnu)
		elif 'n' in ab:
			outp('It is okay.')
	elif 'feedback' in msg:
		outp("Please give feedback now.")
		txt = inp('Feedback')
		add_data = open(my_path+"/feedback.txt", 'a')
		add_data.write("\n"+txt)    # Feedback
		add_data.close()
		outp("Thank you for your valuable feedback.")
	elif 'extra' in msg:
		outp('Please enter what you need extra')
		need=inp('Extra')
		outp('Please enter your room number.')
		rnu=inp('Room')
		outp('Sending Extra'+need+' to Room'+str(rnu) )
		call_human('Extra'+need+' Room'+str(rnu) )
	elif msg=="err":
		outp("I can't hear that.")
	else:
		outp("Sorry. Please repeat.")
		add_data = open(my_path+"/newdata.txt", 'a')
		add_data.write("\n")
		add_data.write(msg)
		add_data.close()


# chat program starts here

print("-----------------------------------------")

if vo_work:
	mixer.music.load(my_path+'/short.mp3')
	mixer.music.play()

while True:
	mesg = inp("You").lower()
	# mesg = lis() # for voice inp
	if mesg == "q" or mesg=="close" or mesg=="quit" or mesg=='exit':
		break
	resp(mesg)

######### End of program  #######



# More info:
"""
# measure time
import datetime
start=datetime.datetime.now()
def pr_now():
	print(datetime.datetime.now()-start)

i=0
while i<4:
	i+=1
	pr_now()
	

# useful to calculate time taken
"""
#

"""
compiling to .pyc file

import py_compile
py_compile.compile("~/Desktop/bt.py")

or

import compileall
compileall.compile_file('~/Desktop/bt.py')
"""


