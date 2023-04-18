from tkinter import *

import mysql.connector as mysql

db = mysql.connect(host="localhost", user="root", password="", database="college")
command_handler = db.cursor(buffered=True)
#from Backend import *

root = Tk()
root.geometry("700x600")
root.title("College Management System")

Label(root, text="Welcome to College Management System", padx=40, pady=40).pack()


def register_stud():  # ADMIN
    query_vals = (stud_name.get(), stud_pass.get())
    command_handler.execute("INSERT INTO users (username,password,privilege) values (%s ,%s,'student')",
                            query_vals)
    db.commit()
    print("registered")
    Label(top, text=f"{stud_name} has been registered ")


def register_teach():  # ADMIN
    query_vals = (teach_name.get(), teach_pass.get())
    command_handler.execute("INSERT INTO users (username,password,privilege) values (%s ,%s,'teacher')",
                            query_vals)
    db.commit()
    print("registered")
    Label(top, text=f"{teach_name} has been registered ")


def del_stu():  # ADMIN
    query_vals = (s_name.get(), "student")
    command_handler.execute("DELETE FROM users WHERE username = %s AND privilege = %s ", query_vals)
    db.commit()

    if command_handler.rowcount < 1:
        print("User not found")
        Label(top, text="Student Record not found")
    else:
        print(f"{s_name} has been deleted")
        Label(top, text=f"{s_name} has been deleted").pack()


def del_t():  # ADMIN
    query_vals = (t_name.get(), "teacher")
    command_handler.execute("DELETE FROM users WHERE username = %s AND privilege = %s ", query_vals)
    db.commit()

    if command_handler.rowcount < 1:
        print("User not found")
        Label(top, text="Faculty Record not found")
    else:
        print(f"{t_name} has been deleted")
        Label(top, text=f"{t_name} has been deleted").pack()


def Reg_del():
    global stud_name
    global stud_pass

    global teach_name
    global teach_pass

    global s_name
    global t_name

    if r.get() == 1:
        Label(top, text="REGISTERING NEW STUDENT RECORD", padx=5, pady=20).pack()
        Label(top, text="Enter Student Name").pack()
        stud_name = Entry(top)
        stud_name.pack()

        Label(top, text="Enter Student Password").pack()
        stud_pass = Entry(top)
        stud_pass.pack()

        Button(top, text='Enter', command=register_stud).pack()

    elif r.get() == 2:
        Label(top, text="REGISTERING NEW FACULTY RECORD", padx=5, pady=20).pack()
        Label(top, text="Enter Faculty Name").pack()
        teach_name = Entry(top)
        teach_name.pack()

        Label(top, text="Enter Faculty Password").pack()
        teach_pass = Entry(top)
        teach_pass.pack()

        Button(top, text='Enter', command=register_teach).pack()

    elif r.get() == 5:
        top.destroy()

    elif r.get() == 3:
        Label(top, text="DELETING EXISTING STUDENT RECORD", padx=5, pady=20).pack()
        Label(top, text="Enter Student Name").pack()
        s_name = Entry(top)
        s_name.pack()

        Button(top, text="Enter", command=del_stu).pack()

    elif r.get() == 4:
        Label(top, text="DELETING EXISTING FACULTY RECORD", padx=5, pady=20).pack()
        Label(top, text="Enter Faculty Name").pack()
        t_name = Entry(top)
        t_name.pack()

        Button(top, text="Enter", command=del_t).pack()


def admin_menu():
    Label(top, text="Admin Menu", pady=10).pack()

    global r

    r = IntVar()
    r.get()

    Radiobutton(top, text="Register New Student ", variable=r, value=1).pack()
    Radiobutton(top, text="Register New Faculty", variable=r, value=2).pack()
    Radiobutton(top, text="Delete Existing Student Record", variable=r, value=3).pack()
    Radiobutton(top, text="Delete Existing Faculty Record", variable=r, value=4).pack()
    Radiobutton(top, text="Log Out", variable=r, value=5).pack()

    Button(top, text="Enter", command=Reg_del).pack()


