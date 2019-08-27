import json
import requests
import time
import urllib
from dbhelper import DBHelper
from heuristicaMOS import taskScheduler

db = DBHelper()
taskSh = taskScheduler()


TOKEN = "784913428:AAFKWZj-d7bxfm4uyRoj2jg_GypOsHFCaT8"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
addingTaskTask = False
addingTaskHours = False
name, percentage, hours, priority, days = "", "", "", "", ""
daysName = ['1st Day', '2nd Day', '3rd Day', '4th Day', '5th Day', '6th Day', '7th Day']


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def handle_updates(updates):
    global addingTask, addingTaskHours, name, percentage, hours, priority, days, daysName
    for update in updates["result"]:
        text = update["message"]["text"]
        chat = update["message"]["chat"]["id"]
        items = db.get_items(chat)
        if text == "/delete":
            keyboard = build_keyboard(items)
            send_message("Select an item to delete", chat, keyboard)
        elif text == "/list":
            message = "\n".join(items)
            send_message(message, chat)
        elif text == "/tasks":
            get_list_tasks(chat)
        elif text == "/hours":
            get_list_hours(chat)
        elif text == "/start":
            send_message("Send /addTask to add a new task \n /addHours to add the hours of the days \n /tasks to see all the tasks \n /hours to add the daily hours \n /delete to remove tasks \n /taskScheduler to receive the task scheduler done", chat)
        elif text == "/taskScheduler":
            get_task_scheduler(chat)
        elif text in items:
            db.delete_item(text, chat)
            items = db.get_items(chat)
            keyboard = build_keyboard(items)
            send_message("Select an item to delete", chat, keyboard)
        elif text == "/addHours":
            addingTaskHours = True
            send_message("For adding the hours, please tell me the hours available of each day (from first to seventh day) separated by comas", chat)
        elif addingTaskHours:
            if isString(text):
                dailyHours = text.split(',')
                for i in range(len(dailyHours)):
                    db.add_hours(daysName[i], dailyHours[i], chat)
                send_message("The hours has been added", chat)
                addingTaskHours = False
            else:
                send_message("There was an error inserting the hours of the days", chat)
        elif text == "/addTask":
            name, percentage, hours, priority, days = "", "", "", "", ""
            addingTask = True
            send_message("For adding a task, please tell me the name of it", chat)
        elif addingTask:
            if name == "":
                if isString(text):
                    name = str(text)
                    send_message("Done, the task name is " + str(name) + " , now please tell me the percentage that the task represents of its subject (the percentage must be between 0 and 1)", chat)
                else:
                    send_message("The name you gave is not valid, please enter a valid name for the task", chat)
            elif percentage == "":
                if isFloat(text):
                    percentage = float(text)
                    send_message("Done, the task's percentage is " + str(percentage) + " , now please tell me the number of hours that the task will take", chat)
                else:
                    send_message("The percentage you gave is not valid, please enter a valid percentage for the task (remember that the percentage must be between 0 and 1)", chat)
            elif hours == "":
                if isFloat(text):
                    hours = float(text)
                    send_message("Done, the task's hours are " + str(hours) + " , now please tell me the priority of the task (it has to be between 1 and 10)", chat)
                else:
                    send_message("The number of hours you gave are not valid, please enter a valid number of hours for the task", chat)
            elif priority == "":
                if isFloat(text):
                    priority = float(text)
                    send_message("Done, the task's priority is " + str(priority) + " , now please tell me the number of days available for doing the task (it can't be zero (0))", chat)
                else:
                    send_message("The priority you gave is not valid, please enter a valid priority for the task (remember it has to be between 1 and 10)", chat)
                    send_message("The number of hours you gave are not valid, please enter a valid number of hours for the task", chat)
            elif days == "":
                if isFloat(text):
                    days = float(text)
                    db.add_item(name, percentage, hours, priority, days, 0, chat)
                    send_message("The task has been created!! \n" + " The name of the task is " + str(name) + " \n The percentage of the task is " + str(percentage) + " \n The hours for doing the task are " + str(hours) + " \n The task's priority is " + str(priority) + " \n The available days for doing the task are " + str(days), chat)
                    send_message("Send /tasks to see all the tasks or /delete to remove a task", chat)
                    addingTask = False
                else:
                    send_message("The days available you gave are not valid, please enter a valid number of available days for the task (remember it cannot be zero (0))", chat)


def get_task_scheduler(owner):
    tasks = db.get_all_tasks(owner)
    hours = db.get_hours(owner)
    msg = taskSh.get_scheduler(tasks, hours)
    send_message(msg, owner)


def get_list_tasks(owner):
    tasks = db.get_all_tasks(owner)
    msg = from_list_to_string(tasks)
    send_message(msg, owner)


def get_list_hours(owner):
    hours = db.get_hours(owner)
    msg = from_list_to_string(hours)
    send_message(msg, owner)


def from_list_to_string(theList):
    msg = ""
    for x in range(len(theList)):
        msg += str(theList[x]) + '\n'
    return msg


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def build_keyboard(items):
    keyboard = [[item] for item in items]
    reply_markup = {"keyboard": keyboard, "one_time_keyboard": True}
    return json.dumps(reply_markup)


def send_message(text, chat_id, reply_markup=None):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
    if reply_markup:
        url += "&reply_markup={}".format(reply_markup)
    get_url(url)


def isString(text):
    try:
        str(text)
        return True
    except:
        return False


def isFloat(text):
    try:
        float(text)
        return True
    except:
        return False


def main():
    global addingTask
    db.setup()
    last_update_id = None
    addingTask = False
    addingTaskHours = False
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            handle_updates(updates)
        time.sleep(0.5)


if __name__ == '__main__':
    main()
