#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from GraphicsEventSystem import *
from Window import *
from UITK import *


class HelloWorld(Widget):
    def __init__(self, originX, originY, width, height, identifier):
        super().__init__(originX, originY, width, height, identifier)
        self.backgroundColor = COLOR_WHITE

        self.greetingText = Label(
            self.width/2, 30, 50, 50, "text", "Hello", COLOR_CLEAR)
        self.germanBtn = Button(50, 60, 51, 51, "Btn1",
                                "print", COLOR_GRAY, lambda: print("clicked!"))

        self.addChildWindow(self.greetingText)
        self.addChildWindow(self.germanBtn)

    def draw(self, ctx):
        super().draw(ctx)
        self.greetingText.draw(ctx)
        self.germanBtn.draw(ctx)


class Colors(Widget):
    def __init__(self, originX, originY, width, height, titleBarHeight):
        super().__init__(originX, originY, width, height, 'Colors')
        self.backgroundColor = COLOR_LIGHT_GREEN
        self.addComponents(titleBarHeight)

    def addComponents(self, titleBarHeight):
        self.sliderR = Slider(15, titleBarHeight +
                              30, self.width - 30, 30, 'SliderR', COLOR_RED)
        self.sliderG = Slider(15, titleBarHeight +
                              70, self.width - 30, 30, 'SliderG', COLOR_GREEN)
        self.sliderB = Slider(15, titleBarHeight +
                              110, self.width - 30, 30, 'SliderB', COLOR_BLUE)
        self.color = self.mapFromRgbToHex()
        self.label = Label(80, titleBarHeight + 220, self.width -
                           30, 30, 'color', self.color, COLOR_CLEAR)

        self.addChildWindow(self.sliderR)
        self.addChildWindow(self.sliderG)
        self.addChildWindow(self.sliderB)
        self.addChildWindow(self.label)

    def mapFromRgbToHex(self):
        return '#{:02x}{:02x}{:02x}'.format(int(self.sliderR.value*255), int(self.sliderG.value*255), int(self.sliderB.value*255))

    def draw(self, ctx):
        # container = Container(self.x, self.y + self.windowTitleBarHeight, self.width, self.height-self.windowTitleBarHeight, 'ColorsContainer', 'vertical', 15)
        super().draw(ctx)
        self.sliderR.draw(ctx)
        self.sliderG.draw(ctx)
        self.sliderB.draw(ctx)
        self.color = self.mapFromRgbToHex()

        ctx.setFillColor(self.color)
        ctx.fillRect(30, 50, self.width - 60, 100)

        self.label.text = self.color
        self.label.draw(ctx)
