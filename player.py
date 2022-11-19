from board import Direction, Rotation, Action
from random import Random
import time


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
        time.sleep(0.2)
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
    
    def score_board(self, board):
        score = 2000000
        bumpiness = 0
        holes = 0
        height = 0
        horizontal_dislocations = 0

        max_height = 25
        heights = []
        for i in range(10):
            j = 25
            for cell in board.cells:
                if cell[0] == i:
                    if cell[1] == 23:
                        continue
                    if cell[1]<j:
                        j = cell[1]
            if j!=25:    
                heights.append(j)
            else:
                heights.append(24)
            if (j!= 25) and ((i, j+1) not in board.cells):
                holes += 1
        for k in range(23, j+1, -1):
            for i in range(9):
                if (((i, k) in board.cells) and ((i +1, k) not in board.cells)) or (((i, k) not in board.cells) and ((i +1, k) in board.cells)):
                    horizontal_dislocations += 1
        for cell in board.cells:
            if cell[1]<max_height:
                max_height=cell[1]
        height = 23 - max_height
        for i in range(9):    
            bumpiness += (abs(heights[i] - heights[i+1]))
        score = score - ((holes*5) + (height*10) + (bumpiness*0) + (horizontal_dislocations)*0)
        print(holes)
        print(score)
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
                    return le_moves
                l_block_start_pos -=1
                if l_block_start_pos == target_pos[0]:
                    break
        elif l_block_start_pos < target_pos[0]:
            while True:
                le_moves.append(Direction.Right)
                if board.move(Direction.Right):
                    return le_moves
                r_block_start_pos+=1
                l_block_start_pos+=1
                if (l_block_start_pos == target_pos[0]) or (r_block_start_pos == 9):
                    break
        if target_rot != 1:
            for i in range(target_rot-1):
                le_moves.append(Rotation.Clockwise)
                if board.rotate(Rotation.Clockwise):
                    return le_moves

        le_moves.append(Direction.Drop)
        board.move(Direction.Drop) 
        print(board.cells)
        return le_moves

    def move_to_target_rot(self, target_rot, target_pos, board):
        le_moves = []
        if target_rot != 1:
            for i in range(target_rot-1):
                le_moves.append(Rotation.Clockwise)
                if board.rotate(Rotation.Clockwise):
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
                    return le_moves
                l_block_start_pos -=1
                if l_block_start_pos == target_pos[0]:
                    break
        elif l_block_start_pos < target_pos[0]:
            while True:
                le_moves.append(Direction.Right)
                if board.move(Direction.Right):
                    return le_moves
                r_block_start_pos+=1
                l_block_start_pos+=1
                if (l_block_start_pos == target_pos[0]) or (r_block_start_pos == 9):
                    break
        
        le_moves.append(Direction.Drop)
        board.move(Direction.Drop) 
        print(board.cells)
        return le_moves

    def choose_action(self, board):
        self.print_board(board)
        time.sleep(0.02)
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
                    actions_to_take = temp_actions
                temp_actions = self.move_to_target_rot(rot, pos, sandbox2)
                if self.score_board(sandbox2) > highest_score:
                    highest_score = self.score_board(sandbox2)
                    actions_to_take = temp_actions
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

    def score_board(self, board):
        score = 5000
        bumpiness = 0
        holes = 0
        height = 0
        horizontal_dislocations = 0

        max_height = 25
        heights = []
        for i in range(10):
            j = 24
            for cell in board.cells:
                if cell[0] == i:
                    if cell[1]<j:
                        j = cell[1]   
            heights.append(j)
        
        holes = self.count_holes(board)

        # for k in range(23, j+1, -1):
        #     for i in range(9):
        #         if (((i, k) in board.cells) and ((i +1, k) not in board.cells)) or (((i, k) not in board.cells) and ((i +1, k) in board.cells)):
        #             horizontal_dislocations += 1
        for cell in board.cells:
            if cell[1]<max_height:
                max_height=cell[1]
        height = 23 - max_height
        for i in range(9):    
            bumpiness += (abs(heights[i] - heights[i+1]))
        if max_height<17:
            score = score - ((holes*100) + (height*1) + (bumpiness*30) + (horizontal_dislocations*0))
        else:
            score = score - ((holes*100) + (height*1) + (bumpiness*4) + (horizontal_dislocations*0))
        print("Height:",height)
        print("Bumpiness:",bumpiness)
        print("Holes:",holes)
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
        self.print_board(board)
        time.sleep(0.002)
        prev_holes = 0
        curr_holes = 0
        discards = 0
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
        # prev_holes = curr_holes
        # curr_holes = self.count_holes(sandbox3)
        # if ((prev_holes - curr_holes) < 0) and (discards<11):
        #     actions_to_take = [Action.Discard]
        #     discards+=1
        return actions_to_take

SelectedPlayer = MyPlayer2
