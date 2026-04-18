import re

from classes import ExcelFile, CSVFile

def main():
    base = ExcelFile("(closed) base_19.03.2026.xlsx")
    cols_to_use = [3, 4, 5, 6, 7, 14, 18, 22, 23, 24, 25, 26, 27, 31, 32, 33, 37, 38]
    base.load_data(cols=cols_to_use)
    dictionary_tool = CSVFile("(RUS-UKR) Большой русско-украинский словарь.csv", encoding="utf-8")
    fast_dict = dictionary_tool.load_as_dict()
    num_of_cols = len(base.data.columns)

    unique_word = set()
    for index, row in base.data.iterrows():
        for i in range(num_of_cols):
            cell_value = str(row.iloc[i]).strip()
            if not cell_value or cell_value.lower() == 'nan':
                continue
            elif not re.search(r'[a-zA-Zа-яА-ЯёЁіІїЇєЄ]', cell_value):
                continue
            words_in_cell = cell_value.split()

            for word in words_in_cell:
                if len(word) <= 3:
                    continue
                clean_word = word.strip('.,!?;:"()')
                if any(c.isalpha() for c in clean_word):
                    print(clean_word)
                    unique_word.add(clean_word)
    print(len(unique_word))


if __name__ == '__main__': main()
