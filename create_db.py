import sys
import sqlite3
import os

def main(args):
    input_file_name = args[1]
    database_name = 'schedule.db'
    is_data_base_exist = os.path.isfile(database_name)
    dbcon = sqlite3.connect(database_name)
    sep_pos = -len(os.linesep)

    with dbcon:
        #idk we copied it from the PS !!
        cursor = dbcon.cursor()

        #checks if the file isn't exist ! , because you know ! who cares !
        if not is_data_base_exist:
            cursor.execute("""
                CREATE TABLE courses(
                    id INTEGER PRIMARY KEY,
                    course_name TEXT NOT NULL,
                    student TEXT NOT NULL,
                    number_of_students INTEGER NOT NULL,
                    class_id INTEGER REFERENCES classrooms(id),
                    course_length INTEGER NOT NULL)""")# create courses
            cursor.execute("""
                CREATE TABLE students(
                    grade TEXT PRIMARY KEY,
                    count INTEGER NOT NULL)""")# create students
            cursor.execute("""
                CREATE TABLE classrooms(
                    id INTEGER PRIMARY KEY,
                    location TEXT NOT NULL,
                    current_course_id INTEGER NOT NULL,
                    current_course_time_left INTEGER NOT NULL)""")#create classrooms

        with open(input_file_name) as input_file:
            for line in input_file:
                if line[sep_pos:] == os.linesep:
                    line = line[:sep_pos]

                #split that ',' , is that ok ?
                data  = line.split(', ')
                
                if data[0] == "S":
                    cursor.execute("INSERT INTO students VALUES(?,?)", (data[1], data[2],))
                elif data[0] == "C":
                    cursor.execute("INSERT INTO courses VALUES(?,?,?,?,?,?)", (data[1], data[2],data[3],data[4],data[5],data[6],))
                elif data[0] == "R":
                    cursor.execute("INSERT INTO classrooms VALUES(?,?,?,?)", (data[1], data[2],0,0,))
        
        
        print_table_as_tuple(cursor, "courses")
        print_table_as_tuple(cursor, "classrooms")
        print_table_as_tuple(cursor, "students")

def print_table_as_tuple(cursor, table_name):
    print(table_name)
    cursor.execute("SELECT * FROM " + table_name)
    rows = cursor.fetchall()
    # rows_as_tuple = [tuple(row) for row in rows]
    print_table(rows)

def print_table(list_of_tuples):
    for item in list_of_tuples:
        print(item)

if __name__ == '__main__':
    main(sys.argv)