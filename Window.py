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
        
    def childWindowAtLocation(self, x, y):
        return None
    
    def hitTest(self, x, y):
        return False
    
    def convertPositionToScreen(self, x, y):
        if self.parentWindow is not None:
            # If this window has a parent, recursively convert local coordinates to screen coordinates
            screenX, screenY = self.parentWindow.convertPositionToScreen(self.x, self.y)
            return screenX + x, screenY + y
        else:
            # If this window has no parent, it is already at global screen coordinates
            return self.x + x, self.y + y
    
    def convertPositionFromScreen(self, x, y):
        if self.parentWindow is not None:
            # If this window has a parent, convert screen coordinates to parent coordinates
            parentX, parentY = self.parentWindow.convertPositionFromScreen(x, y)
            return parentX - self.x, parentY - self.y
        else:
            # If this window has no parent, it is already at global screen coordinates, so just subtract its position from the screen coordinates
            return x - self.x, y - self.y
    
    
    def draw(self, ctx):
        pass
    
    
    
    def handleMouseClicked(self, x, y):
        print("Window " + self.identifier + " was clicked.")
        



class Screen(Window):
    def __init__(self, windowSystem):
        super().__init__(0, 0, windowSystem.width, windowSystem.height, "SCREEN_1")
        self.windowSystem = windowSystem

        
    def draw(self, ctx):
        super().draw(ctx)
    