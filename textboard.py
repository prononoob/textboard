from tkinter import *
from tkinter import ttk


class Board:
	def __init__(self):
		self.catalog = {}
		self.idCounter = 0
		print('Class initialized!')

	def create(self, title):
		self.title = title
		self.catalog[self.idCounter] = self.title
		self.idCounter += 1

	def show(self, amount = 0):
		if amount >= len(self.catalog):
			self.amount = len(self.catalog)
		else:
			self.amount = amount
		print('----------')
		if self.amount:
			for i in range(self.amount):
				if self.catalog[i]:
					print(f'ID: {i} Title: {self.catalog[i]}')
		else:
			for i in self.catalog:
				if self.catalog[i]:
					print(f'ID: {i} Title: {self.catalog[i]}')

	def delete(self, threadID):
		self.threadID = threadID
		if self.threadID in self.catalog:
			self.catalog[self.threadID] = False


class Thread:
	def __init__(self, board):
		self.board = board
		self.replies = {}
		self.replyID = 0

	def reply(self, threadID, replyMsg):
		self.threadID = threadID
		self.replyMsg = replyMsg
		self.replies[self.replyID] = [self.threadID, self.replyMsg]
		self.replyID += 1

	def showReplies(self, threadID):
		self.threadID = threadID
		print('----------')
		print(self.board.catalog[threadID])
		for i in self.replies:
			if self.replies[i] and self.replies[i][0] == self.threadID:
				print(f'    Reply {i}: {self.replies[i][1]}')

	def deleteReply(self, replyID):
		self.replyID = replyID
		self.replies[self.replyID] = False


class Window:
	def __init__(self, board):
		self.board = board
		self.threadOpen = False
		self.root = Tk()
		self.root.geometry('400x350')
		self.frm = ttk.Frame(self.root, padding=10)
		self.mainMenu()
		self.root.mainloop()

	def createQuit(self, side=BOTTOM):
		self.side = side
		self.quitButton = Button(self.root, text='Quit', command=self.quitCommand)
		self.quitButton.pack(ipadx=10, ipady=10, padx=10, pady=25, side=self.side, expand=True)

	def mainMenu(self):
		self.clearScene()
		self.createThreadButton = Button(self.root, text='Create Thread', command=self.createThread, width=15)
		self.createThreadButton.pack(ipadx=10, ipady=10, padx=50, expand=True, fill=X)
		self.catalogButton = Button(self.root, text='Catalog', width=15, command=self.catalogScene)
		self.catalogButton.pack(ipadx=10, ipady=10, padx=50, expand=True, fill=X)
		self.createQuit()

	def allChildren (self):
	    self.scene = self.root.winfo_children()

	    for item in self.scene:
	        if item.winfo_children() and 'button' in item:
	            self.scene.extend(item.winfo_children())

	def clearScene(self):
		self.allChildren()
		[i.pack_forget() for i in self.scene]

	def quitCommand(self):
		exit()

	def createThread(self):
		if not self.threadOpen:
			self.threadContent = Text(self.root, height=5, width=20)
			self.threadContent.pack(ipadx=10, ipady=10, padx=10, side=RIGHT)
			self.threadContent.insert('1.0', 'Content')
			self.threadOpen = True
			self.createButton = Button(self.root, text='Create', command=self.getText)
			self.createButton.pack(ipadx=10, ipady=10, padx=10, side=RIGHT)
		else:
			self.threadContent.destroy()
			self.createButton.destroy()
			self.threadOpen = False

	def createReplyButtons(self, replyButtonId):
		self.replyButtonId = replyButtonId
		if self.firstReply:
			self.fVal += self.replyButtonId
			self.sVal = self.fVal+1
			self.tVal = self.fVal+2
			self.buttonCounter = 0
			self.firstReply = not self.firstReply
		if self.buttonCounter == 0:
			self.buttonCounter += 1
			Button(self.root, text=self.board.catalog[self.replyButtonId], command=lambda: self.replyScene(self.fVal), width=15).pack(ipadx=10, ipady=10, padx=50, expand=True, fill=X)
		elif self.buttonCounter == 1:
			self.buttonCounter += 1
			Button(self.root, text=self.board.catalog[self.replyButtonId], command=lambda: self.replyScene(self.sVal), width=15).pack(ipadx=10, ipady=10, padx=50, expand=True, fill=X)
		elif self.buttonCounter == 2:
			self.buttonCounter += 1
			Button(self.root, text=self.board.catalog[self.replyButtonId], command=lambda: self.replyScene(self.tVal), width=15).pack(ipadx=10, ipady=10, padx=50, expand=True, fill=X)

	def displayThreeThreads(self, guiThreadIndex):
		self.guiThreadIndex = guiThreadIndex
		self.firstReply = True
		self.fVal, self.sVal, self.tVal = 0, 0, 0
		if len(self.board.catalog) <= 3:
			for i in self.board.catalog:
				self.createReplyButtons(i)
		elif self.guiThreadIndex > len(self.board.catalog)-3:
			self.guiThreadIndex = len(self.board.catalog)-3
			for i in range(self.guiThreadIndex, self.guiThreadIndex+3):
				self.createReplyButtons(i)
		else:
			for i in range(self.guiThreadIndex, self.guiThreadIndex+3):
				self.createReplyButtons(i)
	def nextScene(self):
		self.catalogScene(False, self.guiThreadIndex+3)

	def previousScene(self):
		self.catalogScene(False, self.guiThreadIndex-3)

	def catalogScene(self, firstLook=True, guiThreadIndex=0):
		self.clearScene()
		self.firstLook = firstLook
		self.guiThreadIndex = guiThreadIndex
		if self.guiThreadIndex < 0:
			self.guiThreadIndex = 0

		if self.firstLook:
			self.displayedPage = 1
			self.firstLook = False
			self.displayThreeThreads(0)
			if len(self.board.catalog) > 3:
				Button(self.root, text='Next', command=self.nextScene).pack(ipadx=10, ipady=10, padx=10, expand=True, side=LEFT)
		else:
			self.displayThreeThreads(self.guiThreadIndex)
			if self.guiThreadIndex != 0:
				Button(self.root, text='Previous', command=self.previousScene).pack(ipadx=10, ipady=10, padx=10, expand=True, side=LEFT)
			if self.guiThreadIndex < len(self.board.catalog)-3:
				Button(self.root, text='Next', command=self.nextScene).pack(ipadx=10, ipady=10, padx=10, expand=True, side=LEFT)

		self.mainMenuButton = Button(text='Main menu', command=self.mainMenu)
		self.mainMenuButton.pack(ipadx=10, ipady=10, padx=10, expand=True, side=LEFT)
		
		if len(self.board.catalog) > 3:
			self.createQuit(side=LEFT)
		else:
			self.createQuit()

	def replyScene(self, replyID):
		self.replyID = replyID
		print(f'replyID {self.replyID}')

	def getText(self):
		self.content = self.threadContent.get('1.0', 'end').strip()
		self.board.create(self.content)
		print(self.content, self.board.catalog)


if __name__ == '__main__':
	# DODAJ SCENE ODPOWIEDZI
	
	board = Board()
	'''board.create('Thread 1')
	board.create('Thread 2')
	board.create('Thread 3')
	board.show()'''
	thread = Thread(board=board)
	'''thread.reply(0, 'Reply 1')
	thread.reply(0, 'Reply 2')
	thread.showReplies(0)
	thread.deleteReply(0)
	thread.showReplies(0)'''
	window = Window(board=board)