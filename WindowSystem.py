#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Window System - Submission
by  
"""

from GraphicsEventSystem import *
from Window import *
from WindowManager import *
from UITK import *


class WindowSystem(GraphicsEventSystem):
    def start(self):
        self.screen = Screen(self)
        self.windowManager = WindowManager(self)

        # add some windows to test
        s2 = self.createWindowOnScreen(10, 10, 200, 200, "First App")
        s2.backgroundColor = COLOR_GREEN

        s3 = self.createWindowOnScreen(50, 50, 500, 200, "Second App")
        s3.backgroundColor = COLOR_YELLOW

        s4 = self.createWindowOnScreen(300, 200, 300, 300, "My Third App")
        s4.backgroundColor = COLOR_PINK

        # s4_1 = Window(10, 30, 200, 100, "SCREEN_3-1")
        # s4.addChildWindow(s4_1)
        # s4_1.backgroundColor = COLOR_BLACK

        Label1 = Label(0, 30, 50, 50, "Label 1", "hi", COLOR_WHITE)
        s4.addChildWindow(Label1)

        btn1 = Button(50, 60, 51, 51, "Btn1", "print",
                      COLOR_GRAY, lambda: print("clicked!"))
        s4.addChildWindow(btn1)

        slider = Slider(30, 30, 250, 100, 'Slider 1')
        s3.addChildWindow(slider)
        # s4_2 = Window(290, 290, 100, 100, "SCREEN_3-2")
        # s4.addChildWindow(s4_2)
        # s4_2.backgroundColor = COLOR_BLACK
        # s4_2.layoutAnchors = LayoutAnchor.right | LayoutAnchor.bottom

        # s4_3 = Window(150, 150, 100, 100, "SCREEN_3-3")
        # s4.addChildWindow(s4_3)
        # s4_3.backgroundColor = COLOR_BLACK
        # s4_3.layoutAnchors = LayoutAnchor.left | LayoutAnchor.right

    """
    WINDOW MANAGEMENT
    """

    def createWindowOnScreen(self, x, y, width, height, identifier):
        window = Window(x, y, width, height, identifier)
        # add a new window as a screen's child
        self.screen.addChildWindow(window)
        return window

    def bringWindowToFront(self, window):
        currWindow = window
        # check if the window is a top-level window
        # if yes, remove it and add to the end of the child windows list of the screen
        if window.parentWindow == self.screen:
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
        # draw the screen and all of its child windows
        self.screen.draw(self.graphicsContext)

    """
    INPUT EVENTS
    """

    def handleMousePressed(self, x, y):
        # store the current mouse press coordinates
        self.mousePressX = x
        self.mousePressY = y

        # check the window at the given location
        window = self.screen.childWindowAtLocation(x, y)
        self.bringWindowToFront(window)

        if type(window) is Button:
            window.BtnState = BtnState.Pressed

        elif type(window) is Slider:
            localX, localY = window.convertPositionFromScreen(x, y)
            if window.checkHandlePressed(localX, localY):
                window.isHandlePressed = True

        self.requestRepaint()

    def handleMouseReleased(self, x, y):
        # check if the mouse release coordinates match the mouse press coordinates
        if x == self.mousePressX and y == self.mousePressY:
            # check the window Decoration at the given location and then return that window
            decorationClicked, isResizable = self.screen.windowDecorationAtLocation(
                x, y)
            windowTaskbarIconClicked = self.windowManager.hitTaskbarIcon(x, y)

            # if there is a Window Decoration, Window Manager handles the event
            if decorationClicked and isResizable == False:
                localX, localY = decorationClicked.convertPositionFromScreen(
                    x, y)
                self.windowManager.handleMouseClicked(
                    decorationClicked, localX, localY)
                self.requestRepaint()

            # if a window taskbar icon is clicked, Window Manager handles the event
            # if a window taskbar icon is clicked, Window Manager handles the event
            elif windowTaskbarIconClicked:
                # set isHidden property to False and call handleMouseClicked to bring the window to the front
                windowTaskbarIconClicked.isHidden = False
                self.windowManager.handleMouseClicked(
                    windowTaskbarIconClicked, 0, 0)
                self.requestRepaint()
            else:
                # check the window at the given location
                windowClicked = self.screen.childWindowAtLocation(x, y)

                # if there exists a window at the given location
                if windowClicked:
                    if type(windowClicked) is Button:
                        windowClicked.action()
                        windowClicked.BtnState = BtnState.Hovering
                        self.requestRepaint()
                    # propagate the click event to the window
                    windowClicked.handleMouseClicked(x, y)
                else:
                    self.screen.handleMouseClicked(x, y)

    def handleMouseMoved(self, x, y):
        # check the window at the given location
        window = self.screen.childWindowAtLocation(x, y)
        self.setAllBtnNormal(self.screen)
        if type(window) is Button:
            window.BtnState = BtnState.Hovering
        # else :
        #     self.setAllBtnNormal(self.screen)

        self.requestRepaint()

    def setAllBtnNormal(self, window):

        for child in window.childWindows:
            if type(child) is Button:
                child.BtnState = BtnState.Normal

    def setAllBtnNormal(self, window):

        for child in window.childWindows:
            if type(child) is Button:
                child.BtnState = BtnState.Normal

            self.setAllBtnNormal(child)

            self.setAllBtnNormal(child)

    def handleMouseDragged(self, x, y):
        # check if user pressed on the title bar
        windowDecoration, isResizeble = self.screen.windowDecorationAtLocation(
            self.mousePressX, self.mousePressY)
        window = self.screen.childWindowAtLocation(x, y)

        if windowDecoration:
            # calculate the distances between previous and current mouse locations
            deltaX = x - self.mousePressX
            deltaY = y - self.mousePressY

            # calculate new window coordinates based on above distances
            newX = windowDecoration.x + deltaX
            newY = windowDecoration.y + deltaY

            # calculate new window size based on above distances
            newWidth = max(windowDecoration.width + deltaX, MIN_WINDOW_WIDTH)
            newHeight = max(windowDecoration.height +
                            deltaY, MIN_WINDOW_HEIGHT)

            if isResizeble:
                windowDecoration.resize(
                    windowDecoration.x, windowDecoration.y, newWidth, newHeight)

            # if the new position of the window is within the valid bounds
            elif self.windowManager.checkWindowPosition(windowDecoration, newX, newY):
                # set window coordinates to the new ones
                windowDecoration.x = newX
                windowDecoration.y = newY

            # request a repaint
            self.requestRepaint()

        elif type(window) is Slider:
            # calculate new handle coordinates based on above distances
            localX, _ = window.convertPositionFromScreen(x, y)
            window.slideHandle(localX)
            self.requestRepaint()

        # save current coordinates, so they can be used in the next drag to calculate the distance
        self.mousePressX = x
        self.mousePressY = y

    def handleKeyPressed(self, char):
        pass


# Let's start your window system!
w = WindowSystem(800, 600)
