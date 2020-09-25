import pygame
import time
import encrypt

vaultOpen = False
openimg = pygame.image.load('images/Vault_Open.png')
closedimg = pygame.image.load('images/Vault_Closed.png')
dialimg = pygame.image.load('images/Vault_Dial.png')
vaultimg = closedimg
textFont = None
needBox = False
instructionText = ['']

class InputBox:
	def __init__(self, x, y, w, h, tf, text=''):
		self.rect = pygame.Rect(x, y, w, h)
		self.color = pygame.Color('dodgerblue2')
		self.text = text
		self.textFont = tf
		self.txt_surface = self.textFont.render(text, True, self.color)
		self.active = False

	def calc_width(self):
		return max(200, self.txt_surface.get_width()+20)

	def handle_event(self, event):
		self.active = True
		global currentFunction
		global needBox
		global instructionText
		global dataText
		global lastSelect
		global currentKey
		width = self.calc_width()
		self.rect.w = width
		self.color = pygame.Color('dodgerblue2')
		if event.type == pygame.KEYDOWN:
			if self.active:
				if event.key == pygame.K_RETURN:
					if currentFunction == 0:
						if self.text.isnumeric() and int(self.text) in range (0, len(dataText.text)):
							error = encrypt.delete_line_from_file(int(self.text))
							open_vault()
							if error != '':
								push_timed_message(['Error!', error])
							else:
								instructionText.text = []
								push_timed_message(['Success!', ('Password at line #'+str(int(self.text))+' deleted.')])
								needBox = False
								currentFunction = -1
								lastSelect = currentFunction
						else:
							push_timed_message(['Error!', 'Not a valid line number.'])
							self.text = ''
					elif currentFunction == 1:
						error = encrypt.write_encrypted_data_to_file(self.text, currentKey)
						if error != '':
							push_timed_message(['Error!', error])
						else:
							dataText.text = encrypt.decrypt_data_with_key(currentKey)[0]
							instructionText.text = []
							push_timed_message(['Success!', 'Password encrypted and saved to file.'])
							needBox = False
							currentFunction = -1
							lastSelect = currentFunction
					elif currentFunction == 2:
						if self.text == '':
							currentKey = None
							instructionText.text = []
							needBox = False
							currentFunction = -1
							lastSelect = currentFunction
							close_vault()
						else:	
							result = encrypt.read_key_from_file(self.text)
							if result[1] != '':
								push_timed_message(['Error!', result[1]])
							else:
								currentKey = result[0]
								instructionText.text = []
								push_timed_message(['Success!', 'Key loaded from \''+self.text+'\'.'])
								needBox = False
								currentFunction = -1
								lastSelect = currentFunction
								open_vault()
					elif currentFunction == 3:
						error = encrypt.write_random_256bit_key_to_file(self.text)
						if error != '':
							push_timed_message(['Error!', error])
						else:
							instructionText.text = []
							push_timed_message(['Success!', 'Key saved as \''+self.text+'\'.'])
							needBox = False
							currentFunction = -1
							lastSelect = currentFunction
					self.text = ''
				elif event.key == pygame.K_BACKSPACE:
					self.text = self.text[:-1]
				elif event.unicode.isprintable():
					self.text += event.unicode
				# Re-render the text.
				self.txt_surface = self.textFont.render(self.text, True, self.color)
			width = self.calc_width()
	def draw(self, screen):
		screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
		pygame.draw.rect(screen, self.color, self.rect, 2)

