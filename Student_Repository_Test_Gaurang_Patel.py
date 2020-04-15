"""
    Homework-11 : Testing of various classes and functions defined in the filename called 'HW11_Gaurang_Patel.py'
    This program uses the python's 'unittest' to support creation of different test cases for the various functions and classes defined in the file mentioned above. 
"""

import unittest
from HW11_Gaurang_Patel import Repository
from typing import List,Tuple

class RepositoryTest(unittest.TestCase):
    """Test class for 'Repository' class"""
    
    def test_data(self) -> None:
        """Test case for HW-11 data printed on pretty tables"""
        
        stevens:Repository = Repository(r"C:\Users\user\Desktop\StevensSem4\SSW-810 Python\HW11-Repository\test_hw11")  
        
        expected_student:List[Tuple[str,str,str,List[str],List[str],List[str],float]] = [('10103', 'Jobs, S', 'SFEN', ['CS 501', 'SSW 810'], ['SSW 540', 'SSW 555'], [], 3.38), ('10115', 'Bezos, J', 'SFEN', ['SSW 810'], ['SSW 540', 'SSW 555'], ['CS 501', 'CS 546'], 2.0), ('10183', 'Musk, E', 'SFEN', ['SSW 555', 'SSW 810'], ['SSW 540'], ['CS 501', 'CS 546'], 4.0), ('11714', 'Gates, B', 'CS', ['CS 546', 'CS 570', 'SSW 810'], [], [], 3.5)]

        expected_ins:List[Tuple[str,str,str,str,int]] = [('98764', 'Cohen, R', 'SFEN', 'CS 546', 1), ('98763', 'Rowland, J', 'SFEN', 'SSW 810', 4), ('98763', 'Rowland, J', 'SFEN', 'SSW 555', 1), ('98762', 'Hawking, S', 'CS', 'CS 501', 1), ('98762', 'Hawking, S', 'CS', 'CS 546', 1), ('98762', 'Hawking, S', 'CS', 'CS 570', 1)]

        expected_major:List[Tuple[str,List[str],List[str]]] = [('SFEN', ['SSW 540', 'SSW 555', 'SSW 810'], ['CS 501', 'CS 546']), ('CS', ['CS 546', 'CS 570'], ['SSW 565', 'SSW 810'])]

        expected_gs:List[Tuple[str,str,str,str,str]] = [('Bezos, J', '10115', 'SSW 810', 'A', 'Rowland, J'), ('Bezos, J', '10115', 'CS 546', 'F', 'Hawking, S'), ('Gates, B', '11714', 'SSW 810', 'B-', 'Rowland, J'), ('Gates, B', '11714', 'CS 546', 'A', 'Cohen, R'), ('Gates, B', '11714', 'CS 570', 'A-', 'Hawking, S'), ('Jobs, S', '10103', 'SSW 810', 'A-', 'Rowland, J'), ('Jobs, S', '10103', 'CS 501', 'B', 'Hawking, S'), ('Musk, E', '10183', 'SSW 555', 'A', 'Rowland, J'), ('Musk, E', '10183', 'SSW 810', 'A', 'Rowland, J')]

        self.assertEqual(expected_student,stevens.student_data)
        self.assertEqual(expected_ins,stevens.instructor_data)
        self.assertEqual(expected_major,stevens.major_data)
        self.assertEqual(expected_gs,stevens.grade_summary_data)
        

if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
