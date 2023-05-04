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
        self.wallpaperColor = COLOR_PURPLE
        self.titleBarHeight = 20
        
    
    def checkWindowPosition(self, window, x, y):
        # return true if at least some part of the title bar is visible on screen
        return  - window.width < x < self.windowSystem.screen + window.width  and - window.titleBarHeight < y < self.windowSystem.screen +window.titleBarHeight
    
    
    def decorateWindow(self, window, ctx):
        # check if a window's a top-level window by checking if its parent window is the screen
        if window.parentWindow == self.windowSystem.screen:
            # add a title bar and set a different color if it's the foreground window
            # (last on the screen's children list)
            if window == self.windowSystem.screen.childWindows[-1]:
                titleBarColor = COLOR_BLUE
            else:
                titleBarColor = COLOR_LIGHT_BLUE
            ctx.setFillColor(titleBarColor)
            ctx.fillRect(0, 0, window.width, self.titleBarHeight)
            ctx.drawString(window.identifier, 4, 2)
            
            # add a stroked border
            ctx.setStrokeColor(COLOR_LIGHT_GRAY)
            ctx.strokeRect(0, 0, window.width, window.height)

            # add a close button
            ctx.drawLine(window.width - 15, 5, window.width - 5, 15)
            ctx.drawLine(window.width - 15, 15, window.width - 5, 5)

            # add a maximize button
            ctx.strokeRect(window.width - 30, 5, window.width - 20, 15)

            # add a minimize button
            ctx.drawLine(window.width - 45, 10, window.width - 35, 10)
    
    def handleMouseClicked(self, window, x, y):
        print("Window " + window.identifier + "'s Decoration was clicked.")
        
        # check if close button was clicked
        if window.width - 15 <= x <= window.width - 5 and 5 <= y <= 15:
            print('Close button clicked')
            window.removeFromParentWindow()

        # check if minimize button was clicked    
        elif window.width - 45 <= x <= window.width - 35 and 5 <= y <= 15:
            print('Minimize button clicked')
            window.setIsHidden(True)

        # if no button was clicked
        else:
            # bring this window to the front
            self.windowSystem.bringWindowToFront(window)

    def drawDesktop(self, ctx):
        ctx.setFillColor(self.wallpaperColor)
        ctx.fillRect(0, 0, self.windowSystem.width, self.windowSystem.height)
    
    
    def drawTaskbar(self, ctx):
        pass
        