"""
    Homework-10 : Testing of various classes and functions defined in the filename called 'HW10_Gaurang_Patel.py'
    This program uses the python's 'unittest' to support creation of different test cases for the various functions and classes defined in the file mentioned above. 
"""

import unittest
from HW10_Gaurang_Patel import Repository
from typing import List,Tuple

class RepositoryTest(unittest.TestCase):
    """Test class for 'Repository' class"""
    
    def test_student_data(self) -> None:
        """Test case for student data printed on pretty table"""
        stevens:Repository = Repository(r"C:\Users\user\Desktop\StevensSem4\SSW-810 Python\HW10-Repository\test_hw10")  
        expected:List[Tuple[str,str,str,List[str],List[str],List[str],float]] = [('10103', 'Baldwin, C', 'SFEN', ['CS 501', 'SSW 564', 'SSW 567', 'SSW 687'], ['SSW 540', 'SSW 555'], [], 3.44), ('10115', 'Wyatt, X', 'SFEN', ['CS 545', 'SSW 564', 'SSW 567', 'SSW 687'], ['SSW 540', 'SSW 555'], [], 3.81), ('10172', 'Forbes, I', 'SFEN', ['SSW 555', 'SSW 567'], ['SSW 540', 'SSW 564'], ['CS 501', 'CS 513', 'CS 545'], 3.88), ('10175', 'Erickson, D', 'SFEN', ['SSW 564', 'SSW 567', 'SSW 687'], ['SSW 540', 'SSW 555'], ['CS 501', 'CS 513', 'CS 545'], 3.58), ('10183', 'Chapman, O', 'SFEN', ['SSW 689'], ['SSW 540', 'SSW 555', 'SSW 564', 'SSW 567'], ['CS 501', 'CS 513', 'CS 545'], 4.0), ('11399', 'Cordova, I', 'SYEN', ['SSW 540'], ['SYS 612', 'SYS 671', 'SYS 800'], [], 3.0), ('11461', 'Wright, U', 'SYEN', ['SYS 611', 'SYS 750', 'SYS 800'], ['SYS 612', 'SYS 671'], ['SSW 540', 'SSW 565', 'SSW 810'], 3.92), ('11658', 'Kelly, P', 'SYEN', [], ['SYS 612', 'SYS 671', 'SYS 800'], ['SSW 540', 'SSW 565', 'SSW 810'], 0.0), ('11714', 'Morton, A', 'SYEN', ['SYS 611', 'SYS 645'], ['SYS 612', 'SYS 671', 'SYS 800'], ['SSW 540', 'SSW 565', 'SSW 810'], 3.0), ('11788', 'Fuller, E', 'SYEN', ['SSW 540'], ['SYS 612', 'SYS 671', 'SYS 800'], [], 4.0)]

        self.assertEqual(expected,stevens.student_data)

    def test_instructor_data(self) -> None:
        """Test case for instructor data printed on pretty table"""
        stevens:Repository = Repository(r"C:\Users\user\Desktop\StevensSem4\SSW-810 Python\HW10-Repository\test_hw10")
        expected:List[Tuple[str,str,str,str,int]] = [('98765', 'Einstein, A', 'SFEN', 'SSW 567', 4), ('98765', 'Einstein, A', 'SFEN', 'SSW 540', 3), ('98764', 'Feynman, R', 'SFEN', 'SSW 564', 3), ('98764', 'Feynman, R', 'SFEN', 'SSW 687', 3), ('98764', 'Feynman, R', 'SFEN', 'CS 501', 1), ('98764', 'Feynman, R', 'SFEN', 'CS 545', 1), ('98763', 'Newton, I', 'SFEN', 'SSW 555', 1), ('98763', 'Newton, I', 'SFEN', 'SSW 689', 1), ('98760', 'Darwin, C', 'SYEN', 'SYS 800', 1), ('98760', 'Darwin, C', 'SYEN', 'SYS 750', 1), ('98760', 'Darwin, C', 'SYEN', 'SYS 611', 2), ('98760', 'Darwin, C', 'SYEN', 'SYS 645', 1)]

        self.assertEqual(expected,stevens.instructor_data)

    def test_major_data(self) -> None:
        """Test case for major data printed on pretty table"""
        stevens:Repository = Repository(r"C:\Users\user\Desktop\StevensSem4\SSW-810 Python\HW10-Repository\test_hw10")
        expected:List[Tuple[str,List[str],List[str]]] = [('SFEN', ['SSW 540', 'SSW 555', 'SSW 564', 'SSW 567'], ['CS 501', 'CS 513', 'CS 545']), ('SYEN', ['SYS 612', 'SYS 671', 'SYS 800'], ['SSW 540', 'SSW 565', 'SSW 810'])]

        self.assertEqual(expected,stevens.major_data)

    def test_empty_files(self) -> None:
        """Test case for empty data"""
        stevens:Repository = Repository(r"C:\Users\user\Desktop\StevensSem4\SSW-810 Python\HW10-Repository\test_empty")
        self.assertEqual([],stevens.instructor_data)
        self.assertEqual([],stevens.student_data)
        self.assertEqual([],stevens.major_data)
        

if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
