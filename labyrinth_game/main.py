#!/usr/bin/env python3

#from constants import ROOMS
from player_actions import get_input, move_player, show_inventory, take_item, use_item
from utils import attempt_open_treasure, describe_current_room, show_help, solve_puzzle

game_over = False

#Переменная состояния игрока
game_state = {
        'player_inventory': [], # Инвентарь игрока
        'current_room': 'entrance', # Текущая комната
        'game_over': False, # Значения окончания игры
        'steps_taken': 0 # Количество шагов
}
  
def process_command(game_state, command):
    global game_over
    print(command)
    command_seq = command.split()
    #print(len(command_seq))

    if (len(command_seq) == 2):
        action = command_seq[0]
        subject = command_seq[1]
        match action:
            case 'use':
                use_item(game_state, subject)
            case 'go':
                move_player(game_state, subject)
            case 'take':
                take_item(game_state, subject)
            case _:
                show_help()    
    elif(len(command_seq) == 1):
        action = command_seq[0]
        match action:
            case 'look':
                describe_current_room(game_state)
            case 'inventory':
                show_inventory(game_state)
            case 'quit':
                game_over = True
            case 'exit':
                game_over = True
            case 'solve':
                if (game_state['current_room'] == 'treasure_room'):
                    attempt_open_treasure(game_state)
                else:
                    solve_puzzle(game_state)
            case _:
                show_help()
    else:
        show_help()
        return  

def main():
    '''    Точка входа в игру    '''
    print('Добро пожаловать в Лабиринт сокровищ!')
    #from player_actions import  get_input
    #from utils import describe_current_room
    describe_current_room(game_state)
    while(not game_over):
        command = get_input()
        #game_state['steps_taken'] = +1
        process_command(game_state, command)
  

if __name__=='__main__':
    
    main()
 