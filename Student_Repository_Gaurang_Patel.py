"""
    Homework-11 : Modifying Homework-10 with new functionalities
    1) Added Database functionality to create Grade Summary
    2) Added new pretty table for Grade Summary
"""

from collections import defaultdict
from prettytable import PrettyTable
from typing import Dict,DefaultDict,List,Iterator,Any,Tuple
from HW08_Gaurang_Patel import file_reader
import os
import sqlite3


class Major:
    """stores information about majors"""
    PT_FIELD_NAMES:List[str] = ['Major','Required Courses','Electives'] #class attribute for major pretty table

    def __init__(self,major:str) -> None:
        """stores individual major with its required and elective courses in a dictionary"""
        self._major = major
        self._courses:DefaultDict[str,List[str]] = defaultdict(list) #courses['R'] = ['SSW810','SSW510']

    def add_course(self,category:str,course_name:str)-> None:
        """update the courses dictionary to add required and elective courses"""
        self._courses[category].append(course_name)

    def info(self) -> Tuple[str,List[str],List[str]]:
        """return tuple of information needed for major pretty table"""
        return self._major,sorted(self._courses['R']),sorted(self._courses['E'])

    def get_required(self) -> List[str]:
        """return copy of required courses for each student"""
        return list(self._courses['R'])

    def get_electives(self) -> List[str]:
        """return copy of elective courses for each student"""
        return list(self._courses['E'])


class Student:
    """"stores every information regarding a single student"""
    PT_FIELD_NAMES:List[str] = ['CWID','Name','Major','Completed Courses','Remaining Required','Remaining Electives','GPA'] #class attribute for student pretty table    
    
    SCORES:Dict[str,float] = {'A':4.0,'A-':3.75,'B+':3.25,'B':3.0,'B-':2.75,'C+':2.25,'C':2.0,'C-':0,'D+':0,'D':0,'D-':0,'F':0} #to convert grades into score

    def __init__(self, cwid:str, name:str, major:str, required:List[str], electives:List[str])-> None:
        """create instance of a Student class using cwid,name and major argument"""
        self._cwid:str = cwid
        self._name:str = name
        self._major:str = major
        self._courses:Dict[str,str] = dict() #courses['CS510'] = 'A'
        self._remaining_required:List[str] = required
        self._remaining_electives:List[str] = electives
        self._gpa:float = 0.0
        self._all_courses:Dict[str,str] = dict() #all_courses['SSW810'] = 'F' needed for GPA calculation

    def add_course_grade(self, course:str, grade:str)->None:
        """adding course and grade to the respective dictionary and calculating GPA"""
        
        #keep track of all courses taken by student
        self._all_courses[course] = grade

        #Tracking remaining required and electives only if student passed the course
        if grade in ['A','A-','B+','B','B-','C+','C',]:
            self._courses[course] = grade
            if course in self._remaining_required:
                self._remaining_required.remove(course)
            elif course in self._remaining_electives:
                self._remaining_electives = list() #empty list

        #Calculating GPA
        if len(self._courses.values()) > 0 :
            self._gpa = sum([Student.SCORES[grade] for grade in self._all_courses.values()])/len(self._all_courses.values())

    def info(self) -> Tuple[str,str,str,List[str],List[str],List[str],float]:
        """return a tuple with information about a student needed for the pretty table"""
        return self._cwid,self._name,self._major,sorted(self._courses.keys()),sorted(self._remaining_required),sorted(self._remaining_electives),round(self._gpa,2)


class Instructor:
    """store everything regarding a single Instructor"""
    PT_FIELD_NAMES:List[str] = ['CWID','Name','Dept','Courses','Students'] #class attribute for instructor pretty table

    def __init__(self, cwid:str, name:str, dept:str) -> None:
        """create instance of a Instructor class using cwid,name and dept argument"""
        self._cwid:str = cwid
        self._name:str = name
        self._dept:str = dept
        self._courses:DefaultDict[str,int] = defaultdict(int) #courses['SSW810'] = 2

    def store_course_students(self,course:str) -> None:
        """ update the 'courses' and increament the number as the student took that course"""
        self._courses[course] += 1

    def info(self) -> Iterator[Tuple[str,str,str,str,int]]:
        """Generator which yields information about a instructor needed for the pretty table"""
        for course,number_of_students in self._courses.items():
            yield (self._cwid, self._name, self._dept, course, number_of_students)


