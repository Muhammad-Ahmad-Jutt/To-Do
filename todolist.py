from tkinter import *
import pandas as pd
from tksheet import Sheet
from tkinter import ttk
import sqlite3
from datetime import date, time, datetime
from tkcalendar import DateEntry
class todolist(object):
    def __init__(self, master):
        self.master = master

        # creating our main frames
        self.top = Frame(master, bg='grey')
        self.down = Frame(master, height=50, bg='black')
        # making them config to gui
        self.top.grid(row=0, column=0)
        self.down.grid(row=1, column=0)
        # now we will create our rows or dataframs 
        # our tasks has properties like Task name, start date , status, time remaining, 
# Top Frame data
        t_data = self.database()
        print(t_data)
        self.data = Sheet(self.top)
        self.data.pack(fill=Y)
        self.data.set_all_cell_sizes_to_text()
        head_sh =  'Name', 'Day', 'Added','Occurance', 'Status', 'Reschedule', 'Time Remaining'
        self.data.headers(head_sh)
        self.data.set_sheet_data(data=t_data)
# Bottom Frame data
        self.add_bt = ttk.Button(self.down, text = "Add", command= lambda : self.add_t())
        self.add_bt.grid(row=0, column = 0)
        self.del_bt = ttk.Button(self.down, text = "Delete")
        self.del_bt.grid(row=0, column = 1)
        self.del_bt = ttk.Button(self.down, text = "Mark as Completed")
        self.del_bt.grid(row=0, column = 2)
        self.exit_button = Button(self.down, text= "Exit", command=lambda : self.master.destroy())
        self.exit_button.grid(row=0, column = 3)


    def add_t(self):
        add_window = Tk()
        add_window.title("Add new Task") 
        add_window.configure(bg='white')
        # lets create frame for our window
        mainframe = Frame(add_window)
        mainframe.pack()
        t_name_label = Label(mainframe, text="Task Name")
        t_name_entry = Entry(mainframe)
        t_date_label = Label(mainframe, text="Task Date")
        t_date_entry = DateEntry(mainframe, date_pattern = 'yyyy/mm/dd')
        t_date = self.Today()
        date_label = Label(mainframe, text="Today Date")
        today_date = Label(mainframe, text=t_date)
        print(t_name_entry.get())
        add_buton = Button(mainframe, text="Add", command=lambda : self.add_to_data(t_name_entry, t_date_entry, duration_combo))
        duration_label = Label(mainframe, text="Occurance")
        duration_combo = ttk.Combobox(mainframe, values=("Once", "Daily", "Monthly","Yearly"))
        exit_bt = Button(mainframe, text="Exit", command= lambda : add_window.destroy())
        t_name_label.grid(row=0, column=0, padx=5, pady=5)
        t_name_entry.grid(row=0, column=1, padx=5, pady=5)
        t_date_label.grid(row=0, column=2, padx=5, pady=5)
        t_date_entry.grid(row=0, column=3, padx=5, pady=5)
        date_label.grid(row=1, column=0, padx=5, pady=5)
        today_date.grid(row=1, column=1, padx=5, pady=5)
        duration_label.grid(row=1, column=2, padx=5, pady=5)
        duration_combo.grid(row=1, column=3, padx=5, pady=5)
        add_buton.grid(row=2, column=2, padx=5, pady=5)
        exit_bt.grid(row=2, column=3, padx=5, pady=5)


    def add_to_data(self, name, task_date, t_type):
        name = name.get()
        task_date = task_date.get()
        today_date = self.Today()
        t_type = t_type.get()
        status = 'Pending'
        Reschedule = 'No'
        taskdate = datetime.strptime(task_date, "%Y/%M/%d").date()
        todaydate = datetime.strptime(today_date, "%Y/%M/%d").date()
        conn = sqlite3.connect(r"/home/ahmad/Desktop/projects/To Do List/Database/Task.db")
        cur = conn.cursor()
        statement = "INSERT INTO Task (Name, Day, Added, Status, Reschedule, occurance) VALUES(?,?,?,?,?,?)"
        cur.execute(statement, (name,taskdate,todaydate,t_type,status,Reschedule))
        conn.commit()
        conn.close()

    def Today(self):
        t_Date = date.today()
        tldate = str(t_Date)
        tldate = tldate.replace("-", "/")
        
        return tldate
    def database(self):
        conn = sqlite3.connect("/home/ahmad/Desktop/projects/To Do List/Database/Task.db")
        cur = conn.cursor()
        data = cur.execute("SELECT Name, Day, Added, occurance, Status, Reschedule, JULIANDAY(Added)- JULIANDAY(Day) AS Time FROM Task").fetchall()
        return data
    

def guifunction():
    root = Tk()
    app = todolist(root)
    root.title("To Do List")
    root.mainloop()


if __name__ == '__main__':
    guifunction()
