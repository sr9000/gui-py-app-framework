import base64
import io
import random
from typing import List

import PIL
from PIL.Image import Image

from sguif.components import *
from .res import *


class Game(StaticModel):
    icross: Image
    izero: Image
    ifield: Image
    igood: Image
    ievil: Image
    iwincross: Image
    iwinzero: Image
    player_first: bool = True
    field: List[List[int]] = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    seed: int = 0

    def __init__(self) -> None:
        super().__init__()
        self.icross = PIL.Image.open(b642iobytes(crossd))
        self.izero = PIL.Image.open(b642iobytes(zerod))
        self.ifield = PIL.Image.open(b642iobytes(fieldd))
        self.igood = PIL.Image.open(b642iobytes(good))
        self.ievil = PIL.Image.open(b642iobytes(evil))
        self.iwincross = PIL.Image.open(b642iobytes(wincrossd))
        self.iwinzero = PIL.Image.open(b642iobytes(winzerod))


win_places = [
    [(0, 0), (0, 1), (0, 2)],
    [(1, 0), (1, 1), (1, 2)],
    [(2, 0), (2, 1), (2, 2)],
    [(0, 0), (1, 0), (2, 0)],
    [(0, 1), (1, 1), (2, 1)],
    [(0, 2), (1, 2), (2, 2)],
    [(0, 0), (1, 1), (2, 2)],
    [(0, 2), (1, 1), (2, 0)],
]


def b642iobytes(s: str):
    return io.BytesIO(base64.b64decode(s))


def change_turn(m: Game, turn: bool):
    m.player_first = turn


def ai_turn(m: Game):
    turns = [(x, y) for x in range(3) for y in range(3) if m.field[y][x] is None]
    random.shuffle(turns)
    x, y = turns[0]
    m.field[y][x] = not m.player_first


def start_game(m: Game):
    m.field = [[None, None, None], [None, None, None], [None, None, None]]
    m.seed = random.randint(0, 1_000_000)
    if not m.player_first:
        ai_turn(m)


def select_turn_view(m: Game):
    return [[Header('Select your figure')],
            [ComboBoxInput('turn', m.player_first, [True, False], ['Cross', 'Zero'],
                           lambda turn: change_turn(m, turn))],
            [ButtonInput('start', '', img=m.icross if m.player_first else m.izero, img_size=(100, 100),
                         on_input=lambda: start_game(m),
                         transition=lambda: (m, playgame_view))]]


def all_the_same(xs):
    xs = list(xs)
    return len(set(xs)) == 1 and list(set(xs))[0] is not None


def game_ended(m: Game):
    return any(all_the_same(m.field[y][x] for x, y in coords) for coords in win_places)


def player_turn(m: Game, x: int, y: int):
    m.field[y][x] = m.player_first
    if left_turns(m) > 0 and not game_ended(m):
        ai_turn(m)


def left_turns(m: Game):
    return sum(1 for x in range(3) for y in range(3) if m.field[y][x] is None)


def make_field(m: Game, x: int, y: int):
    field = m.field[y][x]
    if field is None:
        return ButtonInput('field', '', lambda: player_turn(m, x, y), img=m.ifield, img_size=(100, 100),
                           transition=lambda: (m, game_ended_view) if game_ended(m) else (m, playgame_view))
    elif field:
        return AutoImage(m.icross, (100, 100), (100, 100))
    else:
        return AutoImage(m.izero, (100, 100), (100, 100))


def fantastic_header(m: Game):
    n = left_turns(m)
    return {
        9: 'YOUR TURN!',
        8: 'FIRST BLOOD!',
        7: 'EXCELLENT!',
        6: 'KILL HIM!',
        5: 'CAN YOU BEAT HIM?',
        4: '2 TURNS LEFT!',
        3: 'DEAD OR ALIVE',
        2: 'FINAL MOVE!',
        1: 'FACE IT!',
        0: 'WOW! IT\'S A DRAW'
    }[n]


def playgame_view(m: Game):
    return [[Header(fantastic_header(m))],
            [Feed(),
             Matrix('game field',
                    [[make_field(m, x, y) for x in range(3)] for y in range(3)]),
             Feed()],
            [] if left_turns(m) > 0 else
            [ButtonInput('reset', 'Fine!', transition=lambda: (m, select_turn_view))]]


def deserved_header(m: Game, strike):
    gw = game_winner(m, strike)
    if gw == m.player_first:
        winh = [
            'easy as pie',
            'easy peasy lemon squeezy',
            'winner winner chicken dinner',
            'G.O.A.T.',
            'GG!'
        ]
        return winh[m.seed % len(winh)]
    else:
        looseh = [
            'Choo Choo Mother Fucker',
            'T2P',
            'what happens in vegas...',
            'btfo',
            'Ok boomer'
        ]
        return looseh[m.seed % len(looseh)]


def game_winner(m, strike):
    x, y = strike[0]
    gw = m.field[y][x]
    return gw


def get_win_strike(m: Game):
    _, strike = next(filter(lambda x: x[0],
                            zip([all_the_same(m.field[y][x] for x, y in coords) for coords in win_places], win_places)))
    return strike


def make_preview(m: Game, x: int, y: int, strike):
    if (x, y) in strike:
        return AutoImage(m.iwincross if m.field[y][x] else m.iwinzero, (100, 100), (100, 100))
    else:
        return ButtonInput(('pv', x, y), '',
                           img={None: m.ifield, True: m.icross, False: m.izero}[m.field[y][x]],
                           img_size=(100, 100),
                           disabled=True)


def game_ended_view(m: Game):
    win_strike = get_win_strike(m)
    return [[Header(deserved_header(m, win_strike))],
            [Feed(),
             Matrix('preview',
                    [[make_preview(m, x, y, win_strike) for x in range(3)] for y in range(3)]),
             Feed()],
            [ButtonInput('reset', '', img_size=(200, 200),
                         img=m.igood if m.player_first == game_winner(m, win_strike) else m.ievil,
                         transition=lambda: (m, select_turn_view))]]
