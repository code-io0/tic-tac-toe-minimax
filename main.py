import numpy as np
import pygame
import sys
from pygame.locals import *
from math import inf

def is_valid_move(board, row, col):
	return board[row][col] == 0

def draw_board():
	for row in range(3):
		for col in range(3):
			if board[row][col] == 1:
				screen.blit(o_image, ((col*200)+8, (row*200)+8))
			elif board[row][col] == -1:
				screen.blit(x_image, ((col*200)+8, (row*200)+8))

def win(state, player):

	win_state = [
		[state[0][0], state[0][1], state[0][2]],
		[state[1][0], state[1][1], state[1][2]],
		[state[2][0], state[2][1], state[2][2]],
		[state[0][0], state[1][0], state[2][0]],
		[state[0][1], state[1][1], state[2][1]],
		[state[0][2], state[1][2], state[2][2]],
		[state[0][0], state[1][1], state[2][2]],
		[state[2][0], state[1][1], state[0][2]],
	]

	if [player, player, player] in win_state:
		return True
	else:
		return False

def game_over(state):
	return win(state, COMP) or win(state, HUMAN)

def evaluate(state):

	if win(state, COMP):
		return 1
	elif win(state, HUMAN):
		return -1

	else:
		return 0

def empty_cells(board):

	cells = []

	for row in range(3):
		for col in range(3):
			if board[row][col] == 0:
				cells.append([row, col])

	return cells


def display_message(msg):
	text = game_font.render(msg, True, white, blue)
	text_rect = text.get_rect(center=(WIDTH//2,HEIGHT//2))
	screen.blit(text, text_rect)


def minimax(state, depth, player):

	if player == COMP:
		best = [-1, -1, -inf]
	else:
		best = [-1, -1, inf]

	if game_over(state) or depth == 0:
		score = evaluate(board)
		return [-1, -1, score]

	for cell in empty_cells(state):
		row, col = cell
		state[row][col] = player
		score = minimax(state, depth - 1, -player)
		state[row][col] = 0
		score[0], score[1] = row, col


		if player == COMP:
			if score[2] > best[2]:
				best = score # max value

		else:
			if score[2] < best[2]:
				best = score # min value

	return best

pygame.init()

WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")

bg_image = pygame.image.load("background.png")
bg_image = pygame.transform.scale(bg_image, (600,600))

board = np.zeros((3,3))


COMP = 1
HUMAN = -1

TURN = 0

o_image = pygame.image.load("o.png")
x_image = pygame.image.load("x.png")

game_font = pygame.font.SysFont('arial', 70)

white = pygame.Color('white')
blue = pygame.Color("#8114FF")

while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()


		if event.type == MOUSEBUTTONDOWN:
			x,y = event.pos

			row = y//200
			col = x//200


			if is_valid_move(board, row, col):
				board[row][col] = -1
				depth = len(empty_cells(board))
				comp_move = minimax(board, depth, COMP)
				row, col = comp_move[0],  comp_move[1]
				board[row][col] = 1



	screen.blit(bg_image, (0,0))
	draw_board()
	pygame.display.update()

	if game_over(board):
		if evaluate(board) == 1:
			display_message("  Computer won!  ")
		else:
			display_message("  You won!  ")

		pygame.display.update()
		pygame.time.delay(3000)
		board = np.zeros((3,3))


	if len(empty_cells(board)) == 0 and evaluate(board) == 0:
		display_message("  Its a draw  ")
		pygame.display.update()
		pygame.time.delay(3000)
		board = np.zeros((3,3))

