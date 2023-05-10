import random as rd
import chess as ch
import chess.polyglot
import time
from IPython.display import display
import chess.variant

class GuilloBot:
    
    def __init__(self, board, maxDepth, color, var):
        self.board = board
        self.var = var
        self.maxDepth = maxDepth
        self.color = color
        self.start = True
        self.pawnTab = [ 0,  0,  0,  0,  0,  0,  0,  0,
                        50, 50, 50, 50, 50, 50, 50, 50,
                        10, 10, 20, 30, 30, 20, 10, 10,
                         5,  5, 10, 25, 25, 10,  5,  5,
                         0,  0,  0, 20, 20,  0,  0,  0,
                         5, -5,-10,  0,  0,-10, -5,  5,
                         5, 10, 10, -10, -10, 10, 10,  5,
                         0,  0,  0,  0,  0,  0,  0,  0]
        self.knightTab = [-50,-20,-30,-30,-30,-30,-20,-50,
                            -40,-20,  0,  0,  0,  0,-20,-40,
                            -30,  0, 10, 15, 15, 10,  0,-30,
                            -30,  5, 15, 20, 20, 15,  5,-30,
                            -30,  0, 15, 20, 20, 15,  0,-30,
                            -30,  5, 10, 15, 15, 10,  5,-30,
                            -40,-20,  0,  5,  5,  0,-20,-40,
                            -50,-20,-30,-30,-30,-30,-20,-50]
        self.bishopTab = [-20,-10,-10,-10,-10,-10,-10,-20,
                            -10,  0,  0,  0,  0,  0,  0,-10,
                            -10,  0,  5, 10, 10,  5,  0,-10,
                            -10,  5,  5, 10, 10,  5,  5,-10,
                            -10,  0, 10, 10, 10, 10,  0,-10,
                            -10, 10, 10, 10, 10, 10, 10,-10,
                            -10,  5,  0,  0,  0,  0,  5,-10,
                            -20,-10,-10,-10,-10,-10,-10,-20]
        self.rookTab = [0,  0,  0,  0,  0,  0,  0,  0,
                          5, 10, 10, 10, 10, 10, 10,  5,
                          -5,  0,  0,  0,  0,  0,  0, -5,
                          -5,  0,  0,  0,  0,  0,  0, -5,
                          -5,  0,  0,  0,  0,  0,  0, -5,
                          -5,  0,  0,  0,  0,  0,  0, -5,
                          -5,  0,  0,  0,  0,  0,  0, -5,
                          0,  0,  0,  5,  5,  0,  0,  0]
        self.queenTab = [-20,-10,-10, -5, -5,-10,-10,-20,
                           -10,  0,  0,  0,  0,  0,  0,-10,
                           -10,  0,  5,  5,  5,  5,  0,-10,
                           -5,  0,  5,  5,  5,  5,  0, -5,
                           0,  0,  5,  5,  5,  5,  0, -5,
                           -10,  5,  5,  5,  5,  5,  0,-10,
                           -10,  0,  5,  0,  0,  0,  0,-10,
                           -20,-10,-10, 200, 200,-10,-10,-20]
        self.kingTabMG = [-30,-40,-40,-50,-50,-40,-40,-30,
                          -30,-40,-40,-50,-50,-40,-40,-30,
                          -30,-40,-40,-50,-50,-40,-40,-30,
                          -30,-40,-40,-50,-50,-40,-40,-30,
                          -20,-30,-30,-40,-40,-30,-30,-20,
                          -10,-20,-20,-20,-20,-20,-20,-10,
                          -20, -20,  -20,  -20,  -20,  -20, -20, -20,
                          20, 30, 10,  0,  0, 10, 30, 20]
        
    def getBestMove(self):
        return self.engine(None, 1)
    
    
    def evalFunct(self):
        compt = 0
        for i in range(64):
            compt += self.squareResPoint(ch.SQUARES[i], i)
        compt += self.mateOpportunity() + 0.001 * rd.random()
        if self.board.is_stalemate():
            return 0
        return compt
        
    def mateOpportunity(self):
        if (self.board.legal_moves.count() == 0):
            if (self.board.turn == self.color):
                return -99999
            else:
                return 99999
        else:
            return 0
    
    def squareResPoint(self, square, i):
        pieceValue = 0
        if(self.board.color_at(square) != self.color):
            turn = -1
        else:
            turn = 1
        if(self.board.piece_type_at(square) == ch.PAWN):
            pieceValue = 100
            if turn == 1:
                pieceValue += self.pawnTab[i]
            else:
                pieceValue += self.pawnTab[63-i]
        if(self.board.piece_type_at(square) == ch.ROOK):
            pieceValue = 500
            if turn == 1:
                pieceValue += self.rookTab[i]
            else:
                pieceValue += self.rookTab[63-i]
        if(self.board.piece_type_at(square) == ch.QUEEN):
            pieceValue = 900
            if turn == 1:
                pieceValue += self.queenTab[i]
            else:
                pieceValue += self.queenTab[63-i]
        if(self.board.piece_type_at(square) == ch.BISHOP):
            pieceValue = 333
            if turn == 1:
                pieceValue += self.bishopTab[i]
            else:
                pieceValue += self.bishopTab[63-i]
        if(self.board.piece_type_at(square) == ch.KNIGHT):
            pieceValue = 320
            if turn == 1:
                pieceValue += self.knightTab[i]
            else:
                pieceValue += self.knightTab[63-i]
        return pieceValue * turn
    

    def engine(self, candidate, depth):
        if self.start and not self.var:
            with ch.polyglot.open_reader("codekiddy.bin") as reader:
                for entry in reader.find_all(self.board):
                    time.sleep(1)
                    move = reader.weighted_choice(self.board).move
                    print(move)
                    return move
        self.start = False
        if (depth == self.maxDepth or self.board.legal_moves.count() == 0):
            return self.evalFunct()
        else:
            moveList = list(self.board.legal_moves)
            
            newCandidate = None
            
            if depth % 2 != 0:
                newCandidate = float("-inf")
            else:
                newCandidate = float("inf")
            for i in moveList:
                self.board.push(i)
                
                value = self.engine(newCandidate, depth+1)
                
                if(value > newCandidate and depth % 2 != 0):
                    newCandidate = value
                    if(depth == 1):
                        move = i
                elif(value < newCandidate and depth % 2 == 0):
                    newCandidate = value
                    
                #Alpha-beta pruning:
                if (candidate != None and value < candidate and depth % 2 == 0):
                    self.board.pop()
                    break
                
                elif (candidate != None and value > candidate and depth % 2 != 0):
                    self.board.pop()
                    break
                
                self.board.pop()
                
        if (depth > 1):
            return newCandidate
        else:
            print(move)
            return move
        
