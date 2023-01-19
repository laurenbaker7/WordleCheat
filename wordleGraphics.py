from tkinter import *
from tkinter import ttk

import sys
import time
import tkinter
import os.path
from wordleMain import *

_Windows = sys.platform == 'win32'  # True if on Win95/98/NT

_root_window = None      # The root window for graphics output
_canvas = None      # The canvas which holds graphics
_canvas_xs = None      # Size of canvas object
_canvas_ys = None
_canvas_x = None      # Current position on canvas
_canvas_y = None
letterDict = {}
allWords = None

def formatColor(r, g, b):
    return '#%02x%02x%02x' % (int(r * 255), int(g * 255), int(b * 255))

if _Windows:
    _canvas_tfonts = ['times new roman', 'lucida console']
else:
    _canvas_tfonts = ['times', 'lucidasans-24']
    pass # XXX need defaults here

def begin_graphics(width=1200, height=700, color=formatColor(193, 193, 193), title=None):

    global _root_window, _canvas, _canvas_x, _canvas_y, _canvas_xs, _canvas_ys, _bg_color

    # Check for duplicate call
    if _root_window is not None:
        # Lose the window.
        _root_window.destroy()

    # Save the canvas size parameters
    _canvas_xs, _canvas_ys = 999, 499
    _canvas_x, _canvas_y = 0, _canvas_ys
    _bg_color = color

    # Create the root window
    _root_window = tkinter.Tk()
    _root_window.protocol('WM_DELETE_WINDOW', _destroy_window)
    _root_window.title(title or 'Graphics Window')
    #_root_window.resizable(0, 0)
    _root_window.geometry('1200x700')

    # Create the canvas object
    try:
        _canvas = tkinter.Canvas(_root_window, width=1000, height=500)
        _canvas.pack()
        draw_background()
        _canvas.update()
    except:
        _root_window = None
        raise

    # Bind to key-down and key-up events
    _root_window.bind( "<KeyPress>", _keypress )
    _root_window.bind( "<KeyRelease>", _keyrelease )
    _root_window.bind( "<FocusIn>", _clear_keys )
    _root_window.bind( "<FocusOut>", _clear_keys )
    _root_window.bind( "<Button-1>", _leftclick )
    _root_window.bind( "<Button-2>", _rightclick )
    _root_window.bind( "<Button-3>", _rightclick )
    _root_window.bind( "<Control-Button-1>", _ctrl_leftclick)
    _clear_keys()

_leftclick_loc = None
_rightclick_loc = None
_ctrl_leftclick_loc = None

def _leftclick(event):
    global _leftclick_loc
    _leftclick_loc = (event.x, event.y)

def _rightclick(event):
    global _rightclick_loc
    _rightclick_loc = (event.x, event.y)

def _ctrl_leftclick(event):
    global _ctrl_leftclick_loc
    _ctrl_leftclick_loc = (event.x, event.y)


def draw_background():
    corners = [(0,0), (0, _canvas_ys), (_canvas_xs, _canvas_ys), (_canvas_xs, 0)]
    polygon(corners, _bg_color, fillColor=_bg_color, filled=True, smoothed=False)

def _destroy_window(event=None):
    sys.exit(0)
#    global _root_window
#    _root_window.destroy()
#    _root_window = None
    #print("DESTROY")

def end_graphics():
    global _root_window, _canvas, _mouse_enabled
    try:
        try:
            sleep(1)
            if _root_window != None:
                _root_window.destroy()
        except SystemExit as e:
            print('Ending graphics raised an exception:', e)
    finally:
        _root_window = None
        _canvas = None
        _mouse_enabled = 0
        _clear_keys()

def clear_screen(background=None):
    global _canvas_x, _canvas_y
    _canvas.delete('all')
    draw_background()
    _canvas_x, _canvas_y = 0, _canvas_ys
    letters = text((75, 20), color='black', contents="Letters:", size=20)
    wordsHeader = text((75, 200), color='black', contents="Possible words:", size=20)

def polygon(coords, outlineColor, fillColor=None, filled=1, smoothed=1, behind=0, width=1):
    c = []
    for coord in coords:
        c.append(coord[0])
        c.append(coord[1])
    if fillColor == None: fillColor = outlineColor
    if filled == 0: fillColor = ""
    poly = _canvas.create_polygon(c, outline=outlineColor, fill=fillColor, smooth=smoothed, width=width)
    if behind > 0:
        _canvas.tag_lower(poly, behind) # Higher should be more visible
    return poly

def refresh():
    _canvas.update_idletasks()

def text(pos, color, contents, font='Helvetica', size=12, style='normal', anchor="nw"):
    global _canvas_x, _canvas_y
    x, y = pos
    font = (font, str(size), style)
    return _canvas.create_text(x, y, fill=color, text=contents, font=font, anchor=anchor)

