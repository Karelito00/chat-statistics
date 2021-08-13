import fpdf

SEPARATOR = '---------------------------------------------------------------------------'

class PDF:

    def __init__(self):
        self.pdf = fpdf.FPDF(format='letter')
        self.pdf.add_page()
        self.pdf.set_font("Courier", size=12)

    def write_text(self, text):
        self.pdf.write(5, text)
        self.write_endlines(1)

    def write_endlines(self, endlines):
        while(endlines):
            self.pdf.ln()
            endlines -= 1

    def write_image(self, path, x = 0, y = 0, w = 150, h = 100):
        self.pdf.image(path, x=x, w=w, h=h)

    def write_separator(self):
        self.write_endlines(4)
        self.write_text(SEPARATOR)
        self.write_endlines(4)

    def print_pdf(self):
        self.pdf.output('summary.pdf')
