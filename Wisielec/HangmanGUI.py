import random
from tkinter import *
from screeninfo import get_monitors
attempts = 8
guess_letters = []
chosen_word = ""
body_parts=[(20,225,60,225),    # bottomstool           
            (40,225,40,25),     # hang post
            (40,25,150,25),     # top beam
            (150,25,150,60),    # rope
            (150,85,20),        # head -> x = 150 y = 85, r = 20 -> [130,65,170,105]
            (150,110,150,190),  # body
            (150,150,170,120),  # right hand
            (150,150,130,120),  # left hand
            (150,190,180,220),  # right leg
            (150,190,120,220)]  # left leg
def mon_resolution():
    monitors = get_monitors()
    if monitors:
        main_monitor = monitors[0]
        width, height = main_monitor.width, main_monitor.height
        return width, height
    else:
        return None
def read_words(filename):
    try:
        with open(filename,'r') as file:
            words = file.read().splitlines()
        return words
    except FileNotFoundError:
        print(f"File '{filename}' not found.")    
        return []
def chooserandomword():
     word = random.choice(read_words("words.txt")).lower() 
     return word
def setdiff(level):
    global attempts
    if level == "Easy":
        attempts = 10
        turnoff_difflvl()
        info_label.config(text = "You have 10 attempts!")
        update_display()
        canvas.delete("line")
    if level == "Medium":
        attempts = 8
        turnoff_difflvl()
        info_label.config(text = "You have 8 attempts!")
        update_display()
        canvas.delete("line")
    if level == "Hard":
        attempts = 6
        turnoff_difflvl()
        info_label.config(text = "You have 6 attempts!")
        update_display()
        canvas.delete("line")
def turnoff_difflvl():
    easy_button.pack_forget()
    medium_button.pack_forget()
    hard_button.pack_forget()
    lvl_label.config(text="")
def turnon_difflvl():
    easy_button.pack(side= LEFT,fill=BOTH)
    medium_button.pack(side= LEFT,fill=BOTH)
    hard_button.pack(side = RIGHT, fill = BOTH)
def new_game():
    global attempts, chosen_word, guess_letters
    chosen_word = chooserandomword()
    guess_letters = []
    attempts = 8
    guess_button.configure(state = NORMAL)
    guess_word_button.configure(state = NORMAL)
    letter_entry.config(state = NORMAL)
    turnon_difflvl()
    info_label.config(text = "Guess a letter!")
    update_display()
    lvl_label.config(text= "You can choose difficulty level before you start!")
def update_display():  
    display = ""
    for letter in chosen_word:
        if letter in guess_letters:
            display += letter
        elif letter == " ":
            display += "   " 
        else:
            display += "_ "      
    
    word_label.config(text = display)
    attempts_label.config(text = f"Attempts left: {attempts}")
    canvas.delete("hangman")
    draw_hangman(canvas,attempts)
    
    if "_" not in display:
        info_label.configure(text= f"Congratz! You guessed the word : {chosen_word}")
        guess_button.configure(state = DISABLED)
        guess_word_button.configure(state = DISABLED)
        letter_entry.config(state = DISABLED)
    if attempts == 0:
        info_label.config(text = f"You lost! The chosen word was : {chosen_word}")
        guess_button.configure(state = DISABLED)
        guess_word_button.configure(state = DISABLED)
        letter_entry.config(state = DISABLED)
    used_letters_label.configure(text = f"You used already these letters: {', '.join(guess_letters)}")
def guess_letter():
    global attempts
    guess = letter_entry.get().lower()
    letter_entry.delete(0, END)
    if len(guess) != 1 or not guess.isalpha():
        info_label.configure(text = "Invalid type!")
        return
    if guess in guess_letters:
        info_label.configure(text = f"You already guessed this letter: {guess}")
        return
    guess_letters.append(guess)
    if guess not in chosen_word:
        attempts -= 1
        turnoff_difflvl()
    else:
        info_label.configure(text = f"There is {guess} in a word!")
    update_display()  
def guess_word():
    global attempts
    guess = letter_entry.get().lower()
    letter_entry.delete(0, END)
    if guess == "":
        info_label.config(text = "Please input some word!")
        return
    if len(guess) != len(chosen_word):
        info_label.config(text= "You even can't count the amount of letters?")
        return
    if guess == chosen_word:
        info_label.configure(text = f"Congratz! You guessed the word : {chosen_word}")
        guess_button.configure(state = DISABLED)
        guess_word_button.configure(state = DISABLED)
    else:
        info_label.config(text="Incorrect word!")
        attempts -= 1
        turnoff_difflvl()
        update_display()
