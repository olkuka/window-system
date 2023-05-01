#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Window System - Submission
by 
"""

from GraphicsEventSystem import *
from WindowManager import *

class Window:
    def __init__(self, originX, originY, width, height, identifier):
        self.x = originX
        self.y = originY
        self.width = width
        self.height = height
        self.identifier = identifier
        
        # self.backgroundColor = COLOR_LIGHT_GRAY
        self.childWindows = []
        self.parentWindow = None
     
    def addChildWindow(self, window):
        # add window to the end of childWindows list
        self.childWindows.append(window)
        # assign window parent
        window.parentWindow = self
        
    def removeFromParentWindow(self):
        # remove window from the childWindows list
        self.parentWindow.childWindows.remove(self)
        # set window parent to None
        self.parentWindow = None
        
    def childWindowAtLocation(self, x, y):
        # check if the current window contains the provided point
        if self.hitTest(x, y):
            # search for child windows in reverse order (topmost to bottommost)
            for child in reversed(self.childWindows):
                # convert the local coordinates to the child window's coordinate system
                childX = x - child.x
                childY = y - child.y
                # recursively check child windows
                result = child.childWindowAtLocation(childX, childY)
                # return the topmost child window found
                if result:
                    return result 
            # if no child window is found, return the current window
            return self
        else:
            return None

    def hitTest(self, x, y):
        # if x and y are in a local coordinate system
        # it's sufficient to check if x and y are within bounds 
        # [0, width] and [0, height] of the current window 
        return 0 <= x <= self.width and 0 <= y <= self.height
    
    def convertPositionToScreen(self, x, y):
        localX = x
        localY = y
        # if this window has no parent, it is already at global screen coordinates
        if not self.parentWindow:
            return localX, localY
        
        # if this window has a parent, recursively convert local coordinates to screen coordinates
        else :
            parentX = localX + self.x 
            parentY = localY + self.y
            return self.parentWindow.convertPositionToScreen(parentX, parentY) 
    
    def convertPositionFromScreen(self, x, y):
        # if this window has no parent, return its coordinates as they are
        if not self.parentWindow:
            return (x, y)
        
        # if this window has a parent, recursively convert screen coordinates to local coordinates
        else:
            localX = x - self.x
            localY = y - self.y
            return self.parentWindow.convertPositionFromScreen(localX, localY)
        
    def draw(self, ctx):
        # set to draw with the window's background color
        # ctx.setFillColor(self.backgroundColor)
        
        # Check if the window has a parent
        if self.parentWindow:
            # Convert the window's local origin to global coordinates
            screenX, screenY = self.parentWindow.convertPositionToScreen(self.x, self.y)
        else:
            # If the window has no parent, its origin is already in global coordinates
            screenX = self.x
            screenY = self.y

        # Set the graphics context's origin to the global coordinates
        ctx.setOrigin(screenX, screenY)

        # Draw a filled rectangle in the window's local coordinate system
        # ctx.fillRect(0, 0, self.width, self.height)

        # draw every child window
        for child in self.childWindows:
            child.draw(ctx)
    
    def handleMouseClicked(self, x, y):
        print("Window " + self.identifier + " was clicked.")
        

class Screen(Window):
    def __init__(self, windowSystem):
        super().__init__(0, 0, windowSystem.width, windowSystem.height, "SCREEN_1")
        self.windowSystem = windowSystem
        self.windowManager = WindowManager(self.windowSystem) # new instance of WindowManager

        
    def draw(self, ctx):
        self.windowManager.drawDesktop(ctx)
        super().draw(ctx)
    