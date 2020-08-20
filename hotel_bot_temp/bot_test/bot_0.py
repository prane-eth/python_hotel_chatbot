import datetime
import requests
import random
import os
from time import sleep
import time
from pygame import mixer
from gtts import gTTS    # Google TTS
import pyautogui as pgui
from sys import path

my_pa = path[0]
tempf = my_pa+"/temp"

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
with open(tempf+"/available_rooms.txt", 'r') as file:
        temp = file.readline()
available_rooms = temp.split(' ')
#
file = open(tempf+"/rooms_names.txt", 'r')
rooms_names = {}
while True:
        temp = file.readline()
        if temp == '':
                break
        temp = temp.split(' ')
        temp_num = temp[0]
        temp_name = temp[1][0:-1]
        rooms_names[temp_num] = temp_name
file.close()


def rewrite():
        av_r=""
        for rn in available_rooms:
                av_r +=str(rn)+' '
        file = open(tempf+"/available_rooms.txt", 'w')
        file.write(av_r)
        file.close()
        # r_nam
        temp1=""
        for elem in rooms_names:
                temp1+=str(elem)+' '+rooms_names[elem]+'\n'
        file = open(tempf+"/rooms_names.txt", 'w')
        file.write(temp1)
        file.close()
        

def outp(text):        
        print("Bot :", text)
        if vo_work:
                tts = gTTS(text)
                tts.save(tempf+'/msg.mp3')
                mixer.music.load(tempf+'/msg.mp3')
                mixer.music.play()


def lis(txt):
        import speech_recognition as spreg
        # Setup the sampling rate and the data size
        sample_rate = 48000
        data_size = 8192
        recog = spreg.Recognizer()
        text = "err"
        with spreg.Microphone(sample_rate=sample_rate, chunk_size=data_size) as source:
            recog.adjust_for_ambient_noise(source)
            speech = recog.listen(source)
            try:
                text = recog.recognize_google(speech)
                print(txt+' : ' + text)
            except:
                text = input(txt+' : ')
            return text


def inp(txt):
        try:
                msg = lis(txt)
        except:
                msg = "err"
        if msg == "err":
                msg = input(txt+" : ")
        return msg


def call_human(text):
    import smtplib, ssl
    sender_email = ""
    password = ""
    context = ssl.create_default_context()
    outp("Calling human")
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(sender_email, password)
        server.sendmail(sender_email, sender_email, text)


def send_human(txt):
        call_human(txt)


def send_sms(ph_numb, msg_text):
        import way2sms
        q=way2sms.Sms('6302523157', 'C2484R')
        # q=way2sms.Sms('6301310434', 'K5928Q')
        # q=way2sms.Sms('6370697891', 'C9882K')
        q.send(ph_numb, msg_text)
        q.logout()
        

def send_sms_later(ph_numb, msg_text, fdate, ftime):
        import way2sms
        q=way2sms.Sms('6302523157', 'C2484R')
        # q=way2sms.Sms('6301310434', 'K5928Q')
        # q=way2sms.Sms('6370697891', 'C9882K')
        q.send_later(ph_numb, msg_text, fdate, ftime)
        q.logout()


def verified_number():
        outp("Phone number will be verified with OTP.")
        ph_num = inp("Phone")
        outp("You entered "+ph_num+". Is it correct?")
        corr = inp("Yes/No")
        if 'n' in corr:
                outp("Please enter a correct number.")
                ph_num = inp("Phone")
        outp("Please wait while we are sending OTP to your number.")
        otp = ""
        for tem_num in range(4):
                otp += str(random.randint(0, 10))
        otp_text = "Dear Customer, \n   Thank you for booking a room in our hotel. \n   Your OTP is given below \n"+otp
        send_sms(ph_num, otp_text)
        outp("Please enter your OTP. Please enter 'no' if you did not recieve it.")
        t_otp = inp("OTP")
        if 'n' in t_otp:
                outp("Sending OTP again")
                send_sms(ph_num, otp_text)
                t_otp = inp("OTP")
        if t_otp == otp:
                return ph_num
        elif t_otp != otp:
                outp("Incorrect OTP. Please enter again.")
                t_otp = inp("OTP")
                if t_otp == otp:
                        return str(ph_num)
                else:
                        return '0'
        else:
                return '0'


