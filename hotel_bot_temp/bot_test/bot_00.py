import pyttsx3

hlo=['hi','hello','hey']
hru=['how are you','how are you doing'] 
def sout(text):
	engine = pyttsx3.init()
	engine.say(text)
	engine.setProperty('rate',120)  #120 words per minute
	engine.setProperty('volume',0.9) 
	engine.runAndWait()

def outp(text):
	print(text)
	sout(text)

msg = ""
sout("Welcome. I am friend bot.")
while True:
    print("You: ", end = "")
    msg = input("")
    msg = msg.lower()
    print("Bot: ", end = "")
    if msg in hlo:
        outp("Hi.")
    elif msg in hru:
        outp("I am fine. What about you?")
    elif msg == "fine" or msg=="good":
        outp("Okay.")
    elif msg == "bye" or msg=="exit" or msg=="go away":
        outp("Bye. See you soon.")
        break
    elif msg == "okay" or msg == "ok" :
        outp("Okay then.")
    elif msg == "thank you" or msg=="thanks":
        outp("You are welcome.")
    elif msg == "weather":
        outp("Temperature is 23 C. It will not rain today.")
    elif msg == "joke":
        outp("What is the biggest lie in the entire universe? A. I have read and agree to the Terms & Conditions.")
    elif msg=="":
        outp("Please enter a message.")
    else:
        outp("I did not understand what you mean.")
