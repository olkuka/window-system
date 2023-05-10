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
    def resize(self, x, y, width, height):
        super().resize(x, y, width, height)


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
    def __init__(self, originX, originY, width, height, identifier, backgroundColor=COLOR_LIGHT_GRAY):
        super().__init__(originX, originY, width, height, identifier)
        self.backgroundColor = backgroundColor

    def draw(self, ctx):
        # draw the background
        super().draw(ctx)

        # draw the inner rectangle and its borders
        borderX1 = 5
        borderX2 = max(borderX1, self.width - borderX1)
        borderY1 = 5
        borderY2 = max(borderY1, self.height - borderY1)
        ctx.setFillColor('#CECECE')
        ctx.fillRect(borderX1, borderY1, borderX2, borderY2)
        ctx.setStrokeColor(COLOR_GRAY)
        ctx.drawLine(borderX1, borderY1, borderX2, borderY1)
        ctx.drawLine(borderX1, borderY1, borderX1, borderY2)
        ctx.setStrokeColor(COLOR_WHITE)
        ctx.drawLine(borderX1, borderY2, borderX2, borderY2)
        ctx.drawLine(borderX2, borderY1, borderX2, borderY2)

        # draw slider white rectangle and its borders
        sliderWidth = self.width//6
        ctx.setFillColor(COLOR_WHITE)
        ctx.fillRect(borderX1+1, borderY1+1, borderX1 +
                     sliderWidth-1, borderY2+1)
        ctx.setStrokeColor(COLOR_LIGHT_GRAY)
        ctx.drawLine(borderX1+1, borderY1+2, borderX1 +
                     sliderWidth-1, borderY1+2)
        ctx.drawLine(borderX1+2, borderY1+1, borderX1+2, borderY2+1)
        ctx.setStrokeColor(COLOR_GRAY)
        ctx.drawLine(borderX1+1, borderY2-1, borderX1+sliderWidth, borderY2-1)
        ctx.drawLine(borderX1+sliderWidth-1, borderY1+2,
                     borderX1+sliderWidth-1, borderY2-1)
