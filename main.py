
# imports modules from tkinter library for windows
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

# imports pyperclic for copy functionality and path from os for file checking
import pyperclip
from os import path

# imports functions from passord file
from password import *

# initializes main window
window = Tk()

class MainWindow: # class to handle input-output through window
    def __init__(self,win):
        self.window = win

        self.filepath = ''
        self.pw = ''
        self.services = []

        self.page = 0
        self.main()

    def main(self): # Draws window as when program is opened
        self.window.iconbitmap('icon.ico')
        self.window.title('Password manager')
        self.window.geometry('350x400')

        self.menubar = Menu(self.window)
        self.window.config(menu=self.menubar)

        self.fileMenu = Menu(self.menubar, tearoff = 0)
        self.aboutMenu = Menu(self.menubar, tearoff = 0)

        self.fileMenu.add_command(label = "Open database", command = self.search_database)
        self.fileMenu.add_command(label = "Exit", command = self.onExit)
        self.menubar.add_cascade(label = "File", menu = self.fileMenu)

        self.aboutMenu.add_command(label = "See on GitHub", command = lambda : pyperclip.copy('google.com'))
        self.menubar.add_cascade(label = "About", menu = self.aboutMenu)

        self.opendatabase = Button(window, text = "Open Database", command = self.search_database)
        self.createdatabase = Button(window, text = "Create Database", command = self.create_database)

        self.opendatabase.place(relx = 0.5, rely = 0.1, anchor = CENTER)
        self.createdatabase.place(relx = 0.5, rely = 0.2, anchor = CENTER)

    def draw(self): # sraws needed items to input/ouptut when file is opened
        self.fileMenu.entryconfig(0, label = "Close database", command = self.close_database)

        self.opendatabase.place_forget()
        self.createdatabase.place_forget()

        self.repag = Button(self.window, text = 'Previous', command = self.previouspage)
        self.avpag = Button(self.window, text = 'Next', command = self.nextpage)

        self.search = Entry(self.window)
        self.new = Button(self.window, text = 'New', command = self.newentry)

        self.searchbutton = Button(self.window, text = 'Search', command = self.search_entries)

        self.new.grid(column = 1, row = 0, padx = 2, pady = 2, sticky = W)
        self.searchbutton.grid(column = 4, row = 0, padx = 2, pady = 2)
        self.search.grid(column = 1, row = 0, padx = 2, pady = 2, sticky = E, columnspan = 3)
        self.repag.grid(column = 0, row = 0, padx = 2, pady = 2, sticky = W)
        self.avpag.grid(column = 0, row = 0, padx = 2, pady = 2, sticky =E)

    def create_database(self): # draws create_database window
        self.top = Toplevel(self.window)
        self.top.attributes("-topmost", True)
        self.top.iconbitmap('icon.ico')
        self.top.title('New password')

        Label(self.top, text = 'Database name*').grid(row = 0, column = 0, sticky = W)
        self.database_name = Entry(self.top, width = 20)

        self.database_name.grid(row = 0, column = 1, sticky = E, padx = 10)

        Label(self.top, text = 'Password*').grid(row = 1, column = 0, sticky = W)
        self.database_password = Entry(self.top, show = '*',width = 20)

        self.database_password.grid(row = 1, column = 1, sticky = E, padx = 10)

        Label(self.top, text = 'Salt size').grid(row = 2, column = 0, sticky = W)
        self.database_salt_size = Spinbox(self.top, from_ = 16, to = 256, width = 5)
        self.database_salt_size.grid(row = 2, column = 1, sticky = E, padx = 10)

        self.submit=Button(self.top, text = 'OK', command = self.new_database_commit)
        self.cancel=Button(self.top, text = 'Cancel', command = self.cancel_changes)

        self.submit.grid(row = 3, column = 0, padx = 5, pady = 5)
        self.cancel.grid(row = 4, column = 0, padx =5 , pady = 5)

    def newentry(self): # draws new entry window
        self.top = Toplevel(self.window)
        self.top.attributes("-topmost", True)
        self.top.iconbitmap('icon.ico')
        self.top.title('New password')

        Label(self.top, text = 'Service*').grid(row = 0, column = 0, sticky = W)
        self.serviceEntry = Entry(self.top, width = 20)

        self.serviceEntry.grid(row = 0, column = 1, sticky = E, padx = 10)

        Label(self.top, text = 'Username*').grid(row = 1, column = 0, sticky = W)
        self.usernameEntry = Entry(self.top, width = 20)

        self.usernameEntry.grid(row = 1, column = 1, sticky = E, padx = 10)

        Label(self.top, text = 'Password*').grid(row = 2, column = 0, sticky = W)
        self.passwordEntry = Entry(self.top, show = '*', width = 20)

        self.passwordEntry.grid(row = 2, column = 1, sticky = E, padx = 10)

        self.showpwd = BooleanVar(self.top)
        Checkbutton(self.top, text = 'Show', variable = self.showpwd, command = self.toggle_vision).grid(row = 2, column = 2)

        self.showpwd.set(False)

        Label(self.top, text = 'Data').grid(row = 3, column = 0, columnspan = 2, sticky = W)
        self.data = Text(self.top, width = 40, height = 10)
        scroll_y = Scrollbar(self.top, orient = "vertical", command = self.data.yview)

        scroll_y.grid(row = 4, column = 3, sticky = 'ns', columnspan = 2)

        self.data.grid(row = 4, column = 0, columnspan = 3, sticky = W, padx = 5, pady = 5)

        self.submit=Button(self.top, text = 'OK', command = self.submit_changes)
        self.cancel=Button(self.top, text = 'Cancel', command = self.cancel_changes)

        self.submit.grid(row = 5, column = 0, padx = 5, pady = 5)
        self.cancel.grid(row = 6, column = 0, padx = 5, pady = 5)

    def new_database_commit(self): # fuinction for create_database window, creates database with given data
        name = self.database_name.get()
        pw = self.database_password.get().encode('utf-8')
        salt_size = int(self.database_salt_size.get())

        if not path.exists(name + '.pwdb'): # checks if file exists
            if name != '' and pw != '': # checks if data is complete
                create_db(name + '.pwdb', pw, salt_size)
                self.top.destroy()
                self.top.update()
            else:
                messagebox.showwarning("!!", "Incomplete data.")
        else:
            messagebox.showwarning("!!", "There is a file with that name.")

    def toggle_vision(self): # function for newentry window to show passord instead of *
        if self.showpwd.get():
            self.passwordEntry.config(show = '')
        else:
            self.passwordEntry.config(show = '*')

    def submit_changes(self): # function for newentry window to add entry
        newservice = self.serviceEntry.get()
        newusername = self.usernameEntry.get()
        newpassword = self.passwordEntry.get()
        newinfo = self.data.get("1.0", END)

        if newservice != '' and newusername != '' and newpassword != '':
            if add_password(self.filepath, self.pw, newservice, newusername, newpassword, newinfo):
                self.top.destroy()
                self.top.update()
                self.showitems(True)
            else:
                messagebox.showwarning("!!", "Service has already an entry.")
        else:
            messagebox.showwarning("!!", "Incomplete data.")

    def cancel_changes(self): # cancels changes for newentry and create_database
        self.top.destroy()
        self.top.update()

    def search_entries(self): # function to search entries by name
        self.services = list_of_services(self.filepath, self.pw)
        looking_for = self.search.get()
        found = []
        for entry in self.services:
            if looking_for in entry:
                found.append(entry)
        self.services = found
        self.page = 0
        self.showitems()

    def nextpage(self): # shows next page of entries
        if 5 * (self.page + 1) < len(self.services):
            self.page += 1
            self.showitems()
        else:
            pass

    def previouspage(self): # shows previous page of entries
        if self.page - 1 >= 0:
            self.page -= 1
            self.showitems()
        else:
            pass

    def deletewidgets(self): # deletes widgets to create new windo from scratch
        for widget in self.window.winfo_children():
            widget.destroy()

    def close_database(self): # clears memory and draws main window
        self.filepath = ''
        self.pw = ''
        self.services = []

        self.deletewidgets()
        self.main()

    def showitems(self, reset = False): # shows selected items
        if reset:
            self.page = 0
            self.services = list_of_services(self.filepath, self.pw)
            self.services = self.services[::-1]
        self.deletewidgets()
        self.main()
        self.draw()

        if len(self.services) == 0:
            Label(self.window, text = 'No results found').grid(column = 0, row = 2, padx = 2, pady = 2)

        count = 0
        for service in self.services[5 * self.page:]:
            if (5 * self.page + count) < len(self.services) and count < 5:
                entry(self.window, count, service)
                count += 1
            else:
                break

    def search_database(self): # opens file dialog to select database file (.pwdb)
        self.window.filename = filedialog.askopenfilename(initialdir = "./", title = "Select file", filetypes = (("database", "*.pwdb"), ("all files", "*.*")))

        self.filepath = self.window.filename

        if self.filepath[-4:] != 'pwdb':
            messagebox.showerror("Error", "Not a valid file.")
            return 0

        self.top = Toplevel(self.window)
        self.top.iconbitmap('icon.ico')
        self.top.title('Open database')
        self.a = Label(self.top, text = 'Enter password: ')
        self.e = Entry(self.top, show = '*', width=40)
        self.b = Button(self.top, text = 'Enter', command = self.check_password)

        self.a.grid(column = 0, row = 0, sticky = W, padx = 10)
        self.e.grid(column = 0, row = 1, padx = 10, pady = 5)
        self.b.grid(column = 0, row = 2, sticky = E, padx = 10, pady = 10)

    def check_password(self): # checks if password is valid for selected database
        self.pw = self.e.get().encode('utf-8')
        self.top.destroy()
        self.top.update()
        if check_password(self.filepath, self.pw):
            self.page = 0
            self.showitems(True)
        else:
            self.pw = ''
            self.filepath = ''
            messagebox.showerror("Error", "Incorrect password.")

    def onExit(self): # clears memory before exiting
        self.pw = ''
        self.window.quit()

