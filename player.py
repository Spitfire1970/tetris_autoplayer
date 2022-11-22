from board import Direction, Rotation, Action
from random import Random
import time
discards = 0
li = []
block_num = 0

class Player:
    def choose_action(self, board):
        raise NotImplementedError


class RandomPlayer(Player):
    def __init__(self, seed=None):
        self.random = Random(seed)

    def print_board(self, board):
        print("--------")
        for y in range(24):
            s = ""
            for x in range(10):
                if (x,y) in board.cells:
                    s += "#"
                else:
                    s += "."
            print(s, y)
            
    def choose_action(self, board):
        self.print_board(board)
        #time.sleep(0.2)
        if self.random.random() > 0.97:
            # 3% chance we'll discard or drop a bomb
            return self.random.choice([
                Action.Discard,
                Action.Bomb,
            ])
        else:
            # 97% chance we'll make a normal move
            return self.random.choice([
                Direction.Left,
                Direction.Right,
                Direction.Down,
                Rotation.Anticlockwise,
                Rotation.Clockwise,
            ])

class MyPlayer(Player):
    def __init__(self, seed=None):
        self.random = Random(seed)

    def print_board(self, board):
        print("--------")
        for y in range(24):
            s = ""
            for x in range(10):
                if (x,y) in board.cells:
                    s += "#"
                else:
                    s += "."
            print(s, y)
    
    def count_holes(self, board):
        holes = 0
        heights = []
        for i in range(10):
            j = 24
            for cell in board.cells:
                if cell[0] == i:
                    if cell[1]<j:
                        j = cell[1]   
            heights.append(j)
        n = 0
        for i in heights:
            j = 24
            temp = 0
            while (j != i):
                if ((n, j - 1) in board.cells) and ((n, j) not in board.cells) and (j!=24):
                    holes += (temp - j)
                elif (((n, j) in board.cells) or (j==24)):
                    temp = j
                j -=1
            n +=1
        return holes

    def heights(self, board):
        heights = []
        for i in range(10):
            j = 24
            for cell in board.cells:
                if cell[0] == i:
                    if cell[1]<j:
                        j = cell[1]   
            heights.append(j)
        return heights

    def max_height(self, board):
        max_height = 25
        for cell in board.cells:
            if cell[1]<max_height:
                max_height=cell[1]
        return (23 - max_height)

    def bumpiness(self, board):
        heights = self.heights(board)
        bumpiness = 0
        for i in range(9):    
            bumpiness += (abs(heights[i] - heights[i+1]))
        return bumpiness

    def cells_in_right_most_lane(self, board):
        num = 0
        for cell in board.cells:
            if (cell[0] == 9):
                num += 1
        return num

    def score_board(self, board):
        score = 5000
        bumpiness = self.bumpiness(board)
        holes = self.count_holes(board)
        max_height = self.max_height(board)
        cells_in_right_lane = self.cells_in_right_most_lane(board)

        if max_height>7:
            score = score - ((holes*80) + (max_height*10) + (bumpiness*30) + (cells_in_right_lane*0))
        else:
            score = score - ((holes*100) + (max_height*1) + (bumpiness*2) + (cells_in_right_lane*0))
        print("Height:",max_height)
        print("Bumpiness:",bumpiness)
        print("Holes:",holes)
        print("Cells in right lane:", cells_in_right_lane)
        print("Score:",score,"\n")
        return score
    
    def move_to_target_pos(self, target_pos, target_rot, board):
        le_moves = []
        l_block_start_pos = 10
        for cell in board.falling.cells:
            if cell[0] < l_block_start_pos:
                l_block_start_pos = cell[0]
        r_block_start_pos = -1
        for cell in board.falling.cells:
            if cell[0] > r_block_start_pos:
                r_block_start_pos = cell[0]
        if l_block_start_pos > target_pos[0]:
            while True:
                le_moves.append(Direction.Left)
                if board.move(Direction.Left):
                    # print(board.cells)
                    return le_moves
                l_block_start_pos -=1
                if l_block_start_pos == target_pos[0]:
                    break
        elif l_block_start_pos < target_pos[0]:
            while True:
                le_moves.append(Direction.Right)
                if board.move(Direction.Right):
                    # print(board.cells)
                    return le_moves
                r_block_start_pos+=1
                l_block_start_pos+=1
                if (l_block_start_pos == target_pos[0]) or (r_block_start_pos == 9):
                    break
        if target_rot != 1:
            for i in range(target_rot-1):
                le_moves.append(Rotation.Clockwise)
                if board.rotate(Rotation.Clockwise):
                    # print(board.cells)
                    return le_moves

        le_moves.append(Direction.Drop)
        board.move(Direction.Drop) 
        # print(board.cells)
        return le_moves

    def move_to_target_rot(self, target_rot, target_pos, board):
        le_moves = []
        if target_rot != 1:
            for i in range(target_rot-1):
                le_moves.append(Rotation.Clockwise)
                if board.rotate(Rotation.Clockwise):
                    # print(board.cells)
                    return le_moves
        l_block_start_pos = 10
        for cell in board.falling.cells:
            if cell[0] < l_block_start_pos:
                l_block_start_pos = cell[0]
        r_block_start_pos = -1
        for cell in board.falling.cells:
            if cell[0] > r_block_start_pos:
                r_block_start_pos = cell[0]
        if l_block_start_pos > target_pos[0]:
            while True:
                le_moves.append(Direction.Left)
                if board.move(Direction.Left):
                    # print(board.cells)
                    return le_moves
                l_block_start_pos -=1
                if l_block_start_pos == target_pos[0]:
                    break
        elif l_block_start_pos < target_pos[0]:
            while True:
                le_moves.append(Direction.Right)
                if board.move(Direction.Right):
                    # print(board.cells)
                    return le_moves
                r_block_start_pos+=1
                l_block_start_pos+=1
                if (l_block_start_pos == target_pos[0]) or (r_block_start_pos == 9):
                    break
        
        le_moves.append(Direction.Drop)
        board.move(Direction.Drop) 
        # print(board.cells)
        return le_moves

    def choose_action(self, board):
        global discards
        self.print_board(board)
        #time.sleep(0.002)
        prev_holes = 0
        curr_holes = 0
        sandbox3 = board.clone()
        target_positions = []
        target_rotations = [1 ,2, 3, 4]
        actions_to_take = []
        temp_actions = []
        highest_score = 0
        for i in range(10):
            j = 0
            for cell in board.cells:
                if cell[0] == i:
                    if cell[1]>j:
                        j = cell[1]
            target_positions.append((i, j-1))
        for pos in target_positions:
            for rot in target_rotations:
                sandbox1 = board.clone()
                sandbox2 = board.clone()
                temp_actions = self.move_to_target_pos(pos, rot, sandbox1)
                if self.score_board(sandbox1) > highest_score:
                    highest_score = self.score_board(sandbox1)
                    sandbox3 = sandbox1.clone()
                    actions_to_take = temp_actions
                temp_actions = self.move_to_target_rot(rot, pos, sandbox2)
                if self.score_board(sandbox2) > highest_score:
                    highest_score = self.score_board(sandbox2)
                    sandbox3 = sandbox2.clone()
                    actions_to_take = temp_actions
        if (discards < 10):    
            prev_holes = curr_holes
            curr_holes = self.count_holes(sandbox3)
            if (((prev_holes - curr_holes) < 0) and (self.max_height(sandbox3)>16)):
                discards+=1
                actions_to_take = [Action.Discard]
        return actions_to_take

