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

    def resize(self, x, y, width, height):
        super().resize(x, y, width, height)
        self.layoutChildren()

    def addChild(self, child):
        self.children.append(child)

    def removeChild(self, child):
        self.children.remove(child)
        self.layoutChildren()

    def layoutChildren(self):
        if self.axis == 'horizontal':
            totalWidth = sum([child.width for child in self.children]
                             ) + self.spacing * (len(self.children) - 1)
            x = self.originX + (self.width - totalWidth) // 2
            y = self.originY
            for child in self.children:
                child.resize(x, y, child.width, child.height)
                x += child.width + self.spacing
        elif self.axis == 'vertical':
            totalHeight = sum([child.height for child in self.children]
                              ) + self.spacing * (len(self.children) - 1)
            x = self.originX
            y = self.originY + (self.height - totalHeight) // 2
            for child in self.children:
                child.resize(x, y, child.width, child.height)
                y += child.height + self.spacing


class Label(Widget):
    def __init__(self, originX, originY, width, height, identifier, text, backgroundColor):
        super().__init__(originX, originY, width, height, identifier)

        self.normalColor = backgroundColor
        self.backgroundColor = self.normalColor
        self.text = text

    def draw(self, ctx):
        super().draw(ctx)
        ctx.setFont(None)
        ctx.setStrokeColor(COLOR_BLACK)
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
    def draw(self, ctx):
        super().draw(ctx)
