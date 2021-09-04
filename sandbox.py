# A file to experiment with stuff in the Python language

import csv

input_filename = "Squadron_semicolons.csv"

#https://docs.python.org/3/library/csv.html#csv.DictReader
with open(input_filename, newline='') as csvfile:
    dialect = csv.Sniffer().sniff(csvfile.read())
    csvfile.seek(0)
    datareader = csv.DictReader(csvfile, dialect=dialect)
    for row in datareader:
        print(row)


