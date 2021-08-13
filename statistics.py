import matplotlib.pyplot as plt
import numpy as np
import collections
from datetime import datetime
from pdf import PDF

class Statistics:

    def __init__(self, data):
        self.data = data

    def getAuthorsActivity(self):
        authorsActivity = collections.Counter(self.data['Author'])
        authorsActivity = [[authorsActivity[author], author] for author in authorsActivity]
        authorsActivity.sort()
        return authorsActivity[::-1]

    def draw_pie_sentiment(self, pdf, column="Positive", ALPHA=0.6):
        data = self.data
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
        plt.savefig('1.png')
        pdf.write_text(name)
        pdf.write_image('1.png')
        pdf.write_endlines(2)
        pdf.write_text(str(new_data[[column]]))
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
        data = self.data
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
        plt.savefig("1.png")
        pdf.write_text(name)
        pdf.write_endlines(2)
        pdf.write_image('1.png')
        pdf.write_separator()

    def percent(self, p, t):
        return round((float(p) / float(t)) * 100, 2)

    def show_authors_activity(self, pdf):
        authorsActivity = self.getAuthorsActivity()
        total = 0
        for messages, author in authorsActivity:
            total += messages

        pdf.write_text("Authors activity")
        for messages, author in authorsActivity:
            pdf.write_text("Author: " + author + ", messages: " + str(messages) + ", percent: " + str(self.percent(messages, total)) + "%")

        pdf.write_separator()

class Summary(Statistics):

    def __init__(self, data):
        Statistics.__init__(self, data)
        self.pdf = PDF()

    def run(self):
        self.show_authors_activity(self.pdf)
        self.draw_pie_sentiment(self.pdf)
        self.draw_pie_sentiment(self.pdf, 'Negative', 0.8)
        self.draw_pie_sentiment(self.pdf, 'Neutral')
        self.show_activity_by_hour(self.pdf)
        self.pdf.print_pdf()
