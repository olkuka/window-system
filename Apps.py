#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from GraphicsEventSystem import *
from Window import *
from UITK import *
from functools import partial


class HelloWorld(Widget):
    def __init__(self, originX, originY, width, height):
        super().__init__(originX, originY, width, height, 'HelloWorld')
        self.backgroundColor = COLOR_WHITE
        self.container = Container(
            0, 0, width, height-50, 'HelloWorldContainer', 'vertical', 10)
        # set container's layout anchors
        self.container.layoutAnchors = LayoutAnchor.top | LayoutAnchor.left | LayoutAnchor.bottom | LayoutAnchor.right
        self.greetingText = Label(
            0, 0, 10, 10, 'GreetingText', 'Select a language!', COLOR_CLEAR)

        # create buttons for different languages
        self.germanBtn = Button(0, 0, 200, 51, 'GermanBtn', 'Deutsch',
                                COLOR_GRAY, lambda: self.clickLanguageBtn('Guten Tag'))

        self.englishBtn = Button(0, 0, 200, 51, 'EnglishBtn', 'English',
                                 COLOR_GRAY, lambda: self.clickLanguageBtn('Good morning'))

        self.frenchBtn = Button(0, 0, 200, 51, 'FrenchBtn', 'Français',
                                COLOR_GRAY, lambda: self.clickLanguageBtn('Bonjour'))

        # create a quit button
        self.quitBtn = Button(self.width-50, self.height-30, 40, 20, 'QuitBtn',
                              'Quit', COLOR_GRAY, lambda: self.removeFromParentWindow())
        self.quitBtn.layoutAnchors = LayoutAnchor.right | LayoutAnchor.bottom

        self.addChildWindow(self.container)
        # add child windows to the container
        self.container.addChildWindow(self.greetingText)
        self.container.addChildWindow(self.germanBtn)
        self.container.addChildWindow(self.englishBtn)
        self.container.addChildWindow(self.frenchBtn)

        self.addChildWindow(self.quitBtn)

    def clickLanguageBtn(self, text):
        """
        Updates the greeting text based on the selected language.
        """
        self.greetingText.text = text


class Calculator(Widget):
    def __init__(self, originX, originY, width, height):
        super().__init__(originX, originY, width, height, 'Calculator')
        self.backgroundColor = COLOR_WHITE

        self.currentInput = ''  # stores the current input expression
        self.buttons = [    # list of buttons on the calculator
            'C', '+/-', '%', '/',
            '7', '8', '9', '*',
            '4', '5', '6', '-',
            '1', '2', '3', '+',
            '0', '00', '.', '='
        ]

        self.container = Container(
            0, 70, width, height-82, 'CalculatorContainer', 'vertical', 0)
        self.container.layoutAnchors = LayoutAnchor.top | LayoutAnchor.left | LayoutAnchor.bottom | LayoutAnchor.right

        self.label = Label(
            0, 10, width, 60, 'CalculatorLabel', '0', COLOR_CLEAR)
        self.label.layoutAnchors = LayoutAnchor.top
        self.addChildWindow(self.label)

        for i in range(5):
            childContainer = Container(
                0, 0, self.width, self.height, 'CalculatorChildContainer'+str(i), 'horizontal', 0)
            childContainer.layoutAnchors = LayoutAnchor.top | LayoutAnchor.left | LayoutAnchor.bottom | LayoutAnchor.right
            self.container.addChildWindow(childContainer)

        row, col = 0, 0
        for btnText in self.buttons:
            # create button object and set its properties
            button = Button(0, 0, 50, 50, btnText, btnText, COLOR_LIGHT_GRAY, partial(
                self.buttonClicked, btnText))

            if row == 0 or col == 3:
                button.normalColor = '#f7e436'

            # add buttons to the appropriate container
            self.container.childWindows[row].addChildWindow(button)
            col += 1

            if col > 3:
                col = 0
                row += 1

        self.addChildWindow(self.container)

    def buttonClicked(self, text):
        """
        Processes the input when a button is clicked.
        """
        self.processInput(text)

    def keyPressed(self, key):
        """
        Processes the input when a keyboard is pressed.
        """
        if key == '':
            key = '='   # clear the input

        if key in self.buttons:
            self.processInput(key)

    def processInput(self, key):
        """
        Processes the input.
        """
        if key == 'C':
            self.currentInput = ''

        elif key == '+/-':
            try:
                # negate the input number
                self.currentInput = str(int(self.currentInput)*-1)
            except:
                self.currentInput = 'Error'    # handle error if input cannot be negated

        elif key == '=':
            try:
                # evaluate the input expression
                result = eval(self.currentInput)
                # store the result as the current input
                self.currentInput = str(result)
            except ZeroDivisionError:
                self.currentInput = 'Error: Division by zero'   # handle division by zero error
            except:
                self.currentInput = 'Error'    # handle other evaluation errors

        else:
            self.currentInput += key    # append the key to the current input

        self.label.text = self.currentInput    # update the label with the current input


