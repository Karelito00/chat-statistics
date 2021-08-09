from parse import PrepareData
from statistics import Summary

data = PrepareData('result.json', 'Telegram').run()
summary = Summary(data)

summary.run()
