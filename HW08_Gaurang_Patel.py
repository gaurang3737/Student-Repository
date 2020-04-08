"""
    Homework-8 : Date Arithmetics, File Reader and File Analyzer
    This file contains 2 functions and 1 class
    1) date_arithmetic() : does date arithmetics and return a tuple
    2) file_reader(path,fields,sep,header): creates a generator which yields tokens on each line of file provided by path
    3) FileAnalyzer class: analyzing each '.py' file (python files) in the provided directory path and printing them using pretty table module
"""

from datetime import datetime,timedelta
from typing import Tuple,List,Iterator,Dict,IO
from prettytable import PrettyTable
import os

#Part-1
def date_arithmetic() -> Tuple[datetime,datetime,int]:
    """Using date arithmetics returns a tuple with the answers of the questions"""
    three_days_after_02272020: datetime = datetime(2020, 2, 27) + timedelta(days=3)
    three_days_after_02272019: datetime = datetime(2019, 2, 27) + timedelta(days=3)
    days_passed_02012019_09302019: timedelta = datetime(2019, 9, 30) - datetime(2019, 2, 1)

    return three_days_after_02272020,three_days_after_02272019,days_passed_02012019_09302019.days

#Part-2
def file_reader(path:str, fields:int, sep:str = ",", header:bool = False) -> Iterator[List[str]]:
    """Creates a generator which yields the expected fields depending upon the arguments passed"""
    try:
        fp:IO = open(path, 'r')
    except FileNotFoundError:
        raise FileNotFoundError(f"Can not open file named:{path}")
    else:
        with fp:
            for line_number,line_content in enumerate(fp): #line_number starts from 0
                line_content = line_content.rstrip("\n")
                tokens:List[str] = line_content.split(sep)
                if len(tokens) != fields:
                    raise ValueError(f"{path} has {len(tokens)} fields on line:{line_number+1} but expected {fields} fields")
                else:
                    if header:
                        header = False #to skip header line but include rest of lines
                    else:
                        yield tokens 

#Part3
class FileAnalyzer:
    """The FileAnalyzer class for analyzing each '.py' files(python files) in the provided directory path and printing them using pretty table module"""
    
    def __init__(self,directory:str) -> None:
        """Storing the provided path of directory and initializing and empty dictionary for file summary"""
        self.directory:str = directory
        self.files_summary:Dict[str,Dict[str,int]] = dict()
        self.analyze_files() #summarizing python files data
        
    def analyze_files(self) -> None:
        """Populating the file summary with file data for each python files residing at provided directory path"""
        try:
            files = os.listdir(self.directory)
        except FileNotFoundError:
            raise FileNotFoundError(f"{self.directory} not exists! Please provide a valid directory!")
        else:
            for file in files:
                if file.endswith(".py"):
                    self.file_stats(os.path.join(self.directory,file))  
  
    def file_stats(self,full_path:str) -> None:
        """Calculating file data for a single file residing at provided full_path"""
        #Initializing file data variables for that one file
        self.files_summary[full_path] = {}
        total_class:int = 0
        total_chars:int = 0
        total_functions:int = 0
        total_lines:int = 0

        try:
            fp:IO = open(full_path, 'r')
        except FileNotFoundError:
            raise FileNotFoundError(f"Can not open file at:{full_path}")
        else:
            with fp:
                for line in fp:
                    if line.startswith("class "):
                        total_class += 1
                    elif line.lstrip().startswith("def "):
                        total_functions += 1
                    total_lines += 1
                    total_chars += len(line)
                    
        #Populating file summary   
        self.files_summary[full_path]['class'] = total_class
        self.files_summary[full_path]['function'] = total_functions
        self.files_summary[full_path]['line'] = total_lines
        self.files_summary[full_path]['char'] = total_chars

    def pretty_print(self) -> None:
        """Printing the file summary using python's pretty_table module"""
        pt: PrettyTable = PrettyTable(field_names=['File Name','classes','functions','lines','chars'])

        for file_name,stats in self.files_summary.items():
            pt.add_row([file_name,stats['class'],stats['function'],stats['line'],stats['char']])

        print(f"Summary for {self.directory}")
        print(pt)