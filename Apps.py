





from GraphicsEventSystem import *
from Window import *
from UITK import *
from functools import partial

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

        self.current_input = ""
        self.buttons = [
            'C', '+/-', '%', '/',
            '7', '8', '9', '*',
            '4', '5', '6', '-',
            '1', '2', '3', '+',
            '0', '00','.', '='
        ]
       
        self.container = Container(0,10+(height-10)*0.2,width,(height-10)*0.8,"Calculator Container",'vertical',0)
        self.label = Label(0, 10, width,(height-10)*0.2, "Label", "0", COLOR_CLEAR)
        
        for i in range(5):
            childContainer = Container(0,0,self.width,self.height,"container"+str(i),'horizontal',0)
            self.container.addChildWindow(childContainer)

        button_row = 0
        button_column = 0

        for btn_text in self.buttons :
            
            # store callable object with partcial
            button = Button(0, 0, 50, 50, btn_text, btn_text, COLOR_LIGHT_GRAY,partial(self.button_clicked,btn_text))
            
            if button_row == 0 or button_column == 3:
                button.normalColor = '#f7e436'
            
            self.container.childWindows[button_row].addChildWindow(button)
            button_column += 1

            
            if button_column > 3:
                button_column = 0
                button_row += 1

        
        self.addChildWindow(self.container)
        self.addChildWindow(self.label)
        
        

    def button_clicked(self, text):
        self.process_input(text)

    
    def key_pressed(self, key): 
        
        if key == "":
            key = '='

        if key in self.buttons :
             self.process_input(key)
        
       

    def process_input(self, key):
        
        if key == 'C':
            self.current_input = ""
        elif key == '+/-':
            
            self.current_input = str(int(self.current_input)*-1)
        elif key == '=':
            try:
        
                result = eval(self.current_input)
                self.current_input = str(result)
            except ZeroDivisionError:
                self.current_input = "Error: Division by zero"
            except :
                self.current_input = "Error"
        else:
            self.current_input += key
        
        self.label.text = self.current_input

    def draw(self,ctx):
        
        super().draw(ctx)      
        self.container.draw(ctx)

