#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Window System - Submission
by  Aleksandra Kukawka (#448975)
and Daso Jung (#446806)
"""

from GraphicsEventSystem import *
from Window import *


class WindowSystem(GraphicsEventSystem):
    def start(self):
        self.screen = Screen(self)
   
    """
    WINDOW MANAGEMENT
    """

    def createWindowOnScreen(self, x, y, width, height, identifier):
        window = Window(x, y, width, height, identifier)
        # add a new window as a screen's child
        self.screen.addChildWindow(window)
        return window

    def bringWindowToFront(self, window):
        currWindow = window
        # check if the window is a top-level window
        # if yes, remove it and add to the end of the child windows list of the screen
        if window.parentWindow == self.screen:
            currWindow.removeFromParentWindow()
            self.screen.addChildWindow(currWindow)

        elif window != self.screen:
            # find the top-level parent window
            topParent = window
            while topParent.parentWindow != self.screen:
                topParent = topParent.parentWindow

            # move the top-level parent window to the front in the same way as before
            topParent.removeFromParentWindow()
            self.screen.addChildWindow(topParent)

    """
    DRAWING
    """

    def handlePaint(self):
        # draw the screen and all of its child windows
        self.screen.draw(self.graphicsContext)
        
    
    """
    INPUT EVENTS
    """

    def handleMousePressed(self, x, y):
        # store the current mouse press coordinates
        self.mousePressX = x
        self.mousePressY = y

    def handleMouseReleased(self, x, y):
        # check if the mouse release coordinates match the mouse press coordinates
        if x == self.mousePressX and y == self.mousePressY:
            # check the window at the given location
            windowClicked = self.screen.childWindowAtLocation(x, y)
            # if there exists a window at the given location
            if windowClicked:
                # bring it to the front and request paint
                self.bringWindowToFront(windowClicked)
                self.requestRepaint()
                # propagate the click event to the window
                windowClicked.handleMouseClicked(x, y)
            else:
                self.screen.handleMouseClicked(x,y)
            
    def handleMouseMoved(self, x, y):
        pass

    def handleMouseDragged(self, x, y):
        # clear the mouse press coordinates when mouse is dragged
        self.mousePressX = None
        self.mousePressY = None

    def handleKeyPressed(self, char):
        pass
    
    
# Let's start your window system!
w = WindowSystem(800,600)
