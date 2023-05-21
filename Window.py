#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Window System - Submission
by 
"""

from GraphicsEventSystem import *
from WindowManager import *
from collections import namedtuple

AllAnchors = namedtuple('AllAnchors', 'top right bottom left')
LayoutAnchor = AllAnchors(1 << 0, 1 << 1, 1 << 2, 1 << 3)
MIN_WINDOW_WIDTH = 5
MIN_WINDOW_HEIGHT = 5


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

        self.isHidden = False   # indicates if window is currently minimized 
        self.taskbarIconX = None    # position of the window icon on the taskbar 
        self.addDecorations = True  # indicates if decorations should be added to this window (default: True)

        self.layoutAnchors = LayoutAnchor.top | LayoutAnchor.left   # default anchors
        self.minWidth = width   # minimum window width (for resizing)
        self.minHeight = height # minimum window height (for resizing)

    def resize(self, x, y, width, height):
        """
        Resizes the window.
        """
        # apply minimum size constraints
        width = max(width, self.minWidth)
        height = max(height, self.minHeight)

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
                # if not top-left or bottom-left
                if not child.layoutAnchors & LayoutAnchor.top and not child.layoutAnchors & LayoutAnchor.bottom:
                    # change child y coordinate to move along with a vertical axis
                    child.y += dh

            # right anchor
            if child.layoutAnchors & LayoutAnchor.right:
                # if not top-right or bottom-right
                if not child.layoutAnchors & LayoutAnchor.top and not child.layoutAnchors & LayoutAnchor.bottom:
                    # change child y coordinate to move along with a vertical axis
                    child.y += dh
                # change child x coordinate to move along with the right window margin
                child.x += dw

            # top anchor (but not top-left or top-right)
            if child.layoutAnchors & LayoutAnchor.top and not child.layoutAnchors & LayoutAnchor.right and not child.layoutAnchors & LayoutAnchor.left:
                # change child x coordinate to move along with a horizontal axis
                child.x = self.width/2 - child.width/2

            # bottom anchor
            if child.layoutAnchors & LayoutAnchor.bottom:
                # if only bottom anchor (not bottom-left or bottom-right)
                if not child.layoutAnchors & LayoutAnchor.right and not child.layoutAnchors & LayoutAnchor.left:
                    child.x = self.width/2 - child.width/2
                # change child y coordinate to move along with the bottom window margin
                child.y += dh

            # right, left, top, bottom anchors - for windows that have every anchor
            if child.layoutAnchors & LayoutAnchor.right and child.layoutAnchors & LayoutAnchor.left and child.layoutAnchors & LayoutAnchor.top and child.layoutAnchors & LayoutAnchor.bottom:
                # change the width and height
                child.width += dw
                child.height += dh
                # ensure that window coordinates changes when the width is changed
                child.x -= dw
                child.y -= dh
            
            child.resize(child.x, child.y, child.width, child.height)   # recursively resize children

    def addChildWindow(self, window):
        """
        Adds window to its parent window children list (at the end) and sets its parent. 
        """
        self.childWindows.append(window)
        window.parentWindow = self

    def removeFromParentWindow(self):
        """
        Removes window from its parent window.
        """
        self.parentWindow.childWindows.remove(self)
        self.parentWindow = None

    def childWindowAtLocation(self, x, y):
        """
        Returns the top-most child window if there exists any. 
        """
        if self.hitTest(x, y):  # check if the current window contains the provided point
            for child in reversed(self.childWindows):   # search for child windows in a reverse order (top-most to bottom-most)
                # convert the local coordinates to the child window's coordinate system
                childX = x - child.x
                childY = y - child.y
                result = child.childWindowAtLocation(childX, childY)    # recursively check child windows
                if result: 
                    return result   # return the top-most child window found
            return self # if no child window is found, return the current window
        return None

    def hitTest(self, x, y):
        """
        Checks if the window was hit.
        """
        # check if x and y are within bounds [0, width] and [0, height] of the current window
        return 0 <= x <= self.width and 0 <= y <= self.height

    def hitTestDecoration(self, x, y):
        """
        Checks if the window decoration was hit.
        """
        if self.parentWindow and self.parentWindow.identifier == 'SCREEN_1':     # a window that has a decoration should be a top-level window
            return 0 <= x <= self.width and 0 <= y <= self.parentWindow.windowSystem.windowManager.titleBarHeight

    def hitTestTitleBar(self, x, y):
        """
        Checks if the title bar was hit.
        """
        if self.parentWindow and self.parentWindow.identifier == 'SCREEN_1':    # a window that has a decoration should be a top-level window
            return 0 <= x <= self.width and 0 <= y <= self.parentWindow.windowSystem.windowManager.titleBarHeight

    def hitTestResizeArea(self, x, y):
        """
        Checks if the resize was hit.
        """
        if self.parentWindow and self.parentWindow.identifier == 'SCREEN_1':    # a window that has a decoration should be a top-level window
            return self.width - 10 <= x <= self.width and self.height - 10 <= y <= self.height

    def convertPositionToScreen(self, x, y):
        """
        Converts coordinates from local to global.
        """
        # if this window has no parent, it is already at global screen coordinates
        if not self.parentWindow:
            return x, y

        # if this window has a parent, recursively convert local coordinates to screen coordinates
        else:
            parentX = x + self.x
            parentY = y + self.y
            return self.parentWindow.convertPositionToScreen(parentX, parentY)

    def convertPositionFromScreen(self, x, y):
        """
        Converts coordinates from global to local.
        """
        # if this window has no parent, return its coordinates as they are
        if not self.parentWindow:
            return (x, y)

        # if this window has a parent, recursively convert screen coordinates to local coordinates
        else:
            localX = x - self.x
            localY = y - self.y
            return self.parentWindow.convertPositionFromScreen(localX, localY)

    def draw(self, ctx):
        """
        Draws the plain window.
        """
        ctx.setFillColor(self.backgroundColor)  # draw with the window's background color

        if self.parentWindow:   # check if the window has a parent
            # convert the window's local origin to global coordinates
            screenX, screenY = self.parentWindow.convertPositionToScreen(
                self.x, self.y)
        else:
            # if the window has no parent, its origin is already in global coordinates
            screenX = self.x
            screenY = self.y

        # set the origin to the global coordinates
        ctx.setOrigin(screenX, screenY)

        # draw a filled rectangle in the window's local coordinate system
        ctx.fillRect(0, 0, self.width, self.height)

        # draw every child window
        for child in self.childWindows:
            child.draw(ctx)

    def handleMouseClicked(self, x, y):
        print('Window ' + self.identifier + ' was clicked.')


class Screen(Window):
    def __init__(self, windowSystem):
        super().__init__(0, 0, windowSystem.width, windowSystem.height, 'SCREEN_1')
        self.windowSystem = windowSystem

    def draw(self, ctx):
        """
        Draws the desktop (with wallpaper), taskbar and screen children.
        """
        # draw wallpaper and task bar
        self.windowSystem.windowManager.drawDesktop(ctx)
        self.windowSystem.windowManager.drawTaskbar(ctx)

        # draw child windows and decorations
        for child in self.childWindows:
            if not child.isHidden:
                child.draw(ctx)
                if child.addDecorations:
                    self.windowSystem.windowManager.decorateWindow(child, ctx)

    def windowDecorationAtLocation(self, x, y):
        """
        Checks if there exist a decoration at a given location.
        """
        for child in reversed(self.childWindows):
            localX, localY = child.convertPositionFromScreen(x, y)
            if child.hitTestTitleBar(localX, localY):   # if there is a title bar
                return child, False
            elif child.hitTestResizeArea(localX, localY):   # if there is a resize indicator
                return child, True

        return None, False
