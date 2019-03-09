#encoding: utf-8
#Bf interpreter by Max Petschack
#Bf is a turing complete cell based programming language invented by Urban Muller
#It is comprised of 8 characters and has no conditionals, only loops, incrementing and decrementing by 1 at a time, reading user input and printing the ascii value of a cell
#Each cell is represented by one byte and there are infinite of them
#Link to the wiki page: en.m.wikipedia.org/wiki/Brainfuck

import re
import time

visualizer = False #Decides if we display a visulisation of the bf program being run
cells = [0] #Creates the list of cells. Starts with one cell with a value of zero
program = open('source.bf').read() #Read source code from file
program = re.sub('[^\[\]\.\,\+\-\<\>]','',program) #Removes all non valid chars using regex
curchar = 0 #Current sourcecode char

try: #Makes sure the source code isn't empty
	char = program[curchar]
except:
	print 'Source file is empty'

curcell = 0 #Current cell
stack = '' #Keeps track of everything we've printed to screen

#Here we define the functions attatched to each bf char
#None can have arguments as we call them blindly

def change_cell_value(): #Increments or decremememts current cell by 1 depending on current char
	cells[curcell] = cells[curcell]+1 if char == '+' else cells[curcell]-1 #Change cell value
	#Keeps cell value within 1 byte
	if cells[curcell] > 255:
		cells[curcell] = 0
	elif cells[curcell] < 0:
		cells[curcell] = 255
		
def change_cell(): #Moves current cell pointer
	global curcell
	curcell = curcell+1 if char == '>' else curcell-1 #Find currchar and move pointer accordingly
	if curcell < 0: #Stop the pointer moving to cells that can't exist ie. moves too far left
		curcell = 0
	if curcell > len(cells)-1: #Creates new cells when needed ie. moves too far right
		cells.append(0)

def get_input(): #Gets exactly one char of input from user and puts its ascii val in the current cell
	inp = raw_input('')[0]
	cells[curcell] = ord(inp) #Erases user input prompt

def print_cell(): #Converts current cell value to ascii char, adds to stack and prints stack
	#Clear incase we've already done this
	global stack
	stack += chr(cells[curcell])
	print stack

def new_loop(): #Check if we should skip the loop and if so do that
	global curchar
	global curcell
	if cells[curcell] == 0:
		looplevel = 1
		while looplevel > 0:
			curchar += 1
			try:
				program[curchar]
			except:
				print 'Brainfuck syntax error. Quitting.'
				print 0/0
			if program[curchar] == ']':
				looplevel -= 1
			elif program[curchar] == '[':
				looplevel += 1

def find_loop(): #Finds the start loop char to match the current end loop char
	global curchar
	global char
	looplevel = 0
	if cells[curcell] != 0: #Checks to make sure the loop shouldn't end yet
		while True:
			curchar -= 1 #Moves the current source char pointer back 1
			char = program[curchar] #Gets the current char
			if char == ']':
				looplevel += 1 #Makes sure we don't accidently stumble into the wrong loop
			if char == '[':
				if looplevel == 0: #If it's higher than 0 then we found the wrong char and need to keep looking
					break
				looplevel -= 1

#Creates character to fucntion lookup
charref = {'+':change_cell_value,'-':change_cell_value,'>':change_cell,'<':change_cell,',':get_input,'.':print_cell,'[':new_loop,
']':find_loop}
	
#Actually start running source
while curchar != len(program):
	char = program[curchar] #Get current char
	charref.get(char)() #Looks up and runs the function attached to the current char
	curchar += 1 #Move char pointer along 1
	if visualizer and char != '.': #Prints the visuliser if it's active and currchar isn't a print char
		print char
		print [[cells[curcell]] if x == curcell else cells[x] for x in range(0,len(cells))]
		time.sleep(0.07)

#Prints at program end
print 'Complete'
print 'Cells:',cells #Can be useful for debugging
