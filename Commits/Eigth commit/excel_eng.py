import pandas as pd
import re

class File: # Create a superclass called File
    def __init__(self, file_path, header=False, dtype=str, encoding="utf-8"):
    # The __init__ constructor is a method of the File object. self is reference to a specific instance of the object that was just created
    # self allows methods inside the class to communicate with each other. without self, the data received in __init__ would be lost immidiately after exiting the function.
    # self.file_path: It stores the file path.
    # self.header: A Bolean value that indicates if the first row contains column headers.
    # self.dtype: Sets the excepted data type (str by default). This is sensible because when working with text/dictionaries, 
    # it's better to have data in string format than to unexpectedly get numbers. Nothing is being converted yet; it’s just an instruction.
    # self.data = None: This is a placeholder for data. We leave it as None because the data is not loaded yet.
    # It's a very sensible approach: first, we set up the object, then we load the data.
    # Lazy loading. We save PC memory by not filling it with data the instant we create the instance.
    # self.encoding: This is crucial for Cyrillic. Setting 'utf-8' by default prevents 'UnicodeDecodeError' errors,
    # which often occur when a program cannot read Ukr chars.
        self.header = header # Are there headers in the Excel/CSV file?
        self.dtype = dtype
        self.file_path = file_path
        self.data = None
        self.encoding = encoding # Protection against Cyrillic reading errors (UTF-8)
        # The process of initializing attributes
        # If we remove self, then the variables file_path, header, dtype, and encoding will be local.
        # They will be destroyed without self as soon as the __init__ function finishes execution.

class ExcelFile(File):
    # The ExcelFile class now inherits from the File class(path, encoding, data type), but it has its own 
    # unique property - reading Excel files specially.
    def load_data (self, cols=None): 
    # In OOP, self is a link. Since load_data is a class method, it must have access to the data we stored earlier 
    # in the __init__ constructor. Without self, the load_data method would not know which specific file to open.
    # It says: Take self.file_path, which we recorded in this obect's passport earlier'. 
    # None - makes the argument optional, if we call load_data, all columns will be loaded.
        with pd.ExcelFile(self.file_path) as reader: # It establishes a connection to the file on the disk.
            # As soon as the code inside the with block finishes, Python automatically releases the file.
            self.data = pd.read_excel(reader, usecols=cols, dtype=self.dtype, sheet_name='БАЗА').fillna('')
            # The .fillna('') method - when an Excel cell is empty, Pandas writes a special value NaN (Not a Number), 
            # Because of this, you cannot execute .split() or .lower(), and the program will crash. 
            # .fillna('') finds all missing values and replaces them with an empty string.
            # Now the loops will work stably.
            # self.data - we store the entire processed table in the object's memory. Now, in any other place 
            # in the program, we can access self.data.
        print(f"Excel-базу завантажено з файлу {self.file_path}")


class CSVFile(File): # A class for handling CSV files.
    def load_as_dict (self, key_col=0, val_col=1):
    # key_col=0: The first column (index 0) will be the keys (e.g., original language words), 
    # val_col=1: The second column (index 1) will be the values (translations).
        df_dict = pd.read_csv( # Reading via pd.read_csv
            self.file_path, encoding=self.encoding, dtype=self.dtype, header=None,
            #encoding=self.encoding: It uses 'utf-8' to read Cyrillic correctly.
			#dtype=self.dtype: It reads everything as strings (str).
			#header=None: We specify that there is no row with column headers in your CSV dictionary, 
            # the data begins straight from the first row.
        )
        return dict(zip(df_dict[key_col], df_dict[val_col])) # it immediately converts the table into a Python dictionary.


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
