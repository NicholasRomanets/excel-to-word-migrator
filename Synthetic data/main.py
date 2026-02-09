import csv

with open('Основа для РОТ(БАЗА)_11.01.2026.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        print(row)

