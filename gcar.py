# -*- coding: utf-8-*-
# Copyright (C) 2020 HandsomeYingyan@gmail.com
# This Plugin is released under GPLV3
# 适用于l298n

import time
import subprocess
import RPi.GPIO as gpio
from robot import logging
from robot.sdk.AbstractPlugin import AbstractPlugin

logger = logging.getLogger(__name__)

class Plugin(AbstractPlugin):
    SLUG = "gcar"
    IS_IMMERSIVE = True #这是一个沉浸式插件
    PIN1=11 #l298n的连接方式
    PIN2=12
    PIN3=13
    PIN4=15
    Immersive_Flag = False #是不是沉浸模式

    def onAsk(self, input):
            if input is not None and any(word in input for word in [u"前进", u"向前", u"前"]):
                self.say('向前进！', cache=True)
                gpio.output(self.PIN1,gpio.LOW)
                gpio.output(self.PIN2,gpio.HIGH)
                gpio.output(self.PIN3,gpio.LOW)
                gpio.output(self.PIN4,gpio.HIGH)
                time.sleep(2)
                self.clean_gpio()
                return

            elif input is not None and any(word in input for word in [u"后退", u"向后", u"后"]):
                self.say('向后退！', cache=True)
                gpio.output(self.PIN1,gpio.HIGH)
                gpio.output(self.PIN2,gpio.LOW)
                gpio.output(self.PIN3,gpio.HIGH)
                gpio.output(self.PIN4,gpio.LOW)
                time.sleep(2)
                self.clean_gpio()
                return

            elif input is not None and any(word in input for word in [u"向左", u"左"]):
                self.say('向左转！', cache=True)
                gpio.output(self.PIN1,gpio.LOW)
                gpio.output(self.PIN2,gpio.HIGH)
                gpio.output(self.PIN3,gpio.HIGH)
                gpio.output(self.PIN4,gpio.LOW)
                time.sleep(2)
                self.clean_gpio()
                return

            elif input is not None and any(word in input for word in [u"向右", u"右"]):
                self.say('向右转！', cache=True)
                gpio.output(self.PIN1,gpio.HIGH)
                gpio.output(self.PIN2,gpio.LOW)
                gpio.output(self.PIN3,gpio.LOW)
                gpio.output(self.PIN4,gpio.HIGH)
                time.sleep(2)
                self.clean_gpio()
                return

            elif input is not None and any(word in input for word in [u"退出", u"出",u"恢复"]):
                self.say("啊好！没开呢!",cache=True)
                self.clean_gpio()
                time.sleep(1)
                self.clearImmersive()
                self.say("沉浸式模式已退出！",cache=True)
                return

            else: #错误处理
                self.say('完了，你到底在说什么啊我听不清楚啊！', cache=True)
                return


    def handle(self, text, parsed):
        self.init_gpio()
        self.install_gpio(self.PIN1,self.PIN2,self.PIN3,self.PIN4)
        if self.Immersive_Flag is True:
            self.Immersive_Flag = False
            self.onAsk(text)
        else:
            self.say('handsome模式已激活，现在全体起立！', cache=True, onCompleted=lambda: self.onAsk(self.activeListen()))

    def isValid(self, text, parsed): #触发条件
        return any(word in text for word in [u"开车", u"车",u"行动",u"驾驶"])

    def isValidImmersive(self, text, parsed):
        self.Immersive_Flag = True
        return any(word in text for word in [u"前进", u"向前", u"前",u"后退", u"向后", u"后",u"向左", u"左",u"向右", u"右",u"退出"])

    def install_gpio(self,pin1,pin2,pin3,pin4):
        gpio.setup(pin1,gpio.OUT)
        gpio.setup(pin2,gpio.OUT)
        gpio.setup(pin3,gpio.OUT)
        gpio.setup(pin4,gpio.OUT)

    def init_gpio(self):
        gpio.setmode(gpio.BOARD)

    def clean_gpio(self):
        gpio.cleanup()

