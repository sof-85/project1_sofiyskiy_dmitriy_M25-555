import math

from labyrinth_game.constants import COMMANDS, ROOMS


def describe_current_room(game_state):
    '''Функция описания комнаты'''
    room = game_state['current_room']
    room_features = ROOMS[room]
    
    print ("== ", room.upper()," ==" )
    
    print (room_features['description'])
    
    if (room_features['items'] != []):
        print ('Заметные предметы:', room_features['items'])
    
    print ('Выходы:', room_features['exits'])
    
    if (room_features['puzzle'] is not None):
        print ("Кажется, здесь есть загадка (используйте команду solve).")

def solve_puzzle(game_state):
    '''Функция решения загадок'''
    from labyrinth_game.player_actions import get_input
    room = game_state['current_room']
    room_puzzle = ROOMS[room]['puzzle']
    if (room_puzzle is not None):
        print(room_puzzle[0])
        init_answer = get_input(prompt="Ваш ответ: ")
        answer = alt_answer(room, init_answer)
        if (answer == room_puzzle[1]):
            print('Правильно! Загадка решена!')
            ROOMS[room]['puzzle'] = None
            reward = give_reward(room)
            print('Вы получаете:', reward)
            game_state['player_inventory'].append(reward)
        else:
            print('Неверно. Попробуйте снова')
            print('Для этого еще раз наберите команду solve')
            if (room == 'trap_room'):
                trigger_trap(game_state)    
        
    else:
        print ('Здесь загадок нет.')
        return
    

def attempt_open_treasure(game_state):
    '''Реализация логики победы'''
    from labyrinth_game.player_actions import get_input
    room = game_state['current_room']
    global game_over

    
    if (('treasure_key' in game_state['player_inventory']) and (room == 'treasure_room')):
        print ("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        game_state['player_inventory'].remove('treasure_key')
        print ("В сундуке сокровище! Вы победили!")
        game_state['game_over'] = True
        return
    else:
        print ('Сундук заперт. ...Ввести код? (да/нет)')
        answer = get_input()
        if (answer == 'да'):
            print (ROOMS[room]['puzzle'][0])
            code = get_input()
            if (code == ROOMS[room]['puzzle'][1]):
                print ("В сундуке сокровище! Вы победили!")
                game_state['game_over'] = True
                return
            else:
                print('Код неверный')
                print('Для повторной попытки используйте команду solve')
                return
        elif (answer == 'нет'):
            print('Вы отступаете от сундука')
            return
        else:
            print('Ответ должен быть \'да\' или \'нет\'')
            print('Вы отступаете от сундука')
            return
            

def show_help(default = COMMANDS):
    '''Функция помощи'''
    print("\nДоступные команды:")
    for i in COMMANDS:
        print(f"{i:<16}{COMMANDS.get(i)}")


'''
def show_help():
    Старая функция помощи
    print("\nДоступные команды:")
    print("  go <direction>  - перейти в направлении (north/south/east/west)")
    print("  look            - осмотреть текущую комнату")
    print("  take <item>     - поднять предмет")
    print("  use <item>      - использовать предмет из инвентаря")
    print("  inventory       - показать инвентарь")
    print("  solve           - попытаться решить загадку в комнате")
    print("  quit            - выйти из игры")
    print("  help            - показать это сообщение")
'''
def pseudo_random(seed, modulo):
    '''Функция  случайности'''
    init_rnd = math.sin(seed*12.9898)
    imp_rnd = init_rnd * 43758.5453
    next_rnd = imp_rnd - math.floor(imp_rnd)
    fin_rnd = int(next_rnd*modulo)
    return fin_rnd

def trigger_trap(game_state):
    global game_over
    print ("Ловушка активирована! Пол стал дрожать...")
    if (game_state['player_inventory'] != []):
        modulo = len(game_state['player_inventory'])
        seed = game_state['steps_taken']
        lost_item = pseudo_random(seed, modulo)
        print('Вы потеряли ', game_state['player_inventory'][lost_item],'!')
        game_state['player_inventory'].extend(game_state['player_inventory'][lost_item])
    else:
        seed = game_state['steps_taken']
        damage = pseudo_random(seed, 9)
        if (damage < 3):
            print('Вы навсегда остались пленником Лабиринта!')
            print('Игра проиграна!')
            game_over = True
        else:
            print("Вы уцелели!")
                
def random_event(game_state):
    '''Функция реализации случайного события'''
    seed = game_state['steps_taken']
    
    room = game_state['current_room']
    
    is_exist =  pseudo_random(seed, 10)
    
    if (is_exist > 0):
        scn = pseudo_random(seed, 3)
        
        match scn:
            case 0:
                ROOMS[room]['items'].append('coin')
                print('Вы видите на полу комнаты монетку')
            case 1:
                print('Вы слышите пугающий шорох в углу комнаты')
                if ('sword' in game_state['player_inventory']):
                    print('Вы отпугнули существо')
            case 2:
                if (room == 'trap_room') and \
                    ('torch' not in game_state['player_inventory']):
                    print ('Здесь опасно!')
                    trigger_trap(game_state)
               
def alt_answer (room, answer):
    '''Функция поддержки альтернативных ответов'''
    match room:
        case 'treasure_room':
            answer = answer.lower()
            if (answer in ['10','десять']):
                return '10'
            else:
                return answer
        case 'hall':
            answer = answer.lower()
            #print(answer)
            #print(answer in ['10','десять'])
            if (answer in ['10','десять']):
                return '10'
            else:
                return answer            
        case 'trap_room':
            answer = answer.lower()
            return answer            
        case 'hall':
            answer = answer.lower()
            return answer            
        case 'library':
            answer = answer.lower()
            return answer
        case _:
            return answer
        
def give_reward(room):
    match room:
        case 'hall':
            return 'coin'
        case 'trap_room':
            return 'treasure_key'
        case 'library':
            return 'book'
        case 'treasure_room':
            return 'piece of gold'


