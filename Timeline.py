import pygame
from pygame.locals import *

import time
import platform
from functools import partial

if platform.system() == 'Linux':
	import evdev
	from evdev import InputDevice, categorize, ecodes

from common.Config import Config
from common.Utilities import Utilities
from common.Button import Button
from common.TouchScreen import TouchScreen

CONFIG_FILENAME = 'assets/config/config.json'

DOT_TEXT_COLOR = (252, 175, 138)
DOT_SELECTED_TEXT_COLOR = (0, 65, 40)

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

		self.loadFonts()

		self.screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
		self.cursor = pygame.image.load('assets/images/cursor.png').convert_alpha()

		self.touchScreen = None
		if self.config.isTouch():
			print("Loading touch screen...")
			self.touchScreen = TouchScreen(self.config.getTouchDevicePartialName(), (self.config.getTouchScreenMaxX(), self.config.getTouchScreenMaxY()))

			if not self.touchScreen.setup():
				self.config.setTouch(False)

		self.background = pygame.image.load('assets/images/background.png').convert()

		self.dotImage = pygame.image.load('assets/images/dot-normal.png').convert()
		self.dotTappedImage = pygame.image.load('assets/images/dot-tapped.png').convert()

		# TODO: Add languages support (currently only Hebrew is needed)
		self.languageButtons = []

		self.dots = self.config.getDots()
		self.dotButtons = []

		for i in range(len(self.dots)):
			dot = self.dots[i]
			x = dot['x']
			y = dot['y']
			dotButton = Button(self.screen, Rect(x - self.dotImage.get_width() // 2, y - self.dotImage.get_height() // 2, self.dotImage.get_width(), self.dotImage.get_height()), 
				self.dotImage, self.dotTappedImage, str(i + 1), DOT_TEXT_COLOR, DOT_SELECTED_TEXT_COLOR, self.numbersFont, partial(self.dotClicked, i))
			self.dotButtons.append(dotButton)
			self.buttons.append(dotButton)

		self.selectedDotIndex = 0
		self.loadDot()

		self.loop()

	def loadFonts(self):
		languageData = self.config.getLanguage()
		self.numbersFont = pygame.font.Font(languageData['fonts']['numbersFont']['filename'], languageData['fonts']['numbersFont']['size'])
		self.headerFont = pygame.font.Font(languageData['fonts']['headerFont']['filename'], languageData['fonts']['headerFont']['size'])
		self.textFont = pygame.font.Font(languageData['fonts']['textFont']['filename'], languageData['fonts']['textFont']['size'])

	def dotClicked(self, index):
		self.selectedDotIndex = index
		self.loadDot()

	def loadDot(self):
		dot = self.dots[self.selectedDotIndex]
		self.currTexts = Utilities.renderTextList(self.config, self.textFont, dot['textKey'])
		self.currHeader = self.headerFont.render(self.config.getText(dot['headerKey']), True, (255, 255 ,255))

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

		self.screen.blit(self.currHeader, (1789, 906))
		Utilities.drawTextsOnRightX(self.screen, self.currTexts, (1791, 960), 50)		

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
