import re

from classes import ExcelFile, CSVFile # import classes


def main(): # the main function from which the program starts.
    base = ExcelFile("(closed) base_19.03.2026.xlsx") # We create an instance of the ExcelFile class.
    cols_to_use = [3, 4, 5, 6, 7, 14, 18, 22, 23, 24, 25, 26, 27, 31, 32, 33, 37, 38] # We load only 18 columns instead of over 40.
    base.load_data(cols=cols_to_use) # We refer to the base object and call the load_data function.
    # cols=cols_to_use - we pass our predefined list of column indices into the method using a keyword argument.
    # Inside the method self.data = pd.read_excel(...) is triggered.
    dictionary_tool = CSVFile("(RUS-UKR) Большой русско-украинский словарь.csv", encoding="utf-8") # We create an instance 
    # of the CSVFile class, encoding="utf-8" - explicit is better than implicit (Zen of Python).
    fast_dict = dictionary_tool.load_as_dict() # we call the load_as_dict() method.
    # Inside the method, Pandas reads your 'Большой словарь' as a temporary table.
    # Since you specified header=None, it treats the first row as data, not as column names. 
    # Zip: the program takes two columns and pairs them up. It produces a set of pairs: (word, translation)
    # The pairs are converted into a Dictionary (Hash-map) data structure.
    # Summary: when you need to find a translation later on, the PC doesn't have to scan the entire dictionary 
    # from start to finish. It jumps instantly to the required word using its hash code.
    num_of_cols = len(base.data.columns) # A 'width counter' for the table, which is needed so that 
    # the program knows how many times it needs to 'step' to the right in each row.

    unique_word = set() # we create a set. It automatically removes duplicates. 
    # Even if the word 'Processor' appears 100 times, the set will keep only a single instance.
    for index, row in base.data.iterrows(): # The loop iterates through the table row by row.
        for i in range(num_of_cols): # Inside every row, the program accesses every cell of the selected columns.
            cell_value = str(row.iloc[i]).strip()
            # We take the entire content of the current row and access a specific column by its index.
            # The str() function forces it: 'I don't care what was there, now it's a string (text).
            # For example, the number 123 becomes the string '123'.
            # .strip() removes all whitespaces, tabs, and line breaks at the begging and the end of the word.
            if not cell_value or cell_value.lower() == 'nan':
                continue
            # We skip the empty cells.
            elif not re.search(r'[a-zA-Zа-яА-ЯёЁіІїЇєЄ]', cell_value):
                continue
            # We skip the cells that don't contain any letters (for example, if there are only numbers 12345 or symbols +++).
            words_in_cell = cell_value.split() # We split the current cell into individual words by spaces.

            for word in words_in_cell:
                if len(word) <= 3:
                    continue # We discard short words, such as conjuctions and prepositions like 'and', 'on' or 'in'.
                clean_word = word.strip('.,!?;:"()') # We remove punctuation marks around the word.
                if any(c.isalpha() for c in clean_word): # Check if any letters remain in the "cleaned" word, 
                    # in case the word consisted only of symbols.
                    print(clean_word)
                    unique_word.add(clean_word) # We add the 'cleaned' word to our set of unique words (to the list).
    print(len(unique_word))


if __name__ == '__main__': main()
