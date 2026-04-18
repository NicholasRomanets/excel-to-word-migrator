import pandas as pd

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
