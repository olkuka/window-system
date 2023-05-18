#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from GraphicsEventSystem import *
from Window import *
from UITK import *


class HelloWorld(Widget):
    def __init__(self, originX, originY, width, height):
        super().__init__(originX, originY, width, height, 'Hello World')
        self.backgroundColor = COLOR_WHITE
        self.container = Container(
            0, 0, width, height-50, "HelloWorldContainer", 'vertical', 10)
        self.greetingText = Label(
            0, 0, 10, 10, "text", "Select a language!", COLOR_CLEAR)
        self.greetingText.layoutAnchors = LayoutAnchor.top

        self.germanBtn = Button(0, 0, 200, 51, "Btn1", "Deutsch",
                                COLOR_GRAY, lambda: self.clickLanguageBtn("Guten Tag"))
        # self.germanBtn.layoutAnchors = LayoutAnchor.top

        self.englishBtn = Button(0, 0, 200, 51, "Btn2", "English",
                                 COLOR_GRAY, lambda: self.clickLanguageBtn("Good morning"))
        # self.englishBtn.layoutAnchors = LayoutAnchor.top

        self.frenchBtn = Button(0, 0, 200, 51, "Btn3", "Français",
                                COLOR_GRAY, lambda: self.clickLanguageBtn("Bonjour"))
        # self.frenchBtn.layoutAnchors = LayoutAnchor.top

        self.quitBtn = Button(self.width-50, self.height-30, 40, 20, "quitBtn",
                              "Quit", COLOR_GRAY, lambda: self.removeFromParentWindow())
        self.frenchBtn.layoutAnchors = LayoutAnchor.bottom | LayoutAnchor.right

        self.addChildWindow(self.container)
        self.container.addChildWindow(self.greetingText)
        self.container.addChildWindow(self.germanBtn)
        self.container.addChildWindow(self.englishBtn)
        self.container.addChildWindow(self.frenchBtn)
        self.addChildWindow(self.quitBtn)

    def clickLanguageBtn(self, text):
        self.greetingText.text = text

    def draw(self, ctx):
        super().draw(ctx)


class Calculator(Widget):
    def __init__(self, originX, originY, width, height):
        super().__init__(originX, originY, width, height, 'Calculator')
        self.backgroundColor = COLOR_WHITE

        self.container = Container(
            originX, originY, width, height, "Calculator Container", 'grid', 0)
        self.greetingText = Label(0, 0, 10, 10, "text", "Hello", COLOR_GRAY)
        self.germanBtn = Button(0, 0, 200, 51, "Btn1", "Deutsch",
                                COLOR_GRAY, lambda: self.clickLanguageBtn("Guten Tag"))
        self.englishBtn = Button(0, 0, 200, 51, "Btn2", "English",
                                 COLOR_GRAY, lambda: self.clickLanguageBtn("Good morning"))
        self.franchBtn = Button(0, 0, 200, 51, "Btn3", "Français",
                                COLOR_GRAY, lambda: self.clickLanguageBtn("Bonjour"))

        self.addChildWindow(self.container)
        self.container.addChildWindow(self.greetingText)
        self.container.addChildWindow(self.germanBtn)
        self.container.addChildWindow(self.englishBtn)
        self.container.addChildWindow(self.franchBtn)

    def clickLanguageBtn(self, text):
        self.greetingText.text = text

    def draw(self, ctx):
        super().draw(ctx)
        self.container.draw(ctx)


class Colors(Widget):
    def __init__(self, originX, originY, width, height):
        super().__init__(originX, originY, width, height, 'Colors')
        self.backgroundColor = COLOR_LIGHT_GREEN
        self.container = Container(
            0, 15, width, height-15, "ColorsContainer", 'vertical', 5)
        self.container.layoutAnchors = LayoutAnchor.top | LayoutAnchor.left | LayoutAnchor.bottom | LayoutAnchor.right
        self.addComponents()

    def addComponents(self):
        self.sliderR = Slider(0, 0, self.width, 75, 'SliderR', COLOR_RED)

        self.sliderG = Slider(0, 0, self.width, 75, 'SliderG', COLOR_GREEN)

        self.sliderB = Slider(0, 0, self.width, 75, 'SliderB', COLOR_BLUE)

        self.color = self.mapFromRgbToHex()
        self.colorLabel = Label(0, 0, self.width, 30,
                                'ColorLabel', '', self.color)

        self.colorText = Label(0, 0, self.width, 5,
                               'ColorText', self.color, COLOR_CLEAR)

        self.addChildWindow(self.container)
        self.container.addChildWindow(self.sliderR)
        self.container.addChildWindow(self.sliderG)
        self.container.addChildWindow(self.sliderB)
        self.container.addChildWindow(self.colorLabel)
        self.container.addChildWindow(self.colorText)

    def mapFromRgbToHex(self):
        return '#{:02x}{:02x}{:02x}'.format(int(self.sliderR.value*255), int(self.sliderG.value*255), int(self.sliderB.value*255))

    def draw(self, ctx):
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
        self.buttonHelloWorld = Button(0, 45, width, 25, "HelloWorldButton", "HelloWorld",
                                       COLOR_GRAY, lambda: self.onAppButtonClick(HelloWorld, screen))
        self.buttonColors = Button(0, 15, width, 25, "ColorsButton", "Colors",
                                   COLOR_GRAY, lambda: self.onAppButtonClick(Colors, screen))
        self.buttonCalculator = Button(0, 75, width, 25, "CalculatorButton", "Calculator",
                                       COLOR_GRAY, lambda: self.onAppButtonClick(Calculator, screen))

        # add quit button to exit the app
        self.buttonExit = Button(0, 105, width, 25, "ExitButton", "Quit",
                                 COLOR_RED, lambda: quit())

        self.addChildWindow(self.buttonHelloWorld)
        self.addChildWindow(self.buttonColors)
        self.addChildWindow(self.buttonCalculator)
        self.addChildWindow(self.buttonExit)

    # action after clicking a button with app
    def onAppButtonClick(self, appName, screen):
        # add app to the screen's children
        screen.addChildWindow(appName(10, 10, 200, 300))
        # close the start menu = remove it from parent window
        self.removeFromParentWindow()

    def draw(self, ctx):
        super().draw(ctx)
