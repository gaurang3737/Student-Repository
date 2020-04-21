from flask import Flask, render_template
from typing import List,Dict
import sqlite3

DB_FILE:str = r"C:\Users\user\Desktop\StevensSem4\SSW-810 Python\HW12-Flask\hw11.db"

app:Flask = Flask(__name__)

@app.route('/hw12')
def student_summary() -> str:
    """Generating Studenr Grade Summary on Flask"""   
    try:
        db:sqlite3.Connection = sqlite3.connect(DB_FILE)
    except sqlite3.OperationalError as e:
        raise sqlite3.OperationalError(e)
    else:
        try:
            query:str = """select s.Name,s.CWID,g.Course,g.Grade,i.Name
            from grades g join students s on g.StudentCWID = s.CWID
            join instructors i on g.InstructorCWID = i.CWID
            order by s.Name
            """
            data:List[Dict[str,str]] = \
                [{'cwid':cwid,'name':name,'course':course,'grade':grade,'ins':instructor} \
            for cwid,name,course,grade,instructor in db.execute(query) ]
        except sqlite3.OperationalError as e:
            raise sqlite3.OperationalError(e)

    db.close()

    return render_template('hw12_table.html',title='Stevens Repository',table_title='Student Grade Summary',students = data)

app.run(debug=True)