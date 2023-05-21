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
        self.taskBarHeight = 40

    def checkWindowPosition(self, window, x, y):
        """
        Returns true if:
        1) at least half of the title bar is visible in terms of horizontal position, and
        2) the whole title bar is visible in terms of vertical position
        """
        return 0 < x + window.width/2 < self.windowSystem.screen.width and 0 < y < self.windowSystem.screen.height - self.titleBarHeight

    def hitTaskbarIcon(self, x, y):
        """
        Checks if the click is within the taskbar and which window's icon was hit.
        """
        if y >= self.windowSystem.screen.height - self.taskBarHeight:
            for child in self.windowSystem.screen.childWindows:
                if child.identifier != 'StartMenu' and child.taskbarIconX <= x <= child.taskbarIconX + 40:
                    return child
        return None

    def hitStartMenu(self, x, y):
        """
        Checks if the click is within the taskbar and if it's a start menu.
        """
        if y >= self.windowSystem.screen.height - self.taskBarHeight and 0 <= x <= 40:
            return True
        return None

    def decorateWindow(self, window, ctx):
        """
        Adds a title bar with a proper color and minimize, maximize and close button.
        """
        # check if a window's a top-level window by checking if its parent window is the screen
        if window.parentWindow == self.windowSystem.screen:
            # add a title bar and set a different color if it's the foreground window
            # (last on the screen's children list)
            if window == self.windowSystem.screen.childWindows[-1]:
                titleBarColor = COLOR_BLUE
            else:
                titleBarColor = COLOR_LIGHT_BLUE

            ctx.setOrigin(window.x, window.y)

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

            # draw the resize indicator in the bottom-right corner
            ctx.setFillColor(COLOR_BLACK)
            ctx.fillRect(window.width - 10, window.height -
                         10, window.width, window.height)

    def handleMouseClicked(self, window, x, y):
        """
        Handles mouse click on window decorations.
        """
        if window.width - 15 <= x <= window.width - 5 and 5 <= y <= 15:  # check if the close button was clicked
            window.removeFromParentWindow()  # remove window completely

        elif window.width - 45 <= x <= window.width - 35 and 5 <= y <= 15:  # check if minimize button was clicked
            window.isHidden = True  # set isHidden to True and bring the other window to the front
            if len(self.windowSystem.screen.childWindows) > 1:
                self.windowSystem.bringWindowToFront(
                    self.windowSystem.screen.childWindows[-2])

        else:
            self.windowSystem.bringWindowToFront(
                window)    # bring this window to the front

    def drawDesktop(self, ctx):
        """
        Draws a wallpaper.
        """
        ctx.setFillColor(self.wallpaperColor)
        ctx.fillRect(0, 0, self.windowSystem.width, self.windowSystem.height)

    def drawTaskbar(self, ctx):
        """
        Draws a taskbar and icons on it. 
        """
        # draw a taskbar rectangle
        ctx.setFillColor(COLOR_LIGHT_GRAY)
        ctx.fillRect(0, self.windowSystem.height - 40,
                     self.windowSystem.width, self.windowSystem.height)

        # draw a start menu icon
        ctx.setFillColor(COLOR_GRAY)
        ctx.fillRect(0, self.windowSystem.height -
                     40, 40, self.windowSystem.height)

        currX = 42  # draw an icon for every child of the screen
        # sort children alphabetically, so we can have a fixed order
        sortedChildren = sorted(
            self.windowSystem.screen.childWindows, key=lambda child: child.identifier)

        ctx.setFont(Font(family='Helvetica', size=14, weight='normal'))
        # for every child draw its icon
        for child in sortedChildren:
            if child.identifier != 'StartMenu':  # don't draw an icon for a Start Menu because it's already drawn
                # if the window is a top-level window and is not currently hidden, set its color to blue
                if child == self.windowSystem.screen.childWindows[-1] and child.isHidden == False:
                    ctx.setFillColor(COLOR_BLUE)
                # if not - set the color to light blue
                else:
                    ctx.setFillColor(COLOR_LIGHT_BLUE)

                child.taskbarIconX = currX
                ctx.fillRect(currX, self.windowSystem.height - 40,
                             currX + 40, self.windowSystem.height)

                ctx.setStrokeColor(COLOR_WHITE)
                ctx.drawString(
                    child.identifier[0], currX + 13, self.windowSystem.height - 32)
                currX = currX + 42
