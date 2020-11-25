# global libraries
from tkinter import *
from tkinter import messagebox, filedialog
# local modules
from modules import auth_module as am


def some_funct(p, some_element):
    some_element.configure(text=p)
    print(p)
    pass


def reg():
    """
    here we should send user/pass to auth_module
    if there is a record like this -- OK
    if not - depends on settings. we could let this user to create a new record.
    find_user - should help with check. if type will be 1 - we found him.
    if not - put_entry - function to create a new one.
    The way to login - email/main. For email - first part, for main - second.
    #############################################################################
    This part is only for sending mails...
    as a beginning we should find out what is the weeknum now. so we will knew
    which letters we should create.
    it seems this part should be in another module. with project_1 for example.
    #############################################################################
    This part is for working with project_1...
    we should check if the user is available for using an app.
    if yes - give him permissions he needs.
    SO the main action - take a key "EMAIL" for this time.
    Check if there is a record inside of config.file.
    :return:
    """
    key = 'email'
    res, some_arr = am.find_config(key)
    if res == 1:
        lbl.configure(text='success')


def new_entry():
    uid_str = uid.get()
    pwd_str = pwd.get()
    if uid_str and pwd_str:
        am.CONN_ARR['TCN'] = 'No'
        am.CONN_ARR['DRV'] = '{SMTP Server}'
        am.CONN_ARR['SRV'] = 'smtp.outlook.com'
        am.CONN_ARR['DBN'] = 'imap.outlook.com'
        am.CONN_ARR['UID'] = uid.get()
        am.CONN_ARR['PWD'] = pwd.get()

        if am.put_entry(selector_key='email') == 1:
            lbl.configure(text='success')
    else:
        lbl.configure(text='there are incorrect data')


def do_some(window, some_str, some_act):
    messagebox.showinfo(title=some_str, message=some_act)
    if some_str == 'Exit':
        window.quit()
    elif some_str == 'Register':
        reg()
    elif some_str == 'NewFile':
        new_entry()


def MenuCreate(main_window):
    nav_menu = Menu(main_window)
    main_window.config(menu=nav_menu)

    file_menu = Menu(nav_menu, tearoff=0)
    nav_menu.add_cascade(label='File', menu=file_menu)
    file_menu.add_command(label='New', command=lambda: do_some(main_window, 'NewFile', 'create NewFile'))
    # file_menu.add_command(label='Open', command=lambda: do_some(main_window, 'OpenFile', 'open some File'))
    # file_menu.add_command(label='Exit', command=lambda: do_some(main_window, 'Exit', 'quit from App'))
    ############################
    register_menu = Menu(nav_menu, tearoff=0)
    nav_menu.add_cascade(label='Register', menu=register_menu)
    register_menu.add_command(label='Register', command=lambda: do_some(main_window, 'Register', 'will try to login'))
    ############################
    help_menu = Menu(nav_menu, tearoff=0)
    nav_menu.add_cascade(label='About', menu=help_menu)
    help_menu.add_command(label='ABOUT', command=lambda: do_some(main_window, 'About', 'this is by STANUS'))


root = Tk()
root.title("FirstApp")
root.geometry('750x450+200+150')
# root.

MenuCreate(root)
lbl = Label(root, text="Hello")
lbl.grid(column=2, row=0)

uid = Entry(root, width=10)
uid.grid(column=1, row=1)

pwd = Entry(root, width=10)
pwd.grid(column=1, row=2)

btn = Button(root, text="Print Some", command=lambda: some_funct(uid.get() + ' : ' + pwd.get(), lbl))
btn.grid(column=2, row=1)

# file_path = filedialog.askopenfilename()

root.mainloop()
