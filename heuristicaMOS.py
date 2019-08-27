import numpy as np
import pandas as pd


class taskScheduler:

    def __init__(self):
        matrTasks = np.zeros((10, 5))

    def get_scheduler(self, tasks, hours):
        matrTasks = np.zeros((10, 5))
        taskNames = ['1st Task', '2nd Task', '3rd Task', '4th Task', '5th Task', '6th Task', '7th Task', '8th Task', '9th Task', '10th Task']
        dailyHours = np.zeros((7, 1))
        days = ['1st Day', '2nd Day', '3rd Day', '4th Day', '5th Day', '6th Day', '7th Day']
        fileWrite = open('resultHeuristic.txt', 'w')
        for i in range(len(tasks)):
            for j in range(len(tasks[0]) - 1):
                matrTasks[i][j] = tasks[i][j + 1]
                print('Adding the variable ' + str(tasks[i][j + 1]))
            taskNames[i] = tasks[i][0]
        for i in range(len(hours)):
            dailyHours[i] = hours[i][1]
        dfResult = pd.DataFrame(index=taskNames, columns=days)
        return self.sortTasks(matrTasks, taskNames, dailyHours, days, dfResult, fileWrite)

    def sortTasks(self, matrTasks, taskNames, dailyHours, days, dfResult, fileWrite):
        for i in range(len(matrTasks)):
            if (matrTasks[i][1] == 0):
                break
            weight = matrTasks[i][0] * matrTasks[i][1] * matrTasks[i][2] / matrTasks[i][3]
            for j in range(i, len(matrTasks)):
                if (matrTasks[j][1] == 0):
                    break
                compareWeight = matrTasks[j][0] * matrTasks[j][1] * matrTasks[j][2] / matrTasks[j][3]
                if compareWeight > weight:
                    temp = [x for x in matrTasks[i]]
                    temp2 = taskNames[i]
                    matrTasks[i] = [x for x in matrTasks[j]]
                    taskNames[i] = taskNames[j]
                    matrTasks[j] = [x for x in temp]
                    taskNames[j] = temp2
                    weight = compareWeight
        return self.organizeTasks(matrTasks, taskNames, dailyHours, days, dfResult, fileWrite)

    def organizeTasks(self, matrTasks, taskNames, dailyHours, days, dfResult, fileWrite):
        # Once they are sorted, its just to put them in the days according to the avalaible hours
        print(matrTasks)
        finalResult = ""
        for i in range(len(dailyHours)):
            for j in range(len(matrTasks)):
                if (matrTasks[j][1] == 0):
                    break
                task = matrTasks[j]
                if (task[4] < 1):
                    hoursTask = task[1]
                    prcnt = 1 if dailyHours[i] / hoursTask >= 1 else float(dailyHours[i] / hoursTask)
                    if (prcnt > 0):
                        if (prcnt > (1 - task[4])):
                            prcnt = (1 - task[4])
                        matrTasks[j][4] += prcnt
                        dailyHours[i] -= matrTasks[j][1] * prcnt
                        dfResult.at[taskNames[j], days[i]] = prcnt
                        result = ("In the " + str(i + 1) + " day, you should make the " + str(prcnt * 100) + "% of the " + str(taskNames[j]) + " task \n")
                        fileWrite.write(result)
                        finalResult += result + ' \n'
        dfResult.to_csv('heuristica.csv', decimal=',', sep=';', encoding='utf-8', float_format='%.3f')
        return finalResult
