import json
import os

# config
save_file = "questlog.json"

# Global state
game_data = {
    "tasklist": [],
    "donelist": []
}

def load_game():
    """Loads data from JSON file if it exists."""
    global game_data
    if os.path.exists(save_file):
        try:
            with open(save_file, 'r') as f:
                game_data = json.load(f)
                message(x=110)
        except (json.JSONDecodeError, ValueError):
            save_game()
            message(x=109)
    else:
        save_game()
        message(x=109)

def save_game():
    with open(save_file, 'w') as f:
        json.dump(game_data, f, indent=4)

def get_task_by_id(user_input):
    """
    Translates a number into a task,
    If the input is not a number, it returns the test as-is.
    """
    # 1. Check if input is a number
    if user_input.isdigit():
        index = int(user_input)
        active_count = len(game_data["tasklist"])
        done_count = len(game_data["donelist"])
        total_count = active_count + done_count

    # 2. If number is out of bounds, fail
        if index < 1 or index > total_count:
            return "out of bounds"

    # 2. Check if number is in the active list (1 to N)
        if index <= active_count:
            return game_data["tasklist"][index - 1]

    # 3. Check if a number is in the done list (n+1 to total)
        else:
            return game_data["donelist"][index - active_count -1]

    # 4. If not a number, return original text
    return user_input

def addtask(task):
    if not task.strip():
        message(x=104)
        return
    if task not in game_data["tasklist"]:
        game_data["tasklist"].append(task)
        save_game()
        message(task, x=101)
    elif task in game_data["tasklist"]:
        message(task, x=100)

def donetask(user_input):
    task = get_task_by_id(user_input)

    if task == "out of bounds":
        message(user_input, 108)
        return

    if user_input.isdigit():
        index = int(user_input)
        working_count = len(game_data["tasklist"])

        if index > working_count:
            message(task, x=104)
            return

    if task in game_data["tasklist"]:
        game_data["donelist"].append(task)
        game_data["tasklist"].remove(task)
        save_game()
        message(task, 102)
    else:
        game_data["donelist"].append(task)
        save_game()
        message(task, 103)

def delete(user_input):
    # Convert Number --> Name
    task = get_task_by_id(user_input)

    if task == "out of bounds":
        message(user_input, 108)
        return

    if task in game_data["tasklist"]:
        game_data["tasklist"].remove(task)
        save_game()
        message(task, x=106)
    elif task in game_data["donelist"]:
        game_data["donelist"].remove(task)
        save_game()
        message(task, x=106)
    else:
        message(task, x=108)

def message(task=None, x=111):
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
    elif x == 111:
        print(f'{f"\u274C{task} created an error!\u274C":=^31}')
    elif x == 112:
        print("access denied")
    elif x == 113:
        print("")

def status():
    print(f"Here's your quest progress!")
    print(f"{'Active Quests':=^23}")
    counter = 1

    if not game_data["tasklist"]:
        print("    (No active quests)")
    else:
        for task in game_data["tasklist"]:
            print(f"{counter}. {task}")
            counter += 1

    print(f"{'Completed Quests':=^23}")

    if not game_data["donelist"]:
        print("    (No quests completed)")
    else:
        for task in game_data["donelist"]:
            print(f"{counter}. {task}")
            counter += 1
    message(x=113)

def entry():
    while True:
        # save_game()
        choice = input(f"""{'\U0001F47E':=^31}
{'Pick from these options': >27}
status | add quest | done quest
delete | save game |    exit
: """)
        if choice == "status":
            status()
        elif choice == "add quest":
            addtask(input("What's the new quest?:"))
        elif choice == "done quest":
            donetask(input("What quest did you complete? (# or name): "))
        elif choice == "exit":
            save_game()
            message(x=105)
            return
        elif choice == "delete":
            delete(input("What would you like to delete? (# or name): "))
        elif choice == "save game":
            save_game()
            message(x=107)
        else:
            message(x=104)

if __name__ == '__main__':
    load_game()
    entry()