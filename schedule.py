import sys
import sqlite3
import os

database_name = 'schedule.db'

def main():
    is_data_base_exist = os.path.isfile(database_name)
    counter = 0

    while is_data_base_exist :
        dbcon = sqlite3.connect(database_name)

        with dbcon :
            cursor = dbcon.cursor()
            cursor.execute("SELECT * FROM classrooms")
            avaliable_class_rooms = cursor.fetchall()

            cursor.execute("SELECT * FROM courses")
            all_courses = cursor.fetchall()

            if len(all_courses) == 0 :
                print_table_as_tuple(cursor, "courses")
                print_table_as_tuple(cursor, "classrooms")
                print_table_as_tuple(cursor, "students")
                break

            for class_room in avaliable_class_rooms:
                course_id = class_room[2]
                if class_room[2] != 0 :
                    cursor.execute("SELECT * FROM courses WHERE id = (?)" , (class_room[2],))
                    the_assigned_course = cursor.fetchall()[0]
                    if len(the_assigned_course) > 0 :
                        
                        
                        time_left = class_room[3] - 1
                     
                        
                        if time_left == 0 :
                            print("(" + str(counter) + ") " + class_room[1] + ": " + the_assigned_course[1] + " is done")
                            cursor.execute("DELETE FROM courses WHERE id = (?)" , (course_id,))        
                            course_id = 0
                        else:
                            print("(" + str(counter) + ") " + class_room[1] + ": occupied by " + the_assigned_course[1])
                        
                        cursor.execute("UPDATE classrooms SET current_course_id = (?), current_course_time_left = (?) WHERE id = (?)" , (course_id, time_left, class_room[0],))
                
                if course_id == 0 :
                    cursor.execute("SELECT * FROM courses WHERE class_id = (?)" , (class_room[0],))
                    assignable_courses = cursor.fetchall()

                    if len(assignable_courses) > 0 :
                        assignable_course=assignable_courses[0]
                        cursor.execute("""UPDATE classrooms SET
                                        current_course_id = (?),
                                        current_course_time_left = (?)
                                        WHERE id = (?)""" , (assignable_course[0],assignable_course[5],class_room[0],))
                        cursor.execute("""UPDATE students SET
                                        count = count - (?)
                                        WHERE grade = (?)""" , (assignable_course[3],assignable_course[2],))
                        print("(" + str(counter) + ") " + class_room[1] + ": " + assignable_course[1] + " is schedule to start")

            print_table_as_tuple(cursor, "courses")
            print_table_as_tuple(cursor, "classrooms")
            print_table_as_tuple(cursor, "students")
        
            counter = counter + 1

def print_table_as_tuple(cursor, table_name):
    print(table_name)
    cursor.execute("SELECT * FROM " + table_name)
    rows = cursor.fetchall()
    print_table(rows)
    return len(rows)

def print_table(list_of_tuples):
    for item in list_of_tuples:
        print(item)

if __name__ == '__main__':
    main()
