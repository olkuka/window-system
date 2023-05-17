#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from GraphicsEventSystem import *
from Window import *
from UITK import *


class HelloWorld(Widget):
    def __init__(self, originX, originY, width, height, identifier):
        super().__init__(originX, originY, width, height, identifier)
        self.backgroundColor = COLOR_WHITE
       
        self.container = Container(25,0,width-100,height-50,"HelloWorldContainer",'vertical',10)
        self.greetingText = Label(0, 0, 10, 10, "text", "Select a language!", COLOR_CLEAR)
        self.germanBtn = Button(0, 0, 200, 51, "Btn1", "Deutsch", COLOR_GRAY, lambda: self.clickLanguageBtn("Guten Tag"))
        self.englishBtn = Button(0, 0, 200, 51, "Btn2", "English", COLOR_GRAY, lambda: self.clickLanguageBtn("Good morning"))
        self.franchBtn = Button(0, 0, 200, 51, "Btn3", "Français", COLOR_GRAY, lambda: self.clickLanguageBtn("Bonjour"))
       
        self.quitBtn = Button(self.width-50, self.height-30, 40, 20, "quitBtn", "Quit", COLOR_GRAY, lambda: self.removeFromParentWindow())
        
        self.addChildWindow(self.container)
        self.container.addChildWindow(self.greetingText)
        self.container.addChildWindow(self.germanBtn)
        self.container.addChildWindow(self.englishBtn)
        self.container.addChildWindow(self.franchBtn)
        self.addChildWindow(self.quitBtn)
   
    def clickLanguageBtn(self,text):
        self.greetingText.text = text

    def draw(self,ctx):
        super().draw(ctx)
        
class Calculator(Widget) :
    def __init__(self, originX, originY, width, height, identifier):
        super().__init__(originX, originY, width, height, identifier)
        self.backgroundColor = COLOR_WHITE
       
        self.container = Container(originX,originY,width,height,"Calculator Container",'grid',0)
        self.greetingText = Label(0, 0, 10, 10, "text", "Hello", COLOR_GRAY)
        self.germanBtn = Button(0, 0, 200, 51, "Btn1", "Deutsch", COLOR_GRAY, lambda: self.clickLanguageBtn("Guten Tag"))
        self.englishBtn = Button(0, 0, 200, 51, "Btn2", "English", COLOR_GRAY, lambda: self.clickLanguageBtn("Good morning"))
        self.franchBtn = Button(0, 0, 200, 51, "Btn3", "Français", COLOR_GRAY, lambda: self.clickLanguageBtn("Bonjour"))
       
        self.addChildWindow(self.container)
        self.container.addChildWindow(self.greetingText)
        self.container.addChildWindow(self.germanBtn)
        self.container.addChildWindow(self.englishBtn)
        self.container.addChildWindow(self.franchBtn)
   
    def clickLanguageBtn(self,text):
        self.greetingText.text = text

    def draw(self,ctx):
        super().draw(ctx)      
        self.container.draw(ctx)


class Colors(Widget):
    def __init__(self, originX, originY, width, height, titleBarHeight):
        super().__init__(originX, originY, width, height, 'Colors')
        self.backgroundColor = COLOR_LIGHT_GREEN
        self.container = Container(0, 15, width, height, "ColorsContainer",'vertical', 30)
        self.addComponents()

    def addComponents(self):
        self.sliderR = Slider(0, 0, self.width, 60, 'SliderR', COLOR_RED)
        self.sliderG = Slider(0, 0, self.width, 30, 'SliderG', COLOR_GREEN)
        self.sliderB = Slider(0, 0, self.width, 30, 'SliderB', COLOR_BLUE)
        self.color = self.mapFromRgbToHex()
        self.colorLabel = Label(0, 0, self.width -
                           30, 30, 'ColorLabel', '', self.color)
        self.colorText = Label(0, 0, self.width -
                           30, 5, 'ColorText', self.color, COLOR_CLEAR)

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
        self.sliderR.draw(ctx)
        self.sliderG.draw(ctx)
        self.sliderB.draw(ctx)
        self.color = self.mapFromRgbToHex()
        self.colorLabel.normalColor = self.color
        self.colorText.text = self.color
        self.colorLabel.draw(ctx)
        self.colorText.draw(ctx)
