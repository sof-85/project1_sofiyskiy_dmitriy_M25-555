#!/usr/bin/env python3
from labyrinth_game.player_actions import get_input, move_player, show_inventory, take_item, use_item
from labyrinth_game.utils import attempt_open_treasure, describe_current_room, show_help, solve_puzzle

#global game_over
#game_over = False

#Переменная состояния игрока
game_state = {
        'player_inventory': [],         # Инвентарь игрока
        'current_room': 'entrance',     # Текущая комната
        'game_over': False,             # Значения окончания игры
        'steps_taken': 0                # Количество шагов
}
  
def process_command(game_state, command):
    '''Функция обработки команд'''
    global game_over
    command_seq = command.split()
    
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
                game_state['game_over'] = True
            case 'exit':
                game_state['game_over'] = True
            case 'solve':
                if (game_state['current_room'] == 'treasure_room'):
                    attempt_open_treasure(game_state)
                    
                else:
                    solve_puzzle(game_state)
            case _:
                if (check_direction(action) is True):
                    move_player(game_state, action)
                else:
                    print("Неправильная команда")
                    show_help()
    else:
        print("Неправильная команда")
        show_help()
        return  

def main():
    '''    Точка входа в игру    '''
    print('Добро пожаловать в Лабиринт сокровищ!')
    describe_current_room(game_state)
    while(not game_state['game_over']):
        command = get_input()
        process_command(game_state, command)
        
 
def check_direction(command):
    '''Функция проверки ввода направления'''
    if command in ['north', 'south', 'east', 'west']:
        return True
    else:
        return False
     
     
     

if __name__=='__main__':
    
    main()
 