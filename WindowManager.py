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
        # return true if:
        # 1) at least half of the title bar is visible in terms of horizontal position, and
        # 2) whole title bar is visible in terms of vertical position
        return 0 < x + window.width/2 < self.windowSystem.screen.width and 0 < y < self.windowSystem.screen.height - self.titleBarHeight

    def hitTaskbarIcon(self, x, y):
        # check if the click is within the taskbar
        if y >= self.windowSystem.screen.height - self.taskBarHeight:
            # if yes - check which window's icon was clicked
            for child in self.windowSystem.screen.childWindows:
                if child.identifier != 'StartMenu' and child.taskbarIconX <= x <= child.taskbarIconX + 40:
                    return child
        return None

    def hitStartMenu(self, x, y):
        # check if the click is within the taskbar and if it's a start menu
        if y >= self.windowSystem.screen.height - self.taskBarHeight and 0 <= x <= 40:
            return True
        return None

    def decorateWindow(self, window, ctx):
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

            # Draw the resize indicator in the bottom-right corner
            ctx.setFillColor(COLOR_LIGHT_GRAY)
            ctx.fillRect(window.width - 10, window.height -
                         10, window.width, window.height)

    def handleMouseClicked(self, window, x, y):
        # check if close button was clicked
        if window.width - 15 <= x <= window.width - 5 and 5 <= y <= 15:
            # remove window completely
            window.removeFromParentWindow()

        # check if minimize button was clicked
        elif window.width - 45 <= x <= window.width - 35 and 5 <= y <= 15:
            # set isHidden to True and bring the other window to the front
            window.isHidden = True
            if len(self.windowSystem.screen.childWindows) > 1:
                self.windowSystem.bringWindowToFront(
                    self.windowSystem.screen.childWindows[-2])

        # if no button was clicked
        else:
            # bring this window to the front
            self.windowSystem.bringWindowToFront(window)

    def drawDesktop(self, ctx):
        ctx.setFillColor(self.wallpaperColor)
        ctx.fillRect(0, 0, self.windowSystem.width, self.windowSystem.height)

    def drawTaskbar(self, ctx):
        # draw a taskbar rectangle
        ctx.setFillColor(COLOR_LIGHT_GRAY)
        ctx.fillRect(0, self.windowSystem.height - 40,
                     self.windowSystem.width, self.windowSystem.height)

        # draw a start menu icon
        ctx.setFillColor(COLOR_GRAY)
        ctx.fillRect(0, self.windowSystem.height -
                     40, 40, self.windowSystem.height)

        # draw an icon for every child of the screen
        currX = 42
        # sort children alphabetically, so we can have a fixed order
        sortedChildren = sorted(
            self.windowSystem.screen.childWindows, key=lambda child: child.identifier)

        ctx.setFont(Font(family="Helvetica", size=14, weight="normal"))
        # for every child draw its icon
        for child in sortedChildren:
            if child.identifier != 'StartMenu':
                # if the window is a top-level window and is not currently hidden, set its color to blue
                if child == self.windowSystem.screen.childWindows[-1] and child.isHidden == False:
                    ctx.setFillColor(COLOR_BLUE)
                # if not - set the color to light blue
                else:
                    ctx.setFillColor(COLOR_LIGHT_BLUE)

                child.taskbarIconX = currX
                ctx.fillRect(currX, self.windowSystem.height - 40,
                             currX + 40, self.windowSystem.height)
                ctx.drawString(
                    child.identifier[0], currX + 13, self.windowSystem.height - 32)
                currX = currX + 42