def taxi_book():
        outp("That will be no problem. Can you please tell me your room number?")
        num = inp('Room')
        outp('For your information the taxi will be provided by the hotel at reasonable rates.')
        sleep(3)
        outp("So For how many members you would like to book the taxi ")
        n_o_p = int(inp('Members'))
        outp('At what time would you like to book the taxi for today')
        sleep(3)
        outp("Please give the input in 24 HOUR format ")
        time_h = inp('Hours')
        time_m = inp('Minutes')
        outp('Your Taxi is booked at :- '+str(time_h)+':'+str(time_m))
        sleep(3)
        outp('A message will be sent to you 15 minutes prior to notify that the taxi is ready')
        sleep(3)
        outp('Would you like me to book the taxi for your return')
        y_n = inp('Yes/No')
        if y_n == 'yes' or y_n == 'okay':
            outp('Well Great!The taxi is also booked for the Return.')
        elif y_n == 'no':
            outp('No problem. ')
        sleep(3)
        outp('Your Taxi is booked and the details will be sent to your mobile number')
        sleep(3)
        '''add_data = open(tempf+"/guest/", 'a')
        add_data.write("\n")
        add_data.write(msg)
        add_data.close()'''
        #
        fhours=int(time_h)
        fmin=int(time_m)
        if fmin<15:
                fhours-=1
                fmin+=60
                fmin-=15
        else:
                fmin-=15
        #
        fhours=str(fhours)
        fmin=str(fmin)
        dat=time.strftime("%d/%m/%Y")
        tim=str(fhours)+":"+str(fmin)
        outp("Please enter your phone nunber.")
        ph_no = inp("Phone")
        sms_txt = "Dear Customer, \n Your taxi is booked. It will arrive in 15 minutes. \nThank you."
        send_sms_later(ph_no, sms_txt, dat, tim)
        outp('Thank You.Have a great Ride')