def login_check():
    if username.get() == "admin" and password.get() == "pass":
        admin_menu()

    else:
        Label(top, text="Wrong login credentials").pack()
        print("Wrong login")


def admin_sess():
    global username
    global password
    global top

    top = Toplevel()
    top.geometry("800x700")

    Label(top, text="Admin Session", pady=25).pack()

    Label(top, text="Username").pack()
    username = Entry(top)
    username.pack()
    # u = username.get()
    # print(u)

    Label(top, text="Password").pack()
    password = Entry(top)
    password.pack()
    # p = password.get()
    # print(p)

    Button(top, text="Enter", command=login_check).pack()


def disp():
    query_vals = (rec, date.get(), attendance.get())
    command_handler.execute("INSERT INTO attendance (username, date, attendance) VALUES (%s,%s,%s)",
                            query_vals)
    db.commit()

    # print(record + " marked as " + attendance)


def att_reg():
    global rec
    global date
    global attendance

    if t.get() == 3:
        top2.destroy()
    elif t.get() == 2:
        command_handler.execute("SELECT username , date ,attendance FROM attendance")
        records = command_handler.fetchall()
        Label(top2, text="VIEWING RECORDS").pack()
        for record in records:
            record = str(record).replace("'", "")
            record = str(record).replace("'", "")
            record = str(record).replace(")", "")
            record = str(record).replace("(", "")
            print(str(record))

            Label(top2, text=f"{str(record)}").pack()

    elif t.get() == 1:
        command_handler.execute("SELECT username FROM users WHERE privilege = 'student'")
        records = command_handler.fetchall()

        Label(top2, text="DATE : YYYY-MM-DD :  ").pack()
        date = Entry(top2)
        date.pack()

        Label(top2, text="P - Present | A - Absent | L - Late").pack()

        for record in records:
            record = str(record).replace(",", "")
            record = str(record).replace("'", "")
            record = str(record).replace(")", "")
            record = str(record).replace("(", "")

            rec = str(record)

            Label(top2, text=f" Mark attendance for : {rec}").pack()

            attendance = Entry(top2)
            attendance.pack()
            Button(top2, text="Enter", command=disp).pack()


def teach_menu():
    Label(top2, text="Faculty Menu", pady=10).pack()

    global t

    t = IntVar()
    t.get()

    Radiobutton(top2, text="Edit register ", variable=t, value=1).pack()
    Radiobutton(top2, text="View Register", variable=t, value=2).pack()
    Radiobutton(top2, text="Logout", variable=t, value=3).pack()

    Button(top2, text="Enter", command=att_reg).pack()


def login_teach():
    query_vals = (teach_username.get(), teach_pass.get())
    command_handler.execute("SELECT * FROM users WHERE username = %s AND password = %s AND privilege = 'teacher'",
                            query_vals)
    db.commit()

    if command_handler.rowcount <= 0:
        Label(top2, text="Login not recognised").pack()
        print("Login not recognised")
    else:
        teach_menu()


def teach_sess():
    global top2

    global teach_username
    global teach_pass

    top2 = Toplevel()
    top2.geometry("700x700")

    Label(top2, text="Faculty Session", pady=20).pack()
    Label(top2, text="Username").pack()
    teach_username = Entry(top2)
    teach_username.pack()

    Label(top2, text="Password").pack()
    teach_pass = Entry(top2)
    teach_pass.pack()

    Button(top2, text="Enter", command=login_teach).pack()


def A_exit():
    root.quit()


Button(root, text="Admin Login  ", bg='black', fg='white', command=admin_sess, padx=5, pady=5).pack()
Button(root, text="Faculty Login", bg='black', fg='white', command=teach_sess, padx=5, pady=5).pack()
Button(root, text="     Exit    ", bg='orange', fg='black', command=A_exit, padx=5, pady=5).pack()

root.mainloop()
