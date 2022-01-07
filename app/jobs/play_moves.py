


import os
#from types import SimpleNamespace as Outcome

from pandas import DataFrame

from app import OPPOSITE_LETTERS
from app.game import Game
from app.player import select_player
from app.jobs.timer import Timer


# for the strategies, use "RANDOM" for random moves, or "MINIMAX-AB" for expert moves
X_STRATEGY = os.getenv("X_STRATEGY", default="RANDOM")
O_STRATEGY = os.getenv("O_STRATEGY", default="RANDOM")

GAME_COUNT = int(os.getenv("GAME_COUNT", default="100_000"))

if __name__ == "__main__":

    timer = Timer()
    timer.start()

    records = []
    for game_counter in range(0, GAME_COUNT):
        game = Game(players=[
            select_player(letter="X", strategy=X_STRATEGY),
            select_player(letter="O", strategy=O_STRATEGY),
        ])

        #
        # PLAY
        #

        game.play()

        # determine reward values for each player
        if game.winner:
            winning_letter = game.winner["letter"]
            losing_letter = OPPOSITE_LETTERS[winning_letter]

            rewards = {winning_letter: 1, losing_letter: 0}
        else:
            rewards = {"X": 1, "O": 0}

        #
        # PLAYBACK
        #

        for move_counter, move in enumerate(game.move_history):
            print(move) #>

            active_player = move.active_player

            records.append({
                "game_id": game_counter + 1, # start ids at 1 instead of 0
                "move_id": move_counter + 1, # start ids at 1 instead of 0
                "board_state": move.board_state,
                "player": active_player,
                "selected_square": move.selected_square,
                "reward": rewards[active_player],
            })

    timer.end()
    print("------------------------")
    print("PLAYED", GAME_COUNT, "GAMES", f"IN {timer.duration_seconds} SECONDS")
    print("TOTAL MOVES:", len(records))

    df = DataFrame(records)
    print(df.head())

    print("------------------------")
    print("SAVING DATA TO FILE...")

    csv_filename = f"{game.players[0].letter}_{game.players[0].player_type}"
    csv_filename += "_vs_"
    csv_filename += f"{game.players[1].letter}_{game.players[1].player_type}"
    csv_filename += f"_{GAME_COUNT}.csv"
    csv_filename = csv_filename.lower()
    csv_filepath = os.path.join(os.path.dirname(__file__), "..", "..", "data", "moves", csv_filename)

    df.to_csv(csv_filepath, index=False)
    print(os.path.abspath(csv_filepath))

    #breakpoint()