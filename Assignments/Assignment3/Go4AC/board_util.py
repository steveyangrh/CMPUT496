EMPTY = 0
BLACK = 1
WHITE = 2
BORDER = 3
FLOODFILL = 4
import numpy as np
from pattern import pat3set
import sys
import random

class GoBoardUtil(object):
    
    @staticmethod       
    def playGame(board, color, **kwargs):
        komi = kwargs.pop('komi', 0)
        limit = kwargs.pop('limit', 1000)
        check_selfatari = kwargs.pop('selfatari', True)
        pattern = kwargs.pop('pattern', True)
        if kwargs:
            raise TypeError('Unexpected **kwargs: %r' % kwargs)
        numPass = 0
        for _ in range(limit):

            # Modify for gtp cmd
            move = GoBoardUtil.generate_move_with_filter(board,pattern,check_selfatari)
                
            # use our policy
            #move = GoBoardUtil.generate_all_policy_moves(board,pattern,check_selfatari)

            
            if move != None:
                isLegalMove = board.move(move,color)
                assert isLegalMove
                numPass = 0
            else:
                board.move(move,color)
                numPass += 1
                if numPass == 2:
                    break
            color = GoBoardUtil.opponent(color)
        winner = board.get_winner(komi)
        return winner
    
    @staticmethod
    def generate_legal_moves(board, color):
        """
        generate a list of legal moves

        Arguments
        ---------
        board : np.array
            a SIZExSIZE array representing the board
        color : {'b','w'}
            the color to generate the move for.
        """
        empty = board.get_empty_points()
        legal_moves = []
        for move in empty:
            if board.check_legal(move, color):
                legal_moves.append(move)
        return legal_moves

    @staticmethod
    def sorted_point_string(points, ns):
        result = []
        for point in points:
            x, y = GoBoardUtil.point_to_coord(point, ns)
            result.append(GoBoardUtil.format_point((x, y)))
        return ' '.join(sorted(result))

    @staticmethod
    def generate_pattern_moves(board):
        color = board.current_player
        pattern_checking_set = board.last_moves_empty_neighbors()
        moves = []
        for p in pattern_checking_set:
            if (board.neighborhood_33(p) in pat3set):
                assert p not in moves
                assert board.board[p] == EMPTY
                moves.append(p)
        final_moves = []
        for al in moves:
            if board.check_legal(al,color):
                final_moves.append(al)
        moves = final_moves;
        return moves
        
    @staticmethod
    def generate_all_policy_moves(board,pattern,check_selfatari):
        """
            generate a list of policy moves on board for board.current_player.
            Use in UI only. For playing, use generate_move_with_filter
            which is more efficient
        """
        
        atari_capture_moves = GoBoardUtil.generate_atari_capture_moves(board)
        atari_capture_moves = GoBoardUtil.filter_moves(board, atari_capture_moves, check_selfatari)     

            
        if len(atari_capture_moves) > 0:
            return atari_capture_moves, "AtariCapture"

        pattern_moves = GoBoardUtil.generate_pattern_moves(board)
        pattern_moves = GoBoardUtil.filter_moves(board, pattern_moves, check_selfatari)


        if len(pattern_moves) > 0:
            return pattern_moves, "Pattern"
            
        return GoBoardUtil.generate_random_moves(board), "Random"


    @staticmethod
    def generate_atari_capture_moves(board):
        color = board.current_player
        '''
        if color == 1:
            color = 'b'
        else:
            color = 'w'
        '''
        moves = []
        last_move = board.last_move
        if last_move is None:
            return moves 

          
        fboard_array = board._flood_fill(last_move)
        board_copy_array= np.array(board.board, copy=True)

        has_liberty = board._liberty_flood(fboard_array)
        if not has_liberty:
            return moves
        else:
            inds = list(*np.where(fboard_array == FLOODFILL))
            total_liberty = 0
            for f in inds:


                if f is None:
                    return []                  

                f_neighbors = board._neighbors(f)                         
                if f_neighbors is None:
                    return []


                for n in f_neighbors:
                    if board_copy_array[n]==EMPTY:

                        
                        row,col = board._point_to_coord(n)
                        #print ("Coor n: " + str([row,col]))
                        #print ("leber: " +str(total_liberty))
                        total_liberty = total_liberty + 1
                        moves.append(n)       

        #remove duplications
        unique_moves=[]
        for i in moves:
            if i not in unique_moves:
                unique_moves.append(i)
        moves=unique_moves;

        if len(moves)==1:
            final_moves = []
            for al in moves:
                if board.check_legal(al,color):
                    final_moves.append(al)
            moves = final_moves;
            return moves
            #respond(self, response = ''):

        moves = []
        return moves         

    def respond(self, response = ''):
        """ Send msg to stdout """
        sys.stdout.write('= {}\n\n'.format(response)); sys.stdout.flush()


    @staticmethod
    def generate_atari_defense_moves(board):
        color = board.current_player
        if color == 1:
            color = 'b'
        else:
            color = 'w'
        moves = []

        opponent_holder = []

        last_move = board.last_move
        if last_move is None:
            return moves
        

        last_move_neighbors = board._neighbors(last_move)
        '''
        print(last_move)
        print(last_move_neighbors)
        '''
        for al in last_move_neighbors: #al are the neighbors of the last move(opponent)
            if (board._points_color(al) == color): 
                fboard_array = board._flood_fill(al)
                board_copy_array = np.array(board.board, copy=True)
                has_liberty = board._liberty_flood(fboard_array)
                if not has_liberty:
                    pass
                else:
                    inds = list(*np.where(fboard_array == FLOODFILL))
                    #inds are the FLOODFILLs
                    temp_moves = []
                    for f in inds:
                        if f is not None:
                            f_neighbors = board._neighbors(f)
                            for n in f_neighbors:
                                if board_copy_array[n]==EMPTY:     
                                    temp_moves.append(n)
                                if color == 'w':
                                    if board_copy_array[n]== BLACK:
                                        opponent_holder.append(n)
                                if color == 'b':
                                    if board_copy_array[n]== WHITE:
                                        opponent_holder.append(n)
                    temp_unique_moves=[]
                    for i in temp_moves:
                        if i not in temp_unique_moves:
                            temp_unique_moves.append(i)
                    temp_moves=temp_unique_moves
                    if(len(temp_moves)==1):
                        moves.extend(temp_moves)
                
        unique_moves=[]
        for i in moves:
            if i not in unique_moves:
                unique_moves.append(i)
        moves=unique_moves;

        unique_opponent_moves=[]
        for i in opponent_holder:
            if i not in unique_opponent_moves:
                unique_opponent_moves.append(i)
        opponent_holder=unique_opponent_moves;

        for o in opponent_holder:
            fboard_array = board._flood_fill(o)
            board_copy_array = np.array(board.board, copy=True)
            has_liberty = board._liberty_flood(fboard_array)
            if not has_liberty:
                pass
            else:
                inds = list(*np.where(fboard_array == FLOODFILL))
                #inds are the FLOODFILLs
                temp_moves = []
                for f in inds:
                    if f is not None:
                        f_neighbors = board._neighbors(f)
                        for n in f_neighbors:
                            if board_copy_array[n]==EMPTY:     
                                temp_moves.append(n)
                    temp_unique_moves=[]
                    for i in temp_moves:
                        if i not in temp_unique_moves:
                            temp_unique_moves.append(i)
                    temp_moves=temp_unique_moves
                    if(len(temp_moves)==1):
                        moves.extend(temp_moves)
          
        unique_moves=[]
        for i in moves:
            if i not in unique_moves:
                unique_moves.append(i)
        moves=unique_moves; 

        final_moves = []
        color = board.current_player
        for al in moves:
            if board.check_legal(al,color):
                final_moves.append(al)
        moves = final_moves;     
        return moves

        
    @staticmethod
    def generate_random_move(board):
        color = board.current_player
        moves = board.get_empty_points()
        while len(moves) > 0:
            index = random.randint(0,len(moves) - 1)
            move = moves[index]
            if board.check_legal(move, color) and not board.is_eye(move, color):
                return move
            else:
                # delete moves[index] by overwriting with last in list
                lastIndex = len(moves) - 1
                if index < lastIndex:
                    moves[index] = moves[lastIndex]
                moves.pop()
        return None
    
    @staticmethod
    def generate_random_moves(board):
        empty_points = board.get_empty_points()
        color = board.current_player
        moves = []
        for move in empty_points:
            if board.check_legal(move, color) and not board.is_eye(move, color):
                moves.append(move)
        return moves

    @staticmethod
    def filter_moves(board, moves, check_selfatari):
        color = board.current_player
        good_moves = []
        for move in moves:
            if not GoBoardUtil.filter(board,move,color,check_selfatari):
                good_moves.append(move)
        return good_moves
    # return True if move should be filtered
    @staticmethod
    def filter(board, move, color, check_selfatari):

        '''
        ataFileter=GoBoardUtil.selfatari_filter(board, move, color)
        eyeFilter=GoBoardUtil.filleye_filter(board, move, color)

        if (ataFileter is True) or (eyeFilter is True):
            return True
        return False
        '''     

        
        
        if check_selfatari:
            return GoBoardUtil.selfatari_filter(board, move, color)
        else:
            return GoBoardUtil.filleye_filter(board, move, color)
        

    # return True if move should be filtered
    @staticmethod
    def filleye_filter(board, move, color):
        assert move != None
        return not board.check_legal(move, color) or board.is_eye(move, color)
    
    # return True if move should be filtered
    @staticmethod
    def selfatari_filter(board, move, color):
        return (  GoBoardUtil.filleye_filter(board, move, color)
               or GoBoardUtil.selfatari(board, move, color)
               )


    @staticmethod 
    def filter_moves_and_generate(board, moves, check_selfatari):
        color = board.current_player
        while len(moves) > 0:
            candidate = random.choice(moves)
            if GoBoardUtil.filter(board, candidate, color, check_selfatari):
                moves.remove(candidate)
            else:
                return candidate
        return None
        
    @staticmethod
    def generate_move_with_filter(board, use_pattern, check_selfatari):
        """
            Arguments
            ---------
            check_selfatari: filter selfatari moves?
                Note that even if True, this filter only applies to pattern moves
            use_pattern: Use pattern policy?
        """
        move = None
        if use_pattern:
            moves = GoBoardUtil.generate_pattern_moves(board)
            move = GoBoardUtil.filter_moves_and_generate(board, moves, 
                                                         check_selfatari)
            # gneratve atari and defence

                                                         
        if move == None:
            move = GoBoardUtil.generate_random_move(board)
        return move 
    
    @staticmethod
    def selfatari(board, move, color):
        max_old_liberty = GoBoardUtil.blocks_max_liberty(board, move, color, 2)
        if max_old_liberty > 2:
            return False
        cboard = board.copy()
        # swap out true board for simulation board, and try to play the move
        isLegal = cboard.move(move, color) 
        if isLegal:               
            new_liberty = cboard._liberty(move,color)
            if new_liberty==1:
                return True 
        return False

    @staticmethod
    def blocks_max_liberty(board, point, color, limit):
        assert board.board[point] == EMPTY
        max_lib = -1 # will return this value if this point is a new block
        neighbors = board._neighbors(point)
        for n in neighbors:
            if board.board[n] == color:
                num_lib = board._liberty(n,color) 
                if num_lib > limit:
                    return num_lib
                if num_lib > max_lib:
                    max_lib = num_lib
        return max_lib
        
    @staticmethod
    def format_point(move):
        """
        Return coordinates as a string like 'a1', or 'pass'.

        Arguments
        ---------
        move : (row, col), or None for pass

        Returns
        -------
        The move converted from a tuple to a Go position (e.g. d4)
        """
        column_letters = "abcdefghjklmnopqrstuvwxyz"
        if move is None:
            return "pass"
        row, col = move
        if not 0 <= row < 25 or not 0 <= col < 25:
            raise ValueError
        return    column_letters[col - 1] + str(row) 
        
    @staticmethod
    def move_to_coord(point, board_size):
        """
        Interpret a string representing a point, as specified by GTP.

        Arguments
        ---------
        point : str
            the point to convert to a tuple
        board_size : int
            size of the board

        Returns
        -------
        a pair of coordinates (row, col) in range(1, board_size+1)

        Raises
        ------
        ValueError : 'point' isn't a valid GTP point specification for a board of size 'board_size'.
        """
        if not 0 < board_size <= 25:
            raise ValueError("board_size out of range")
        try:
            s = point.lower()
        except Exception:
            raise ValueError("invalid point")
        if s == "pass":
            return None
        try:
            col_c = s[0]
            if (not "a" <= col_c <= "z") or col_c == "i":
                raise ValueError
            if col_c > "i":
                col = ord(col_c) - ord("a")
            else:
                col = ord(col_c) - ord("a") + 1
            row = int(s[1:])
            if row < 1:
                raise ValueError
        except (IndexError, ValueError):
            raise ValueError("wrong coordinate")
        if not (col <= board_size and row <= board_size):
            raise ValueError("wrong coordinate")
        return row, col
    
    @staticmethod
    def opponent(color):
        opponent = {WHITE:BLACK, BLACK:WHITE} 
        try:
            return opponent[color]    
        except:
            raise ValueError("Wrong color provided for opponent function")
            
    @staticmethod
    def color_to_int(c):
        """convert character representing player color to the appropriate number"""
        color_to_int = {"b": BLACK , "w": WHITE, "e":EMPTY, "BORDER":BORDER, "FLOODFILL":FLOODFILL}
        try:
           return color_to_int[c] 
        except:
            raise ValueError("wrong color")
    
    @staticmethod
    def int_to_color(i):
        """convert number representing player color to the appropriate character """
        int_to_color = {BLACK:"b", WHITE:"w", EMPTY:"e", BORDER:"BORDER", FLOODFILL:"FLOODFILL"}
        try:
           return int_to_color[i] 
        except:
            raise ValueError("Provided integer value for color is invalid")
         
    @staticmethod
    def copyb2b(board, copy_board):
        """Return an independent copy of this Board."""
        copy_board.board = np.copy(board.board)
        copy_board.suicide = board.suicide  # checking for suicide move
        copy_board.winner = board.winner 
        copy_board.NS = board.NS
        copy_board.WE = board.WE
        copy_board._is_empty = board._is_empty
        copy_board.passes_black = board.passes_black
        copy_board.passes_white = board.passes_white
        copy_board.current_player = board.current_player
        copy_board.ko_constraint =  board.ko_constraint 
        copy_board.white_captures = board.white_captures
        copy_board.black_captures = board.black_captures 

        
    @staticmethod
    def point_to_coord(point, ns):
        """
        Transform one dimensional point presentation to two dimensional.

        Arguments
        ---------
        point

        Returns
        -------
        x , y : int
                coordinates of the point  1 <= x, y <= size
        """
        if point is None:
            return 'pass'
        row, col = divmod(point, ns)
        return row,col