def get_wthr():
        try:
                url = "http://api.openweathermap.org/data/2.5/weather?appid=0c42f7f6b53b244c78a418f4f181282a&q="
                city = "vijayawada"
                url = url+city
                json_data = requests.get(url).json()           # get weather
                formatted_data = json_data['weather'][0]['main']
                tmp = int(json_data["main"]["temp"] - 273.15)
                my_str = formatted_data.lower()
                if 'clou' in my_str:
                        my_str = 'cloudy'
                elif 'mist' in my_str:
                        my_str = 'misty'
                elif 'sun' in my_str:
                        my_str = 'sunny'
                elif 'rain' in my_str:
                        my_str = 'raining'
                elif 'haz' in my_str:
                        my_str = 'hazy'
                elif 'clea' in my_str:
                        my_str = 'clear'
                else:
                        my_str = my_str+'y'
                return "Temperature is " + str(tmp) + " C. It is " + my_str + "."
        except:
                return "Sorry. No internet connection."


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
        outp("That seems good. Which type of room do you want? \n 1. Non-AC room. \n 2. AC room. \n 3. Deluxe room.")
        rm_inp1 = inp('Room type')
        rm_inp = rm_inp1.lower()
        if 'non' in rm_inp or 'na' in rm_inp:
                room_type = 'na'
        elif 'ac' in rm_inp or 'ac' in rm_inp:
                room_type = 'ac'
        elif 'del' in rm_inp:
                room_type = 'de'
        outp("How many people are you?")
        mem = int(inp('Members'))
        outp(rm_inp1+" room is registered with "+str(mem)+" people.")
        outp("Please tell the type of room required.")
        option4 = "Family room (max. 4 persons)."
        option2 = "Double bedded room(max. 2 persons)"
        option1 = "Single bedded room(max. 1 person)"
        options = ""
        if mem == 1:
                options += "\n "+option1
        if mem <= 2:
                options += "\n "+option2
        if mem <= 4:
                options += "\n "+option4
        outp(options)
        rm_cp = 1
        rate = 1000
        rm_cap = inp('Type')
        if "sin" in rm_cap or "one" in rm_cap or "1" in rm_cap:
                rm_cp = 1
        elif "dou" in rm_cap or "two" in rm_cap or "2" in rm_cap:
                rm_cp = 2
        elif "fam" in rm_cap or "4" in rm_cap or "four" in rm_cap:
                rm_cp = 4
        if rm_cp == 1:
                if room_type == 'na':
                        rate = 1000
                elif room_type == 'ac':
                        rate = 1500
                elif room_type == 'del':
                        rate = 1900
        elif rm_cp == 2:
                if room_type == 'na':
                        rate = 1700
                elif room_type == 'ac':
                        rate = 2200
                elif room_type == 'del':
                        rate = 2800
        elif rm_cp == 4:
                if room_type == 'na':
                        rate = 2500
                elif room_type == 'ac':
                        rate = 3200
                elif room_type == 'del':
                        rate = 4000
        outp("How many "+rm_cap+" rooms do you want?")
        nr = int(inp('Rooms'))
        rate_final = rate*nr
        outp("How many days do you want to be in that room?")
        days = int(inp('Days'))
        tot = rate_final*days
        # outp("Your cost per day will be Rs."+rate+"/-")
        outp("Please tell names of "+str(mem)+" people")
        names = []
        for i in range(mem):
                names.append(inp(str(i+1)))
        outp("Please tell your contact number")
        ph_no = verified_number()  # phone number
        if ph_no == '0':
                ph_no = verified_number()
        outp("Phone number is "+str(ph_no))
        outp("Please tell your Aadhar number")
        adh = str(inp('Aadhar'))
        '''i=0
        while True:
                if len(str(adh))==12:
                        break
                outp("Invalid Aadhar number. Please tell again")
                adh=str(inp('Aadhar'))
                i+=1
                if i==3:
                        outp("Aadhar number invalid.")
                        call_human("Aadhar number invalid")
                        break'''
        outp("These are the details that you have registered")
        outp("Names : ")
        for name in names:
                outp(name)
        outp("Room type : "+rm_inp1)
        outp("Phone number : "+str(ph_no))
        outp("Aadhar ID : "+adh)
        outp("Number of people : " + str(mem))
        outp("Total amount to be paid : "+str(tot))
        outp("The amount can be given to the cash receiver")
        sleep(10)
        outp("Cash is received")
        outp("Thank you for booking")
        room_number = random.choice(available_rooms)
        outp("The room number is "+room_number)
        name = names[0]
        u_file = tempf+"/guest/" + name + ".txt"
        cmd = "touch " + u_file
        os.system(cmd)
        add_dta = open(u_file, 'a')
        add_dta.write("in : "+room_number+" \nDate and time : "+time_now()+" "+date_now()+" \nRoom type : "+rm_inp1+" \nPhone  : "+str(ph_no)+" \nAadhar ID : "+adh+" \nNumber of people : "+"\nNames : "+str(names)+ str(mem)+"\nTotal amount to be paid : "+str(tot))
        add_dta.close()
        rooms_names[room_number] = names[0]
        available_rooms.remove(room_number)
        call_human('Booking : '+room_number)
        rewrite()
        outp("SMS will be sent to you with room details.")
        sms_txt = "Dear Customer, \nThank you for booking room. \nYour room number is : "+str(room_number)
        send_sms(ph_no, sms_txt)


