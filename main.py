import random
import os

def print_mines_layout():

	global mine_values
	global n

	print()
	print("\t\t\tTERMINATE\n")

	st = "   "
	for i in range(n):
		st = st + "     " + str(i + 1)
	print(st)

	for r in range(n):
		st = "     "
		if r == 0:
			for c in range(n):
				st = st + "______"
			print(st)

		st = "     "
		for c in range(n):
			st = st + "|     "
		print(st + "|")

		st = "  " + str(r + 1) + "  "
		for c in range(n):
			st = st + "|  " + str(mine_values[r][c]) + "  "
		print(st + "|")

		st = "     "
		for c in range(n):
			st = st + "|_____"
		print(st + '|')

	print()

def set_mines():

	global numbers
	global mines_no
	global n
	count = 0
	while count < mines_no:

		val = random.randint(0, n*n-1)

		r = val // n
		c = val % n

		if numbers[r][c] != -1:
			count = count + 1
			numbers[r][c] = -1

def set_values():

	global numbers
	global n

	for r in range(n):
		for c in range(n):

			if numbers[r][c] == -1:
				continue

			if r > 0 and numbers[r-1][c] == -1:
				numbers[r][c] = numbers[r][c] + 1
			if r < n-1  and numbers[r+1][c] == -1:
				numbers[r][c] = numbers[r][c] + 1
			if c > 0 and numbers[r][c-1] == -1:
				numbers[r][c] = numbers[r][c] + 1
			if c < n-1 and numbers[r][c+1] == -1:
				numbers[r][c] = numbers[r][c] + 1
			if r > 0 and c > 0 and numbers[r-1][c-1] == -1:
				numbers[r][c] = numbers[r][c] + 1
			if r > 0 and c < n-1 and numbers[r-1][c+1] == -1:
				numbers[r][c] = numbers[r][c] + 1
			if r < n-1 and c > 0 and numbers[r+1][c-1] == -1:
				numbers[r][c] = numbers[r][c] + 1
			if r < n-1 and c < n-1 and numbers[r+1][c+1] == -1:
				numbers[r][c] = numbers[r][c] + 1

def neighbours(r, c):

	global mine_values
	global numbers
	global vis

	if [r,c] not in vis:

		vis.append([r,c])

		if numbers[r][c] == 0:

			mine_values[r][c] = numbers[r][c]
			if r > 0:
				neighbours(r-1, c)
			if r < n-1:
				neighbours(r+1, c)
			if c > 0:
				neighbours(r, c-1)
			if c < n-1:
				neighbours(r, c+1)
			if r > 0 and c > 0:
				neighbours(r-1, c-1)
			if r > 0 and c < n-1:
				neighbours(r-1, c+1)
			if r < n-1 and c > 0:
				neighbours(r+1, c-1)
			if r < n-1 and c < n-1:
				neighbours(r+1, c+1)

		if numbers[r][c] != 0:
				mine_values[r][c] = numbers[r][c]

def clear():
	os.system("clear")

def instructions():
	print("Instructions:")
	print("1. Enter row and column number to select a cell, Example \"2 3\"")
	print("2. In order to flag a mine, enter F after row and column numbers, Example \"2 3 F\"")

def check_over():
	global mine_values
	global n
	global mines_no

	count = 0

	for r in range(n):
		for c in range(n):

			if mine_values[r][c] != ' ' and mine_values[r][c] != 'F':
				count = count + 1

	if count == n * n - mines_no:
		return True
	else:
		return False

def show_mines():
	global mine_values
	global numbers
	global n

	for r in range(n):
		for c in range(n):
			if numbers[r][c] == -1:
				mine_values[r][c] = 'M'


if __name__ == "__main__":
	print("Set the size of board")
	n = int(input())
	print("Set the number of mines")
	mines_no = int(input())

	numbers = [[0 for y in range(n)] for x in range(n)]
	mine_values = [[' ' for y in range(n)] for x in range(n)]
	flags = []

	set_mines()

	set_values()

	instructions()

	over = False

	while not over:
		print_mines_layout()

		inp = input("Enter row number followed by space and column number = ").split()

		if len(inp) == 2:

			try:
				val = list(map(int, inp))
			except ValueError:
				clear()
				print("Wrong input!")
				instructions()
				continue

		elif len(inp) == 3:
			if inp[2] != 'F' and inp[2] != 'f':
				clear()
				print("Wrong Input!")
				instructions()
				continue

			try:
				val = list(map(int, inp[:2]))
			except ValueError:
				clear()
				print("Wrong input!")
				instructions()
				continue

			if val[0] > n or val[0] < 1 or val[1] > n or val[1] < 1:
				clear()
				print("Wrong input!")
				instructions()
				continue

			r = val[0]-1
			c = val[1]-1

			if [r, c] in flags:
				clear()
				print("Flag already set")
				continue

			if mine_values[r][c] != ' ':
				clear()
				print("Value already known")
				continue

			if len(flags) < mines_no:
				clear()
				print("Flag set")

				flags.append([r, c])

				mine_values[r][c] = 'F'
				continue
			else:
				clear()
				print("Flags finished")
				continue

		else:
			clear()
			print("Wrong input!")
			instructions()
			continue


		if val[0] > n or val[0] < 1 or val[1] > n or val[1] < 1:
			clear()
			print("Wrong Input!")
			instructions()
			continue

		r = val[0]-1
		c = val[1]-1

		if [r, c] in flags:
			flags.remove([r, c])

		if numbers[r][c] == -1:
			mine_values[r][c] = 'M'
			show_mines()
			print_mines_layout()
			print("Landed on a mine. GAME OVER!!!!!")
			over = True
			continue

		elif numbers[r][c] == 0:
			vis = []
			mine_values[r][c] = '0'
			neighbours(r, c)

		else:
			mine_values[r][c] = numbers[r][c]

		if(check_over()):
			show_mines()
			print_mines_layout()
			print("Congratulations!!! YOU WIN")
			over = True
			continue
		clear()