class Repository:
    """store all student, instructors for a university and print pretty tables"""
    
    def __init__(self,path:str,flag=False) -> None:
        """storing all students, instructors using appropriate classes and reading students.txt, grade.txt, instructor.txt and generating pretty tables"""
        self._path:str = path #path where all files is stored
        self._students:Dict[str,Student] = dict() #students['12345'] = Student()
        self._instructors:Dict[str,Instructor] = dict() #instructiors['96654'] = Instructor()
        self._majors:Dict[str,Major] = dict() #majors['SYEN'] = Major()

        #reading the respective ASCII text files located at give 'path'
        try:
            self._read_majors()
            self._read_students() 
            self._read_instructors()
            self._read_grades()
                
            #for testing purpose
            self.student_data:List[Tuple[str,str,str,List[str],List[str],List[str],float]] = list() 
            self.instructor_data:List[Tuple[str,str,str,str,int]] = list() 
            self.major_data:List[Tuple[str,List[str],List[str]]] = list()
            self.grade_summary_data:List[Tuple[str,str,str,str,str]] = list() 

            #Generating pretty tables
            self._major_pt:PrettyTable = self.major_pretty_table()
            self._s_pt:PrettyTable = self.student_pretty_table()
            self._ins_pt:PrettyTable = self.instructor_pretty_table()
            self._gs_pt:PrettyTable = self.grade_summary_pretty_table()

            #Print the pretty tables only if required
            if flag:
                print(f"\nMajor Summary")
                print(self._major_pt)
                print(f"\nStudent Summary")
                print(self._s_pt)
                print(f"\nInstructor Summary")
                print(self._ins_pt)
                print(f"\nStudent Grade Summary")
                print(self._gs_pt)

        except FileNotFoundError as fe:
            print(fe) #Just Print the message
        except ValueError as ve:
            print(ve) #Just print the message


    def _grade_summary(self) -> Iterator[Tuple[str,str,str,str,str]]:
        """Generator for reading data from database located at given path"""
        try:
            db:sqlite3.Connection = sqlite3.connect(os.path.join(self._path,"hw11.db"))
        except sqlite3.OperationalError as e:
                print(e)
        else:
            try:
                query:str = """select s.Name,s.CWID,g.Course,g.Grade,i.Name
                            from grades g join students s on g.StudentCWID = s.CWID
                            join instructors i on g.InstructorCWID = i.CWID
                            order by s.Name
                            """
                for tup in db.execute(query):
                    yield tup
            except sqlite3.OperationalError as e:
                print(e)

    def _read_majors(self) -> None:
        """reading major.txt and updating the 'majors' dictionary"""
        for major,category,course_name in file_reader(os.path.join(self._path,"majors.txt"),3,sep='\t',header=True):
            if self._majors.get(major) is None: #New Major Found
                self._majors[major] = Major(major)
            self._majors[major].add_course(category,course_name)

    def _read_students(self) -> None:
        """reading students.txt and updating the 'students' dictionary"""
        for cwid,name,major in file_reader(os.path.join(self._path,"students.txt"),3,sep='\t',header=True):
            if self._majors.get(major) is None:#Student with major not found in major.txt
                self._students[cwid] = Student(cwid,name,major,[],[])
            else:
                self._students[cwid] = Student(cwid,name,major,self._majors[major].get_required(),self._majors[major].get_electives())

    def _read_instructors(self) -> None:
        """reading instructors.txt and updating the 'instructors' dictionary"""
        for cwid,name,dept in file_reader(os.path.join(self._path,"instructors.txt"),3,sep='\t',header=True):
            self._instructors[cwid] = Instructor(cwid,name,dept)

    def _read_grades(self) -> None:
        """reading grades.txt and updating respective instances of Student and Instructor class"""
        for student_cwid,course_name,grade,instructor_cwid in \
        file_reader(os.path.join(self._path,"grades.txt"),4,sep='\t',header=True):
            if self._students.get(student_cwid) is None: #Unknown Student
                print(f"Student with CWID = {student_cwid} does not exists!")
            elif self._instructors.get(instructor_cwid) is None: #Unknown Instructor
                print(f"Instructor with CWID = {instructor_cwid} does not exists!")
            else:
                s : Student = self._students[student_cwid]
                s.add_course_grade(course_name,grade)       
                inst: Instructor = self._instructors[instructor_cwid]
                inst.store_course_students(course_name)

    def student_pretty_table(self) -> PrettyTable:
        """For generating the Student pretty table"""
        s_pt:PrettyTable = PrettyTable(field_names=Student.PT_FIELD_NAMES)
        for student in self._students.values():
            s_pt.add_row(student.info())
            self.student_data.append(student.info())
        return s_pt

    def instructor_pretty_table(self) -> PrettyTable:
        """For generating the Instructor pretty table"""
        ins_pt:PrettyTable = PrettyTable(field_names=Instructor.PT_FIELD_NAMES)
        for instructor in self._instructors.values():
            for row in list(instructor.info()):
                ins_pt.add_row(row)
                self.instructor_data.append(row)
        return ins_pt

    def major_pretty_table(self) -> PrettyTable:
        """For generating Major pretty table"""
        major_pt:PrettyTable = PrettyTable(field_names=Major.PT_FIELD_NAMES)
        for major in self._majors.values():
            major_pt.add_row(major.info())
            self.major_data.append(major.info())
        return major_pt

    def grade_summary_pretty_table(self) -> PrettyTable:
        """For generating grade summary pretty table"""
        gs_pt:PrettyTable = PrettyTable(field_names=['Name','CWID','Course','Grade','Instructor'])
        for row in list(self._grade_summary()):
            gs_pt.add_row(row)
            self.grade_summary_data.append(row)
        return gs_pt


def main() -> None:
    """define two Repositories, one for Stevens and one for NYU"""
    stevens:Repository = Repository(r"C:\Users\user\Desktop\StevensSem4\SSW-810 Python\HW11-Repository\test_hw11",True)  

if __name__ == "__main__":
    main() 
