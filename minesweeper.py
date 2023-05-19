#!/usr/bin/env python

import collections
import copy
import itertools
import pprint
import random
from typing import Optional, List, Union

# TODO(jdbus): Make these flags
_WIDTH = 10
_HEIGHT = 16
_BOMBCOUNT = 10

# Tiles will be 'X' for bomb or 0-9 representing adjacent bombs.
TileValue = Union[int, str]
Board = List[List[TileValue]]  # this should really be an object...

def adjacent_squares(row, col) -> List[List[int]]:
  """Returns a list of (row, col) tiles next to specified tile."""
  squares = itertools.product([row-1, row, row+1], [col-1, col, col+1])
  return [square for square in squares
          if _HEIGHT > square[0] >= 0 
          and _WIDTH > square[1] >= 0
          and (square[0]!=row or square[1]!=col)  # don't return the original
         ]

def buildBoard() -> Board:
  """Builds a board of specified height and width."""
  board = [[0] * _WIDTH for x in range(0,_HEIGHT)]
  bombs = zip(
      [random.randrange(0, _HEIGHT) for x in range(0,_BOMBCOUNT)],
      [random.randrange(0, _WIDTH) for x in range(0,_BOMBCOUNT)])
  for (row,col) in bombs:
    board[row][col] = 'X'
    # Every square around this bomb gets +1 bombcount.
    for adj_square in adjacent_squares(row, col):
      (adj_row, adj_col) = adj_square
      print(f'Bomb in row{row} col{col} adjacent cell row{adj_row} col{adj_col}')
      if board[adj_row][adj_col] != 'X':
        board[adj_row][adj_col] += 1

  return board


def clickTile(
    board: Board, 
    exposures_input: List[List[bool]], 
    row: int, 
    col: int) -> Union[List[List[bool]], str]:  # TODO: return sane values
  print('Click!')
  if board[row][col] == 'X':
    return 'BOOM!'

  exposures = copy.deepcopy(exposures_input)

  to_check = collections.deque()
  to_check.append((row, col))
  while to_check:
    row, col = to_check.popleft()
    print(f'popping and checking r{row} c{col}')
    if exposures[row][col]:
      print('  already exposed, continuing')
      continue  # If this queue is already exposed, don't re-add to queue
    exposures[row][col] = True  # it is now exposed
    if board[row][col] == 0:
      print('  has zero nextdoor, expanding..')
      adjacents = adjacent_squares(row, col)
      for newrow, newcol in adjacents:
        if not exposures[newrow][newcol]:  # only add previously-unexposed
          if (newrow, newcol) not in to_check:  # don't add twice!
            print(f'  appending neighbor r{newrow} c{newcol}')
            to_check.append((newrow, newcol))
          else:
            print(f'  Not appending r{newrow} c{newcol}, already queued')
  return exposures


def visualizeBoard(
  board: Board,
  exposures: Optional[List[List[bool]]] = None,
  uncovered: bool=False) -> List[str]:
  """Returns a row-by-row visualization fo the board.

  If uncovered is true, show the value of ALL tiles, not just user-exposed
  tiles.
  """
  row_template = ' '.join(['{}' for x in range(0, len(board[0]))])
  if uncovered:
    return [row_template.format(*x) for x in board]
  if exposures is None:
    raise ValueError('no exposures map provided')

  # With that out of the way, create a visual of what the user has exposed.
  exposed_board = []
  for row_exposure, row in zip(exposures, board):
    exposed_row = []
    for char_exposure, char in zip(row_exposure, row):
      if not char_exposure:
        newchar = '■'
      elif char_exposure and char==0:
        newchar = ' '
      else:
        newchar = char
      exposed_row.append(newchar)
    exposed_board.append(exposed_row)
  return [row_template.format(*x) for x in exposed_board]


def main():
  playing_board = buildBoard()
  pprint.pprint(visualizeBoard(playing_board, uncovered=True))

  exposed_tiles = [[False] * _WIDTH for x in range(0,_HEIGHT)]


if __name__ == '__main__':
  main()
