import random
def read_words(filename):
    try:
        with open(filename,'r') as file:
            words = file.read().splitlines()
        return words
    except FileNotFoundError:
        print(f"File '{filename}' not found.")    
        return []
def display_word(word,guess_letter):
    display = ""
    for letter in word:
        if letter in guess_letter:
            display += letter
        else:
            display += "_"
    return display
def chooserandomword():
    words = read_words("words.txt")
    word = random.choice(words).lower() 
    return word    
def difflevel():
    diflvl = input("Easy/Medium/Hard ").lower()
    if diflvl == "easy":
        return 10
    if diflvl == "medium":
        return 8
    if diflvl == "hard":
        return 6
    

    
def hangman():
    attempts = difflevel()
    word = chooserandomword()
    letter_guess = []
    print("Hangman Game!")
    while True:
       print(f"Attempts left {attempts}")
       print(display_word(word,letter_guess))
       print("Used letters:", letter_guess)
       if "_"  not in display_word(word,letter_guess):
            print("Congratz! You guessed the word:", word)
            break
       
       if attempts == 0:
           print("You lost! The correct word was:", word)
           break
       
       guess = input("Guess a letter: ").lower()

       if len(guess) != 1 or not guess.isalpha():
           print("Invalid type!")
           continue
       
       if guess in letter_guess:
           print("You already typed that letter!")
           continue
       
       letter_guess.append(guess)

       if guess not in word:
           attempts -= 1
           print("Incorrect guess!")
        
         
    

hangman()