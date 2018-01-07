class Tender:
    price = 0
    number = 0
    company = ""
    date = ""
    description = ""
    link = ""

    def __init__(self):
        self.price = 0

    def __str__(self):
        return str(self.link) + " " + str(self.number) + " " + str(self.date) + " " + str(self.price) + " " + self.company + " " + self.description

    def to_list(self):
        return [self.number, self.link, self.price, self.date, self.description, self.company]