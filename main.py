from parse import PrepareData
from statistics import Summary

data = PrepareData('_chat.txt', 'WhatsApp').run()
summary = Summary(data)

summary.run()
