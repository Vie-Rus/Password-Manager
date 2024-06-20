from tkinter import *
from tkinter import ttk, Tk, Label, LabelFrame, messagebox
from tkinter.simpledialog import askstring
from datetime import datetime

#Dictionary for tab titles and corresponding tab objects
accName = "Account "
ErrorMissingInfo = None
Edit_Accindex = None
tab_accounts = {}
tabs = {}
accountCounter = 0
hidePassInt = 0
nextTabCounter = 0
timestamp = datetime.now().strftime("%m-%d-%Y %H:%M:%S")

def focusIn(event):
    search_Entry = event.widget
    if search_Entry.get() == "Search Tab: ":
        search_Entry.delete(0, END)
        search_Entry.config(fg='black')
    
def focusOut(event):
    search_Entry = event.widget
    if search_Entry.get() == "":
        search_Entry.insert(0, "Search Tab: ")
        search_Entry.config(fg='grey')

def searchTabs():
    query = search_Entry.get()
    example_Sug0.grid_forget()
    example_Sug1.grid_forget()
    example_Sug2.grid_forget()
    if query and query != "Search Tab: ":
        matchTabs = [title for title in tabs.keys() if query.lower() in title.lower()]
        matchTabs = matchTabs[:3] 
        for i, title in enumerate(matchTabs):
            if i==0:
                example_Sug0.config(text=title)
                example_Sug0.grid(row=5, column=0, pady=5, padx=5)
            elif i==1:
                example_Sug1.config(text=title)
                example_Sug1.grid(row=5, column=1, pady=5, padx=5)
            elif i==2:
                example_Sug2.config(text=title)
                example_Sug2.grid(row=5, column=2, pady=5, padx=5)
         
def nextTab():
    global nextTabCounter
    totalTabs = notebook.index("end")
    if totalTabs > 1:
        nextTabCounter = (nextTabCounter+1) % totalTabs
        notebook.select(nextTabCounter)
    else: nextTab.config(state=DISABLED)
    
def prevTab():
    global nextTabCounter
    totalTabs = notebook.index("end")
    if totalTabs > 1:
        nextTabCounter = (nextTabCounter-1) % totalTabs
        notebook.select(nextTabCounter)
    else: prevTab.config(state=DISABLED) 