def check_out():
        outp("Please tell your room number.")
        room_number = inp('Room')
        name = rooms_names[room_number]
        u_file = tempf+"/guest/" + name + ".txt"
        # calculate bill during check out
        outp("Check out completed for room "+room_number)
        outp("Thank you. Visit again.")
        rooms_names[room_number] = 'avl'
        available_rooms.append(room_number)
        os.system('mv '+u_file+' '+tempf+'/backup')
        call_human("check-out : "+room_number)
        rewrite()


def tourist_places():
        outp("These are the famous tourist places in Vijayawada.About which place do you want to know? \n 1. Sri Durga Malleswara Swamy Varla Davasthanam \n 2. Prakasham Barrage \n 3. Undavali Caves \n 4. Bhavani Island \n 5. Paritala Anjaneya Swami temple \n 6. Amaravati Museum \n 7. Gunadala Matha Shrine \n 8. Gandhi Hill \n 9. Lenin Statue \n 10. Mogalarajapuram Caves ")
        outp("Packages are available for trip. \n 11. Package A contains 1,2,4,9,10. Package A price-Rs 1800 per person (inclusive of the entry tickets for the places in Package A) \n 12. Package B contains 3,5,6,7,8. Package B price-Rs 2200 per person (inclusive of the entry tickets for the places in Package B) \n  You can select your package by choosing the respective no.s (for package A-11,for package B-12) for packages")
        print('------')
        tp_inp1 = inp('Enter an option')
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


def translate():
        from googletrans import Translator
        translator = Translator()
        outp("Which language do you want to translate to?")
        lan = inp("Language")
        la = lan[0:2].lower()
        outp("Enter the text.")
        txt = str(inp("Text"))
        outp("The translated sentence is "+translator.translate(txt, dest=la))
        outp("Do you want to repeat the process?")
        rep = inp("Yes/No")
        if 'y' in rep or 'Y' in inp:
                translate()
        else:
                outp("Okay.")


