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

    """
    WINDOW MANAGEMENT
    """

    def createWindowOnScreen(self, x, y, width, height, identifier):
        window = Window(x, y, width, height, identifier)
        self.screen.addChildWindow(window)
        return window

    def bringWindowToFront(self, window):
        currWindow = window
        while currWindow not in self.screen.childWindows and currWindow != self.screen:
            currWindow = currWindow.parentWindow

        if currWindow != self.screen:
            currWindow.removeFromParentWindow()
            self.screen.addChildWindow(currWindow)

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
w = WindowSystem(800, 600)
w.start()
w.createWindowOnScreen(0, 0, 200, 200, 'test_window')

w2 = Window(0, 0, 100, 100, 'child_of_test_window')
w.screen.childWindows[0].addChildWindow(w2)
print(w.screen.childWindows[0].childWindows[0].identifier)

w.createWindowOnScreen(0, 0, 150, 150, 'test_window_2')

# test_window_2 should be a top-level window (last on the list)
print(w.screen.childWindows[1].identifier)
# bring test_window to the front
w.bringWindowToFront(w.screen.childWindows[0])
# test_window should be a top-level window (last on the list)
print(w.screen.childWindows[1].identifier)
