# import multitasking # <== Remove this if not using multitasking
# import signal
# import threading
# import sys
import time

# kill all tasks on ctrl-c
# signal.signal(signal.SIGINT, multitasking.killall)
# multitasking.set_max_threads(10)

def createBoard(rows):
    return [True for i in range(int((rows*(rows+1))/2))]


def calcValidMoves(rows):
    levels = []
    counter = 0
    moves = []

    for i in range(1, rows+1):
        if i == 0: continue
        level = []
        for j in range(i):
            level.append(counter)
            counter += 1
        levels.append(level)

    for l in range(rows):
        for p in range(l+1):
            #down-left
            if l < rows-2: moves.append( ( levels[l][p], levels[l+1][p], levels[l+2][p] ) )
            
            #down-right
            if l < rows-2: moves.append( ( levels[l][p], levels[l+1][p+1], levels[l+2][p+2] ) )
            
            #right
            if p < l-1: moves.append( ( levels[l][p], levels[l][p+1], levels[l][p+2] ) )
    
    reverse_moves = []
    for m in moves:
        reverse_moves.append(m[::-1])
    moves += reverse_moves
    return moves


def getMoves(board):
    moves = []

    for start in range(len(board)):
        if board[start] == False:
            continue

        for m in valid_moves:
            if m[0] == start and board[m[1]] == True and board[m[2]] == False:
                moves.append(m)

    return moves

def trim_min_chain(min_chain):
    if len(min_chain) > 0:
        if min_chain[-1].count('-') == 1:
            min_chain.pop()
        else:
            min_chain[-1] = min_chain[-1][:min_chain[-1].rindex('-')]
    return trim_min_chain

def shrink_chain(move, output=[]):
    if (len(output) == 1):
        current = ""
        last_end = -1
    else:
        current = output[-1]
        last_end = int(current[-1].split('-')[-1])

    if current != "" and move[0] == last_end:
        current += "-" + str(move[2]+1)
        output[-1] = current
    else:
        current = str(move[0]+1) + "-" + str(move[2]+1)
        output.append(current)
    
    return output

min_length = 999999999
min_chains = []

def update_min_chains(chain):
    global min_chains, min_length
    if len(chain) < min_length:
        min_chains.clear()
        min_chains.append(chain)
        min_length = len(chain)

    elif len(chain) == min_length:
        min_chains.append(chain)

solved = 0
deadend = 0
def testBoard(test_board, move, chain=[], min_chain=[]):
    global solved, deadend, min_length
    chain.append(move)
    min_chain = shrink_chain(move, min_chain)
    
    if len(min_chain) > min_length:
        deadend += 1
        min_chain = trim_min_chain(min_chain)
        return

    test_board[move[0]] = False
    test_board[move[1]] = False
    test_board[move[2]] = True

    if test_board.count(True) == 1: 
        solved  += 1
        solved_chains.append(chain.copy())
        update_min_chains(min_chain.copy())
    else:
        moves = getMoves(test_board)
        if len(moves) > 0: 
            for m in moves: testBoard(test_board, m, chain, min_chain)
        else:
            deadend += 1

    test_board[move[0]] = True
    test_board[move[1]] = True
    test_board[move[2]] = False
    chain.pop()
    min_chain = trim_min_chain(min_chain)

finished = 0
# @multitasking.task # <== Remove this if not using multitasking
def startTestBoard(board, start):
    global finished
    board[start] = False
    moves = getMoves(board)

    if len(moves) > 0: 
        for m in moves: testBoard(board.copy(), m, min_chain=[start+1])

    finished += 1

start = time.perf_counter()
   
# Number of rows in our board
number_of_rows = 4

# Create the the initial board list
start_board = createBoard(number_of_rows)
positions = len(start_board)

# Moves are tuples representing (start, hop, end) positions
valid_moves = calcValidMoves(number_of_rows)

print(valid_moves)

solved_chains = []

#-------------------------- Multitasking version
# for i in range(len(start_board)):
#     print("Testing: ", i+1)
#     startTestBoard(start_board.copy(),i)

# while threading.active_count() > 1:
#     time.sleep(0.1)
#     sys.stdout.write("\rTotal checks: %i   " % (deadend + solved) + "  Threads: %i " % threading.active_count())
#     sys.stdout.flush()
#-------------------------- End multitasking version

#-------------------------- Non-multitasking
for i in range(len(start_board)):
    print("Testing: ", i+1)
    startTestBoard(start_board.copy(),i)
#-------------------------- End non-multitasking version


print("")
for chain in min_chains:
    print(f"Starting blank: {chain[0]}, Steps: {len(chain[1:])}, Moves:", chain[1:])

stop = time.perf_counter()

print(f"Completed in {stop - start:0.4f} seconds")
print("Solutions: ", solved)
print("Deadends: ", deadend)
print("Total: ", deadend+ solved)
print("Matching min: ", len(min_chains))