"""
Here we will build some visual environment, so next step will be creation
of parameters needed to
"""
# global libraries
from tkinter import *
from tkinter import messagebox, filedialog
from typing import Any

from modules import auth_module as am


def output_some(text, output_place):
    output_place.configure(text=text)


class MainApp:
    """
        Authorize
        PutNewEntry/UpdateEntry
        CheckValues
        StartIssues
        BuildMenues - run inside of Init
    """
    def __init__(self, main_window):
        self.root = main_window
        self.root.title("Sending Emails")
        self.root.geometry('+300+450')
        self.menu_create(self.root)
        lbl = Label(self.root, text="Here we will try to combine some strings for sending an email. \n" +
                                    "Please, register to get permissions")
        lbl.grid(column=0, row=0, columnspan=3)
        
        # userid = StringVar()
        
        self.root.uid = Entry(self.root, width=10)  # , command=lambda: userid.set(uid.get())
        self.root.uid.grid(column=1, row=1)

        self.root.pwd = Entry(self.root, width=10)
        self.root.pwd.grid(column=1, row=2)
        
        btn = Button(self.root, text="Print Some", command=lambda: output_some(text=self.root.uid.get() + ' : ' +
                                                                                    self.root.pwd.get(),
                                                                               output_place=lbl))
        btn.grid(column=2, row=1)
        
        status_bar = Label(self.root, text='some test message for status bar')
        status_bar.grid(sticky=N+E+W, columnspan=3)

    def menu_create(self, window):
        menu_var = Menu(window, tearoff=0)
        window.config(menu=menu_var)
        file_menu = Menu(menu_var, tearoff=0)
        menu_var.add_cascade(label='File', menu=file_menu)
        file_menu.add_command(label='New',  command=lambda: self.do_some('NewFile', 'create NewFile'))
        file_menu.add_command(label='Open', command=lambda: self.do_some('OpenFile', 'open some File'))
        file_menu.add_command(label='Exit', command=lambda: self.do_some('Exit', 'quit from App'))
        ############################
        register_menu = Menu(menu_var, tearoff=0)
        menu_var.add_cascade(label='Register', menu=register_menu)
        register_menu.add_command(label='Register',
                                  command=lambda: self.do_some('Register', 'will try to login'))
        ############################
        help_menu = Menu(menu_var, tearoff=0)
        menu_var.add_cascade(label='About', menu=help_menu)
        help_menu.add_command(label='ABOUT', command=lambda: self.do_some('About', 'this is by STANUS'))

    def do_some(self, some_str, some_act):
        messagebox.showinfo(title=some_str, message=some_act)
        if some_str == 'Exit':
            self.root.quit()
        elif some_str == 'Register':
            self.reg()
        elif some_str == 'NewFile':
            self.new_entry()
            
    def reg(self):
        pass

    def new_entry(self):
        uid_str = self.root.uid.get()
        pwd_str = self.root.pwd.get()
        str_res = ''
        if uid_str and pwd_str:
            am.CONN_ARR['TCN'] = 'No'
            am.CONN_ARR['DRV'] = '{SMTP Server}'
            am.CONN_ARR['SRV'] = 'smtp.outlook.com'
            am.CONN_ARR['DBN'] = 'imap.outlook.com'
            am.CONN_ARR['UID'] = uid_str
            am.CONN_ARR['PWD'] = pwd_str
        
            if am.put_entry(selector_key='email', conn_str=am.CONN_ARR) == 1:
                str_res = 'success'
        else:
            str_res = 'there are incorrect data'
        self.status_bar.configure(text=str_res)
        

if __name__ == '__main__':
    root = Tk()
    application = MainApp(root)
    root.mainloop()

#
# root.title("Sending Emails")
# root.geometry('750x450+500+450')
# file_path = filedialog.askopenfilename()
