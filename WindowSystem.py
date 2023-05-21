#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Window System - Submission
by  
"""

from Apps import *
from GraphicsEventSystem import *
from Window import *
from WindowManager import *
from UITK import *
from Apps import *


class WindowSystem(GraphicsEventSystem):
    def start(self):
        self.screen = Screen(self)
        self.windowManager = WindowManager(self)

    """
    WINDOW MANAGEMENT
    """

    def createWindowOnScreen(self, x, y, width, height, identifier):
        """
        Adds a new created window as a screen's child.
        """
        window = Window(x, y, width, height, identifier)
        self.screen.addChildWindow(window)
        return window

    def bringWindowToFront(self, window):
        """
        Finds the top-level window and adds it to the end of the child windows list of the screen.
        """
        currWindow = window
        if window.parentWindow == self.screen:  # check if the window is a top-level window
            # if yes, remove it and add to the end of the child windows list of the screen
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
        """
        Draws the screen and all of its child windows.
        """
        # draw the screen and all of its child windows
        self.screen.draw(self.graphicsContext)

    """
    INPUT EVENTS
    """

    def handleMousePressed(self, x, y):
        """
        Performs actions when the mouse is pressed.
        """
        # store the current mouse press coordinates
        self.mousePressX, self.mousePressY = x, y
        self.clickedX, self.clickedY = x, y

        # check the window at the given location
        window = self.screen.childWindowAtLocation(x, y)
        self.bringWindowToFront(window)

        if type(window) is Button:  # if the returned window is a button
            window.BtnState = BtnState.Pressed  # change it state to 'pressed'

        elif type(window) is Slider:    # if the returned window is a slider
            localX, localY = window.convertPositionFromScreen(x, y)
            # checks if a handle was pressed
            if window.checkHandlePressed(localX, localY):
                window.isHandlePressed = True

        self.requestRepaint()   # request repaint

    def handleMouseReleased(self, x, y):
        """
        Performs actions when the mouse is released.
        """
        # check if the mouse release coordinates match the mouse press coordinates
        if x == self.clickedX and y == self.clickedY:
            decorationClicked, isResizable = self.screen.windowDecorationAtLocation(
                x, y)   # check if there exists a window decoration at the given location
            # check if there exists a taskbar icon at the given location
            windowTaskbarIconClicked = self.windowManager.hitTaskbarIcon(x, y)
            # check if there exists a start menu at the given location
            startMenuClicked = self.windowManager.hitStartMenu(x, y)

            # if there is a window decoration (but not a resize indicator), Window Manager handles the event
            if decorationClicked and isResizable == False:
                localX, localY = decorationClicked.convertPositionFromScreen(
                    x, y)
                self.windowManager.handleMouseClicked(
                    decorationClicked, localX, localY)

            # if a window taskbar icon is clicked, Window Manager handles the event
            elif windowTaskbarIconClicked:
                # set isHidden property to False and call WM handleMouseClicked to bring the window to the front
                windowTaskbarIconClicked.isHidden = False
                self.windowManager.handleMouseClicked(
                    windowTaskbarIconClicked, 0, 0)

            # if a start menu is clidked, add start menu to the screen children
            elif startMenuClicked:
                self.screen.addChildWindow(StartMenu(self.screen))

            else:
                windowClicked = self.screen.childWindowAtLocation(
                    x, y)  # check the window at the given location

                if windowClicked:   # if there exists a window at the given location

                    # if it's a button - call it's action and set state to hovering
                    if type(windowClicked) is Button:
                        windowClicked.action()
                        windowClicked.BtnState = BtnState.Hovering

                    elif type(windowClicked) is Slider:  # if it's a slider
                        windowClicked.isHandlePressed = False

                    # propagate the click event to the window
                    windowClicked.handleMouseClicked(x, y)
                else:
                    # propagate the click event to the screen
                    self.screen.handleMouseClicked(x, y)

            self.requestRepaint()   # request a repaint because something has to change in every case

        else:   # if the mouse release coordinates don't match the mouse press coordinates
            # reset sliders to the default state
            self.resetAllSliders(self.screen)
            # reset buttons to the default state
            self.resetAllButtons(self.screen)

    def handleMouseMoved(self, x, y):
        """
        Performs actions when the mouse is moved.
        """
        self.mousePressX = x
        self.mousePressY = y

        # check the window at the given location
        window = self.screen.childWindowAtLocation(x, y)
        self.resetAllButtons(self.screen)

        # if there exists a button at a given location - call it's action and set state to hovering
        if type(window) is Button:
            window.BtnState = BtnState.Hovering
            self.requestRepaint()

    def handleMouseDragged(self, x, y):
        """
        Performs actions when the mouse is dragged.
        """
        windowDecoration, isResizeble = self.screen.windowDecorationAtLocation(
            self.mousePressX, self.mousePressY)  # check if user pressed on the title bar
        window = self.screen.childWindowAtLocation(x, y)

        if windowDecoration:
            # calculate the distances between previous and current mouse locations
            deltaX = x - self.mousePressX
            deltaY = y - self.mousePressY

            # calculate new window coordinates based on above distances
            newX = windowDecoration.x + deltaX
            newY = windowDecoration.y + deltaY

            # calculate new window size based on above distances
            newWidth = windowDecoration.width + deltaX
            newHeight = windowDecoration.height + deltaY

            if isResizeble:  # if resize indicator is dragged
                windowDecoration.resize(
                    windowDecoration.x, windowDecoration.y, newWidth, newHeight)    # resize the window
                self.requestRepaint()

            # if the taskbar is dragged and the new position of the window is within the valid bounds
            elif self.windowManager.checkWindowPosition(windowDecoration, newX, newY):
                # set window coordinates to the new ones
                windowDecoration.x = newX
                windowDecoration.y = newY
                self.requestRepaint()

        elif type(window) is Slider:
            # calculate new handle coordinates based on above distances
            localX, _ = window.convertPositionFromScreen(x, y)
            # perform action to slide the handle on the screen
            window.slideHandle(localX)
            self.requestRepaint()

        # save current coordinates, so they can be used in the next drag to calculate the distance
        self.mousePressX = x
        self.mousePressY = y

    def handleKeyPressed(self, char):
        """
        Performs actions when the keyboard is pressed.
        """
        pointedWindow = self.screen.childWindows[-1]
        # ensure that keyboard works only in the Calculator app
        if type(pointedWindow) is Calculator:
            pointedWindow.keyPressed(char)
            self.requestRepaint()

    def resetAllButtons(self, window):
        """
        Resets all buttons in a window by setting their states to normal. 
        """
        for child in window.childWindows:
            if type(child) is Button and child.BtnState is not BtnState.Normal:
                child.BtnState = BtnState.Normal
                self.requestRepaint()
            self.resetAllButtons(child)

    def resetAllSliders(self, window):
        """
        Resets all sliders in a window by setting isHandlePressed property to default (False).
        """
        for child in window.childWindows:
            if type(child) is Slider and child.isHandlePressed:
                child.isHandlePressed = False
                self.requestRepaint()
            self.resetAllSliders(child)


# Let's start your window system!
w = WindowSystem(800, 600)
