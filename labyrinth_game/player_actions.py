from labyrinth_game.constants import ROOMS

def show_inventory(game_state):
    '''Функция отображения инвентаря'''
    inventory = game_state['player_inventory']
    if (inventory != []):
        print ('У вас есть:', inventory)
    else:
        print ('Инвентарь пуст!')
    
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
    from labyrinth_game.utils import describe_current_room, random_event
    room = game_state['current_room']
    room_exits = ROOMS[room]['exits']
    
    if (direction in room_exits):
        game_state['current_room'] = room_exits[direction]

        if (game_state['current_room'] == 'treasure_room'):
            print('rusty_key' in game_state['player_inventory'])
            if ('rusty_key' in game_state['player_inventory']):
                print ("Вы используете найденный ключ,\
 чтобы открыть путь в комнату сокровищ.")
            else:
                game_state['current_room'] = room
                
                print("Дверь заперта. Нужен ключ, чтобы пройти дальше.")
                return
        game_state['steps_taken'] += 1
        describe_current_room(game_state)
        random_event(game_state)
               
    else:
        print('Нельзя пойти в этом направлении')
    
def take_item(game_state, item_name):
    '''Функция взятия предмета'''
    room = game_state['current_room']
    room_items = ROOMS[room]['items']
    if (item_name in room_items):
        if (item_name == 'treasure_chest'):
            print('Вы не можете поднять сундук, он слишком тяжелый')
            return
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