def create_new_tab(tab_title=None):  
    def clearAccount():
        global Edit_Accindex    
        email_var.set("Email: required ")
        password_var.set("Password: required ")
        username_var.set("Username: ")
        submit.config(command=lambda: enterAccount(edit_index=None))
        Edit_Accindex = None
        delete_account.grid_remove()
        print("Clears:: submissions > new submission\n")    

    def deleteTab(tab_title):
        global timestamp
        response = messagebox.askyesno("Delete Tab", "By deleting this tab you are also deleting the accounts connected to it. Are you sure?")
        if response == 1:
            print(f"Deletion:: Tab: '{tab_title}' at '{timestamp}'")
            notebook.forget(tabs[tab_title])
            del tab[tab_title]
            del tab_accounts[tab_title]
        else:
            pass

    def deleteAccount(): 
        global Edit_Accindex, accName, accountCounter, timestamp
        accounts = tab_accounts[tab_title]
        print(f"Deletion:: Account: '{accName}' - {timestamp}")
        if Edit_Accindex is not None:
            frame, set_email, set_password, set_username, edit_button = accounts.pop(Edit_Accindex)
            frame.grid_forget()
            frame.destroy()
            #Reposition remaining accounts after deletion
            for i in range(Edit_Accindex, len(accounts)):
                frame, set_email, set_password, set_username, edit_button = accounts[i]
                frame.grid(row=5, column=i, padx=10, pady=10)
            accountCounter -= 1
            Edit_Accindex = None
            delete_account.grid_remove()
            submit.config(command=lambda: enterAccount(edit_index=None))
            clearAccount()    

    def editAccount(accountName, emailName, passwordName, userName, index):
        global Edit_Accindex
        print(f"Edit Account:: Account: '{accountName}' - Email: {emailName}, Password: {passwordName}, User: {userName}, Index: {index}\n")
        account_name.config(text=accountName)
        Emailname_Entry.delete(0, END)
        Emailname_Entry.insert(0, emailName)
        Passwordname_Entry.delete(0, END)
        Passwordname_Entry.insert(0, passwordName)
        Username_Entry.delete(0, END)
        Username_Entry.insert(0, userName)
        #Specific Entry Updation for editted account
        submit.config(command=lambda: enterAccount(edit_index=index))
        Edit_Accindex = index
        delete_account.grid()

    def editAccountName():
        global accName
        new_accountName = askstring("New Account name", "Account's name")
        if new_accountName:
            print(f"Edit Title:: Account: '{accName}' >> Account: '{new_accountName}'")
            accName = new_accountName
            account_name.config(text=accName)
            if Edit_Accindex is not None:
                accounts = tab_accounts[tab_title]
                frame, set_email, set_password, set_username, edit_button = accounts[Edit_Accindex]
                frame.config(text=accName)

    def enterAccount(edit_index=None):
        global accName, ErrorMissingInfo, accountCounter, Edit_Accindex
        emailName = email_var.get().replace("Email: required ", "")
        passwordName = password_var.get().replace("Password: required ", "")
        userName = username_var.get().replace("Username: ", "")
        if ErrorMissingInfo:
            ErrorMissingInfo.grid_forget()
            ErrorMissingInfo = None
        if emailName == "" or passwordName == "":
            if ErrorMissingInfo is None:
                ErrorMissingInfo = Label(new_tab, text="Email and Password are required", fg='red')
                ErrorMissingInfo.grid(row=1, column=1, padx=10, pady=10)
        elif '@' not in emailName or not emailName.endswith(".com"):
            if ErrorMissingInfo is None:
                ErrorMissingInfo = Label(new_tab, text="Email format is not acceptable", fg='red')
                ErrorMissingInfo.grid(row=1, column=1, padx=10, pady=10)
                print(f"FAILED Create:: ABOVE")
        else:
            passwordNameMask = '*' * len(passwordName)  #Mask the password
            accounts = tab_accounts[tab_title]
            if edit_index is not None:
                frame, set_email, set_password, set_username, editAccount_Button = accounts[edit_index]
                set_email.config(text="Email: " + emailName)
                set_password.config(text="Password: " + passwordNameMask)
                set_username.config(text="Username: " + userName)
                editAccount_Button.config(command=lambda a=accName, e=emailName, p=passwordName, u=userName, i=edit_index: editAccount(a, e, p, u, i))
            else:    
                set_account = LabelFrame(new_tab, text=accName)
                set_account.grid(row=5, column=len(accounts), padx=10, pady=10)
                set_email = Label(set_account, text="Email: " + emailName, anchor=W)
                set_email.grid(row=1, column=1+len(accounts), padx=10, pady=10, sticky=W+E)
                set_password = Label(set_account, text="Password: " + passwordNameMask, anchor=W)
                set_password.grid(row=2, column=1+len(accounts), padx=10, pady=10, sticky=W+E)
                set_username = Label(set_account, text="Username: " + userName, anchor=W)
                set_username.grid(row=3, column=1+len(accounts), padx=10, pady=10, sticky=W+E)
                editAccount_Button = Button(set_account, text="Edit", command=lambda a=accName, e=emailName, p=passwordName, u=userName, i=accountCounter: editAccount(a, e, p, u, i))
                editAccount_Button.grid(row=4, column=1+len(accounts), padx=10, pady=10, sticky=W+E)
                accounts.append((set_account, set_email, set_password, set_username, editAccount_Button))
                accountCounter += 1
                print(f"Create:: Tab: '{tab_title}', Account: '{accName}' - Email: {emailName}, Password: {passwordName}")
            email_var.set("Email: required ")
            password_var.set("Password: required ")
            username_var.set("Username: ")
            accName = "Account " + str(len(tab_accounts[tab_title]))
            account_name.config(text=accName)
            delete_account.grid_remove()
            Edit_Accindex = None
            clearAccount()

    def focusIn(event):
        widget = event.widget
        if widget == Emailname_Entry and email_var.get() == "Email: required ":
            email_var.set("")
            Emailname_Entry.config(fg='black')
        elif widget == Passwordname_Entry and password_var.get() == "Password: required ":
            password_var.set("")
            Passwordname_Entry.config(show='*', fg='black')
        elif widget == Username_Entry and username_var.get() == "Username: ":
            username_var.set("")
            Username_Entry.config(fg='black')

    def focusOut(event):
        widget = event.widget
        if widget == Emailname_Entry and email_var.get() == "":
            email_var.set("Email: required ")
            Emailname_Entry.config(fg='grey')
        elif widget == Passwordname_Entry and password_var.get() == "":
            password_var.set("Password: required ")
            Passwordname_Entry.config(show='', fg='grey')
        elif widget == Username_Entry and username_var.get() == "":
            username_var.set("Username: ")
            Username_Entry.config(fg='grey')

    def unhiddenPass():
        global hidePassInt
        if hidePassInt == 0:  #Unhide
            Passwordname_Entry.config(show='', fg='black')
            hidePassInt += 1
        else:  #Hide
            Passwordname_Entry.config(show='*', fg='black')
            hidePassInt -= 1

