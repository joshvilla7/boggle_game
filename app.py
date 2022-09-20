from flask import Flask, request, session, render_template, jsonify
from boggle import Boggle

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret_key"
boggle_game = Boggle()


@app.route('/')
def show_board():
    """shows gameboard on route page"""
    board = boggle_game.make_board()

    #add board, highscore, and num_plays to session
    session['board'] = board
    highscore = session.get("highscore", 0)
    num_plays = session.get("num_plays", 0)

    return render_template("index.html", board=board,highscore=highscore,num_plays=num_plays)

@app.route('/check-word')
def check_word():
    """check if submitted word is a word"""
    word = request.args["word"]
    board = session["board"]
    res = boggle_game.check_valid_word(board, word)

    return jsonify({'result': res})

@app.route('/game-over', methods=["POST"])
def game_over():
    """when timer runs out, finalize score, updates highscore and number of times played"""
    score = request.json["score"]
    highscore = session.get('highscore', 0)
    num_plays = session.get('num_plays', 0)

    session['num_plays'] = num_plays + 1
    session['highscore'] = max(score, highscore)

    return jsonify(newRecord=score > highscore)
    
    