class Colors(Widget):
    def __init__(self, originX, originY, width, height):
        super().__init__(originX, originY, width, height, 'Colors')
        self.backgroundColor = COLOR_WHITE
        self.container = Container(
            0, 20, width, height-20, 'ColorsContainer', 'vertical', 10)
        self.container.layoutAnchors = LayoutAnchor.top | LayoutAnchor.left | LayoutAnchor.bottom | LayoutAnchor.right
        self.addComponents()

    def addComponents(self):
        """
        Adds elements to the application window.
        """
        # create sliders for each color channel
        self.sliderR = Slider(0, 0, self.width, 50, 'SliderR', COLOR_RED)
        self.sliderG = Slider(0, 0, self.width, 50, 'SliderG', COLOR_GREEN)
        self.sliderB = Slider(0, 0, self.width, 50, 'SliderB', COLOR_BLUE)

        # initialize color label and text
        self.color = self.mapFromRgbToHex()
        self.colorLabel = Label(0, 0, self.width, 30,
                                'ColorLabel', '', self.color)

        self.colorText = Label(0, 0, self.width, 5,
                               'ColorText', self.color, COLOR_CLEAR)

        self.addChildWindow(self.container)
        # add child windows to the container
        self.container.addChildWindow(self.sliderR)
        self.container.addChildWindow(self.sliderG)
        self.container.addChildWindow(self.sliderB)
        self.container.addChildWindow(self.colorLabel)
        self.container.addChildWindow(self.colorText)

    def mapFromRgbToHex(self):
        """
        Converts RGB values to hexadecimal representation.
        """
        return '#{:02x}{:02x}{:02x}'.format(int(self.sliderR.value*255), int(self.sliderG.value*255), int(self.sliderB.value*255))

    def draw(self, ctx):
        """
        Draws the application and manages the color change. 
        """
        super().draw(ctx)
        self.color = self.mapFromRgbToHex()
        self.colorLabel.backgroundColor = self.color
        self.colorText.text = self.color
        self.container.draw(ctx)


class StartMenu(Window):
    def __init__(self, screen, originX=0, originY=400, width=150, height=150):
        super().__init__(originX, originY, width, height, 'StartMenu')
        self.backgroundColor = COLOR_LIGHT_GRAY
        # set decorations to false because we don't want a title bar
        self.addDecorations = False

        # add buttons for every app
        self.buttonHelloWorld = Button(0, 45, width, 25, 'HelloWorldButton', 'HelloWorld',
                                       COLOR_GRAY, lambda: self.onAppButtonClick(HelloWorld, screen))
        self.buttonColors = Button(0, 15, width, 25, 'ColorsButton', 'Colors',
                                   COLOR_GRAY, lambda: self.onAppButtonClick(Colors, screen))
        self.buttonCalculator = Button(0, 75, width, 25, 'CalculatorButton', 'Calculator',
                                       COLOR_GRAY, lambda: self.onAppButtonClick(Calculator, screen))

        # add quit button to exit the app
        self.buttonExit = Button(0, 105, width, 25, 'ExitButton', 'Quit',
                                 COLOR_RED, lambda: quit())

        # add child windows to the start menu
        self.addChildWindow(self.buttonHelloWorld)
        self.addChildWindow(self.buttonColors)
        self.addChildWindow(self.buttonCalculator)
        self.addChildWindow(self.buttonExit)

    def onAppButtonClick(self, appName, screen):
        """
        Adds app to the screen children and closes the start menu.
        """
        # add app to the screen's children
        screen.addChildWindow(appName(10, 10, 200, 300))
        # close the start menu by removing it from the parent window
        self.removeFromParentWindow()
