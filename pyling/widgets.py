#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys, re, string
from PyQt5.QtGui import *
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *



class Choices(QWidget): #widget to give user options (eg. accents, categories)
	finished = pyqtSignal(str)

	def __init__(self, typeC):
		QWidget.__init__(self)
		self.typeC = typeC
		self.initUIChoices()

	def initUIChoices(self):
		self.accentbox = QVBoxLayout()
		self.placeButtons() #gets buttons for options
		self.VAccentbox = QVBoxLayout()
		self.VAccentbox.addLayout(self.accentbox)
		self.setLayout(self.VAccentbox)
		self.setWindowTitle('Choices')
		self.show()

	def placeButtons(self): #makes list of options, each as a button
		symbolList = ['é','è','ê','ë','à','â','â','ç','ù','ü','û','î','ï']
		categoryList = ['Animals', 'Colors', 'Foods', 'Transportation', 'Countries', 'Sports', 'Emotions', 'Actions', 'Months', 'Numbers', 'Day of the Week', 'Pronouns']
		if self.typeC == 'accent': self.buttons = [QPushButton(x,self) for x in symbolList]
		elif self.typeC == 'category': self.buttons = [QPushButton(x,self) for x in categoryList]
		for self.button in self.buttons:
			self.accentbox.addWidget(self.button)
			self.button.clicked.connect(self.chosen)

	def chosen(self): #report which button clicked
		chosen = self.sender().text() #sender is button that was clicked
		self.finished.emit(chosen)
		self.close() #close options



class TextEntryWidget(QWidget): #lets user input text
	finished = pyqtSignal(str)

	def __init__(self, w, testT, parent = None):
		super(TextEntryWidget, self).__init__(parent)
		self.testT = testT #True when user being tested, False when user initally inputting words for testing
		self.edit = QLineEdit(self)
		self.label = QLabel(w)
		self.BAccents = QPushButton("Add accent mark",self)
		layout = QHBoxLayout()
		layout.addWidget(self.label)
		layout.addWidget(self.edit)
		layout.addWidget(self.BAccents)
		self.setLayout(layout)
		#self.edit.setFocus()
		#self.edit.setFocus(Qt.MouseFocusReason)
		self.BAccents.clicked.connect(self.openAccents)

	def openAccents(self): #user wants to input accent mark
		self.accents = Choices('accent')
		self.accents.show()
		self.accents.finished.connect(self.handleAccentFinished)

	def handleAccentFinished(self,char):
		self.char = char
		self.edit.insert(char)

	def keyPressEvent(self, event):
		if event.key() == Qt.Key_Return:
			if not self.testT: ##not test, just word prompt at beginning
				self.confirmFinished() #ask user to be sure they dont want to add more words
				return
			else:
				self.finished.emit(self.edit.text())
				return
		super(TextEntryWidget, self).keyPressEvent(event)

	def confirmFinished(self):
		reply = QMessageBox.question(self, 'Message',
			"Would you like to add more words?", QMessageBox.Yes |
			QMessageBox.No, QMessageBox.No)
		if reply == QMessageBox.No:
			self.edit.insert(' ') #was having problem getting last character, adding space at end fixes it
			self.finished.emit(self.edit.text())
		else:
			self.edit.insert(' ')