#Main Account Creation--------------------------------------------------------------------------------
    if len(tabs) == 9:  #0-9 = 10
        print("YOU CAN NOT MAKE ANY MORE ACCOUNTS")
        Label(initial_tab, text="Max Tabs Created", fg='red').grid(row=2, column=1)
        new_tab_button = Button(initial_tab, text="Create New Tab", state=DISABLED)
        new_tab_button.grid(row=1, column=1, pady=10)
    else:
        if not tab_title:
            tab_title = askstring("Tab Title", "Enter the title for the new tab:")
        if tab_title:
            if tab_title in tabs:
                messagebox.showerror("Error", f"Tab with title '{tab_title}' already exists.")
                return
            #Creates a new frame for the content of the tab
            new_tab = ttk.Frame(notebook)
            print(f"New tab: '{tab_title}', has been created")
            #Name of account placement within the Input Entry boxes
            account_name = Label(new_tab, text=accName, anchor=W)
            account_name.grid(row=0, column=0, padx=10, pady=10, sticky=W+E)   
            email_var = StringVar(value="Email: required ")
            password_var = StringVar(value="Password: required ")  
            username_var = StringVar(value="Username: ")
            #Additional information to the tab    
            Emailname_Entry = Entry(new_tab, textvariable=email_var, width=25)
            Emailname_Entry.grid(row=1, column=0, padx=10, pady=10) #Entered Email Entry
            Emailname_Entry.bind('<FocusIn>', focusIn)
            Emailname_Entry.bind('<FocusOut>', focusOut)
            Passwordname_Entry = Entry(new_tab, textvariable=password_var, width=25)
            Passwordname_Entry.grid(row=2, column=0, padx=10, pady=10) #Entered Password Entry
            Passwordname_Entry.bind('<FocusIn>', focusIn)
            Passwordname_Entry.bind('<FocusOut>', focusOut)
            Username_Entry = Entry(new_tab, textvariable=username_var, width=25)
            Username_Entry.grid(row=3, column=0, padx=10, pady=10) #Entered Username Entry
            Username_Entry.bind('<FocusIn>', focusIn)
            Username_Entry.bind('<FocusOut>', focusOut)
            #Submit, Create New, Delete Tab, Hide/unhide Password, Edit Account Name, Edit Account
            submit = Button(new_tab, text="Submit >", command=lambda: enterAccount())
            submit.grid(row=4, column=0, padx=10, pady=10)
            new_submission = Button(new_tab, text="Add Account", command=lambda: clearAccount())
            new_submission.grid(row=4, column=1, padx=10, pady=10)
            delete_tab = Button(new_tab, text="Delete Tab", command=lambda: deleteTab(tab_title))
            delete_tab.grid(row=8, column=0, padx=10, pady=10)
            delete_account = Button(new_tab, text="Delete Account", command=lambda: deleteAccount())
            delete_account.grid(row=4, column=2, padx=10, pady=10)
            delete_account.grid_remove()
            show_Password = Button(new_tab, text="Hide/unhide Password", command=lambda: unhiddenPass())
            show_Password.grid(row=2, column=1, padx=10, pady=10)
            AccName_button = Button(new_tab, text="Edit account name", command=lambda: editAccountName())
            AccName_button.grid(row=0, column=1, pady=10)
            #Add the new tab to the notebook with the title the user typed in
            notebook.add(new_tab, text=tab_title)
            #Update the tabs dictionary
            tabs[tab_title] = new_tab    
            tab_accounts[tab_title] = []
            #This will sort the tabs in alphabetical order and rearrange them as needed
            sorted_tabs = sorted(tabs.items(), key=lambda x: x[0])
            for title, tab in sorted_tabs:
                notebook.insert("end", tab, text=title)
#Main Notebook----------------------------------------------------------------------------------------
#Create the main application window
myApp = Tk()
myApp.title("Password Manager")
myApp.geometry("745x600")
notebook = ttk.Notebook(myApp)
notebook.pack(fill='both', expand=True)

#Initially create one tab
initial_tab = Frame(notebook)
label = Label(initial_tab, text="Welcome to the Password Manager. Press the 'Create Tab' button to get started or select a website below to add accounts too.")
label.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky=W+E)
notebook.add(initial_tab, text="Homepage")

#Create a new tab
new_tab_button = Button(initial_tab, text="Create New Tab", command=create_new_tab)
new_tab_button.grid(row=1, column=1, pady=10)

