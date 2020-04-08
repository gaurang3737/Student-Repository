"""
    Homework-9 : Testing of various classes and functions defined in the filename called 'HW09_Gaurang_Patel.py'
    This program uses the python's 'unittest' to support creation of different test cases for the various functions and classes defined in the file mentioned above. 
"""

import unittest
from HW09_Gaurang_Patel import Repository
from typing import List

class RepositoryTest(unittest.TestCase):
    """Test class for 'Repository' class"""
    
    def test_student_data(self) -> None:
        """Test case for student data printed on pretty table"""
        stevens:Repository = Repository(r"C:\Users\user\Desktop\StevensSem4\SSW-810 Python\HW09-Repository\test_hw9")
        expected:List[List[str]] = [['10103', 'Baldwin, C', ['CS 501', 'SSW 564', 'SSW 567', 'SSW 687']], ['10115', 'Wyatt, X', ['CS 545', 'SSW 564', 'SSW 567', 'SSW 687']], ['10172', 'Forbes, I', ['SSW 555', 'SSW 567']], ['10175', 'Erickson, D', ['SSW 564', 'SSW 567', 'SSW 687']], ['10183', 'Chapman, O', ['SSW 689']], ['11399', 'Cordova, I', ['SSW 540']], ['11461', 'Wright, U', ['SYS 611', 'SYS 750', 'SYS 800']], ['11658', 'Kelly, P', ['SSW 540']], ['11714', 'Morton, A', ['SYS 611', 'SYS 645']], ['11788', 'Fuller, E', ['SSW 540']]]

        self.assertEqual(expected,stevens.student_data)

    def test_instructor_data(self) -> None:
        """Test case for instructor data printed on pretty table"""
        stevens:Repository = Repository(r"C:\Users\user\Desktop\StevensSem4\SSW-810 Python\HW09-Repository\test_hw9")
        expected:List[List[str]] = [['98765', 'Einstein, A', 'SFEN', 'SSW 567', 4], ['98765', 'Einstein, A', 'SFEN', 'SSW 540', 3], ['98764', 'Feynman, R', 'SFEN', 'SSW 564', 3], ['98764', 'Feynman, R', 'SFEN', 'SSW 687', 3], ['98764', 'Feynman, R', 'SFEN', 'CS 501', 1], ['98764', 'Feynman, R', 'SFEN', 'CS 545', 1], ['98763', 'Newton, I', 'SFEN', 'SSW 555', 1], ['98763', 'Newton, I', 'SFEN', 'SSW 689', 1], ['98760', 'Darwin, C', 'SYEN', 'SYS 800', 1], ['98760', 'Darwin, C', 'SYEN', 'SYS 750', 1], ['98760', 'Darwin, C', 'SYEN', 'SYS 611', 2], ['98760', 'Darwin, C', 'SYEN', 'SYS 645', 1]]

        self.assertEqual(expected,stevens.instructor_data)
    
    def test_empty_files(self) -> None:
        """Test case for empty data"""
        stevens:Repository = Repository(r"C:\Users\user\Desktop\StevensSem4\SSW-810 Python\HW09-Repository\test_empty")
        self.assertEqual([],stevens.instructor_data)
        self.assertEqual([],stevens.student_data)
        

if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)