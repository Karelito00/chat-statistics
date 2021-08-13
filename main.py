from parse import PrepareData
from statistics import Summary

Platforms = ['WhatsApp', 'Telegram']
def show_platforms():
    for i in range(len(Platforms)):
        print("[" + str(i + 1) + "] " + Platforms[i])

print("Name of the file:")
filename = input()

print("Platform:")
show_platforms()
selected_platform = int(input())


data = PrepareData(filename, Platforms[selected_platform - 1]).run()
summary = Summary(data)

summary.run()
