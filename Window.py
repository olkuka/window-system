#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Window System - Submission
by 
"""

from GraphicsEventSystem import *
from WindowManager import *
from collections import namedtuple

AllAnchors = namedtuple('AllAnchors', "top right bottom left")
LayoutAnchor = AllAnchors(1 << 0, 1 << 1, 1 << 2, 1 << 3)
MIN_WINDOW_WIDTH = 50
MIN_WINDOW_HEIGHT = 50


class Window:
    def __init__(self, originX, originY, width, height, identifier):
        self.x = originX
        self.y = originY
        self.width = width
        self.height = height
        self.identifier = identifier

        self.backgroundColor = None
        self.childWindows = []
        self.parentWindow = None

        self.isHidden = False
        self.taskbarIconX = None

        self.layoutAnchors = LayoutAnchor.top | LayoutAnchor.left

    def resize(self, x, y, width, height):
        # apply minimum size constraints
        width = max(width, MIN_WINDOW_WIDTH)
        height = max(height, MIN_WINDOW_HEIGHT)

        # calculate the differences between current width/height and previous width/height
        dw = width - self.width
        dh = height - self.height

         # set new coordinates, width and height
        self.x = x
        self.y = y
        self.width = width
        self.height = height


        for child in self.childWindows:
            # left anchor
            if child.layoutAnchors & LayoutAnchor.left:
                # if not top-left or bottom-left corner
                if not child.layoutAnchors & LayoutAnchor.top and not child.layoutAnchors & LayoutAnchor.bottom:
                    # change child y coordinate to be exactly at the half of the vertical axis
                    child.y = self.height // 2 - child.height//2

            # right anchor
            if child.layoutAnchors & LayoutAnchor.right:
                # if not top-right or bottom-right corner
                if not child.layoutAnchors & LayoutAnchor.top and not child.layoutAnchors & LayoutAnchor.bottom:
                    # change child y coordinate to be exactly at the half of the vertical axis
                    child.y = self.height // 2 - child.height//2
                # change child x coordinate to move along with the right window margin 
                child.x += dw
            
            # top anchor (but not top-left or top-right)
            if child.layoutAnchors & LayoutAnchor.top and not child.layoutAnchors & LayoutAnchor.right and not child.layoutAnchors & LayoutAnchor.left:
                # change child x coordinate to be exactly at the half of the horizontal axis
                child.x = self.width // 2 - child.width//2

            # bottom anchor
            if child.layoutAnchors & LayoutAnchor.bottom:
                # if only bottom anchor (not bottom-left or bottom-right)
                if not child.layoutAnchors & LayoutAnchor.right and not child.layoutAnchors & LayoutAnchor.left:
                    child.x = self.width // 2 - child.width//2
                # change child y coordinate to move along with the bottom window margin 
                child.y += dh 

            # right, left, top, bottom anchors - for windows that have every anchor
            if child.layoutAnchors & LayoutAnchor.right and child.layoutAnchors & LayoutAnchor.left and child.layoutAnchors & LayoutAnchor.top and child.layoutAnchors & LayoutAnchor.bottom:
                # ensure that window is always in the middle by changing coordinates 
                child.x = self.width // 2 - child.width//2
                child.y = self.height // 2 - child.height//2
                # additionally change the width and the height
                child.width += dw
                child.height += dh

    def addChildWindow(self, window):
        # add window to the end of childWindows list
        self.childWindows.append(window)
        # assign window parent
        window.parentWindow = self

    def removeFromParentWindow(self):
        # remove window from the childWindows list
        self.parentWindow.childWindows.remove(self)
        # set window parent to None
        self.parentWindow = None

    def childWindowAtLocation(self, x, y):
        # check if the current window contains the provided point
        if self.hitTest(x, y):
            # search for child windows in reverse order (topmost to bottommost)
            for child in reversed(self.childWindows):
                # convert the local coordinates to the child window's coordinate system
                childX = x - child.x
                childY = y - child.y
                # recursively check child windows
                result = child.childWindowAtLocation(childX, childY)
                # return the topmost child window found
                if result:
                    return result
            # if no child window is found, return the current window
            return self
        else:
            return None

    def hitTest(self, x, y):
        # if x and y are in a local coordinate system
        # it's sufficient to check if x and y are within bounds
        # [0, width] and [0, height] of the current window
        return 0 <= x <= self.width and 0 <= y <= self.height

    def hitTestDecoration(self, x, y):
        # the given x, y are in a local corrdinate system
        # check if x and y are within its decoration bounds
        # A window that has a decoration should be a Top-level window
        if self.parentWindow != None and self.parentWindow.identifier == "SCREEN_1":
            return 0 <= x <= self.width and 0 <= y <= self.parentWindow.windowSystem.windowManager.titleBarHeight

    def hitTestTitleBar(self, x, y):
        # the given x, y are in a local corrdinate system
        # check if x and y are within title bar
        # A window that has a decoration should be a Top-level window
        if self.parentWindow != None and self.parentWindow.identifier == "SCREEN_1":
            return 0 <= x <= self.width and 0 <= y <= self.parentWindow.windowSystem.windowManager.titleBarHeight

    def hitTestResizeArea(self, x, y):
        # the given x, y are in a local corrdinate system
        # check if x and y are within resize area
        # A window that has a decoration should be a Top-level window
        if self.parentWindow != None and self.parentWindow.identifier == "SCREEN_1":
            return self.width - 10 <= x <= self.width and self.height - 10 <= y <= self.height

    def convertPositionToScreen(self, x, y):
        localX = x
        localY = y
        # if this window has no parent, it is already at global screen coordinates
        if not self.parentWindow:
            return localX, localY

        # if this window has a parent, recursively convert local coordinates to screen coordinates
        else:
            parentX = localX + self.x
            parentY = localY + self.y
            return self.parentWindow.convertPositionToScreen(parentX, parentY)

    def convertPositionFromScreen(self, x, y):
        # if this window has no parent, return its coordinates as they are
        if not self.parentWindow:
            return (x, y)

        # if this window has a parent, recursively convert screen coordinates to local coordinates
        else:
            localX = x - self.x
            localY = y - self.y
            return self.parentWindow.convertPositionFromScreen(localX, localY)

    def draw(self, ctx):
        # set to draw with the window's background color
        ctx.setFillColor(self.backgroundColor)

        # Check if the window has a parent
        if self.parentWindow:
            # Convert the window's local origin to global coordinates
            screenX, screenY = self.parentWindow.convertPositionToScreen(
                self.x, self.y)
        else:
            # If the window has no parent, its origin is already in global coordinates
            screenX = self.x
            screenY = self.y

        # Set the graphics context's origin to the global coordinates
        ctx.setOrigin(screenX, screenY)

        # Draw a filled rectangle in the window's local coordinate system
        ctx.fillRect(0, 0, self.width, self.height)

        # draw every child window
        for child in self.childWindows:
            child.draw(ctx)

    def handleMouseClicked(self, x, y):
        print("Window " + self.identifier + " was clicked.")


class Screen(Window):
    def __init__(self, windowSystem):
        super().__init__(0, 0, windowSystem.width, windowSystem.height, "SCREEN_1")
        self.windowSystem = windowSystem

    def draw(self, ctx):
        # draw wallpaper and task bar
        self.windowSystem.windowManager.drawDesktop(ctx)
        self.windowSystem.windowManager.drawTaskbar(ctx)

        # draw child window and decoration
        for child in self.childWindows:
            if not child.isHidden:
                child.draw(ctx)
                self.windowSystem.windowManager.decorateWindow(child, ctx)

    def windowDecorationAtLocation(self, x, y):
        for child in reversed(self.childWindows):
            localX, localY = child.convertPositionFromScreen(x, y)
            if child.hitTestTitleBar(localX, localY):
                return child, False
            elif child.hitTestResizeArea(localX, localY):
                return child, True

        return None, False
