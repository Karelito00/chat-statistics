import matplotlib.pyplot as plt
import numpy as np
import collections
from datetime import datetime
from pdf import PDF
from prettytable import PrettyTable
import os
from spam.spam_detection import SpamDetection
from core.lang_recognition import recognize

class Statistics:

    def __init__(self, data):
        self.data = data

    def build_pretty_table(self, columns, data):
        t = PrettyTable(columns)
        for index, row in data.iterrows():
            t_row = [index]

            for column in columns[1:]:
                t_row.append(row[column])

            t.add_row(t_row)
            if(index == 5):
                break

        return t

    def getAuthorsActivity(self):
        authorsActivity = collections.Counter(self.data['Author'])
        authorsActivity = [[authorsActivity[author], author] for author in authorsActivity]
        authorsActivity.sort()
        return authorsActivity[::-1]

    def draw_pie_sentiment(self, pdf, column="Positive", ALPHA=0.6):
        data = self.data.copy()
        data[column] = [1 if x > ALPHA else 0 for x in data[column]]
        data[column] = data[column].astype(int)

        new_data = data.groupby(data['Author']).sum()
        new_data = new_data.sort_values(by=column, ascending=False).head(5)

        index = new_data.index
        values = new_data[column]

        custom_colors = ["skyblue", "yellowgreen", 'tomato', "blue", "red"]
        plt.figure(figsize=(8, 6))
        plt.pie(values, labels=index, colors=custom_colors[:len(index)])
        central_circle = plt.Circle((0, 0), 0.5, color='white')
        fig = plt.gcf()
        fig.gca().add_artist(central_circle)
        plt.rc('font', size=12)

        name = "Top " + str(len(index)) + " chat authors more " + column
        plt.title(name, fontsize=20)
        figure = plt.gcf()
        figure.set_size_inches(11, 8)
        plt.savefig(name + '.png')
        plt.close()
        pdf.write_text(name)
        pdf.write_image(name + '.png')
        os.remove(name + '.png')
        pdf.write_endlines(2)
        new_data = new_data[[column]]
        t = self.build_pretty_table(['Author', column], new_data)
        pdf.write_text(t.get_string())
        pdf.write_separator()

    def get_hour(self, time):
        num = 0
        for c in time:
            if(c == ':'):
                break
            num = num * 10 + int(c)

        if(time[-2] == 'P'):
            num += 12
        if(num == 24):
            num = 0
        return num

    def show_activity_by_hour(self, pdf):
        data = self.data.copy()
        authorsActivity = self.getAuthorsActivity()

        authorsActivity = authorsActivity[:min(len(authorsActivity), 5)]
        authors = [author for messages, author in authorsActivity]

        data['Message'] = 1
        data['Time'] = [self.get_hour(time) for time in data['Time']]
        data = data.pivot_table('Message', index="Time", columns='Author', aggfunc='sum')
        data = data[authors]
        data = data.fillna(0).astype(int)
        data.plot()

        name = "Activity according to time"
        plt.ylabel(name)
        figure = plt.gcf()
        figure.set_size_inches(11, 8)
        plt.savefig(name + ".png")
        plt.close()
        pdf.write_text(name)
        pdf.write_endlines(2)
        pdf.write_image(name + '.png', w=200)
        os.remove(name + '.png')
        pdf.write_separator()

    def percent(self, p, t):
        return round((float(p) / float(t)) * 100, 2)

    def show_authors_activity(self, pdf):
        authorsActivity = self.getAuthorsActivity()
        total = 0
        for messages, author in authorsActivity:
            total += messages

        pdf.write_text("Authors activity")
        t = PrettyTable(['Author', 'Messages', 'Percent'])
        for messages, author in authorsActivity:
            t.add_row([author, messages, str(self.percent(messages, total)) + "%"])

        t.add_row(["Total", total, "100%"])
        pdf.write_text(t.get_string())
        pdf.write_separator()

    def clasify_spam_or_ham(self, pdf):
        spam_d = SpamDetection()
        spam_d.train_model()
        data = self.data.copy()
        data['Message_Summary'] = data['Message_Summary'].astype(str)
        data['Spam'] = spam_d.predict_array(data['Message_Summary'])
        data = data[['Author', 'Spam']]

        data = data.groupby(data['Author']).sum()
        data = data.sort_values(by="Spam", ascending=False).head()

        name = "Spam frecuency by Author"

        plt.bar(data.index, data['Spam'], align='center')
        plt.xlabel('Author')
        plt.ylabel('Spam frequency')
        figure = plt.gcf()
        figure.set_size_inches(10, 8)
        plt.savefig(name + ".png")
        plt.close()
        pdf.write_text(name)
        pdf.write_endlines(2)
        pdf.write_image(name + '.png', w=200)
        os.remove(name + '.png')
        pdf.write_separator()

    def recognize_func(self, text):
        return recognize(text).best_lang

    def recognize_language(self, pdf):
        data = self.data.copy()
        data['language'] = data['Message'].apply(self.recognize_func)
        data = data[['language', 'Message']]
        data['Message'] = 1
        data = data.groupby(data['language']).sum()
        data = data.sort_values(by='Message', ascending=False).head()

        name = "Language frecuency"

        plt.bar(data.index, data['Message'], align='center')
        plt.xlabel('Language')
        plt.ylabel('Frequency')
        figure = plt.gcf()
        figure.set_size_inches(11, 9)
        plt.savefig(name + ".png",)
        plt.close()
        pdf.write_text(name)
        pdf.write_endlines(2)
        pdf.write_image(name + '.png', w=200)
        os.remove(name + '.png')
        pdf.write_separator()


class Summary(Statistics):

    def __init__(self, data):
        Statistics.__init__(self, data)
        self.pdf = PDF()

    def show_sliced_names(self):
        data = self.data
        new_data = data[data['Author'] != data['Real Name']]
        new_data = new_data.drop_duplicates(subset='Author', keep="last")
        results = []
        for index, row in new_data.iterrows():
            results.append([row['Author'], row['Real Name']])
        if(len(results)):
            self.pdf.write_text("Somes names was sliced")
            for author, real_name in results:
                self.pdf.write_text(author + "  ->  " + real_name)
            self.pdf.write_separator()

    def run(self):
        self.show_sliced_names()
        self.show_authors_activity(self.pdf)
        self.draw_pie_sentiment(self.pdf)
        self.draw_pie_sentiment(self.pdf, 'Negative', 0.8)
        self.draw_pie_sentiment(self.pdf, 'Neutral')
        self.show_activity_by_hour(self.pdf)
        self.clasify_spam_or_ham(self.pdf)
        self.recognize_language(self.pdf)
        self.pdf.print_pdf()
