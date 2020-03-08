#!/usr/bin/env python
#coding:utf-8

"""
Each sudoku board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8
"""

ROW = "ABCDEFGHI"
COL = "123456789"
constraints = []


def print_board(board):
    """Helper function to print board in a square."""
    print("-----------------")
    for i in ROW:
        row = ''
        for j in COL:
            row += (str(board[i + j]) + " ")
        print(row)


def board_to_string(board):
    """Helper function to convert board dictionary to string for writing."""
    ordered_vals = []
    for r in ROW:
        for c in COL:
            ordered_vals.append(str(board[r + c]))
    return ''.join(ordered_vals)



def get_possible_values(key,board):

    all_possible_values = {1,2,3,4,5,6,7,8,9}
    not_possible_values = set()

    for domain in constraints:
        if key in domain:
            for i in domain:
                if board[i]!=0:
                    not_possible_values.add(board[i])

    return all_possible_values.difference(not_possible_values)

def print_possible_values(board_possible_vals):
    for x,y in board_possible_vals.items():
        print(x,y)

def generate_possible_values_dict(board):

    board_possible_vals = dict()

    for key in board.keys():
        if board[key]==0:
            vals = get_possible_values(key,board)
            #if len(vals)!=0:
            board_possible_vals[key] = vals

    return board_possible_vals






def select_unassigned_variable(board_possible_vals):
    selected_variable = None
    selected_values = None
    for key in board_possible_vals.keys():
        if selected_variable == None or len(board_possible_vals[key]) < len(selected_values):
            selected_variable = key
            selected_values = board_possible_vals[key]
    return selected_variable, list(selected_values)


def verify_spot(updated_key,updated_value,board):
    #loop through all constrains
    for constraint in constraints:
        if updated_key in constraint:
            for key in constraint:
                if updated_value == board[key]:
                    return false
    return True









def backtracking(board):
    """Takes a board and returns solved board."""

    # generate the constraints for the board
    if(len(constraints)==0): generate_constraints(board)

    #get the structure to tell what possible values we can assign to the board
    board_possible_vals = generate_possible_values_dict(board)



    goal_test(board)

    x, solved_board = backtracking_helper(None,board)

    #old code, remove
    if x==False:
        print('failed')
    return solved_board

def backtracking_helper(possible_values,board):
    #if the goal test is passed, return the board
    #print(goal_test(cps))

    #for now im going to regenerate possible values instad of passing it in
    board_possible_vals = generate_possible_values_dict(board)
    # print_board(board)

    # for x,y in board_possible_vals.items():
    #     print(x,y)

    #goal check
    if not board_possible_vals:
        return True, board


    #grab a variable with the least number of possiblities

    chosen_key, possible_values = select_unassigned_variable(board_possible_vals)
    # print(chosen_key)
    # print(possible_values)
    # print(len(possible_values))
    if len(possible_values)==0:
        return False, board

    for value in possible_values:
        if verify_spot(chosen_key,value,board):
            board[chosen_key] = value
            x, sol = backtracking_helper(None,board)
            if x == True:
                return True, sol
            board[chosen_key] = 0
    return False, board





    return
    #variable = select the most optimistic based on the 3 heristic operations


def generate_constraints(board):
    #create constraints based on ROWS
    for letter in ROW:
        sub_constraint = []
        for val in board.keys():
            if letter in val:
                sub_constraint.append(val)
        constraints.append(sub_constraint)

    #create constraints based on COL
    for number in COL:
        sub_constraint = []
        for val in board.keys():
            if number in val:
                sub_constraint.append(val)
        constraints.append(sub_constraint)

    #hard codeing these for now bc i cant get the loops, square units
    constraints.append(['A1','A2','A3','B1','B2','B3','C1','C2','C3'])
    constraints.append(['D1','D2','D3','E1','E2','E3','F1','F2','F3'])
    constraints.append(['G1','G2','G3','H1','H2','H3','I1','I2','I3'])
    constraints.append(['A4','A5','A6','B4','B5','B6','C4','C5','C6'])
    constraints.append(['D4','D5','D6','E4','E5','E6','F4','F5','F6'])
    constraints.append(['G4','G5','G6','H4','H5','H6','I4','I5','I6'])
    constraints.append(['A7','A8','A9','B7','B8','B9','C7','C8','C9'])
    constraints.append(['D7','D8','D9','E7','E8','E9','F7','F8','F9'])
    constraints.append(['G7','G8','G9','H7','H8','H9','I7','I8','I9'])

    #create constraints based on square
    # for d in range(3):
    #     sub_constraint = []
    #     for step in range(3):
    #         for i in range(3):
    #             index = i + ( 3* d)
    #             stepI = step + (3 * d)
    #             sub_constraint.append(f'{ROW[step]}{COL[index]}')


    # for x in constraints:
    #     print(x)

    # print(len(constraints))

def goal_test(board):
    for constraint in constraints:
        as_a_set = set()

        for key in constraint:
            #print(as_a_set)
            if board[key] in as_a_set:
                return False
            else:
                as_a_set.add(board[key])
    return True










if __name__ == '__main__':
    #  Read boards from source.
    src_filename = 'sudokus_start.txt'
    try:
        srcfile = open(src_filename, "r")
        sudoku_list = srcfile.read()
    except:
        print("Error reading the sudoku file %s" % src_filename)
        exit()

    # Setup output file
    out_filename = 'output.txt'
    outfile = open(out_filename, "w")

    # Solve each board using backtracking
    for line in sudoku_list.split("\n"):

        if len(line) < 9:
            continue

        # Parse boards to dict representation, scanning board L to R, Up to Down
        board = { ROW[r] + COL[c]: int(line[9*r+c])
                  for r in range(9) for c in range(9)}


        # Print starting board. TODO: Comment this out when timing runs.
        #print_board(board)

        # Solve with backtracking
        solved_board = backtracking(board)

        # Print solved board. TODO: Comment this out when timing runs.
        #print_board(solved_board)

        # Write board to file
        outfile.write(board_to_string(solved_board))
        outfile.write('\n')

    print("Finishing all boards in file.")