





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
       
        self.greetingText = Label(self.width/2, 30, 50, 50, "text", "Hello", COLOR_CLEAR)
        self.germanBtn = Button(50, 60, 51, 51, "Btn1", "print", COLOR_GRAY, lambda: print("clicked!"))
       
        self.addChildWindow(self.greetingText)
        self.addChildWindow(self.germanBtn)
   
    def draw(self,ctx):
        
        super().draw(ctx)
        
        self.greetingText.draw(ctx)
        self.germanBtn.draw(ctx)



