import random
from sys import float_info.max


def show(word):
    # prints the word and the positions of each letter
    text = ""
    for char in word:
        text += char + "  "
    text += "\n"
    for i in range(1, len(word) + 1):
        text += str(i) + "  "
    print(text)


def giveword():
    n = random.randint(5, 9)
    file = open("words_alpha.txt", "r")
    words = [word for word in file.readlines() if
             len(word) == n + 1]
    word = random.choice(words)
    counter = 6
    answer = ["_" for _ in range(n)]

    print("\t \t Your turn to guess \n ")
    while counter:
        print("please enter a letter. You have -=<[{ ", counter, " }]>=- chances left")
        letter = input()
        while not letter.isalpha():
            letter = input("please enter a valid letter\t")
        positions = reply(word, letter)
        if not positions:
            counter -= 1
        for position in positions:
            answer[position] = letter
        show(answer)
        if "_" not in answer:
            return True
    print("The correct answer is:  ", word)
    return False


def guessword():
    # sets n as the length of the word
    print("\t \t My turn to guess \n ")
    n = input("Please enter the length of your word\t")
    while not n.isnumeric():
        n = input("please enter a valid number\t")
    n = int(n)

    counter = 0  # checks how many tries we make
    solution = ["_" for _ in range(n)]  # the word we found so far
    file = open("words_alpha.txt", "r")
    words = [word for word in file.readlines() if
             len(word) == n + 1]  # imports words from a dictionary. The n+1 is for the \n
    empty = [i for i in range(n)]  # holds the indexes of the empty cells
    guesses = []  # holds all attempted letters

    while counter < 6:  # as long as we didn't lose
        letter = guessletter(guesses, words)
        correct = input(
            "does " + letter + " appear in your word?\n enter the "
                               "number of appearances it makes in your word, enter 0 if it doesnt appear at all \t")

        # takes the number of occurences of the letter. retries until it's valid
        while not correct.isnumeric() or int(correct) > len(empty):
            correct = input("please enter a valid number\t")
        correct = int(correct)
        if correct:
            positions = []  # holds the positions of the letter
            i = correct
            show(solution)
            print("please enter the positions of the letter\n")

            # takes the positions of the letter. repeats until vaild
            while i:
                pos = input()
                while not pos.isnumeric() or int(pos) > n or int(pos) - 1 not in empty:
                    pos = input("please enter a valid number\t")
                pos = int(pos)
                empty.remove(pos - 1)
                positions.append(pos)
                solution[pos - 1] = letter
                i -= 1

            # filter the words
            filteredwords = []
            for word in words:
                for pos in positions:
                    if word[pos - 1] != letter:
                        break
                else:
                    filteredwords.append(word)
            words = filteredwords

        # in case our letter doesn't appear in the word
        else:
            counter += 1
            words = [word for word in words if letter not in word]

        # if we found the solution
        if solution.count("_") == 0:
            print("The answer is " + "".join(solution))
            return True
    return False


def guessletter(guesses, words):
    values = {chr(i): 0 for i in range(97, 123)}
    # counts in how many words each letter appears
    for word in words:
        letters = []
        for letter in word[:-1]:
            if letter not in letters:
                letters.append(letter)
                values[letter] += 1
    # gives the letters already found the value 0
    for letter in guesses:
        values[letter] = float_info.max
    n = len(words)
    # returns the letter wich appears the closest to half the words
    answer = min(values.keys(), key=lambda x: abs(values[x] - n / 2))
    guesses.append(answer)
    return answer


def reply(solution, answer):
    locations = []
    for i in range(len(solution)):
        if answer == solution[i]:
            locations.append(i)
    return locations


def game():
    wins = 0
    losses = 0
    play = 1
    while play:
        print("Welcome to this hangman game. Think you can beat me? \n")
        choice = input("enter H for head and T for tail \n")
        while choice not in "HT":
            choice = input("enter H for head and T for tail \n")
        p = random.random()
        if p > 0.5:
            ht = "H"
        else:
            ht = "T"
        print("You chose  ", choice, ", the throw gave a ", ht)
        if ht == choice:
            start = input("You guessed right. Enter 1 if you want to guess first and 2 otherwise.\n")
            while start not in "12":
                start = input("Please enter 1 if you want to guess first and 2 otherwise.]n")
        else:
            start = "2"
        if start == "1":
            if giveword():
                wins += 1
            if guessword():
                losses += 1
        else:
            if guessword():
                losses += 1
            if giveword():
                wins += 1
        print("the results are:\t", wins, " - ", losses)
        print("do you want to continue playing?")
        yn = input("enter 1 to continue playing. enter any other value to quit")
        if yn != "1":
            play = 0


game()
