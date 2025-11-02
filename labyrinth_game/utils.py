from constants import ROOMS

#from main import *

def describe_current_room(game_state):
    '''Функция описания комнаты'''
    room = game_state['current_room']
    room_features = ROOMS[room]
    
    print ("== ", room.upper()," ==" )
    
    print (room_features['description'])
    
    if (room_features['items'] != []):
        print ('Заметные предметы:', room_features['items'])
    else:
        pass
    
    print ('Выходы:', room_features['exits'])
    
    if (room_features['puzzle'] is not None):
        print ("Кажется, здесь есть загадка (используйте команду solve).")
    else:
        pass


def solve_puzzle(game_state):
    '''Функция решения загадок'''
    from player_actions import get_input
    room = game_state['current_room']
    room_puzzle = ROOMS[room]['puzzle']
    if (room_puzzle != []):
        print(room_puzzle[0])
        answer = get_input(prompt="Ваш ответ: ")
        if (answer == room_puzzle[1]):
            print('Правильно! Загадка решена!')
            ROOMS[room]['puzzle'] = None
            #Добавить награду
        else:
            print('Неверно. Попробуйте снова')    
        
    else:
        print ('Здесь загадок нет.')
        return
    

def attempt_open_treasure(game_state):
    '''Реализация логики победы'''
    from player_actions import get_input
    room = game_state['current_room']
    global game_over
    if 'treasure_key' in game_state['player_inventory']:
        print ("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        ROOMS[room]['items'].remove('treasure_key')
        print ("В сундуке сокровище! Вы победили!")
        game_over= True
    else:
        print ('Сундук заперт. ...Ввести код? (да/нет)')
        answer = get_input()
        if (answer == 'да'):
            print (ROOMS[room]['puzzle'][0])
            code = get_input()
            if (code == ROOMS[room]['puzzle'][1]):
                print ("В сундуке сокровище! Вы победили!")
                game_over= True
            else:
                print('Код неверный')
        elif (answer == 'нет'):
            print('Вы отступаете от сундука')
            

def show_help():
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
game_state = {
        'player_inventory': [], # Инвентарь игрока
        'current_room': 'entrance', # Текущая комната
        'game_over': False, # Значения окончания игры
        'steps_taken': 0 # Количество шагов
}


game_state['current_room'] = 'library'
solve_puzzle(game_state)

#room = ROOMS[game_state['current_room']]
#room = game_state['current_room']
#room_features = ROOMS[room]
#print(room_features['items'] != [])
#print('Заметные предметы:', room_features['items'])

#describe_current_room(game_state)

if __name__=='__main__':
    describe_current_room(game_state)
'''

