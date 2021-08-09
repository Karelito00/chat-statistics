import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import json
from datetime import datetime

class ParseConversation:

    def __init__(self, filename = "_chat.txt"):
        self.filename = filename

    def convert_to_df(self, data):
        df = pd.DataFrame(data, columns=["Date", 'Time', 'Author', 'Message'])
        df['Date'] = pd.to_datetime(df['Date'])

        data = df.dropna()

        sentiments = SentimentIntensityAnalyzer()
        data["Positive"] = [sentiments.polarity_scores(i)["pos"] for i in data["Message"]]
        data["Negative"] = [sentiments.polarity_scores(i)["neg"] for i in data["Message"]]
        data["Neutral"] = [sentiments.polarity_scores(i)["neu"] for i in data["Message"]]

        return data

class WhatsApp(ParseConversation):

    def __init__(self, filename):
        ParseConversation.__init__(self, filename)

    # Extract Time
    def date_time(self, s):
        if(s[0] != '['):
            return None
        sol = ""
        for c in s:
            if(c == '['):
                continue
            if(c == ']'):
                break
            sol += c
        return sol

    # Find Authors or Contacts
    def find_author(self, s):
        s = s[::-1]
        sol = ""
        for c in s:
            if c == ']':
                break
            sol += c
        return sol[::-1].strip()

    # Parse Line
    def parse_line(self, line):
        splitline = line.split(':')
        if(len(splitline) < 4):
            return []
        dateTime = self.date_time(":".join(splitline[:3]))
        if(dateTime == None):
            return []
        date, time = dateTime.split(", ")
        message = ":".join(splitline[3:])
        author = self.find_author(":".join(splitline[:3]))

        return [date, time, author, message]

    def prepare_data(self):
        data = []
        with open(self.filename, encoding="utf-8") as fp:
            fp.readline()
            while True:
                line = fp.readline()
                if not line:
                    break
                parseLine = self.parse_line(line)
                if(len(parseLine) != 4):
                    continue
                data.append(parseLine)

        return self.convert_to_df(data)

class Telegram(ParseConversation):
    def __init__(self, filename):
        ParseConversation.__init__(self, filename)

    def prepare_data(self):
        data = []
        f = open(self.filename, encoding="utf-8")
        json_file = json.load(f)
        messages = json_file['messages']
        for _message in messages:
            if(_message['type'] == 'service'):
                continue
            author = _message['from']
            message = _message['text']
            date, time = _message['date'].split('T')
            data.append([date, time, author, str(message)])

        f.close()

        return self.convert_to_df(data)


class PrepareData:
    def __init__(self, filename, chat_type):
        self.chat_type = chat_type
        self.filename = filename

    def run(self):
        if self.chat_type == 'WhatsApp':
            return WhatsApp(self.filename).prepare_data()
        elif self.chat_type == 'Telegram':
            return Telegram(self.filename).prepare_data()


