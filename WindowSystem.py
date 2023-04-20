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
    # def start(self):
    #     screen = Screen(self)
    # why start method instead of __init__?
    def __init__(self):
        self.screen = Screen(self)
    
    
    """
    WINDOW MANAGEMENT
    """
        
    def createWindowOnScreen(self, x, y, width, height, identifier):
        window = Window(x, y, width, height, identifier)
        self.screen.childWindows = window.identifier
        return window
    
    def bringWindowToFront(self, window):
        pass

    
    
    """
    DRAWING
    """
    
    def handlePaint(self):
        pass
    
    
    """
    INPUT EVENTS
    """
    
    def handleMousePressed(self, x, y):
        pass
        
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