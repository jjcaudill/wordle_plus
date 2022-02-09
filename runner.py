import time
import sys
import random
from string import ascii_lowercase
import enum
from termcolor import colored

LIMIT = 6

class InvalidSizeError(Exception):
	pass

class Match(enum.Enum):
	UNKNOWN = 1
	NONE = 2
	LETTER = 3
	SPACE = 4

COLORS_GUESSES = {
	Match.NONE : 'red', 
	Match.LETTER : 'yellow', 
	Match.SPACE : 'green', 
}

COLORS_LETTERS = {
	Match.UNKNOWN : 'white', 
	Match.LETTER : 'cyan', 
	Match.SPACE : 'cyan', 
}

def print_out(s):
	sys.stdout.write(f'\r{s}')
	sys.stdout.flush()

def set_up_game():
	word_size = input('What word size: ')
	try:
		return Wordle(int(word_size))
	except (InvalidSizeError, ValueError) as e:
		print('Try a different word size')
		return set_up_game()

def import_dict(size):
	d = []
	filename = 'dictionary.txt'
	with open(filename, 'r') as f:
		for line in f:
			d += line.trim()


class Wordle:
	def __init__(self, word_size):
		# (Word -> [charcter, Match])
		self._guesses = []
		self._size = word_size
		self._dict = set()
		self.import_dict(word_size)
		num = len(self._dict)
		print(f'There are {num} English words of length {word_size}')
		if num < 2:
			raise InvalidSizeError()
		self._answer = list(self._dict)[random.randint(0, num-1)]
		self._answer_count = {}
		for c in self._answer:
			if c not in self._answer_count:
				self._answer_count[c] = 0
			self._answer_count[c] += 1
		self._letters = {c : Match.UNKNOWN for c in ascii_lowercase}

	def import_dict(self, size):
		filename = 'dictionary.txt'
		with open(filename, 'r') as f:
			for line in f:
				word = line.rstrip()
				if len(word) == size:
					self._dict.add(word.lower())

	def play_turn(self, error=''):
		print(f'\n{error}\n')
		self.print_guesses()
		self.print_letters()
		guess = input('Enter next guess: ').lower()
		if len(guess) != self._size:
			return self.play_turn('Enter a word of valid length')
		if guess not in self._dict:
			return self.play_turn('Enter a valid English word')
		if guess in [k for k,_ in self._guesses]:
			return self.play_turn('Enter a new word')

		match = []
		counts = {k:v for k,v in self._answer_count.items()}
		for i in range(self._size):
			c = guess[i]
			if c == self._answer[i]:
				match.append((c,Match.SPACE))
				counts[c] -= 1
			else:
				match.append((c,Match.NONE))

		# Go back through and make letter matches
		for i in range(self._size):
			c,m = match[i]
			if m == Match.NONE and c in counts and counts[c] > 0:
				match[i] = (c, Match.LETTER)


		self._guesses.append((guess, match))

		self.update_letters(match)
		return guess

	def update_letters(self, match):
		for c, m in match:
			self._letters[c] = m

	def print_guesses(self):
		for _, m in self._guesses:
			color_guess = ''
			for c, t in m:
				color_guess += colored(c, COLORS_GUESSES[t])
			print(color_guess)

	def print_letters(self):
		letters = ''
		for c,m in self._letters.items():
			if m != Match.NONE:
				letters += colored(c, COLORS_LETTERS[m])

		print(letters)

	def get_answer(self):
		return self._answer

def main():
	game = set_up_game()
	answer = game.get_answer()
	turn = 0
	while turn < LIMIT:
		guess = game.play_turn()
		if guess == answer:
			print('You win!')
			return
		turn += 1
	print(f'It was {answer}')

if __name__ == '__main__':
    main()