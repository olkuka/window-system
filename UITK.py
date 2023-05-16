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
        self.children = []

    # resize the container
    def resize(self, x, y, width, height):
        super().resize(x, y, width, height)
        self.layoutChildren()

    # add a new child
    def addChild(self, child):
        self.children.append(child)

    # remove a child
    def removeChild(self, child):
        self.children.remove(child)
        self.layoutChildren()

    def layoutChildren(self):
        if self.axis == 'horizontal':
            # calculate the total width of the container taking its children and spacing into account
            totalWidth = sum([child.width for child in self.children]
                             ) + self.spacing * (len(self.children) - 1)
            # set a new x coordinate
            x = self.originX + (self.width - totalWidth) // 2
            y = self.originY

            # resize each children recursively and take care of the spacing
            for child in self.children:
                child.resize(x, y, child.width, child.height)
                x += child.width + self.spacing

        elif self.axis == 'vertical':
            # calculate the total height of the container taking its children and spacing into account
            totalHeight = sum([child.height for child in self.children]
                              ) + self.spacing * (len(self.children) - 1)
            x = self.originX
            # set a new y coordinate
            y = self.originY + (self.height - totalHeight) // 2
            # resize each children recursively and take care of the spacing
            for child in self.children:
                child.resize(x, y, child.width, child.height)
                y += child.height + self.spacing


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
        ctx.drawString(self.text, 0, 0)


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

        # handle properties
        self.handleX = min(6, self.width)  # handle X coordinate
        self.handleY = min(6, self.height)  # handle Y coordinate
        self.handleWidth = self.width//6
        self.handleHeight = self.height//2
        self.isHandlePressed = False  # if the slider is currently pressed

        # inner rectangle coordinates
        self.innerX1 = 5
        self.innerX2 = max(self.innerX1, self.width - self.innerX1)
        self.innerY1 = 5
        self.innerY2 = max(self.innerY1, self.innerY1 + self.handleHeight)

        self.value = 0  # sliders value

    def draw(self, ctx):
        # draw the background
        super().draw(ctx)

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
