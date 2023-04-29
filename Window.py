#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Window System - Submission
by  Student Name 1 (#999999)
and Student Name 2 (#999999)
"""

from GraphicsEventSystem import *

class Window:
    def __init__(self, originX, originY, width, height, identifier):
        self.x = originX
        self.y = originY
        self.width = width
        self.height = height
        self.identifier = identifier
        
        self.backgroundColor = COLOR_LIGHT_GRAY
        self.childWindows = []
        self.parentWindow = None
     
    def addChildWindow(self, window):
        self.childWindows.append(window)
        window.parentWindow = self
        
    def removeFromParentWindow(self):
        self.parentWindow.childWindows.remove(self)
        self.parentWindow = None
        
    # def childWindowAtLocation(self, x, y):
    #     # if the window has no children, return None
    #     topMostWindow = None

    #     if self.childWindows:
    #         # iterate through child windows, from the bottom to the top
    #         for childWindow in self.childWindows:
    #             # check if position is within a given child window
    #             # before, convert x and y to the local coordination system of the child window
    #             if childWindow.hitTest(x - childWindow.x, y - childWindow.y):
    #                 # if position is within a given child window, assign window to the variable
    #                 topMostWindow = childWindow
    
    #     # return a topmost found child window or None if no window exists             
    #     return topMostWindow

    
    
    def childWindowAtLocation(self, x, y):
        # Check if the current window contains the provided point
        if self.hitTest(x, y):
            # Search for child windows in reverse order (topmost to bottommost)
            for child in reversed(self.childWindows):
                # Convert the local coordinates to the child window's coordinate system
                childX = x - child.x
                childY = y - child.y
                # Recursively check child windows
                result = child.childWindowAtLocation(childX, childY)
                # Return the topmost child window found
                if result is not None :
                    return result 
            # If no child window is found, return the current window
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

        # If this window has no parent, it is already at global screen coordinates
        if self.parentWindow is None :
            return localX, localY
        
        # If this window has a parent, recursively convert local coordinates to screen coordinates
        else :
            parentX = localX+ self.x 
            parentY = localY+ self.y
            return self.parentWindow.convertPositionToScreen(parentX,parentY) 
    
    def convertPositionFromScreen(self, x, y):

        if self.parentWindow is None:
            return (x, y)
        
        else :
            
            localX = x - self.x
            localY = y - self.y
            
            return self.parentWindow.convertPositionFromScreen(localX, localY)
        
    
    
    def draw(self, ctx):
        # Draw the window's background color
        ctx.setFillColor(self.backgroundColor)

        if self.parentWindow is not None : 
            ScreenX, ScreenY = self.parentWindow.convertPositionToScreen(self.x,self.y)
        else :
            ScreenX = self.x
            ScreenY = self.y
        
        ctx.setOrigin(ScreenX,ScreenY)
        ctx.fillRect(0,0,self.width, self.height)

        # Draw any child windows
        for child in self.childWindows:
            child.draw(ctx)
    
    
    
    def handleMouseClicked(self, x, y):
        print("Window " + self.identifier + " was clicked.")
        



class Screen(Window):
    def __init__(self, windowSystem):
        super().__init__(0, 0, windowSystem.width, windowSystem.height, "SCREEN_1")
        self.windowSystem = windowSystem

        
    def draw(self, ctx):
        super().draw(ctx)
    