class Main:

    def __init__(self, board=ch.Board):
        self.board=board

    #play human move
    def playHumanMove(self):
        try:
            print(self.board.legal_moves)
            print("""To undo your last move, type "undo".""")
            #get human move
            play = input("Your move: ")
            if (play=="undo"):
                self.board.pop()
                self.board.pop()
                display(self.board)
                self.playHumanMove()
                return
            self.board.push_san(play)
        except:
            self.playHumanMove()

    #play engine move
    def playEngineMove(self, maxDepth, color, var):
        engine = GuilloBot(self.board, maxDepth, color, var)
        self.board.push(engine.getBestMove())

    #start a game
    def startGame(self, var):
        #get human player's color
        color=None
        while(color!="b" and color!="w"):
            color = input("""Play as (type "b" or "w"): """)
        maxDepth=None
        while(isinstance(maxDepth, int)==False):
            maxDepth = int(input("""Choose depth: """))
        if color=="b":
            while (self.board.is_checkmate()==False):
                print("The engine is thinking...")
                self.playEngineMove(maxDepth, ch.WHITE, var)
                display(self.board)
                self.playEngineMove(maxDepth, ch.BLACK, var)
                display(self.board)
            print(self.board)
            print(self.board.outcome())    
        elif color=="w":
            while (self.board.is_checkmate()==False):
                display(self.board)
                self.playHumanMove()
                display(self.board)
                print("The engine is thinking...")
                self.playEngineMove(maxDepth, ch.BLACK, var)
            print(self.board)
            print(self.board.outcome())
        #reset the board
        self.board.reset
        #start another game
        self.startGame()

#create an instance and start a game
newBoard = ch.Board()
game = Main(newBoard)
bruh = game.startGame(False)