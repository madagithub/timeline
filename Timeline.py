import pygame
from pygame.locals import *

import time

import platform

if platform.system() == 'Linux':
	import evdev
	from evdev import InputDevice, categorize, ecodes

from common.Config import Config
from common.Button import Button
from common.TouchScreen import TouchScreen

CONFIG_FILENAME = 'assets/config/config.json'

class Timeline:
	def __init__(self):
		self.touchPos = (0,0)

	def start(self):
		self.buttons = []
		self.blitCursor = True

		self.config = Config(CONFIG_FILENAME)

		pygame.mixer.pre_init(44100, -16, 1, 512)
		pygame.init()
		pygame.mouse.set_visible(False)

		self.screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
		self.cursor = pygame.image.load('assets/images/cursor.png').convert_alpha()

		self.touchScreen = None
		if self.config.isTouch():
			print("Loading touch screen...")
			self.touchScreen = TouchScreen(self.config.getTouchDevicePartialName(), (self.config.getTouchScreenMaxX(), self.config.getTouchScreenMaxY()))

			if not self.touchScreen.setup():
				self.config.setTouch(False)

		self.background = pygame.image.load('assets/images/background.png').convert()

		dot = pygame.image.load('assets/images/dot-normal.png').convert()
		dotSelected = pygame.image.load('assets/images/dot-tapped.png').convert()

		self.languageButtons = []

		#languages = self.config.getLanguages()
		#for i in range(len(languages)):
		#	language = None

		#dots = self.config.getDots()
		#for i in range(len(dots)):
		#	dot = dots[i]

		self.selectedDotIndex = 0
		#self.loadDot()

		self.loop()

	def loadDot(self):
		self.currText = None

	def onMouseDown(self, pos):
		for button in self.buttons:
			button.onMouseDown(pos)

	def onMouseUp(self, pos):
		for button in self.buttons:
			button.onMouseUp(pos)

	def onMouseMove(self, pos):
		pass

	def draw(self, dt):
		self.screen.blit(self.background, (0, 0))

		for button in self.buttons:
			button.draw()

	def loop(self):
		isGameRunning = True
		clock = pygame.time.Clock()
		lastTime = pygame.time.get_ticks()
		font = pygame.font.Font(None, 30)

		while isGameRunning:
			for event in pygame.event.get():
				if event.type == MOUSEBUTTONDOWN:
					if not self.config.isTouch():
						self.onMouseDown(event.pos)
				elif event.type == MOUSEBUTTONUP:
					if not self.config.isTouch():
						self.onMouseUp(event.pos)
				elif event.type == KEYDOWN:
					if event.key == K_ESCAPE:
						isGameRunning = False

			if self.config.isTouch():
				event = self.touchScreen.readUpDownEvent()
				while event is not None:
					if event['type'] == TouchScreen.DOWN_EVENT:
						self.onMouseDown(event['pos'])
					elif event['type'] == Touchscreen.UP_EVENT:
						self.onMouseUp(event['pos'])
					event = self.touchScreen.readUpDownEvent()

			if not self.config.isTouch():
				self.onMouseMove(pygame.mouse.get_pos())
			else:
				pos = self.touchScreen.getPosition()
				self.onMouseMove(pos)

			self.screen.fill([0,0,0])
			currTime = pygame.time.get_ticks()
			dt = currTime - lastTime
			lastTime = currTime

			self.draw(dt / 1000)

			if not self.config.isTouch() and self.blitCursor:
				self.screen.blit(self.cursor, (pygame.mouse.get_pos()))

			if self.config.showFPS():
				fps = font.render(str(int(clock.get_fps())), True, Color('white'))
				self.screen.blit(fps, (50, 50))

			pygame.display.flip()
			clock.tick(60)

		pygame.quit()

if __name__ == '__main__':
	Timeline().start()