class InstructionText:
	def __init__(self, x, y, w, h, textFont2, text=[]):
		self.textFont = textFont2
		self.txt_surfaces = []
		self.spacing = 15
		self.rect = pygame.Rect(x, y, w, h)
		self.color = (0, 0, 0)
		self.text = text
		for t in text:
			self.txt_surfaces.append(self.textFont.render(text, True, self.color))

	def update(self):
		self.txt_surfaces = []
		for t in self.text:
			self.txt_surfaces.append(self.textFont.render(t, True, self.color))
		mx = 0
		for s in self.txt_surfaces:
			mx = s.get_width()+10
			break
		linesSize = 0
		for s in self.txt_surfaces:
			linesSize += self.spacing
			linesSize += s.get_height()
			if s.get_width()+10 > mx:
				mx = s.get_width()+10
		width = max(200, mx)
		height = max(75, linesSize)
		self.rect.w = width
		self.rect.h = height
	def draw(self, screen):
		if self.text != []:
			position = (self.rect.x+5, self.rect.y+5)
			fontSize = self.textFont.get_height()
			for line in range(len(self.txt_surfaces)):
				screen.blit(self.txt_surfaces[line], (position[0], position[1]+(line*fontSize)+(self.spacing*line)))




def open_vault():
	global vaultOpen
	global vaultimg
	global dataText
	vaultOpen = True
	vaultimg = openimg
	result = encrypt.decrypt_data_with_key(currentKey)
	if result[1] != '':
		push_timed_message(['Error!', result[1]])
	else:
		dataText.text = result[0]

def close_vault():
	global vaultOpen
	global vaultimg
	vaultOpen = False
	vaultimg = closedimg


def push_timed_message(msg):
	global timerActive
	global timerStart
	global pastText
	global instructionText
	global origText
	if not timerActive:
		origText = instructionText.text
	timerActive = True
	timerStart = time.time()
	pastText = msg
	instructionText.text = msg