# Responses
def resp(msg):                      # for correct responses
        if 'hi' in msg or 'hello' in msg or 'hey' in msg or ('good' in msg and 'n' in msg) :
                outp(wish())
        elif 'how' in msg and 'you' in msg:
                outp("I am fine. Thank you. What about you?")
        elif msg == "fine" or msg == "good" or msg == "well" or msg == 'no':
                outp("Okay.")
        elif "kill" in msg or "destroy" in msg:
                outp("I don't want to kill.")
        elif 'room' in msg and ('book' in msg or 'register' in msg):  # Booking
                book_room()
        elif ('avail' in msg or 'free' in msg) and 'room' in msg:
                num = len(available_rooms)
                if num == 0:
                        num = "Sorry. No"
                outp(str(num)+" rooms are available.")
        elif msg == "check-out" or msg == "check out" or msg == "Leave room":
                check_out()                                  # Leaving
        elif "emergency" in msg or 'police' in msg or 'ambulance' in msg:
                outp("Calling human.")
                call_human('emergency')
        elif 'call' in msg or 'human' in msg or 'help' in msg:
                outp('Please enter your room number.')
                rr_no = inp('Room')
                call_human('Help '+rr_no)
        elif 'food' in msg:
                outp('Please tell your room number.')
                r_numb = inp('Room')
                outp('Which food do you want and how many?')
                fd = inp('Food')
                outp('Sending '+fd)
                call_human('Food'+fd+' to room'+r_numb)
        elif 'taxi' in msg and 'book' in msg or 'organi' in msg or 'cab' in msg:
                taxi_book()
        elif 'sleep' in msg:
                outp("Sleeping for 10 seconds...")
                sleep(10)
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
                outp(time_now())
        elif 'date' in msg:
                date = date_now()
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
                with open(tempf+"/info.txt", 'r') as file11:
                        outp(file11.read())
        elif "music" in msg or 'song' in msg:
                fil_nam = random.choice(os.listdir(tempf+"/songs/"))
                if vo_work:
                        outp("Playing music...")
                        mixer.music.load(tempf+'/songs/'+fil_nam)
                        mixer.music.play()
                else:
                        print('Error playing music.')
        elif 'translate' in msg:
                translate()
        elif 'ok' in msg or 'okay' in msg:
                outp("Okay then.")
        elif "what" in msg and "you" in msg:
                with open(tempf+"/what_can_do.txt", 'r') as file0:
                        outp(file0.read())
        elif 'password' in msg or 'wifi' in msg or 'wi-fi' in msg:
                outp("Wi-Fi password is hotel123. I repeat hotel123.")
        elif 'stop' in msg:
                if vo_work:
                        mixer.music.stop()
                else:
                        print('Unable to stop.')
        elif 'problem' in msg:
                outp('Please enter the problem.')
                prob = str(inp('Problem'))
                call_human('Problem'+prob)
                add_data = open(tempf+"/feedback.txt", 'a')
                add_data.write("\n"+prob)          # Feedback
                add_data.close()
        elif 'clean' in msg:
                outp('Do you want us to clean the room?')
                ab = inp('Yes/No')
                if 'y' in ab:
                        outp('Please enter room number.')
                        rnu = inp('Room')
                        call_human('Clean room'+rnu)
                elif 'n' in ab:
                        outp('It is okay.')
        elif 'feedback' in msg:
                outp("Please give feedback now.")
                txt = inp('Feedback')
                add_data = open(tempf+"/feedback.txt", 'a')
                add_data.write("\n"+txt)    # Feedback
                add_data.close()
                outp("Thank you for your valuable feedback.")
        elif 'extra' in msg:
                outp('Please enter what you need extra')
                need = inp('Extra')
                outp('Please enter your room number.')
                rnu = inp('Room')
                outp('Sending Extra '+need+' to Room'+str(rnu))
                call_human('Extra : '+need+' Room : '+str(rnu))
        elif 'wake' in msg:
                outp("Do you want a wakeup call?")
                response = inp("Yes/No")
                if 'y' in response:
                        outp("Please enter your room number.")
                        rn = inp("Room")
                        outp("Enter at what time you want.")
                        tm = inp("Time")
                        call_human("Wakeup call : "+rn+" "+tm)
                else:
                        outp("Okay.")
        elif 'search' in msg:
                outp("Please enter what you want to search for.")
                sea = inp("Search")
                url = "google.com/search?q="+sea
                pgui.click(69, 19)  # click on browser
                sleep(5)
                pgui.typewrite(url)
                pgui.press('enter')
        elif 'change' in msg and 'room' in msg:
                outp("Please enter your room number.")
                r_num=inp("Room")
                outp("What problems do you have in your room?")
                prob=inp("Problems.")
                add_data = open(tempf+"/feedback.txt", 'a')
                add_data.write("\n"+txt)    # Feedback
                add_data.close()
                if len(available_rooms)>0:
                        next_room=random.choice(available_rooms)
                        outp("Room is changed from "+r_num+" to "+next_room)
                        call_human("Room change from "+r_num+" to "+next_room+" Problem : "+prob)
                        rooms_names[next_room] = rooms_names[r_num]
                        available_rooms.remove(next_room)
                        rooms_names[r_num] = 'avl'
                        available_rooms.append(r_num)
                        rewrite()
                else:
                        outp("Sorry. No rooms are available. Your problem will be fixed immediately.")
                        call_human("Urgent. Room: "+r_num+" Problem : "+prob)
        elif msg == "err":
                outp("I can't hear that.")
        else:
                outp("Sorry. Please repeat.")
                add_data = open(tempf+"/newdata.txt", 'a')
                add_data.write("\n")
                add_data.write(msg)
                add_data.close()


# main method starts here

def main():
        print("-----------------------------------------")
        '''if vo_work:
                mixer.music.load(tempf+'/short.mp3')
                mixer.music.play()'''

        while True:
                mesg = inp("You").lower()
                if mesg == "q" or mesg == "close" or mesg == "quit" or mesg == 'exit':
                        break
                resp(mesg)


main()

# program ends here