##############################################################################
### Keypress handling ########################################################
##############################################################################

# We bind to key-down and key-up events.

_keysdown = {}
_keyswaiting = {}
# This holds an unprocessed key release.  We delay key releases by up to
# one call to keys_pressed() to get round a problem with auto repeat.
_got_release = None

def _keypress(event):
    global _got_release
    #remap_arrows(event)
    _keysdown[event.keysym] = 1
    _keyswaiting[event.keysym] = 1
#    print(event.char, event.keycode)
    _got_release = None

def _keyrelease(event):
    global _got_release
    #remap_arrows(event)
    try:
        del _keysdown[event.keysym]
    except:
        pass
    _got_release = 1

def _clear_keys(event=None):
    global _keysdown, _got_release, _keyswaiting
    _keysdown = {}
    _keyswaiting = {}
    _got_release = None

def createLetterDict():
    global letterDict
    alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
        'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    for letter in alphabet:
        letterDict[letter] = 'black'
    displayLetters()

def updateLetterDict(word, outcomes):
    for i in range(5):
        letter = word[i]
        result = outcomes[i]
        if (result == 0):
            letterDict[letter] = 'green'
        elif (result == 1):
            if (letterDict[letter] != 'green'):
                letterDict[letter] = 'gold1'
        elif (result == 2):
            if (letterDict[letter] == 'black'):
                letterDict[letter] = 'red'
        displayLetters()

def displayLetters():
    clear_screen()
    alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
        'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    i = 300
    for letter in alphabet[:10]:
        text((i, 10), color=letterDict[letter], contents=letter, size=30)
        i += 50
    i = 300
    for letter in alphabet[10:20]:
        text((i, 60), color=letterDict[letter], contents=letter, size=30)
        i += 50
    i = 400
    for letter in alphabet[20:]:
        text((i, 110), color=letterDict[letter], contents=letter, size=30)
        i += 50
    refresh()

def updateButton():
    word = e1.get()
    outcome = e2.get()
    outArr = list()
    for num in outcome:
        outArr.append(int(num))
    #printWords(word, outArr)
    updateLetterDict(word, outArr)
    printWords(word, outArr)

def printWords(word, outArr):
    global allWords
    wrong = list()
    for i in range(5):
        if (outArr[i] == 2):
            if not (word[i] in word[0:i]):
                wrong.append(word[i])
        elif (outArr[i] == 0):
            allWords = CorrectLetter(word[i], i, allWords)
        elif (outArr[i] == 1):
            allWords = InWord(word[i], i, allWords)
    allWords = NotInWord(wrong, allWords)
    numWords = len(allWords)
    if (numWords > 6):
        i = 250
        for word in allWords[0:7]:
            text((i, 190), color='black', contents=word, size=15)
            i+=95
        if (numWords > 13):
            i = 250
            for word in allWords[7:14]:
                text((i, 240), color='black', contents=word, size=15)
                i+=95
            if (numWords > 20):
                i = 250
                for word in allWords[14:21]:
                    text((i, 290), color='black', contents=word, size=15)
                    i+=95
            else:
                i = 250
                for word in allWords[14:]:
                    text((i, 290), color='black', contents=word, size=15)
                    i+=95
        else:
            i = 250
            for word in allWords[7:]:
                text((i, 240), color='black', contents=word, size=15)
                i+=95
    else:
        i = 300
        for word in allWords:
            text((i, 200), color='black', contents=word, size=15)
            i+=95
    if (numWords > 21):
        text((250, 340), color='black', contents="...", size=20)
    refresh()

def startingWords():
    global allWords
    allWords = newGame()

def startOver():
    startingWords()
    clear_screen()
    createLetterDict()


if __name__ == '__main__':
    begin_graphics()
    startingWords()

    frm = Frame(_root_window)
    frm.pack()

    letters = text((75, 20), color='black', contents="Letters:", size=20)
    createLetterDict()

    wordsHeader = text((75, 200), color='black', contents="Possible words:", size=20)
    refresh()

    ttk.Label(frm, text="GUESS (5 letter word, all uppercase):").grid(row=0)
    ttk.Label(frm, text="OUTCOME (5 number string, 0 = correct, 1 = wrong place, 2 = wrong)").grid(row=1)

    e1 = ttk.Entry(frm)
    e2 = ttk.Entry(frm)

    e1.grid(row=0, column=1)
    e2.grid(row=1, column=1)

    ttk.Button(frm, text = 'Quit', command=_root_window.quit).grid(row=3, column=0)
    ttk.Button(frm, text='Update', command=updateButton).grid(row=3, column=1)
    ttk.Button(frm, text='Start Over', command=startOver).grid(row=3, column=2)

    _root_window.mainloop()
