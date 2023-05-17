





from GraphicsEventSystem import *
from Window import *
from UITK import *


class App(Widget) :
    def __init__(self, originX, originY, width, height, identifier):
        super().__init__(originX, originY, width, height, identifier)
        self.backgroundColor = COLOR_CLEAR

class HelloWorld(App) :
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
        
class Calculator(App) :
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