class MyPlayer2(Player):
    def __init__(self, seed=None):
        self.random = Random(seed)

    def print_board(self, board):
        print("--------")
        for y in range(24):
            s = ""
            for x in range(10):
                if (x,y) in board.cells:
                    s += "#"
                else:
                    s += "."
            print(s, y)
    
    def heights(self, board):
            heights = []
            for i in range(10):
                j = 24
                for cell in board.cells:
                    if cell[0] == i:
                        if cell[1]<j:
                            j = cell[1]   
                heights.append(j)
            return heights

    def count_holes(self, board):
        holes = 0
        # heights = self.heights(board)
        # n = 0
        # for i in heights:
        #     j = 24
        #     temp = 0
        #     while (j != i):
        #         if ((n, j - 1) in board.cells) and ((n, j) not in board.cells) and (j!=24):
        #             holes += (temp - j)
        #         elif (((n, j) in board.cells) or (j==24)):
        #             temp = j
        #         j -=1
        #     n +=1
        for i in range(10):
            for j in range(24):
                if (i, j) not in board.cells:
                    for s in range(0, j):
                        if (i, s) in board.cells:
                            holes += 1
                            break
        return holes

    def count_intell_holes(self, board):
        holes = 0
        intell_holes = []
        for i in range(10):
            for j in range(24):
                if (i, j) not in board.cells:
                    for s in range(0, j):
                        if (i, s) in board.cells:
                            intell_holes.append((i, j))
                            break
        for i in range(10):
            for j in range(24):
                n = 0.5
                if (i, j) in intell_holes:
                    for r in range(j +1, 24):
                        if (i ,r) in intell_holes:
                            n += 0.5
                    holes += n
        return holes

    def max_height(self, board):
        max_height = 25
        for cell in board.cells:
            if cell[1]<max_height:
                max_height=cell[1]
        max_height = 24 - max_height
        return (max_height)

    def bumpiness(self, board):
        heights = self.heights(board)
        bumpiness = 0
        for i in range(9):    
            bumpiness += (abs(heights[i] - heights[i+1]))
        return bumpiness

    def num_pillars(self, board):
        pillars = 0
        for i in range(1, 9):
            for j in range(24):
                if ((((i ,j) not in board.cells) and ((i, j-1) not in board.cells) and ((i, j-2) not in board.cells)) and ((((i-1, j) in board.cells) and ((i-1, j-1) in board.cells) and ((i-1, j-2) in board.cells)) and (((i+1, j) in board.cells) and ((i+1, j-1) in board.cells) and ((i+1, j-2) in board.cells)))):
                    pillars+=1
                    break
        for j in range(24):
            if ((((0 ,j) not in board.cells) and ((0, j-1) not in board.cells) and ((0, j-2) not in board.cells)) and (((1, j) in board.cells) and ((1, j-1) in board.cells) and ((1, j-2) in board.cells))):
                    pillars+=1
                    break
        for j in range(24):
            if ((((9 ,j) not in board.cells) and ((9, j-1) not in board.cells) and ((9, j-2) not in board.cells)) and (((8, j) in board.cells) and ((8, j-1) in board.cells) and ((8, j-2) in board.cells))):
                    pillars+=1
                    break
        if pillars == 1:
            pillars = 0
        elif pillars == 0:
            pillars = 0
        else:
            pillars -=1
        return pillars

    def blockades(self, board):
        return

    def score_board(self, board, prev_num_cell):
        score = 5000
        bumpiness = self.bumpiness(board)
        holes = self.count_holes(board)
        max_height = self.max_height(board)
        rows_cleared = (prev_num_cell - len(board.cells) + 4)/10
        pillars = self.num_pillars(board)

        cells_left = 240 - len(board.cells)

        if max_height>13 and cells_left < 105:
            score = score - ((holes*115) + (max_height*30) + (bumpiness*75) + ((rows_cleared))*0 + (pillars)*25)
        # if max_height>5 and cells_left < 180:
        #     score = score - ((holes*120) + (max_height*15) + (bumpiness*25)+ ((rows_cleared-4))*10 + (pillars)*0)
        elif max_height>8 and cells_left < 160:
            score = score - ((holes*142) + (max_height*10) + (bumpiness*45) + ((rows_cleared))*45 + (pillars)*110)
        else:
            score = score - ((holes*170) + (max_height*1) + (bumpiness*2) + ((rows_cleared))*80 + (pillars)*70)
        if rows_cleared == 4 or rows_cleared == 4.0:
            score =10000
        # print("Height:",max_height)
        # print("Bumpiness:",bumpiness)
        # print("Holes:",holes)
        # print("Rows Cleared:",rows_cleared)
        # print("Pillars:",pillars)
        # print("Score:",score,"\n")
        return score
    
    def move_to_target_pos(self, target_pos, target_rot, board):
        # global li
        # li.append(board.falling.shape)
        # print(li)
        # print(board.falling.shape)
        le_moves = []
        if board.falling.shape == "I":
            for i in range(9, -1, -1):
                for j in range(21):
                    if (((i ,j) not in board.cells) and ((i, j-1) not in board.cells) and ((i, j-2) not in board.cells) and ((i, j-3) not in board.cells) and ((((i-1, j) in board.cells) and ((i-1, j-1) in board.cells) and ((i-1, j-2) in board.cells) and ((i-1, j-3) in board.cells)) or (((i+1, j) in board.cells) and ((i+1, j-1) in board.cells) and ((i+1, j-2) in board.cells) and ((i+1, j-3) in board.cells)))):
                        for cell in board.falling.cells:
                            k = cell[0]
                            if k == i:
                                while True:
                                    le_moves.append(Direction.Down)
                                    if board.move(Direction.Down):
                                        return le_moves
                            if k<i:
                                while True:
                                    le_moves.append(Direction.Right)
                                    if board.move(Direction.Right):
                                        return le_moves
                                    k += 1
                                    if k == i:
                                        break
                            if k > i:
                                while True:
                                    le_moves.append(Direction.Left)
                                    if board.move(Direction.Left):
                                        return le_moves
                                    k -= 1
                                    if k == i:
                                        break
                                    
        l_block_start_pos = 10
        for cell in board.falling.cells:
            if cell[0] < l_block_start_pos:
                l_block_start_pos = cell[0]
        r_block_start_pos = -1
        for cell in board.falling.cells:
            if cell[0] > r_block_start_pos:
                r_block_start_pos = cell[0]
        if l_block_start_pos > target_pos[0]:
            while True:
                le_moves.append(Direction.Left)
                if board.move(Direction.Left):
                    # print(board.cells)
                    return le_moves
                l_block_start_pos -=1
                if l_block_start_pos == target_pos[0]:
                    break
        elif l_block_start_pos < target_pos[0]:
            while True:
                le_moves.append(Direction.Right)
                if board.move(Direction.Right):
                    # print(board.cells)
                    return le_moves
                r_block_start_pos+=1
                l_block_start_pos+=1
                if (l_block_start_pos == target_pos[0]) or (r_block_start_pos == 9):
                    break
        if target_rot != 1:
            for i in range(target_rot-1):
                le_moves.append(Rotation.Clockwise)
                if board.rotate(Rotation.Clockwise):
                    # print(board.cells)
                    return le_moves

        while True:
            le_moves.append(Direction.Down)
            if board.move(Direction.Down): 
            # print(board.cells)
                return le_moves

    def move_to_target_rot(self, target_rot, target_pos, board):
        # global li
        # li.append(board.falling.shape)
        # print(li)
        # print(board.falling.shape)
        le_moves = []
        if board.falling.shape == "I":
            for i in range(9, -1, -1):
                for j in range(21):
                    if (((i ,j) not in board.cells) and ((i, j-1) not in board.cells) and ((i, j-2) not in board.cells) and ((i, j-3) not in board.cells) and ((((i-1, j) in board.cells) and ((i-1, j-1) in board.cells) and ((i-1, j-2) in board.cells) and ((i-1, j-3) in board.cells)) or (((i+1, j) in board.cells) and ((i+1, j-1) in board.cells) and ((i+1, j-2) in board.cells) and ((i+1, j-3) in board.cells)))):
                        for cell in board.falling.cells:
                            k = cell[0]
                            if k == i:
                                while True:
                                    le_moves.append(Direction.Down)
                                    if board.move(Direction.Down):
                                        return le_moves
                            if k<i:
                                while True:
                                    le_moves.append(Direction.Right)
                                    if board.move(Direction.Right):
                                        return le_moves
                                    k += 1
                                    if k == i:
                                        break
                            if k > i:
                                while True:
                                    le_moves.append(Direction.Left)
                                    if board.move(Direction.Left):
                                        return le_moves
                                    k -= 1
                                    if k == i:
                                        break
        if target_rot != 1:
            for i in range(target_rot-1):
                le_moves.append(Rotation.Clockwise)
                if board.rotate(Rotation.Clockwise):
                    # print(board.cells)
                    return le_moves
        l_block_start_pos = 10
        for cell in board.falling.cells:
            if cell[0] < l_block_start_pos:
                l_block_start_pos = cell[0]
        r_block_start_pos = -1
        for cell in board.falling.cells:
            if cell[0] > r_block_start_pos:
                r_block_start_pos = cell[0]
        if l_block_start_pos > target_pos[0]:
            while True:
                le_moves.append(Direction.Left)
                if board.move(Direction.Left):
                    # print(board.cells)
                    return le_moves
                l_block_start_pos -=1
                if l_block_start_pos == target_pos[0]:
                    break
        elif l_block_start_pos < target_pos[0]:
            while True:
                le_moves.append(Direction.Right)
                if board.move(Direction.Right):
                    # print(board.cells)
                    return le_moves
                r_block_start_pos+=1
                l_block_start_pos+=1
                if (l_block_start_pos == target_pos[0]) or (r_block_start_pos == 9):
                    break
        
        while True:
            le_moves.append(Direction.Down)
            if board.move(Direction.Down): 
            # print(board.cells)
                return le_moves

    def choose_action(self, board):
        global block_num
        global discards
        block_num +=1
        fin_prev_num_cell = 0
        print("Block", block_num)
        #time.sleep(0.5)
        self.print_board(board)
        prev_holes = 0
        curr_holes = 0
        num_cells = 0
        sandbox3 = board.clone()
        target_positions = []
        target_rotations = [1 ,2, 3, 4]
        actions_to_take = []
        temp_actions = []
        highest_score = 0
        for i in range(10):
            j = 0
            for cell in board.cells:
                if cell[0] == i:
                    if cell[1]>j:
                        j = cell[1]
            target_positions.append((i, j-1))
        for pos in target_positions:
            for rot in target_rotations:
                sandbox1 = board.clone()
                sandbox2 = board.clone()
                num_cells = len(sandbox1.cells)
                temp_actions = self.move_to_target_pos(pos, rot, sandbox1)
                if self.score_board(sandbox1, num_cells) > highest_score:
                    highest_score = self.score_board(sandbox1, num_cells)
                    sandbox3 = sandbox1.clone()
                    fin_prev_num_cell = num_cells
                    actions_to_take = temp_actions
                num_cells = len(sandbox2.cells)
                temp_actions = self.move_to_target_rot(rot, pos, sandbox2)
                if self.score_board(sandbox2, num_cells) > highest_score:
                    highest_score = self.score_board(sandbox2, num_cells)
                    sandbox3 = sandbox2.clone()
                    fin_prev_num_cell = num_cells
                    actions_to_take = temp_actions
        bumpiness = self.bumpiness(sandbox3)
        holes = self.count_holes(sandbox3)
        max_height = self.max_height(sandbox3)
        rows_cleared = (fin_prev_num_cell - len(sandbox3.cells) + 4)/10
        pillars = self.num_pillars(sandbox3)
        print("Height:",max_height)
        print("Bumpiness:",bumpiness)
        print("Holes:",holes)
        print("Rows Cleared:",rows_cleared)
        print("Pillars:",pillars)
        if (discards < 10):    
            prev_holes = curr_holes
            curr_holes = self.count_holes(sandbox3)
            if ((prev_holes - curr_holes) < 0):
                discards+=1
                actions_to_take = [Action.Discard]
                block_num -=1
        return actions_to_take

SelectedPlayer = MyPlayer2
