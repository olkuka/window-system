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
       
        s2 = self.createWindowOnScreen(10,10,200,200,"SCREEN_2")
        s2.backgroundColor = COLOR_BLUE    

      
        s3 = self.createWindowOnScreen(50,50,200,200,"SCREEN_3")
        s3.backgroundColor = COLOR_YELLOW   


        s3_1 = Window(0,0,50,50,"SCREEN_3-1")
        s3.addChildWindow(s3_1)
        s3_1.backgroundColor = COLOR_BLACK

        
        s3_2 = Window(10,10,50,50,"SCREEN_3-2")
        s3.addChildWindow(s3_2)
        s3_2.backgroundColor = COLOR_PINK
        
        x,y = s3.convertPositionFromScreen(75,75) 
        print(x, y)

    
    
    """
    WINDOW MANAGEMENT
    """

    def createWindowOnScreen(self, x, y, width, height, identifier):
        window = Window(x, y, width, height, identifier)
        self.screen.addChildWindow(window)
        return window

    # def bringWindowToFront(self, window):
    #     currWindow = window
    #     while currWindow not in self.screen.childWindows and currWindow != self.screen:
    #         currWindow = currWindow.parentWindow

    #     if currWindow != self.screen:
    #         currWindow.removeFromParentWindow()
    #         self.screen.addChildWindow(currWindow)

    def bringWindowToFront(self, window):
        currWindow = window
        # Check if the window is a top-level window
        if window.parentWindow == self.screen:
            currWindow.removeFromParentWindow()
            self.screen.addChildWindow(currWindow)

        elif window != self.screen:
            # Find the top-level parent window
            topParent = window
            while topParent.parentWindow != self.screen:
                topParent = topParent.parentWindow
            
            # Move the top-level parent window to the front
            topParent.removeFromParentWindow()
            self.screen.addChildWindow(topParent)

    """
    DRAWING
    """

    def handlePaint(self):
        
        # Draw the screen and all its child windows
        self.screen.draw(self.graphicsContext)
        
    
    """
    INPUT EVENTS
    """

    def handleMousePressed(self, x, y):
    # Store the current mouse press coordinates
        self.mousePressX = x
        self.mousePressY = y

    def handleMouseReleased(self, x, y):
        # Check if the mouse release coordinates match the mouse press coordinates
        if x == self.mousePressX and y == self.mousePressY:
            # Check the window at the given location
            windowClicked = self.screen.childWindowAtLocation(x, y)
            # If there is a window at the location
            if windowClicked:
                # Bring it to the front
                self.bringWindowToFront(windowClicked)
                self.requestRepaint( )
                # Propagate the click event to the window
                windowClicked.handleMouseClicked(x, y)
            else :
                self.screen.handleMouseClicked(x,y)
            

    def handleMouseMoved(self, x, y):
        pass

    def handleMouseDragged(self, x, y):
        # Clear the mouse press coordinates when mouse is dragged
        self.mousePressX = None
        self.mousePressY = None

    def handleKeyPressed(self, char):
        pass
        
    
# Let's start your window system!
w = WindowSystem(800,600)
