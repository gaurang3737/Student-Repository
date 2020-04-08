"""
    Homework-9 : Implementing University Data Repository
    This file contains 3 classes 
    1) Student class: class defines necessary information and methods for a single student
    2) Instructor class: class defines necessary information and methods for a single instructor
    3) Repository class: class defines necessary information and methods for creating whole university repository using helps from Student and Instructor classes
"""

from collections import defaultdict
from prettytable import PrettyTable
from typing import Dict,DefaultDict,List,Iterator,Any
from HW08_Gaurang_Patel import file_reader
import os

class Student:
    """"stores every information regarding a single student"""
    PT_FIELD_NAMES = ['CWID','Name','Completed Courses'] #class attribute for student pretty table

    def __init__(self, cwid:str, name:str, major:str)-> None:
        """create instance of a Student class using cwid,name and major argument"""
        self._cwid:str = cwid
        self._name:str = name
        self._major:str = major
        self._courses:Dict[str,str] = dict() #Dictionary for respective courses and grades

    def add_course_grade(self, course:str, grade:str)->None:
        """adding course and grade to the 'courses' dictionary"""
        self._courses[course] = grade

    def info(self) -> List[Any]:
        """return a list of information about a student needed for the pretty table"""
        return [self._cwid,self._name,sorted(self._courses.keys())]


class Instructor:
    """store everything regarding a single Instructor"""
    PT_FIELD_NAMES = ['CWID','Name','Dept','Courses','Students'] #class attribute for instructor pretty table

    def __init__(self, cwid:str, name:str, dept:str) -> None:
        """create instance of a Instructor class using cwid,name and dept argument"""
        self._cwid:str = cwid
        self._name:str = name
        self._dept:str = dept
        self._courses:DefaultDict[str,int] = defaultdict(int) #for counting number of student to courses taught
        
    def store_course_students(self,course:str) -> None:
        """ update the 'courses' and increament the number as the student took that course"""
        self._courses[course] += 1

    def info(self) -> Iterator[List[Any]]:
        """Generator which yields information about a instructor needed for the pretty table"""
        for course,number_of_students in self._courses.items():
            yield [self._cwid, self._name, self._dept, course, number_of_students]

class Repository:
    """store all student, instructors for a university and print pretty tables"""
    def __init__(self,path:str) -> None:
        """storing all students, instructors using appropriate classes and reading students.txt, grade.txt, instructor.txt and generating pretty tables"""
        self._path:str = path #path where all files is stored
        self._students:Dict[str,Student] = dict() #Dict for each instance of Student class
        self._instructors:Dict[str,Instructor] = dict() #Dict for each instance of Instructor class       

        #reading the respective ASCII text files located at give 'path'
        try:
            self._read_students() 
            self._read_instructors()
            self._read_grades()
        except FileNotFoundError as fe:
            print(fe) #Just Print the message
        except ValueError as ve:
            print(ve) #Just print the message
        
        #Generating pretty tables
        self.student_data:List[List[str]] = list() #for testing purpose
        self.instructor_data:List[List[str]] = list() #for testing purpose
        self.student_pretty_table()
        self.instructor_pretty_table()
        
    def _read_students(self) -> None:
        """reading students.txt and updating the 'students' dictionary"""
        for cwid,name,major in file_reader(os.path.join(self._path,"students.txt"),3,sep='\t',header=False):
            self._students[cwid] = Student(cwid,name,major)
    
    def _read_instructors(self) -> None:
        """reading instructors.txt and updating the 'instructors' dictionary"""
        for cwid,name,dept in file_reader(os.path.join(self._path,"instructors.txt"),3,sep='\t',header=False):
            self._instructors[cwid] = Instructor(cwid,name,dept)

    def _read_grades(self) -> None:
        """reading grades.txt and updating respective instances of Student and Instructor class"""
        for student_cwid,course_name,grade,instructor_cwid in \
        file_reader(os.path.join(self._path,"grades.txt"),4,sep='\t',header=False):
            if self._students.get(student_cwid) is None: #Unknown Student
                print(f"Student with CWID = {student_cwid} does not exists!")
            elif self._instructors.get(instructor_cwid) is None: #Unknown Instructor
                print(f"Instructor with CWID = {instructor_cwid} does not exists!")
            else:
                s : Student = self._students[student_cwid]
                s.add_course_grade(course_name,grade)       
                inst: Instructor = self._instructors[instructor_cwid]
                inst.store_course_students(course_name)

    def student_pretty_table(self) -> None:
        """For generating and printing the Student pretty table"""
        s_pt:PrettyTable = PrettyTable(field_names=Student.PT_FIELD_NAMES)
        for student in self._students.values():
            s_pt.add_row(student.info())
            self.student_data.append(student.info())
        print(s_pt)

    def instructor_pretty_table(self) -> None:
        """For generating and printing the Instructor pretty table"""
        ins_pt:PrettyTable = PrettyTable(field_names=Instructor.PT_FIELD_NAMES)
        for instructor in self._instructors.values():
            for row in list(instructor.info()):
                ins_pt.add_row(row)
                self.instructor_data.append(row)
        print(ins_pt)
    
def main() -> None:
    """define two Repositories, one for Stevens and one for NYU"""
    stevens:Repository = Repository(r"C:\Users\user\Desktop\StevensSem4\SSW-810 Python\HW09-Repository\test_lol")
    stevens1:Repository = Repository(r"C:\Users\user\Desktop\StevensSem4\SSW-810 Python\HW09-Repository\test_empty")
    stevens2:Repository = Repository(r"C:\Users\user\Desktop\StevensSem4\SSW-810 Python\HW09-Repository\test_hw9")
    print(stevens2.student_data)
    print(f"\n")
    print(stevens2.instructor_data)


if __name__ == "__main__":
    main() 