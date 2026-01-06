tasklist = []
donelist = []

def addtask(task):
    if task not in tasklist:
        tasklist.append(task)
        message(task, 101)
    else:
        message(task, 100)

def donetask(task):
    if task in tasklist:
        donelist.append(task)
        tasklist.remove(task)
        message(task, 102)
    else:
        donelist.append(task)
        message(task, 103)

def message(task=None, x=104):
    if x == 100:
        print(f'{f"{task} already in list":=^30}')
    elif x == 101:
        print(f'{f"{task} added to list":=^30}')
    elif x == 102:
        print(f'{f"{task} complete! Added to done list":=^36}')
    elif x == 103:
        print(f'{f"{task} added to the done list":=^30}')
    elif x == 104:
        print(f'{f"You cant do that!":=^20}')
    elif x == 105:
        print(f'{f"Continue...":?^16}')


def status():
    print(f"""Here's your quest progress!
    {'Tasklist:':=^23}
    {tasklist}
    {'Donelist:':=^23}
    {donelist}
""")

def entry():
    while True:
        #pass
        #ask player to enter message
        choice = input(f"""{'Pick from these options': >27}
status | add quest | done quest
: """)
        if choice == "status":
            status()
        elif choice == "add quest":
            addtask(input("What's the new quest?: "))
        elif choice == "done quest":
            donetask(input("What quest did you complete?: "))
        elif choice == "exit":
            message(x=105)
            return
        else:
            message(x=104)

if __name__ == '__main__':
    entry()


