from constants import ROOMS

#from utils import describe_current_room
#from main import *

def show_inventory(game_state):
    '''Функция отображения инвентаря'''
    inventory = game_state['player_inventory']
    if (inventory != []):
        print ('У вас есть:', inventory)
    else:
        print ('Инвентарь пуст!')
    pass

def get_input(prompt="> "):
    '''Функция обработки ввода пользователя'''       
    try:
        user_input = input(prompt)
        return user_input
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"
    
def move_player(game_state, direction):
    '''Функция перемещения'''
    from utils import describe_current_room, random_event
    room = game_state['current_room']
    room_exits = ROOMS[room]['exits']
    
    if (direction in room_exits):
        game_state['current_room'] = room_exits[direction]
        game_state['steps_taken'] += 1
        print ('число шагов', game_state['steps_taken'])
        #random_event(game_state)
        print(game_state['steps_taken'])
        describe_current_room(game_state)
        random_event(game_state)
               
    else:
        print('Нельзя пойти в этом направлении')
    
def take_item(game_state, item_name):
    '''Функция взятия предмета'''
    room = game_state['current_room']
    room_items = ROOMS[room]['items']
    if (item_name in room_items):
        game_state['player_inventory'].append(item_name)
        ROOMS[room]['items'].remove(item_name)
        print('Вы подняли ', item_name)
               
    else:
        print('Такого предмета здесь нет')
      

def use_item(game_state, item_name):
    '''Функция использования предмета'''
    if (item_name in game_state['player_inventory']):
        match item_name:
            case 'torch':
                print ('Стало светлее')
            case 'sword':
                print ('Вы чувствуете уверенность')            
            case 'bronze_box':
                print ('Вы открыли шкатулку')
                if ('rusty_key' not in game_state['player_inventory']):
                    game_state['player_inventory'].append('rusty_key')
                    print('Вы взяли \'rusty_key\'')
                else:
                    pass
            case _:
                print ('Вы не знаете как использовать', item_name)         


