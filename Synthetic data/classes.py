import pandas as pd

class File:
    def __init__(self, file_path, header=False, dtype=str, encoding="utf-8"):
        self.header = header
        self.dtype = dtype
        self.file_path = file_path
        self.data = None
        self.encoding = encoding

class ExcelFile(File):
    def load_data (self, cols=None):
        with pd.ExcelFile(self.file_path) as reader:
            self.data = pd.read_excel(reader, usecols=cols, dtype=self.dtype, sheet_name='БАЗА').fillna('')
        print(f"Excel-базу завантажено з файлу {self.file_path}")


class CSVFile(File):
    def load_as_dict (self, key_col=0, val_col=1):
        df_dict = pd.read_csv(
            self.file_path, encoding=self.encoding, dtype=self.dtype, header=None,
        )
        return dict(zip(df_dict[key_col], df_dict[val_col]))