class entry: # class to handle each entry
    def __init__(self, win, pos, name): # draws entry
        self.id = name
        self.name = Label(win, text = name)
        self.name.config(font = ('TkDefaultFont', 15))

        self.deletebutton=Button(win, text = 'Delete', command = self.delete_entry)
        self.copypassword=Button(win, text = 'Copy password', command = self.copy_password)
        self.copyusername=Button(win, text = 'Copy username', command = self.copy_username)
        self.edit=Button(win, text = 'Edit', command = self.edit_entry)

        self.name.grid(column = 0, row = (2 * pos) + 1, sticky = W, padx = 10, pady = 3, columnspan = 100)

        self.deletebutton.grid(column = 3, row = (2 * pos) + 2, padx = 4, pady = 4)
        self.copypassword.grid(column = 0, row = (2 * pos) + 2, padx = 4, pady = 4)
        self.copyusername.grid(column = 1, row = (2 * pos) + 2, padx = 4, pady = 4)
        self.edit.grid(column = 2, row = (2 * pos) + 2, padx = 4, pady = 4)

    def edit_entry(self): # window to edit entry
        self.top = Toplevel(app.window)
        self.top.attributes("-topmost", True)
        self.top.iconbitmap('icon.ico')
        self.top.title('Edit password')

        previous_data=retrieve_password(app.filepath, app.pw, self.id)

        Label(self.top,text = 'Service*').grid(row = 0, column = 0, sticky = W)
        self.serviceEntry = Label(self.top,text = previous_data[0])

        self.serviceEntry.grid(row = 0, column = 1, padx = 10)

        Label(self.top,text = 'Username*').grid(row = 1, column = 0, sticky = W)
        self.usernameEntry = Entry(self.top,width = 20)

        self.usernameEntry.insert(0,previous_data[1])
        self.usernameEntry.grid(row = 1, column = 1, sticky = E, padx = 10)

        Label(self.top,text = 'Password*').grid(row = 2, column = 0, sticky = W)
        self.passwordEntry = Entry(self.top, show = '*', width = 20)

        self.passwordEntry.insert(0, previous_data[2])
        self.passwordEntry.grid(row = 2, column = 1, sticky = E, padx = 10)

        self.showpwd = BooleanVar(self.top)

        Checkbutton(self.top, text = 'Show', variable = self.showpwd, command = self.toggle_vision).grid(row = 2,column = 2)
        self.showpwd.set(False)

        Label(self.top,text = 'Data').grid(row = 3, column = 0, columnspan = 2, sticky = W)
        self.data=Text(self.top, width = 40, height = 10)

        self.data.insert('1.0', previous_data[3])

        scroll_y = Scrollbar(self.top, orient = "vertical", command = self.data.yview)

        scroll_y.grid(row = 4, column = 3, sticky = 'ns', columnspan = 2)
        self.data.grid(row = 4, column = 0, columnspan = 3, sticky = W, padx = 5, pady = 5)

        self.submit = Button(self.top, text = 'OK', command = self.submit_changes)
        self.cancel = Button(self.top, text = 'Cancel', command = self.cancel_changes)

        self.submit.grid(row = 5, column = 0, padx = 5, pady = 5)
        self.cancel.grid(row = 6, column = 0, padx = 5, pady = 5)

    def delete_entry(self): # function to delete entry
        remove_password(app.filepath, app.pw, self.id)
        app.showitems(True)

    def copy_username(self): # function to copy username
        pyperclip.copy(retrieve_password(app.filepath, app.pw, self.id)[1])

    def copy_password(self): # function to copy password
        pyperclip.copy(retrieve_password(app.filepath, app.pw, self.id)[2])

    def toggle_vision(self): # function to show/hide password
        if self.showpwd.get():
            self.passwordEntry.config(show = '')
        else:
            self.passwordEntry.config(show = '*')

    def submit_changes(self): # updates entry in the database
        changedusername = self.usernameEntry.get()
        changedpassword = self.passwordEntry.get()
        changedinfo = self.data.get("1.0", END)

        if changedusername != '' and changedpassword != '':
            edit_password(app.filepath, app.pw, self.id, changedusername, changedpassword, changedinfo)
            self.top.destroy()
            self.top.update()
            app.showitems(True)
        else:
            messagebox.showwarning("!!", "Incomplete data.")

    def cancel_changes(self): # cancels changes
        self.top.destroy()
        self.top.update()

app=MainWindow(window) # sets main window's app

window.mainloop() # starts window
