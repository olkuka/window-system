#!/usr/bin/env
# -*- coding: utf-8 -*-

"""
Submission for Project Milestone 1, Task 3
by  Aleksandra Kukawka 
and Daso Jung
"""

from tkinter import *

window = Tk()
window.geometry('250x300')

languageLabel = Label(window, text= 'Please select a language.', fg = '#F6A800')
languageLabel.pack(pady=4)

# button to display German greeting 
deuBtn = Button(window,
    text='Deutsch',
    width=25,
    # change languageLabel text when user selects the button
    command = lambda: languageLabel.config(text='Guten Tag')
)

# button to display English greeting 
engBtn = Button(window,
    text='English',
    width=25,
    # change languageLabel text when user selects the button
    command = lambda: languageLabel.config(text='Good morning')
)

# button to display English greeting 
fraBtn = Button(window,
    text='Français',
    width=25,
    # change languageLabel text when user selects the button
    command = lambda: languageLabel.config(text='Bonjour')
)

# button to quit the window
quitBtn = Button(window,
    text='Quit',
    width=5,
    # destroy the window when user selects the button
    command=window.destroy
)

# display elements on the window
deuBtn.pack(pady=4)
engBtn.pack(pady=4)
fraBtn.pack(pady=4)

# push the quit button to right bottom corner
quitBtn.pack(pady=4, side=BOTTOM, anchor='e')

window.mainloop()
