import os
import random

def choose_first():
    return random.randint(0,1)

def choose_side():
    choice = input("Player 1: Do you want to be 'X' or 'O'? ")
    
    while(choice.lower() != 'x' and choice.lower() != 'o'):
        choice = input("Please, select a valid option ('X' or 'O'): ")

    if(choice.lower() == 'x'):
        return ('X','O')
    else:
        return ('O','X')

def print_board(board):
    # clear the screen
    os.system('clear')

    # print the board
    print(' --- --- ---            --- --- --- ')
    print('| {} | {} | {} |          | {} | {} | {} |'.format(7, 8, 9, board[7], board[8], board[9]))
    print(' --- --- ---            --- --- --- ')
    print('| {} | {} | {} |    --    | {} | {} | {} |'.format(4, 5, 6, board[4], board[5], board[6]))
    print(' --- --- ---            --- --- --- ')
    print('| {} | {} | {} |          | {} | {} | {} |'.format(1, 2, 3, board[1], board[2], board[3]))
    print(' --- --- ---            --- --- --- ')
    
def player_input(board, turn, players):
    position = -1
    symbol = ''

    if(turn % 2 == 0):           
        print('Player 1\'s turn.')
        symbol = players[0]
    else:                        
        print('Player 2\'s turn.')
        symbol = players[1]
        
    while(0 > position or position > 9 or board[position] != ' '):
        position_str = input('Choose your next move (1-9) or press 0 to exit: ')
        try:
            position = int(position_str)
        except ValueError:
            print('Please, choose a number from 1 to 9 or press 0 to exit: ')

    # add the symbol for current player to the board
    board[position] = symbol
    return board

def check_line(players, pos1, pos2, pos3):
    # at the begining the board list is full of spaces and we don't want to check them
    if (pos1 != ' ' and pos1 == pos2 and pos2  == pos3):
        # get the position in players of the 'X' or 'O' that is in the positions
        # return index + 1 (player[0] is player 1 and player[1] is player 2)
        return players.index(pos1) + 1
    else:
        return 0

def check_game_status(board, players):
    status = 0

    if(board[0] != ' '):
        return -1

    possible_lines = []
    # check rows
    possible_lines.append(tuple(board[1:4]))
    possible_lines.append(tuple(board[4:7]))
    possible_lines.append(tuple(board[7:10]))
    # check columns
    possible_lines.append(tuple(board[1:10:3]))
    possible_lines.append(tuple(board[2:10:3]))
    possible_lines.append(tuple(board[3:10:3]))
    # check diagonals
    possible_lines.append(tuple([board[1], board[5], board[9]]))
    possible_lines.append(tuple([board[3], board[5], board[7]]))
    
    for pos1,pos2,pos3 in possible_lines:
        status = check_line(players, pos1, pos2, pos3)
        if (status != 0):
            break

    return status

def play_again():
    print('Do you want to play again?')
    return yes_or_no()

def check_ready(turn):
    print('Player {} moves first.'.format(turn + 1))
    print('Are you ready?')
    return yes_or_no()

def yes_or_no():
    response = input('Enter yes or no: ')
    response = response.lower()
    
    while(response != 'yes' and response != 'no' and response != 'y' and response != 'n'):
        response = input('Please, enter yes(\'y\') or no(\'n\'): ')
        response = response.lower()
        
    return response == 'yes' or response == 'y'

def board_full(board):
    for x in board[1:]:
        if (x == ' '):
            return False
        else:
            continue
    else:
        return True

def game_loop():
    play = True
    while(play):
        players = choose_side()
        board = [' '] * 10
        turn = choose_first()

        # if the player is ready this won't do anything
        # else this will ask if he/she wants to keep playing
        if(not check_ready(turn)):
            if(play_again()):
                continue
            else:
                break

        # the game can start
        game_status = 0
        while(game_status == 0 and not board_full(board)):
            print_board(board)
            board = player_input(board, turn, players)
            game_status = check_game_status(board, players)
            turn += 1

            # check if the user wants to exit
            if(game_status < 0):
                break
        else:
            # print result of the game
            # only gets executed if we don't break out of the loop
            print_board(board)
            if (game_status == 0):
                print('Draw!')
            else:
                print('Player {} wins the game. Congratulations!'.format(game_status))
            
        play = play_again()

    print('Until the next time!')

##############################
### Start of python script ###
##############################

print('Welcome to TicTacToe!\n')
game_loop()
