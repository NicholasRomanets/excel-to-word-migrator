from glob import translate

from re import sub as sub
import pandas as pd
from numpy.f2py.crackfortran import word_pattern
from numpy.ma.extras import row_stack

#df = pd.read_excel("(closed) base_19.03.2026.xlsx", dtype=str, sheet_name="БАЗА", usecols=[3,4,5,6,7,14,18,22,23,24,25,26,27,31,32,33,37,38])
#df = pd.read_csv("(RUS-UKR) Большой русско-украинский словарь.csv", skiprows=5, usecols=[1])

def main():
    result = find_word_in_dictionary("абзацний")
    if result:
        print("Результат:", result)
    else:
        print("Слово не знайдено")


def find_word_in_dictionary(target_word='абзацний'):
    found = None

    for chunk in pd.read_csv(
        "(RUS-UKR) Большой русско-украинский словарь.csv",
        header=None,              # якщо немає заголовка
        chunksize=1000,
        encoding="utf-8",
        dtype=str
    ):
        mask = chunk.iloc[:, 1].astype(str).str.contains(target_word, na=False, case=False)
        if mask.any():
            found = chunk.loc[mask, 0].iloc[0]
            print(f"Знайдено: {found}")
    return found


if __name__=='__main__':
    main()