#Search for tabs,3 Suggestions from search
search_Entry = Entry(initial_tab, width=35)
search_Entry.insert(0, "Search Tab: ")
search_Entry.grid(row=3, column=1, pady=10, padx=10)
search_Entry.bind('<FocusIn>', focusIn)
search_Entry.bind('<FocusOut>', focusOut)
search_Button = Button(initial_tab, text=">", command=searchTabs).grid(row=3,column=1, sticky=E)
blank = Label(initial_tab, text="").grid(row=4, column=0)#SPACER
example_Sug0 = Button(initial_tab, text="", command=lambda: notebook.select(tabs[example_Sug0.cget("text")]))#.grid(row=5,column=0, pady=5, padx=5)
example_Sug1 = Button(initial_tab, text="", command=lambda: notebook.select(tabs[example_Sug1.cget("text")]))
example_Sug2 = Button(initial_tab, text="", command=lambda: notebook.select(tabs[example_Sug2.cget("text")]))
example_Sug0.grid_forget()
example_Sug1.grid_forget()
example_Sug2.grid_forget()
blank2 = Label(initial_tab, text="").grid(row=6, column=0) #SPACER

#SOCIAL MEDIA SUGGESTIONS: X (Twitter) Instagram Facebook TikTok Snapchat Reddit Discord
socialMedia_Sug = LabelFrame(initial_tab, text="Social Media Suggestions")
socialMedia_Sug.grid(row=7, column=0, pady=10, padx=10)
insta_Sug = Button(socialMedia_Sug, text="Instagram", command=lambda: create_new_tab("Instagram")).grid(row=1,column=1, pady=5, padx=5)
face_Sug = Button(socialMedia_Sug, text="Facebook", command=lambda: create_new_tab("Facebook")).grid(row=1,column=2, pady=5, padx=5)
snap_Sug = Button(socialMedia_Sug, text="SnapChat", command=lambda: create_new_tab("SnapChat")).grid(row=1,column=3, pady=5, padx=5)
discord_Sug = Button(socialMedia_Sug, text="Discord", command=lambda: create_new_tab("Discord")).grid(row=2,column=1, pady=5, padx=5)
twitter_Sug = Button(socialMedia_Sug, text="X/Twitter", command=lambda: create_new_tab("X/Twitter")).grid(row=2,column=2, pady=5, padx=5)

#STREAMING SUGGESTIONS: Netflix Hulu Max Youtube TV+ Disney+ Prime Videos Apple TV+
streaming_Sug = LabelFrame(initial_tab, text="Streaming Suggestions")
streaming_Sug.grid(row=7, column=1, pady=10, padx=10)
netflix_Sug = Button(streaming_Sug, text="Netflix", command=lambda: create_new_tab("Netflix")).grid(row=1,column=1, pady=5, padx=5)
hulu_Sug = Button(streaming_Sug, text="Hulu", command=lambda: create_new_tab("Hulu")).grid(row=1,column=2, pady=5, padx=5)
disney_Sug = Button(streaming_Sug, text="Disney+", command=lambda: create_new_tab("Disney+")).grid(row=1,column=3, pady=5, padx=5)
apple_Sug = Button(streaming_Sug, text="Apple TV+", command=lambda: create_new_tab("Apple TV+")).grid(row=2,column=1, pady=5, padx=5)
prime_Sug = Button(streaming_Sug, text="Prime Videos", command=lambda: create_new_tab("Prime Videos")).grid(row=2,column=2, pady=5, padx=5)

#TRAVEL SUGGESTIONS: Uber Lyft AirBnB Greyhound MegaBus Waze
travel_Sug = LabelFrame(initial_tab, text="Travel Suggestions")
travel_Sug.grid(row=7, column=2, pady=10, padx=10)
uber_Sug = Button(travel_Sug, text="Uber", command=lambda: create_new_tab("Uber")).grid(row=1,column=1, pady=5, padx=5)
lyft_Sug = Button(travel_Sug, text="Lyft", command=lambda: create_new_tab("Lyft")).grid(row=1,column=2, pady=5, padx=5)
greyhound_Sug = Button(travel_Sug, text="Greyhound", command=lambda: create_new_tab("GreyHound")).grid(row=1,column=3, pady=5, padx=5)
megabus_Sug = Button(travel_Sug, text="MegaBus", command=lambda: create_new_tab("MegaBus")).grid(row=2,column=1, pady=5, padx=5)
waze_Sug = Button(travel_Sug, text="Waze", command=lambda: create_new_tab("Waze")).grid(row=2,column=2, pady=5, padx=5)

#Spacer of suggestion
blank2 = Label(initial_tab, text="").grid(row=8, column=0) #SPACER
blank2 = Label(initial_tab, text="").grid(row=9, column=0) #SPACER
blank2 = Label(initial_tab, text="").grid(row=10, column=0) #SPACER

#Prev/Next Tab Buttons
prevTab = Button(myApp, text="<Prev tab", command=prevTab)
prevTab.pack()
nextTab = Button(myApp, text="Next tab >", command=nextTab)
nextTab.pack()
exit = Button(initial_tab, text="Exit", command=lambda: myApp.destroy()).grid(row=11, column=0, padx=10, pady=10, sticky=W)

#Start the Tkinter event loop
myApp.mainloop()