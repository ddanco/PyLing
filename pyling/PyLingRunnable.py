#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import os

if getattr(sys, 'frozen', False):
	root = os.path.dirname(sys.executable)
else:
	root = os.path.dirname(os.path.abspath(__file__))
logo_dir = os.path.join(root,'logos')
categories_dir = os.path.join(root,'categories')


##for app bundle, use top two import lines, for running file from terminal, use second two import lines
#from pyling.widgets import *
#from pyling.dictionaryMaker import *
from widgets import *
from dictionaryMaker import *

class Tester(QMainWindow):

	def __init__(self):
		super(QMainWindow, self).__init__()
		self.initUI()
		palette = QtGui.QPalette()
		palette.setColor(QPalette.Background,QColor.fromRgb(174,207,239))
		self.setPalette(palette)

	def initUI(self): #opens welcome window
		self.win = QWidget()
		self.l1 = QLabel(self)
		self.l2 = QLabel(self)
		self.l1.setPixmap(QPixmap(os.path.join(logo_dir, "logo3.png")))
		bInstructions = QPushButton("Instructions")
		self.l2.setText("What would you like to learn?")
		self.l1.setAlignment(Qt.AlignCenter)
		self.l2.setAlignment(Qt.AlignCenter)
		bFr = QPushButton("My French words",self)
		bEn = QPushButton("My English words",self)
		bCategories = QPushButton("Categories",self)
		self.box = QVBoxLayout()
		self.statusBar()
		self.box.addWidget(self.l1)
		self.box.addWidget(bInstructions)
		self.box.addWidget(self.l2)
		self.box.addWidget(bFr)
		self.box.addWidget(bEn)
		self.box.addWidget(bCategories)
		self.win.setLayout(self.box)
		self.setCentralWidget(self.win)
		self.resize(500, 500)
		self.setAutoFillBackground(True)
		p = self.win.palette()
		p.setColor(self.win.backgroundRole(), Qt.red)
		self.win.setPalette(p)
		bFr.clicked.connect(self.startFrench)
		bEn.clicked.connect(self.startEnglish)
		bCategories.clicked.connect(self.openCategories)
		bInstructions.clicked.connect(self.showInstructions)
		self.setWindowTitle("PyLing")

	def showInstructions(self):
		reply = QMessageBox.question(self, 'Instructions',
			"PyLing will help you master French vocabulary words. \n\nEnter words you'd like to learn (you can put in English or French words, we'll find the translations), or pick one of our pre-made categories. \n\nYou'll be tested on those words until you've mastered them! \n\n(The more times you get a word wrong, the more times you'll need to get it right to move on.)", QMessageBox.Ok)
		if reply == QMessageBox.Ok:
			self.initUI() #was having problem getting last character, adding space at end fixes it

	def openCategories(self): #user selected to learn from a category, open list of options
		self.categories = Choices('category')
		self.categories.show()
		self.categories.finished.connect(self.handleCategoryFinished)

	def handleCategoryFinished(self,name): #when category chosen
		self.name = name
		if self.name == 'Days of the Week': #special case for days of the week, since file name has no spaces
			self.name = "days_of_week"
			self.startCategory()
		else: self.startCategory()

	def placeLogo(self): #sets small version of logo to top of screen
		self.logo = QLabel(self)
		self.logo.setPixmap(QPixmap(os.path.join(logo_dir, "logosmall.png")))
		self.logo.setAlignment(Qt.AlignCenter)
		self.box.addWidget(self.logo)

	def startFrench(self): #user inputting french words
		self.categoryList = False
		self.clearPage()
		self.placeLogo()
		self.edit = TextEntryWidget('Enter your words here:',False)
		self.inputLang = 'fr'
		self.edit.finished.connect(self.handleFinished)
		layout = self.centralWidget().layout()
		layout.addWidget(self.edit)

	def startEnglish(self): #user inputting enlish words
		self.categoryList = False
		self.clearPage()
		self.placeLogo()
		self.edit = TextEntryWidget('Enter your words here:',False)
		self.inputLang = 'en'
		self.edit.finished.connect(self.handleFinished)
		layout = self.centralWidget().layout()
		layout.addWidget(self.edit)

	def startCategory(self): #user will select pre-made category
		self.categoryList = True
		self.clearPage()
		self.placeLogo()
		fName = os.path.join(categories_dir, self.name + '.txt')
		with open(fName,'r', encoding='utf8') as f:
			text = f.read()
		self.edit = text
		self.inputLang = 'fr'
		self.handleFinished(self.edit)

	def noWords(self): #user didnt enter any words (or only put non-words)
		self.clearPage()
		self.placeLogo()
		self.putWords = QLabel(self)
		self.putWords.setText("You need to enter more words!")
		self.putWords.setAlignment(Qt.AlignCenter)
		self.box.addWidget(self.putWords)
		bBack = QPushButton("Go back",self)
		self.box.addWidget(bBack)
		bBack.clicked.connect(self.initUI)

	def handleFinished(self,inputS): #input finished, make dictionary
		self.inputS = inputS
		if len(self.inputS) == 1:
			self.noWords()
		else:
			self.clearPage()
			self.placeLogo()
			layout = self.centralWidget().layout()
			newDict = DictConstructor(self.inputS,self.inputLang)
			self.curDict,self.nonWords = newDict.listChosen()
			if self.inputLang == 'en':
				self.flipDict() #swaps words and their definitions, since user gave english words
			self.copy = self.curDict.copy() #to be used if user starts over
			self.dictCopy = list(self.curDict)
			self.chooseLang()

	def clearPage(self):
		layout = self.centralWidget().layout()
		for i in reversed(range(layout.count())):
			w = layout.itemAt(i).widget()
			w.setParent(None)
			w.deleteLater()

	def chooseLang(self):
		self.choose = QLabel(self)
		self.choose.setText("Would you like to be prompted in French or English?")
		self.choose.setAlignment(Qt.AlignCenter)
		self.box.addWidget(self.choose)
		bF = QPushButton("French",self)
		self.box.addWidget(bF)
		bF.clicked.connect(self.frChosen)
		bE = QPushButton("English",self)
		self.box.addWidget(bE)
		bE.clicked.connect(self.enChosen)

	def frChosen(self):
		self.language = 'fr'
		self.startQuiz()

	def enChosen(self):
		self.language = 'en'
		self.flipDict() #flip dictionary so english words will be used as prompts
		self.startQuiz()

	def flipDict(self): #swaps words and their translations
		newDict = {}
		for k in self.curDict.keys():
			keyOptions = self.curDict[k]
			for key in keyOptions:
				word = key
				newDict[word] = [k]
		self.curDict = newDict

	def startQuiz(self):
		self.clearPage()
		self.placeLogo()
		self.record = {}
		self.errors = ''
		for w in self.curDict.keys():
			self.record[w] = [0,0]
		self.dictList = list(self.curDict)
		self.spaceTaker = QLabel(self)
		self.spaceTaker.setText("") #for spacing purposes
		self.newPrompt()
		self.box.addWidget(self.spaceTaker)
		self.win.setLayout(self.box)
		return

	def newPrompt(self): #ask user the translation of a word
		if len(self.dictList) == 0 : self.noWords()
		else:
			self.w = self.dictList[0]
			self.prompt = QLabel(self)
			if self.language == 'fr': self.prompt.setText("Please give the English translation, then press enter.")
			if self.language == 'en' : self.prompt.setText("Please give the French translation, then press enter.")
			self.prompt.setAlignment(Qt.AlignCenter)
			self.box.addWidget(self.prompt)
			if self.curDict[self.w][0][0:3] in ['les', 'la ', 'le ']: defW = 'the ' + self.w #prompt with "the" if article needed
			if self.curDict[self.w][0][0:3] in ['un ', 'une']: defW = 'a ' + self.w
			else: defW = self.w
			self.edit = TextEntryWidget(defW,True,self) #prompt user for input with defW as word
			layout = self.centralWidget().layout()
			layout.addWidget(self.edit)
			#self.edit.setFocus()
			self.edit.finished.connect(self.checkAnswer)

	def statusUpdate(self): #report to user how many more tries are needed for word
		for x in range(sys.maxsize):
			if (self.record[self.w][0]+x) > 0.5 * (self.record[self.w][1]+x):
				i = x
				break

		if i > 0:
			self.statusBar().showMessage(str(i) + " more correct responses needed for \'" + self.w + '\'')
		else: self.statusBar().clearMessage()


	def checkAnswer(self,answer):
		self.answer = answer.lower() #to avoid issues with capital/lowercase letters
		if (self.answer in self.curDict[self.w]
				or ((answer[0:4] == "the ") and (answer[4:] in self.curDict[self.w])) #allows some flexibility in user input
				or ((answer[0:3] == "to ") and (answer[3:] in self.curDict[self.w]))
				or ((answer[0:2] == "a ") and (answer[2:] in self.curDict[self.w]))):
				self.clearPage()
				self.placeLogo()
				self.correct = QLabel(self)
				self.correct.setText("Correct!")
				self.correct.setAlignment(Qt.AlignCenter)
				self.correctAnswer()
				if len(self.dictList) > 0: #still words left in dictionary
					self.newPrompt()
					self.box.addWidget(self.correct)
				else: self.endTest() #test finished
		else:
			self.clearPage()
			self.placeLogo()
			self.wrongAnswer()

	def correctAnswer(self): #when answer matches dictionary
		self.record[self.w][1] += 1 #+1 try
		self.record[self.w][0] += 1 #+1 correct
		self.statusUpdate() #say how many more correct tries needed
		if (float(self.record[self.w][0])/float(self.record[self.w][1]) > 0.5) : #if user has gotten word right more than 50% of the time, remove word
			del self.curDict[self.w]
			self.dictList.remove(self.w)

	def wrongAnswer(self): #when answer incorrect (give option of overriding)
		self.record[self.w][1] += 1 #+1 try
		self.statusUpdate() #say how many more correct tries needed
		self.commaList = '/'.join(str(x) for x in self.curDict[self.w]) #report all possible translations of word
		self.dictList.remove(self.w)
		self.dictList.append(self.w) #moves word from front of list to end of list
		self.wrong = QLabel(self)
		self.wrong.setText("Incorrect! Translation for " + self.w + " is: " + self.commaList + "\n\nDo you disagree? Click \'remove\' to skip this word.")
		self.wrong.setAlignment(Qt.AlignCenter)
		self.box.addWidget(self.wrong)
		bDis = QPushButton("Remove")
		bContinue = QPushButton("Continue")
		self.box.addWidget(bContinue)
		self.box.addWidget(bDis)
		bDis.clicked.connect(self.remWord)
		bContinue.clicked.connect(self.moveOn)

	def remWord(self): #user wants to get rid of current word in dictionary
		del self.curDict[self.w]
		del self.record[self.w]
		if self.errors == '':
			self.errors += self.w
		else: self.errors += ", " + self.w
		self.dictList.remove(self.w)
		self.moveOn()

	def moveOn(self):
		self.clearPage()
		self.placeLogo()
		if len(self.dictList) > 0: #still other words left in dictionary
			self.newPrompt()
		else: self.endTest()

	def compareCount(self): #checks which premade category is most similar to user's inputted words
		countList = []
		categoryList = ['Animals', 'Colors', 'Foods', 'Transportation', 'Sports', 'Emotions', 'Actions', 'Months', 'Numbers', 'days_of_week', 'Pronouns']
		for x in categoryList: countList.append((x,self.categoryFileCrawl(os.path.join(categories_dir, x + '.txt'))))
		countList.sort(key=lambda x: x[1])
		self.bestCategory,self.number = countList[-1]

	def categoryFileCrawl(self,fName): #gets count of word matches between input and each category
		count = 0
		with open(fName,'r', encoding='utf8') as f:
			fi = f.read()
		terms = fi.split(' ')
		for w in self.dictCopy:
			for indW in w.split(" "):
				if indW in terms and indW not in ['un', 'une', 'les', 'la', 'le']: #ignores articles
					count += 1
		return count

	def endTest(self): #user has gotten each word correct enough times
		self.clearPage()
		self.statusBar().clearMessage()
		self.placeLogo()
		self.compareCount() #give user option of other list to try
		self.done = QLabel(self)
		self.done.setText("List complete! Number of times incorrect per word:")
		self.done.setAlignment(Qt.AlignCenter)
		self.box.addWidget(self.done)
		self.showRecord()
		if self.number > 0 and (not self.categoryList) : self.suggestLists()
		bRe = QPushButton("Restart (same words)",self) #option to restart test (same words)
		self.box.addWidget(bRe)
		bRe.clicked.connect(self.restart)
		bNew = QPushButton("New words",self) #option to restart test (inputting new words)
		self.box.addWidget(bNew)
		bNew.clicked.connect(self.initUI)

	def restart(self): #restart with same words as before
		self.clearPage()
		self.placeLogo()
		self.curDict = self.copy
		self.chooseLang()

	def showRecord(self): #show how many times each word was correct
		for i in self.record.keys():
			reportString = i + ": " + str((self.record[i][1])-(self.record[i][0]))
			i = QLabel(self)
			i.setText(reportString)
			i.setAlignment(Qt.AlignCenter)
			self.box.addWidget(i)
		self.nonW = QLabel(self)
		if self.nonWords != []:
			s = ''
			for item in self.nonWords:
				if s == '': s += item[0]
				else: s += (", " + item[0])
			self.nonW.setText("Definitions not found for: " + s) #report nonWords
			self.nonW.setAlignment(Qt.AlignCenter)
			self.box.addWidget(self.nonW)

	def suggestLists(self):
		self.suggestion = QLabel(self)
		self.suggestion.setText("Your list was most similar to: \'" + self.bestCategory + "\'. Would you like to study that list next?")
		bSuggest = QPushButton("Sure!",self)
		self.box.addWidget(self.suggestion)
		self.box.addWidget(bSuggest)
		self.name = self.bestCategory
		bSuggest.clicked.connect(self.startCategory)



if __name__ == '__main__':
	app = QApplication(sys.argv)
	tester = Tester()
	tester.show()
	sys.exit(app.exec_())




