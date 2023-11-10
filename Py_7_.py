import speech_recognition as sr
import pyttsx3
import smtplib
import getpass
import imaplib
import email

# Function to listen to user input
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio).lower()
        print("User said:", command)
    except sr.UnknownValueError:
        print("Couldn't understand audio!")
        command = ""
    return command

# Function to speak out the response
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Function to send an email
def send_email():
    speak("Please provide your email credentials.")
    email_address = input("Email Address: ")
    password = getpass.getpass("Password: ")
    recipient = input("Recipient Email Address: ")
    subject = input("Subject: ")
    message = input("Message: ")
    
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email_address, password)
        server.sendmail(email_address, recipient, 
                        f"Subject: {subject}\n\n{message}")
        server.quit()
        speak("Email sent successfully!")
    except Exception as e:
        speak(f"Failed to send email. Error: {str(e)}")

# Function to read inbox emails
def read_inbox():
    speak("Please provide your email credentials.")
    email_address = input("Email Address: ")
    password = getpass.getpass("Password: ")
    
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(email_address, password)
        mail.select("inbox")
        _, data = mail.search(None, "ALL")
        mail_ids = data[0].split()
        
        count = 0
        for num in data[0].split():
            _, email_data = mail.fetch(num, "(RFC822)")
            _, b = email_data[0]
            msg = email.message_from_bytes(b)
            speak(f"Email {count+1} received from {msg['From']}.")
            speak(f"Subject: {msg['Subject']}")
            count += 1
            
        speak("End of emails.")
    except Exception as e:
        speak(f"Failed to read inbox emails. Error: {str(e)}")

# Main function to handle voice commands
def jarvis():
    command = listen()
    
    if "send email" in command:
        send_email()
    elif "read emails" in command:
        read_inbox()
    else:
        speak("Sorry, I didn't understand the command. Please try again.")

# Run Jarvis voice assistant
speak("Hello! How can I assist you today?")
jarvis()

