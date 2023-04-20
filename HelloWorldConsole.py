#!/usr/bin/env
# -*- coding: utf-8 -*-

"""
Submission for Project Milestone 1, Task 2
by  Aleksandra Kukawka (#448975)
and  Daso Jung (#446806)
"""

#insert your code here

# dictionary for mapping letters to greetings
letterMapping = {'D': 'Guten Tag', 'd': 'Guten Tag', 
                  'E': 'Good morning', 'e': 'Good morning', 
                  'F': 'Bonjour', 'f': 'Bonjour'}

def main():
    # loop the program infinitely before user quits it
    while True:
        print('\nSelect one of the following:')
        print('\t[D]eutsch')
        print('\t[E]nglish')
        print('\t[F]rançais')
        print('\t[Q]uit')

        # capture user input
        letter = input()

        # if the letter is in the provided dictionary, display the greeting
        if letter in letterMapping:
            print(letterMapping[letter])

        # if the letter is q or Q, quit
        elif letter in ['q','Q']:
            print('Quitting...')
            exit()

        # if the input is not appropriate, display the warning
        else:
            print('Invalid input!')

if __name__ == "__main__":
    main()
