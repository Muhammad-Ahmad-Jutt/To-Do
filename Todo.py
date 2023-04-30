from tkinter import *
from tkinter import ttk
from tksheet import Sheet
import sqlite3
from tkcalendar import DateEntry
from datetime import date
class todolist(object):
    def __init__(self, master):
        self.master = master

        # creating our main frames
        top = Frame(master, bg='grey')
        self.data_sheet = Sheet(top, width=750, theme= 'dark green')
        top.pack()
        self.data_sheet.pack()
        # now the connection to the database
        self.data_statement = f'SELECT Name, Day, Added, Status, Occurance, Reschedule From Task '
        sh_data = self.database_connect(self.data_statement)
        head_sh =  'Name', 'Day', 'Added', 'Status', 'Occurance', 'Reschedule'
        self.data_sheet.headers(head_sh)
        self.data_sheet.set_sheet_data(data = sh_data)
        self.data_sheet.enable_bindings("single_select",
                                   "right_click_popup_menu",
                                   "rc_select")
        self.data_sheet.popup_menu_add_command("Add new task", self.add_task)
        self.data_sheet.popup_menu_add_command("Mark as Completed", self.completed)
        self.data_sheet.popup_menu_add_command("Refresh", self.reload_sheet)
        self.data_sheet.popup_menu_add_command("Delete Task", self.delete_task)
        self.data_sheet.popup_menu_add_command("Exit", exit)
# we will create a seprate function for the database connectivity 
    def reload_sheet(self):
        sh_data = self.database_connect(self.data_statement)
        self.data_sheet.set_sheet_data(data = sh_data)
        self.data_sheet.refresh()

    def add_task(self):
        self.add_window = Tk()
        self.add_window.title("Add new Task") 
        self.add_window.configure(bg='white')
        # lets create frame for our window
        mainframe = Frame(self.add_window)
        mainframe.pack()
        t_name_label = Label(mainframe, text="Task Name")
        self.t_name_entry = Entry(mainframe)
        t_date_label = Label(mainframe, text="Task Date")
        self.t_date_entry = DateEntry(mainframe, date_pattern = 'yyyy/mm/dd')
        t_date = date.today()
        date_label = Label(mainframe, text="Today Date")
        today_date = Label(mainframe, text=t_date)
        duration_label = Label(mainframe, text="Occurance")
        self.duration_combo = ttk.Combobox(mainframe, values=("Once", "Daily", "Monthly","Yearly"))
        self.status_label = Label(mainframe, text='Press button to add')
        add_buton = Button(mainframe, text="Add", command=self.addto_db)
        exit_bt = Button(mainframe, text="Exit", command= lambda : self.add_window.destroy())
        t_name_label.grid(row=0, column=0, padx=5, pady=5)
        self.t_name_entry.grid(row=0, column=1, padx=5, pady=5)
        t_date_label.grid(row=0, column=2, padx=5, pady=5)
        self.t_date_entry.grid(row=0, column=3, padx=5, pady=5)
        date_label.grid(row=1, column=0, padx=5, pady=5)
        today_date.grid(row=1, column=1, padx=5, pady=5)
        duration_label.grid(row=1, column=2, padx=5, pady=5)
        self.duration_combo.grid(row=1, column=3, padx=5, pady=5)
        self.status_label.grid(row=2, column=0, padx=5, pady=5)
        add_buton.grid(row=2, column=2, padx=5, pady=5)
        exit_bt.grid(row=2, column=3, padx=5, pady=5)

    def addto_db(self):
        tname = self.t_name_entry.get()
        tdate = self.t_date_entry.get()
        tduration = self.duration_combo.get()
        if tname and tdate and tduration != "":
            todaydate = date.today()
            reschedule = 'No'
            status = 'Pending'
            print(tname)
            add_statement = f"INSERT INTO Task( Name, Day, Added, Status, Occurance, Reschedule)  VALUES(?,?,?,?,?,?)"
            try:
                conn = sqlite3.connect("/home/ahmad/Desktop/projects/To Do List/Database/Task.db")
                cur = conn.cursor()
                cur.execute(f"SELECT *FROM Task WHERE Name = '{tname}'")
                if cur.fetchone() is None:
                    cur.execute(add_statement,(tname,tdate,todaydate,status,tduration,reschedule))
                    self.status_label.config(text="Added Sucessfull", fg="green")
                else:
                    self.status_label.config(text="Already Exist", fg="red")
                conn.commit()
                conn.close
            except:
                self.status_label.config(text="Erroe While connecting to the database", fg='red')
        else:
            self.status_label.config(text="Fields Empty", fg='red')
        self.reload_sheet()    
    def delete_task(self):
        cell_Data = self.get_celldata()
        del_statement = f"DELETE FROM Task WHERE Name = '{cell_Data}'"
        self.database_connect(del_statement)
        self.reload_sheet()
    
    def get_celldata(self):
        cell_vertic = self.data_sheet.get_selected_cells()
        row = list(cell_vertic)
        cell_data = self.data_sheet.get_cell_data(row[0][0],0, return_copy=True)
        return cell_data
    
    def completed(self):
        
        cell_data = self.get_celldata()
        up_statement = f"UPDATE TASK SET Status = '{'Completed'}' Where Name = '{cell_data}'"
        self.database_connect(up_statement)
        self.reload_sheet()

    def database_connect(self, statement):
        try:
            conn = sqlite3.connect('/home/ahmad/Desktop/projects/To Do List/Database/Task.db')   
            cur = conn.cursor()
            data = cur.execute(statement).fetchall()
            conn.commit()
            conn.close
            return data
        except :
            print("Bad class or table name")

def guifunction():
    root = Tk()
    app = todolist(root)
    root.title("To Do List")
    x= 800
    y = 30
    root.geometry("+%d+%d" %(x,y))
    root.mainloop()


if __name__ == '__main__':
    guifunction()