def main():
	global vaultOpen
	global vaultimg
	global textFont
	global needBox
	global showData
	global instructionText
	global dataText
	global currentFunction
	#Initialize
	timer = 2
	global timerStart
	timerStart = time.time()
	global timerActive
	global pastText
	global origText
	global lastSelect
	global currentKey
	showData = False
	timerActive = False
	pastText = []
	origText = []
	currentFunction = -1
	lastSelect = -1
	currentKey = None
	pygame.init()
	pygame.display.set_caption('Password Vault')
	icon = pygame.image.load('images/Vault_Icon.png')
	keyimg = pygame.image.load('images/Key.png')
	folderimg = pygame.image.load('images/Folder.png')
	notepadimg = pygame.image.load('images/Notepad.png')
	deleteimg = pygame.image.load('images/Delete.png')
	notesimg = pygame.image.load('images/Notes.png')
	pygame.display.set_icon(icon)
	screen = pygame.display.set_mode((800, 600))
	running = True
	textFont = pygame.font.Font(None, 40)
	textFont2 = pygame.font.Font(None, 30)
	textFont3 = pygame.font.Font(None, 21)
	input_box = InputBox(300, 360, 200, 40, textFont)
	instructionText = InstructionText(300, 200, 200, 40, textFont2)
	instructionText.text = []
	dataText = InstructionText(5, 3, 790, 590, textFont3)
	blackRectList = [pygame.Rect(0, 0, 156, 156), pygame.Rect(644, 0, 156, 156), pygame.Rect(0, 444, 156, 156), pygame.Rect(644, 444, 156, 156)]
	
	while running:
		if (instructionText.text != pastText) and timerActive:
			timerActive = False
		if timerActive:
			if ((time.time()-timerStart) >= timer):
				timerActive = False
				instructionText.text = origText
		pastText = instructionText.text
		screen.fill((171, 178, 185))
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if needBox:
				input_box.handle_event(event)
			if event.type == pygame.MOUSEBUTTONDOWN:
				#deselect routine
				currentFunction = -1
				instructionText.text = []
				needBox = False
				pos = pygame.mouse.get_pos()
				if showData:
					showData = False
				elif pygame.Rect(157, 95, 486, 420).collidepoint(pos):
					if lastSelect == -1:
						if vaultOpen:
								showData = True
						elif currentKey != None:
							open_vault()
						else:
							push_timed_message(['Cannot decrypt data without a key!'])
				#0
				elif pygame.Rect(0, 0, 156, 156).collidepoint(pos):
					if lastSelect != 0:
						if currentKey == None:
							push_timed_message(['Vault must be open in order to delete password!'])
						elif len(dataText.text) == 0:
							push_timed_message(['Error!', 'Data file empty!'])
						else:
							currentFunction = 0
							instructionText.text = ['Delete Password:', 'Please enter a valid line number to delete (0 - '+str(len(dataText.text)-1)+').', 'Hit ENTER to confirm.']
							needBox = True
				#1
				elif pygame.Rect(644, 0, 156, 156).collidepoint(pos):
					if lastSelect != 1:
						if len(dataText.text) >= 20:
							push_timed_message(['Error!', 'Data file full!'])
						elif currentKey != None:
							currentFunction = 1
							instructionText.text = ['Add Password:', 'Please enter a password to add.', 'Hit ENTER to confirm.']
							needBox = True
						else:
							push_timed_message(['Cannot add a new password without a key!'])
				#2
				elif pygame.Rect(0, 444, 156, 156).collidepoint(pos):
					if lastSelect != 2:
						currentFunction = 2
						instructionText.text = ['Load Key:', 'Please enter the key filename to load.', 'Hit ENTER to confirm.']
						needBox = True
				#3
				elif pygame.Rect(644, 444, 156, 156).collidepoint(pos):
					if lastSelect != 3:
						currentFunction = 3
						instructionText.text = ['Create Key:', 'Please enter the name of the new key file.', 'Hit ENTER to confirm.']
						needBox = True
				else:
					currentFunction = -1
					instructionText.text = []
					needBox = False
				lastSelect = currentFunction
		instructionText.update()
		dataText.update()
		for i in range(len(blackRectList)):
			r = blackRectList[i]
			pygame.draw.rect(screen, (0,0,0), r)
			c = (255,255,255)
			if i == currentFunction:
				c = (88, 214, 141)
			pygame.draw.rect(screen, c, pygame.Rect(r.x+3, r.y+3, 150, 150))
		screen.blit(vaultimg, (50, 0))
		if vaultOpen:
			screen.blit(notesimg, (310, 280))
		screen.blit(deleteimg, (3, 3))
		screen.blit(notepadimg, (649, 0))
		screen.blit(folderimg, (-2, 442))
		screen.blit(keyimg, (644, 444))
		r = input_box.rect
		input_box.rect = pygame.Rect(400-(r.width/2), 380-(r.height/2), r.width, r.height)
		if not needBox:
			input_box.text = ''
			input_box.txt_surface = input_box.textFont.render(input_box.text, True, input_box.color)
			input_box.rect.w = input_box.calc_width()
		else:
			pygame.draw.rect(screen, pygame.Color('lightskyblue3'), pygame.Rect(r.x-20, r.y-20, r.width+40, r.height+40))
			pygame.draw.rect(screen, (255,255,255), pygame.Rect(r.x-18, r.y-18, r.width+36, r.height+36))
			input_box.draw(screen)
		r = instructionText.rect
		instructionText.rect = pygame.Rect(400-(r.width/2), 260-(r.height/2), r.width, r.height)
		if instructionText.text != []:
			r = instructionText.rect
			pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(r.x-20, r.y-20, r.width+40, r.height+40))
			pygame.draw.rect(screen, (255,255,255), pygame.Rect(r.x-18, r.y-18, r.width+36, r.height+36))
			instructionText.draw(screen)
		if showData:
			bordercolor = (0, 0, 255)
			fillcolor = (255, 255, 255)
			pygame.draw.rect(screen, bordercolor, pygame.Rect(0, 0, 800, 600))
			pygame.draw.rect(screen, fillcolor, pygame.Rect(2, 2, 796, 596))
			pygame.draw.rect(screen, bordercolor, pygame.Rect(3, 3, 794, 594))
			pygame.draw.rect(screen, fillcolor, pygame.Rect(5, 5, 790, 590))
			dataText.draw(screen)
		pygame.display.update()
		pygame.time.wait(17)

if __name__ == '__main__':
	main()