def draw_hangman(canvas,attempts):
    for i in range(10 - attempts):
        if len(body_parts[i]) == 4:
            x1,y1,x2,y2 = body_parts[i]
            canvas.create_line(x1,y1,x2,y2,fill="white", width=3, tags="hangman")
        elif len(body_parts[i]) == 3:
            x,y,r = body_parts[i]
            canvas.create_oval(x-r,y-r,x+r,y+r, fill="white", width=3, tags="hangman")


window = Tk()
window.title("Hangman Game!")
window.configure(bg = "black")

users_width, users_height = mon_resolution()

window_width, window_height = users_width//2, users_height//2

window.geometry(f"{window_width}x{window_height}+{(users_width-window_width)//2}+{(users_height - window_height)//2}")

window.resizable(0,0)


canvas = Canvas(window, bg="black", width=200, height=250, highlightthickness=0)
canvas.place(x=30,y=20)

word_label = Label(window, font = ("Arial", 25), bg = "black", fg = "#90EE90")
word_label.pack(pady=(50,0), side = TOP)

attempts_label = Label(window, font = ("Arial", 10), bg = "black", fg = "white")
attempts_label.pack(pady = (0,5))

big_frame = Frame(window, bg = "black")
big_frame.pack()

frame_entry = Frame(big_frame)
frame_entry.pack(fill = BOTH, pady=(0,5))

letter_entry = Entry(frame_entry, font = ("Arial", 25), bg = "white", fg = "black")
letter_entry.pack(side = LEFT, fill = BOTH)

frame_in_frame = Frame(frame_entry)
frame_in_frame.pack(side = RIGHT, fill = BOTH)

bspace_button = Button(frame_entry, font = ("Arial",10), bg = "white", fg = "black", text = "\u2190", command = lambda: letter_entry.delete(len(letter_entry.get())-1,END))
bspace_button.pack(side = TOP, fill = BOTH)

del_button = Button(frame_entry, text = "Delete", command = lambda: letter_entry.delete(0, END) )
del_button.pack(side = BOTTOM, fill= BOTH)

button_frame = Frame(big_frame, bg="black")
button_frame.pack(fill = BOTH)

guess_button = Button(button_frame, text = "Guess Letter", font = ("Arial", 17), bg = "black", command = guess_letter, fg = "white", activebackground= "black", activeforeground="white")
guess_button.pack(side = LEFT,fill = BOTH)

guess_word_button = Button(button_frame, text = "Guess Word", font = ("Arial", 17), bg = "black", command = guess_word, fg = "white", activebackground= "black", activeforeground="white")
guess_word_button.pack(side = RIGHT, fill = BOTH)

new_game_button = Button(button_frame, text = "New Game", font = ("Arial", 17), bg = "black", command = new_game, fg = "white", activebackground= "black", activeforeground="white")
new_game_button.pack(fill = BOTH)

info_label = Label(window, font = ("Arial", 25), bg = "black", fg = "red")
info_label.pack(pady=(20,0))

used_letters_label = Label(window, font = ("Arial", 25), bg = "black", fg = "#90EE90")
used_letters_label.pack(pady = (30,0))

difflvl_frame = Frame(window, background="black")
difflvl_frame.pack(side = BOTTOM)

lvl_label = Label(window, font = ("Arial", 25), bg = "black", fg = "#90EE90", text = "You can choose difficulty level before you start!")
lvl_label.pack(side = BOTTOM)

easy_button = Button(difflvl_frame, text = "Easy", font = ("Arial", 17), bg = "black", command = lambda: setdiff("Easy"), fg = "white", activebackground= "black", activeforeground="white")
easy_button.pack(side = LEFT, fill=BOTH)

medium_button = Button(difflvl_frame, text = "Medium", font = ("Arial", 17), bg = "black", command = lambda: setdiff("Medium"), fg = "white", activebackground= "black", activeforeground="white")
medium_button.pack(side= LEFT,fill=BOTH)

hard_button = Button(difflvl_frame, text = "Hard", font = ("Arial", 17), bg = "black", command = lambda: setdiff("Hard"), fg = "white", activebackground= "black", activeforeground="white")
hard_button.pack(side = RIGHT, fill = BOTH)
new_game()
window.mainloop()         
    

