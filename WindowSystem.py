#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Window System - Submission
by  Student Name 1 (#999999)
and Student Name 2 (#999999)
"""

from GraphicsEventSystem import *
from Window import *


class WindowSystem(GraphicsEventSystem):
    def start(self):
        self.screen = Screen(self)
       
        s2 = self.createWindowOnScreen(10,10,100,100,"SCREEN_2")
        s2.backgroundColor = COLOR_BLUE    
    
    """
    WINDOW MANAGEMENT
    """

    def createWindowOnScreen(self, x, y, width, height, identifier):
        window = Window(x, y, width, height, identifier)
        self.screen.addChildWindow(window)
        return window

    def bringWindowToFront(self, window):
        currWindow = window
        while currWindow not in self.screen.childWindows and currWindow != self.screen:
            currWindow = currWindow.parentWindow

        if currWindow != self.screen:
            currWindow.removeFromParentWindow()
            self.screen.addChildWindow(currWindow)

    """
    DRAWING
    """

    def handlePaint(self):
        
        #self.graphicsContext.setFillColor(COLOR_WHITE)
        #self.graphicsContext.fillRect(0, 0, self.width, self.height)

        # Draw the screen and all its child windows
        self.screen.draw(self.graphicsContext)
        
    
    """
    INPUT EVENTS
    """

    def handleMousePressed(self, x, y):
        # check the window at the given location
        windowPressed = self.screen.childWindowAtLocation(x, y)
        # if there exists a window in a given location
        if windowPressed:
            # bring it to the front
            self.bringWindowToFront(windowPressed)

    def handleMouseReleased(self, x, y):
        pass

    def handleMouseMoved(self, x, y):
        pass

    def handleMouseDragged(self, x, y):
        pass

    def handleKeyPressed(self, char):
        pass
        
    
# Let's start your window system!
w = WindowSystem(800,600)
