#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Window System - Submission
by  Student Name 1 (#999999)
and Student Name 2 (#999999)
"""

from GraphicsEventSystem import *
from Window import *

class WindowManager:
    def __init__(self, windowSystem):
        self.windowSystem = windowSystem
        self.wallpaperColor = COLOR_LIGHT_BLUE
    
    def checkWindowPosition(self, window, x, y):
        pass
    
    
    def decorateWindow(self, window, ctx):
        pass
    
    
    def drawDesktop(self, ctx):
        ctx.setFillColor(self.wallpaperColor)
        ctx.fillRect(0, 0, self.windowSystem.width, self.windowSystem.height)
    
    
    def drawTaskbar(self, ctx):
        pass
        