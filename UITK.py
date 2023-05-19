#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Window System - Submission
by  Student Name 1 (#999999)
and Student Name 2 (#999999)
"""

from GraphicsEventSystem import *
from Window import *
import enum


class Widget(Window):
    def __init__(self, originX, originY, width, height, identifier):
        super().__init__(originX, originY, width, height, identifier)
        self.backgroundColor = COLOR_CLEAR


class Container(Widget):
    def __init__(self, originX, originY, width, height, identifier, axis='horizontal', spacing=0):
        super().__init__(originX, originY, width, height, identifier)
        self.axis = axis
        self.spacing = spacing

    def addChildWindow(self, window):
        super().addChildWindow(window)
        self.layoutChildren()

    def removeFromParentWindow(self):
        super().removeFromParentWindow()
        self.layoutChildren()

    def layoutChildren(self):
        numChildren = len(self.childWindows)
        if numChildren == 0:
            return
        
        totalSpacing = self.spacing * (numChildren - 1)

        if self.axis == 'horizontal':
            self.minWidth = MIN_WINDOW_WIDTH*numChildren
            self.minHeight = MIN_WINDOW_HEIGHT
            if self.width < totalSpacing:
                return  # Not enough space to distribute equally
            for i, child in enumerate(self.childWindows):
                child.width = (self.width - totalSpacing) // numChildren
                child.height = self.height
                child.x = i * (child.width + self.spacing)
                child.y = 0

        elif self.axis == 'vertical':
            self.minWidth = MIN_WINDOW_WIDTH
            self.minHeight = MIN_WINDOW_HEIGHT*numChildren
            # spaces between children, on the top and on the bottom
            if self.height < totalSpacing:
                return  # Not enough space to distribute equally
            for i, child in enumerate(self.childWindows):
                child.width = self.width
                child.height = (self.height - totalSpacing) // numChildren
                child.x = 0
                child.y = i * (child.height + self.spacing)

    def resize(self, x, y, width, height):
        numChildren = len(self.childWindows)
        if numChildren == 0:
            return

        # apply minimum size constraints
        height = max(height, self.minHeight)
        width = max(width, self.minWidth)

        # calculate the differences between current width/height and previous width/height
        dw = width - self.width
        dh = height - self.height

        totalSpacing = self.spacing * (numChildren - 1)

        if self.axis == 'horizontal':
            for i, child in enumerate(self.childWindows):
                child.resize(child.x ,child.y,self.width,child.height)
                child.width = (self.width  - totalSpacing) // numChildren
                child.height = self.height + dh
                child.x = i * (child.width + self.spacing)
                child.y = 0
                

        elif self.axis == 'vertical':
            for i, child in enumerate(self.childWindows):
                child.resize(child.x ,child.y,child.width,child.height)
                child.width = self.width + dw
                child.height = (self.height - totalSpacing) // numChildren
                child.x = 0
                child.y = i * (child.height + self.spacing)
                child.resize(child.x ,child.y,child.width,child.height)
        

class Label(Widget):
    def __init__(self, originX, originY, width, height, identifier, text, backgroundColor):
        super().__init__(originX, originY, width, height, identifier)

        self.normalColor = backgroundColor
        self.backgroundColor = self.normalColor
        self.text = text
        self.textColor = COLOR_BLACK

    def draw(self, ctx):
        super().draw(ctx)
        ctx.setFont(None)
        ctx.setStrokeColor(self.textColor)
        ctx.drawString(self.text, (self.width-len(self.text)*7) /
                       2, (self.height-14)/2)


class Button(Label):
    def __init__(self, originX, originY, width, height, identifier, text, backgroundColor, action):
        super().__init__(originX, originY, width, height, identifier, text, backgroundColor)
        self.backgroundColor = backgroundColor
        self.action = action
        self.BtnState = BtnState.Normal

    def draw(self, ctx):
        if self.BtnState == BtnState.Normal:
            self.backgroundColor = self.normalColor
        if self.BtnState == BtnState.Hovering:
            self.backgroundColor = COLOR_BLUE
        if self.BtnState == BtnState.Pressed:
            self.backgroundColor = COLOR_DARK_BLUE

        super().draw(ctx)

        # draw a button's frame
        ctx.setStrokeColor(COLOR_WHITE)
        ctx.drawLine(0, 0, self.width, 0)
        ctx.drawLine(0, 0, 0, self.height)

        ctx.setStrokeColor(COLOR_GRAY)
        ctx.drawLine(self.width-1, 0, self.width-1, self.height)
        ctx.drawLine(0, self.height, self.width-1, self.height)

        ctx.setStrokeColor(COLOR_BLACK)
        ctx.drawLine(self.width, 0, self.width, self.height)
        ctx.drawLine(0, self.height, self.width, self.height)


# Using enum class to define the possible states of a button widget.
class BtnState(enum.Enum):
    Normal = 1
    Hovering = 2
    Pressed = 3


class Slider(Widget):
    def __init__(self, originX, originY, width, height, identifier, backgroundColor=COLOR_LIGHT_GRAY):
        super().__init__(originX, originY, width, height, identifier)
        self.backgroundColor = backgroundColor

        self.isHandlePressed = False  # if the slider is currently pressed
        self.handleX = min(6, self.width)  # handle X coordinate
        self.handleY = min(6, self.height)  # handle Y coordinate
        self.handleWidth = self.width/6
        self.handleHeight = self.height/2

        # inner rectangle
        self.innerX1 = 5
        self.innerY1 = 5

        self.value = 0  # sliders value
    
    def resize(self, x, y, width, height):
        
        dw = width - self.width 
        self.handleX -= dw
        print(dw)
        # super().resize(x, y, width, height)
    
    def draw(self, ctx):
        # draw the background
        super().draw(ctx)

        # these properties that have to be set here because they depend on width/height and
        # they have to change their values every time user resizes the window
        self.handleWidth = self.width//6
        self.handleHeight = self.height//2
        self.innerX2 = max(self.innerX1, self.width - self.innerX1)
        self.innerY2 = max(self.innerY1, self.innerY1 + self.handleHeight)

        # draw the inner rectangle and its borders
        ctx.setFillColor('#CECECE')
        ctx.fillRect(self.innerX1, self.innerY1, self.innerX2, self.innerY2)
        ctx.setStrokeColor(COLOR_GRAY)
        ctx.drawLine(self.innerX1, self.innerY1, self.innerX2, self.innerY1)
        ctx.drawLine(self.innerX1, self.innerY1, self.innerX1, self.innerY2)
        ctx.setStrokeColor(COLOR_WHITE)
        ctx.drawLine(self.innerX1, self.innerY2, self.innerX2, self.innerY2)
        ctx.drawLine(self.innerX2, self.innerY1, self.innerX2, self.innerY2)

        # draw the handle and its borders
        if self.isHandlePressed:
            ctx.setFillColor(COLOR_DARK_BLUE)
        else:
            ctx.setFillColor(COLOR_WHITE)

        ctx.fillRect(self.handleX, self.handleY, self.handleX +
                     self.handleWidth, self.handleY + self.handleHeight)

    # check if x and y coordinates are on the slider's handle
    def checkHandlePressed(self, x, y):
        return 0 <= x - self.handleX <= self.handleWidth and 0 <= y - self.handleY <= self.height

    def slideHandle(self, newX):
        # check if the new X coordinate is within the inner rectangle
        if self.innerX1 <= newX <= self.innerX2 - self.handleWidth:
            self.isHandlePressed = True
            # assign new X coordinate
            self.handleX = newX
            # update slider's value based on a current handle position
            self.value = (self.handleX - self.innerX1) / \
                (self.innerX2 - self.innerX1 - self.handleWidth)
        else:
            self.isHandlePressed = False
