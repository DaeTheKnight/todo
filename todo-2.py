"""todo app version 2 is designed to allow you to save your list to a file"""

import json
import os

# Configuration
SAVE_FILE = "questlog.json"

# Global state (loaded at startup)
game_data = {
    "tasklist": [],
    "donelist": []
}

def load_game():
    """Loads data from JSON file if it exists."""
    global game_data
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, 'r') as f:
            game_data = json.load(f)
            message(x=110)
    else:
        save_game()
        message(x=109)

def save_game():
    with open(SAVE_FILE, 'w') as f:
        json.dump(game_data, f, indent=4)

def addtask(task):
    if task not in game_data["tasklist"]:
        game_data["tasklist"].append(task)
        save_game()
        message(task, 101)
    elif task in game_data["tasklist"]:
        message(task, x=100)

def donetask(task):
    if task in game_data["tasklist"]:
        game_data["donelist"].append(task)
        game_data["tasklist"].remove(task)
        save_game()
        message(task, 102)
    else:
        game_data["donelist"].append(task)
        message(task, 103)

def delete(task):
    if task in game_data["donelist"]:
        game_data["donelist"].remove(task)
        message(task, x=106)
    elif task in game_data["tasklist"]:
        game_data["tasklist"].remove(task)
        message(task, x=106)
    else:
        message(task, x=108)

def message(task=None, x=104):
    if x == 100:
        print(f'{f"\u274C{task} already in Quests\u274C":=^30}')
    elif x == 101:
        print(f'{f"\u2705{task} added to Quests\u2705":=^30}')
    elif x == 102:
        print(f'{f"\U0001F3C6{task} complete! Added to Completed Quests\U0001F3C6":=^36}')
    elif x == 103:
        print(f'{f"\U0001F3C6{task} added to the Completed Quests\U0001F3C6":=^30}')
    elif x == 104:
        print(f'{f"\u274CYou cant do that!\u274C":=^31}')
    elif x == 105:
        print(f'{f"\U0001F4BESaving and exiting...\U0001F4BE":=^40}')
    elif x == 106:
        print(f'{f"\U0001F5D1\uFE0F{task} deleted\U0001F5D1\uFE0F":=^31}')
    elif x == 107:
        print(f'{f"\U0001F4BESaving Game...\U0001F4BE":=^31}')
    elif x == 108:
        print(f'{f"\u274CQuest does not exist...\u274C":=^31}')
    elif x == 109:
        print(f'{"\U0001f4bfNew Save Created!\U0001f4bf":=^31}')
    elif x == 110:
        print(f'{"\U0001F4C2Game Loaded from Previous Save File!\U0001F4C2":=^31}')

def status():
    print(f"""Here's your quest progress!
    {'Active Quests':=^23}
    {game_data['tasklist']}
    {'Completed Quests':=^23}
    {game_data['donelist']}
""")

def entry():
    while True:
        save_game()
        #pass
        #ask player to enter message
        choice = input(f"""{'\U0001F47E':=^31}
{'Pick from these options': >27}
status | add quest | done quest
delete | save game |    exit
: """)
        if choice == "status":
            status()
        elif choice == "add quest":
            addtask(input("What's the new quest?: "))
        elif choice == "done quest":
            donetask(input("What quest did you complete?: "))
        elif choice == "exit":
            save_game()
            message(x=105)
            return
        elif choice == "delete":
            deleted_task = input("What would you like to delete?: ")
            delete(deleted_task)
        elif choice == "save game":
            save_game()
            message(x=107)
        else:
            message(x=104)

if __name__ == '__main__':
    load_game()
    entry()

