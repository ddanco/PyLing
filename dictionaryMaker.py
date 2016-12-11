#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys, re, string


class DictConstructor(object):

	def __init__(self, inputS, inputLang):
		self.inputS = inputS
		self.inputLang = inputLang
		self.dictW = self.listChosen()

	def listChosen(self): #puts together dictionary
		self.words = self.listMaker() #gets list of words with no punctuation
		self.curDict,self.nonWords = self.dictMaker() #makes dictionary, and list of nonWords (not in dict.txt)
		if self.nonWords != []: #deletes words with no definition
			for item in self.nonWords:
				del self.curDict[item[0]]
		for w in list(self.curDict): #deletes articles
			if w in ['le', 'la', 'les', 'l\'', 'un', 'une']:
				del self.curDict[w]
		self.addBackArticles() #puts articles back in, in the same entry as the word they were entered with
		return self.curDict,self.nonWords

	def listMaker(self): #eliminates punctuation at beginning or end of words
		self.noElips = self.inputS.replace('...', ' ')
		self.wordList = self.noElips.split()
		self.finalWords = []
		for word in self.wordList:
			index = 0
			posCount = 0
			goodStart = word
			while re.search("[^a-zA-Zéèêëàâçùüîïû]", goodStart[index]):
				posCount += 1
				index += 1
			goodStart = word[posCount:] #now word has no beginning punctuation
			backCount = len(goodStart)-1
			index = len(goodStart)-1
			goodEnd = goodStart
			while re.search("[^a-zA-Zéèêëàâçùüîïû]", goodStart[backCount]):
				backCount -= 1
				index -= 1
			goodEnd = goodStart[:backCount+1] #now word has no ending punctuation
			if '\'' in goodEnd: #if word is contraction, only uses the part of the word after '
				goodEnd = goodEnd[goodEnd.index('\'')+1:]
			self.finalWords.append(goodEnd.lower())
		return self.finalWords

	def addBackArticles(self): #puts articles back in the entry of a word, if they were entered together
		for word in self.curDict:
			if word in self.finalWords and self.finalWords.index(word) > 0 :
				if self.finalWords[self.finalWords.index(word) - 1] == 'un':
					#eg. if previous word before 'x' in input string was 'un', change entry of 'x' to 'un x'
					self.curDict['un ' + word] = self.curDict[word]
					del self.curDict[word]
				if self.finalWords[self.finalWords.index(word) - 1] == 'le':
					self.curDict['le ' + word] = self.curDict[word]
					del self.curDict[word]
				if self.finalWords[self.finalWords.index(word) - 1] == 'la':
					self.curDict['la ' + word] = self.curDict[word]
					del self.curDict[word]
				if self.finalWords[self.finalWords.index(word) - 1] == 'les':
					self.curDict['les ' + word] = self.curDict[word]
					del self.curDict[word]
				if self.finalWords[self.finalWords.index(word) - 1] == 'une':
					self.curDict['une ' + word] = self.curDict[word]
					del self.curDict[word]

	def lexiqueAndDictionary(self):
		dictionary = open('dict.txt').read() #english-french dictionary
		lexique = open('Lexique381.txt').read() #french lexical dictionary
		dictlines = dictionary.split('\n')
		lexlines = lexique.split('\n')
		lexDict = {}
		textDict = {}
		prev = ''
		for xline in lexlines: #makes dictionary with each word and its lexical info
			xSplit = re.split(r'\t+',xline)
			lexDict[xSplit[0]] = xSplit
		for line in dictlines: #makes dictionary with each english word (from dict.txt) and its french definition
			lineSplit = re.split(' : |, ',line)
			textDict[lineSplit[0]] = lineSplit #leaving term (lineSplit[0]) in dict to keep indexing the same as first code-through
		return lexDict,textDict,dictlines


	def dictMaker(self):#create dictionary out of input words
		dictW = {}
		self.nonWords = []
		lexDict,textDict,dictlines = self.lexiqueAndDictionary() #make dictionary of all translations and lexical info
		if self.inputLang == 'en': #when input is in english
			for w in self.words:
				dictW[w] = []
				if w in textDict.keys(): #word translation found
					for item in textDict[w][1:]:
						dictW[w].append(item) #add all possible translations
			if dictW[w] == []: #word translation not found, add to nonWords
					self.nonWords.append([w,True])
		else: #input language is french
			for w in self.words:
				dictW[w] = []
				if w in lexDict.keys(): #word form found in lexical dictionary
					wLen = len(w)
					for line in dictlines: #gets all possible english translations of the root of word (found from lexdict)
						lineSplit = re.split(' : |, ',line)
						if w in lineSplit and (w + " ") != line[0:(len(w)+1)]:#second half makes sure that first word in line isnt w, (aka isnt the english word)
							if lineSplit[0].lower() not in dictW[w]: dictW[w].append(lineSplit[0].lower())
						if lexDict[w[-wLen:]][2] in lineSplit and lexDict[w[-wLen:]][2] != line[0:len(lexDict[w[-wLen:]][2])]:#second half makes sure that first word in line isnt w, (aka isnt the english word)
							if lineSplit[0].lower() not in dictW[w]:
								dictW[w].append(lineSplit[0].lower())
						if (lexDict[w[-wLen:]][5] == "p") :
							#if word entered was plural, will look for singular form in translation dictionary
							#so need to add back 's' to translation found (limitation: will give wrong word when plural form is formed differently)
							for index, l in enumerate(dictW[w]):
								if l[-1] != 's' and w not in ['elles', 'ils']: dictW[w][index] = str(l)+"s"
				if dictW[w] == []:
					self.nonWords.append([w,False])#"false" indicates non-english
		return dictW,self.nonWords


