#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from GraphicsEventSystem import *
from UITK import *


class Colors(Widget):
    def __init__(self, originX, originY, width, height, titleBarHeight):
        super().__init__(originX, originY, width, height, 'Colors')
        self.backgroundColor = COLOR_LIGHT_GREEN
        self.windowTitleBarHeight = titleBarHeight

    def draw(self, ctx):
        super().draw(ctx)
        # container = Container(self.x, self.y + self.windowTitleBarHeight, self.width, self.height-self.windowTitleBarHeight, 'ColorsContainer', 'vertical', 15)
        # sliderR = Slider(self.x + 15, self.y + self.windowTitleBarHeight + 30, self.width - 30, 30, 'SliderR', COLOR_RED)
        # sliderG = Slider(self.x + 15, self.y + self.windowTitleBarHeight + 70, self.width - 30, 30, 'SliderR', COLOR_GREEN)
        # sliderB = Slider(self.x + 15, self.y + self.windowTitleBarHeight + 110, self.width - 30, 30, 'SliderR', COLOR_BLUE)
        btn1 = Button(self.x + 15, self.y + self.windowTitleBarHeight + 110, self.width - 30, 30, "Btn1", "print",
                      COLOR_GRAY, lambda: print("clicked!"))
        self.addChildWindow(btn1)
        # btn1.draw(ctx)
        # sliderR.draw(ctx)
        # sliderG.draw(ctx)
        # sliderB.draw(ctx)

        # sliderG
        # sliderB