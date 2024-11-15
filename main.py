#=========================Imports=============================
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter.simpledialog import askinteger, askstring
import mysql.connector
#=========================Colors=============================
color1 = "#287094"
color2 = "#d4d4ce"
color3 = "#f6f6f6"
color4 = "#023246"
#=========================Mysql=============================
def Create_Connection():
    connection = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "password",
        database = "subdivisiondb"
    )
    return connection
mydb = Create_Connection()
mycursor = mydb.cursor()
#=========================Functions============================= 
current_user_id = 0
current_user_unit_id = 0
current_user_name = ""
current_user_age = 0
current_user_sex = ""
current_user_phone_number = 0
current_user_move_in_date = ""
temp = 0

#====================Portal Functions=============================
def Show_Login():
    portal_window.pack_forget()
    login_window.pack(pady=100)
def Show_Signup():
    mydb = Create_Connection()
    mycursor = mydb.cursor()
    mycursor.execute("select unit_id from unit")
    myresult = mycursor.fetchall()

    signup_unit_id_combobox_choices = []
    for x in range(len(myresult)):
        signup_unit_id_combobox_choices.append(myresult[x][0])
    signup_unit_id_combobox.config(values=signup_unit_id_combobox_choices)
    portal_window.pack_forget()
    signup_window.pack(pady=100)
#====================Login Functions=============================
def Find_User(myresult):
    found = False
    for x in range(len(myresult)):
        if(int(login_id_entry.get())==myresult[x][0]):
            global current_user_id
            current_user_id = login_id_entry.get()
            found = True
    return found

def Set_Current_User():
    mydb = Create_Connection()
    mycursor = mydb.cursor()
    mycursor.execute(f"select * from occupants where occupant_id = {current_user_id}")
    myresult = mycursor.fetchall()

    global current_user_unit_id
    global current_user_name
    global current_user_age
    global current_user_sex
    global current_user_phone_number
    global current_user_move_in_date
    current_user_unit_id = myresult[0][1]
    current_user_name = myresult[0][2]
    current_user_age = myresult[0][3]
    current_user_sex = myresult[0][4]
    current_user_phone_number = myresult[0][5]
    current_user_move_in_date = myresult[0][6]

    user_id.config(text=f"{current_user_id}")
    user_name.config(text=f"{current_user_name}")
    user_age.config(text=f"{current_user_age}")
    user_sex.config(text=f"{current_user_sex}")
    user_phone_number.config(text=f"{current_user_phone_number}")
    user_unit.config(text=f"{current_user_unit_id}")
    user_move_in_date.config(text=f"{current_user_move_in_date}")

def Login():
    mydb = Create_Connection()
    mycursor = mydb.cursor()
    mycursor.execute("select occupant_id, unit_id, occupant_name from occupants")
    myresult = mycursor.fetchall()
    
    if(login_type_combobox.get()!=""):
        if(login_type_combobox.get()=="User" and Find_User(myresult)):
            Set_Current_User()
            username_tab1_label.config(text=f"{current_user_name}")
            login_window.pack_forget()
            user_window.pack(pady=80)
            mydb
        elif(login_type_combobox.get()=="Admin" and int(login_id_entry.get())==1234):
            login_window.pack_forget()
            admin_window.pack(pady=80)
        else:
            messagebox.showinfo(title="User not found", message="Please check if input was correct")

def Login_Return():
    login_type_combobox.set("")
    login_id_entry.delete(0, END)
    login_window.pack_forget()
    portal_window.pack(pady=100)

#====================Signup Functions=============================

def Signup():
    mydb = Create_Connection()
    mycursor = mydb.cursor()

    try:
        if(signup_radio_var.get()==1):
            signup_sex = "Male"
        else:
            signup_sex = "Female"
        sql = "insert into occupants(occupant_name, occupant_age, occupant_sex, occupant_phone_number, move_in_date, unit_id) values(%s, %s, %s, %s, %s, %s)"
        val = (signup_name_entry.get().title(), signup_age_entry.get(), signup_sex, signup_phone_number_entry.get(), signup_move_in_date_dateentry.get_date(), signup_unit_id_combobox.get())
        mycursor.execute(sql, val)
        mydb.commit()
        messagebox.showinfo("Success", "Signup was successful")
    except:
        messagebox.showerror("Error", "Please fill-up all information properly")

def Signup_Return():
    signup_name_entry.delete(0, END)
    signup_age_entry.delete(0, END)
    signup_phone_number_entry.delete(0, END)
    signup_unit_id_combobox.set("")
    signup_window.pack_forget()
    portal_window.pack(pady=100)
#====================User Functions=============================
def User_Logout():
    try:
        user_bill_window.destroy()
    except:
        pass
    user_bill_id_entry.delete(0, END)
    user_payment_amount_entry.delete(0, END)
    user_payment_method_combobox.set("")
    user_window.pack_forget()
    login_window.pack(pady=100)
def Show_Bills():
    global user_bill_window
    user_bill_window = Tk()
    mydb = Create_Connection()
    mycursor = mydb.cursor()
    
    user_bill_label = Label(user_bill_window, text="Bill ID", font=("raleway", 15))
    user_bill_label.grid(row=0, column=0)
    user_bill_label = Label(user_bill_window, text="Unit ID", font=("raleway", 15))
    user_bill_label.grid(row=0, column=1)
    user_bill_label = Label(user_bill_window, text="Category", font=("raleway", 15))
    user_bill_label.grid(row=0, column=2)
    user_bill_label = Label(user_bill_window, text="Amount", font=("raleway", 15))
    user_bill_label.grid(row=0, column=3)
    user_bill_label = Label(user_bill_window, text="Billing Date", font=("raleway", 15))
    user_bill_label.grid(row=0, column=4)
    user_bill_label = Label(user_bill_window, text="Status", font=("raleway", 15))
    user_bill_label.grid(row=0, column=5)
    
    mycursor.execute(f"select * from bills where unit_id = {current_user_unit_id}")
    myresult = mycursor.fetchall()
    for x in range(len(myresult)):
        for y in range(6):
            user_bills = Label(user_bill_window, text=f"{myresult[x][y]}", font=("raleway", 15))
            user_bills.grid(row=x+1, column=y)
    
    user_bill_window.mainloop()
def User_Payment_Submit():
    try:
        sql = "insert into payment(bill_id, payment_amount, payment_method, payment_date) values(%s, %s, %s, %s)"
        val = (user_bill_id_entry.get(), user_payment_amount_entry.get(), user_payment_method_combobox.get(), user_payment_date_dateentry.get_date())
        mycursor.execute(sql, val)
        mydb.commit()
        messagebox.showinfo("Success", "Payment Successful")
    except:
        messagebox.showerror("Error", "Please fill-up all information properly")

#====================Admin Functions=============================
def Admin_Logout():
    admin_window.pack_forget()
    login_window.pack(pady=100)
def Create():
    admin_window.pack_forget()
    admin_create_window.pack(pady=100)
def Read():
    mydb = Create_Connection()
    mycursor = mydb.cursor()
    mycursor.execute(F"select * from _block")
    myresult = mycursor.fetchall()
    admin_read_block_combobox_choices.clear()
    for x in range(len(myresult)):
        admin_read_block_combobox_choices.append(myresult[x][0])
    admin_read_block_combobox.config(values=admin_read_block_combobox_choices)
    admin_window.pack_forget()
    admin_read_window.pack(pady=100)
def Update():
    mydb = Create_Connection()
    mycursor = mydb.cursor()
    mycursor.execute(F"select * from _block")
    myresult = mycursor.fetchall()
    admin_update_block_combobox_choices.clear()
    for x in range(len(myresult)):
        admin_update_block_combobox_choices.append(myresult[x][0])
    admin_update_block_combobox.config(values=admin_update_block_combobox_choices)
    admin_window.pack_forget()
    admin_update_window.pack(pady=100)
def Delete():
    mydb = Create_Connection()
    mycursor = mydb.cursor()
    mycursor.execute(F"select * from _block")
    myresult = mycursor.fetchall()
    admin_delete_block_combobox_choices.clear()
    for x in range(len(myresult)):
        admin_delete_block_combobox_choices.append(myresult[x][0])
    admin_delete_block_combobox.config(values=admin_delete_block_combobox_choices)
    admin_window.pack_forget()
    admin_delete_window.pack(pady=80)
    
#====================Create Functions=============================
def Set_Block():
    mydb = Create_Connection()
    mycursor = mydb.cursor()
    try:
        sql = ("insert into _block(number_of_units, block_total_area, address) values(%s, %s, %s)")
        val = (add_block_number_of_units.get(), add_block_total_area.get(), add_block_address.get())
        mycursor.execute(sql, val)
        mydb.commit()
        messagebox.showinfo("Success", "Block added successfully")
        Add_Block_Cancel()
    except:
        messagebox.showerror("Error", "Please fill-up information properly")
    
def Add_Block_Cancel():
    add_block_window.destroy()

def Add_Block():
    global add_block_window
    add_block_window = Tk()
    add_block_window.title("Add Block")
    add_block_window.geometry("600x200")

    Label(add_block_window).grid(row=0, column=0)
    Label(add_block_window, text="Enter Details:", font=("raleway", 15, "bold"), fg=color4, width=20).grid(row=1, column=0)

    Label(add_block_window, text="Number of Units:", font=("raleway", 11, "bold"), fg=color4, width=20).grid(row=2, column=0)
    global add_block_number_of_units
    add_block_number_of_units = Entry(add_block_window, font=("raleway", 11, "bold"), fg=color4, width=35)
    add_block_number_of_units.grid(row=2, column=1)

    Label(add_block_window, text="Block Total Area:", font=("raleway", 11, "bold"), fg=color4, width=20).grid(row=3, column=0)
    global add_block_total_area
    add_block_total_area = Entry(add_block_window, font=("raleway", 11, "bold"), fg=color4, width=35)
    add_block_total_area.grid(row=3, column=1)

    Label(add_block_window, text="Address:", font=("raleway", 11, "bold"), fg=color4, width=20).grid(row=4, column=0)
    global add_block_address
    add_block_address = Entry(add_block_window, font=("raleway", 11, "bold"), fg=color4, width=35)
    add_block_address.grid(row=4, column=1)

    Label(add_block_window).grid(row=5, column=0)
    Button(add_block_window, text="Confirm", font=("raleway",8, "bold"), bg=color4, fg=color3, width=8, command=Set_Block).grid(row=6, column=0)
    Button(add_block_window, text="Cancel", font=("raleway",8, "bold"), bg=color4, fg=color3, width=8, command=Add_Block_Cancel).grid(row=6, column=1)

    add_block_window.mainloop()    

def Set_Unit():
    mydb = Create_Connection()
    mycursor = mydb.cursor()
    occupancy_status = ""
    if(add_unit_occupancy_status_combobox.get()=="Occupied"):
        occupancy_status = 1
    else:
        occupancy_status = 0
    try:
        sql = ("insert into unit(block_id, occupancy_status, number_of_floors, unit_total_area) values(%s, %s, %s, %s)")
        val = (add_unit_block_id_combobox.get(), occupancy_status, add_unit_number_of_floors.get(), add_unit_unit_total_area.get())
        mycursor.execute(sql, val)
        mydb.commit()
        messagebox.showinfo("Success", "Unit added successfully")
        Add_Unit_Cancel()
    except:
        messagebox.showerror("Error", "Please fill-up information properly")

def Add_Unit_Cancel():
    add_unit_window.destroy()

def Add_Unit():
    global add_unit_window
    add_unit_window = Tk()
    add_unit_window.title("Add Unit")
    add_unit_window.geometry("600x200")

    mydb = Create_Connection()
    mycursor = mydb.cursor()
    mycursor.execute("select block_id from _block")
    myresult = mycursor.fetchall()

    Label(add_unit_window).grid(row=0, column=0)
    Label(add_unit_window, text="Enter Details:", font=("raleway", 15, "bold"), fg=color4, width=20).grid(row=1, column=0)

    add_unit_block_id_combobox_choices = []
    for x in range(len(myresult)):
        add_unit_block_id_combobox_choices.append(myresult[x][0])

    Label(add_unit_window, text="Block ID:", font=("raleway", 11, "bold"), fg=color4, width=20).grid(row=2, column=0)
    global add_unit_block_id_combobox
    add_unit_block_id_combobox = ttk.Combobox(add_unit_window, font=("raleway", 11, "bold"), width=33, values=add_unit_block_id_combobox_choices, state="readonly")
    add_unit_block_id_combobox.grid(row=2, column=1)

    add_unit_block_id_combobox_choices = ["Occupied", "Not occupied"]
    Label(add_unit_window, text="Occupancy Status:", font=("raleway", 11, "bold"), fg=color4, width=20).grid(row=3, column=0)
    global add_unit_occupancy_status_combobox
    add_unit_occupancy_status_combobox = ttk.Combobox(add_unit_window, font=("raleway", 11, "bold"), width=33, values=add_unit_block_id_combobox_choices, state="readonly")
    add_unit_occupancy_status_combobox.grid(row=3, column=1)

    Label(add_unit_window, text="Number of Floors:", font=("raleway", 11, "bold"), fg=color4, width=20).grid(row=4, column=0)
    global add_unit_number_of_floors
    add_unit_number_of_floors = Entry(add_unit_window, font=("raleway", 11, "bold"), fg=color4, width=35)
    add_unit_number_of_floors.grid(row=4, column=1)

    Label(add_unit_window, text="Unit Total Area:", font=("raleway", 11, "bold"), fg=color4, width=20).grid(row=5, column=0)
    global add_unit_unit_total_area
    add_unit_unit_total_area = Entry(add_unit_window, font=("raleway", 11, "bold"), fg=color4, width=35)
    add_unit_unit_total_area.grid(row=5, column=1)

    Label(add_unit_window).grid(row=6, column=0)
    Button(add_unit_window, text="Confirm", font=("raleway",8, "bold"), bg=color4, fg=color3, width=8, command=Set_Unit).grid(row=7, column=0)
    Button(add_unit_window, text="Cancel", font=("raleway",8, "bold"), bg=color4, fg=color3, width=8, command=Add_Unit_Cancel).grid(row=7, column=1)

    add_unit_window.mainloop()   

def Create_Cancel():
    admin_create_window.pack_forget()
    admin_window.pack(pady=100)

#====================Read Functions=============================
def Set_Read():
    read_confirm_window_block_entry.config(state="normal")
    read_confirm_window_block_entry.delete(0, END)
    read_confirm_window_block_entry.insert(0, admin_read_block_combobox.get())
    read_confirm_window_block_entry.config(state="disabled")
    read_confirm_window_unit_entry.config(state="normal")
    read_confirm_window_unit_entry.delete(0, END)
    read_confirm_window_unit_entry.insert(0, admin_read_unit_combobox.get())
    read_confirm_window_unit_entry.config(state="disabled")

    mydb = Create_Connection()
    mycursor = mydb.cursor()

    global read_confirm_occupants_table
    read_confirm_occupants_table = Frame(read_confirm_window, width=875, height=125, highlightbackground=color4, highlightthickness=2)
    read_confirm_occupants_table.place(x=60, y=210)
    Label(read_confirm_occupants_table, text="ID", font=("raleway", 10, "bold"), fg=color4, width=20).grid(row=0, column=0)
    Label(read_confirm_occupants_table, text="Name", font=("raleway", 10, "bold"), fg=color4, width=20).grid(row=0, column=1)
    Label(read_confirm_occupants_table, text="Age", font=("raleway", 10, "bold"), fg=color4, width=20).grid(row=0, column=2)
    Label(read_confirm_occupants_table, text="Sex", font=("raleway", 10, "bold"), fg=color4, width=20).grid(row=0, column=3)
    Label(read_confirm_occupants_table, text="Phone Number", font=("raleway", 10, "bold"), fg=color4, width=20).grid(row=0, column=4)

    try:
        mycursor.execute(f"SELECT occupant_id, occupant_name, occupant_age, occupant_sex, occupant_phone_number, move_in_date FROM _block join unit  on _block.block_id = unit.block_id join occupants on unit.unit_id = occupants.unit_id where unit.unit_id = {admin_read_unit_combobox.get()}")
        myresult = mycursor.fetchall()
        read_confirm_window_move_in_date_entry.config(state="normal")
        read_confirm_window_move_in_date_entry.delete(0, END)
        read_confirm_window_move_in_date_entry.insert(0, myresult[0][5])
        
        for x in range(len(myresult)):
            for y in range(5):
                Label(read_confirm_occupants_table, text=f"{myresult[x][y]}", font=("raleway", 10, "bold"), fg=color4, width=20).grid(row=x+1, column=y)
    except:
        pass

    global read_confirm_bill_table
    read_confirm_bill_table = Frame(read_confirm_window, width=875, height=125, highlightbackground=color4, highlightthickness=2)
    read_confirm_bill_table.place(x=60, y=390)

    Label(read_confirm_bill_table, text="ID", font=("raleway", 10, "bold"), fg=color4, width=20).grid(row=0, column=0)
    Label(read_confirm_bill_table, text="Category", font=("raleway", 10, "bold"), fg=color4, width=20).grid(row=0, column=1)
    Label(read_confirm_bill_table, text="Amount", font=("raleway", 10, "bold"), fg=color4, width=20).grid(row=0, column=2)
    Label(read_confirm_bill_table, text="Billing Date", font=("raleway", 10, "bold"), fg=color4, width=20).grid(row=0, column=3)
    Label(read_confirm_bill_table, text="Status", font=("raleway", 10, "bold"), fg=color4, width=20).grid(row=0, column=4)

    try: 
        mycursor.execute(f"SELECT bill_id, bill_category, bill_amount, billing_date, bill_status FROM bills where unit_id = {admin_read_unit_combobox.get()}")
        myresult = mycursor.fetchall()
        for x in range(len(myresult)):
            for y in range(5):
                Label(read_confirm_bill_table, text=f"{myresult[x][y]}", font=("raleway", 10, "bold"), fg=color4, width=20).grid(row=x+1, column=y)
    except:
        pass
    read_confirm_window_move_in_date_entry.config(state="disabled")

def Read_Confirm():
    if(admin_read_block_combobox.get()!="" and admin_read_unit_combobox.get()!=""):
        Set_Read()
        admin_read_window.pack_forget()
        read_confirm_window.pack(pady=80)
    else:
        messagebox.showerror("Error", "Please fill-up all information properly")
def Read_Cancel():
    admin_read_block_combobox.set("")
    admin_read_unit_combobox.set("")
    admin_read_window.pack_forget()
    admin_window.pack(pady=100)
def Read_Block_Selected(e):
    admin_read_unit_combobox_choices.clear()
    admin_read_unit_combobox.set("")
    block_selected = admin_read_block_combobox.get()
    mydb = Create_Connection()
    mycursor = mydb.cursor()
    mycursor.execute(F"select * from unit where block_id = {block_selected}")
    myresult = mycursor.fetchall()
    for x in range(len(myresult)):
        admin_read_unit_combobox_choices.append(myresult[x][0])
    admin_read_unit_combobox.config(values=admin_read_unit_combobox_choices)
#====================Read Confirm Functions=============================
def Read_Return():
    read_confirm_bill_table.destroy()
    read_confirm_occupants_table.destroy()
    read_confirm_window.pack_forget()
    admin_read_window.pack(pady=80)

#====================Update Functions=============================

def Set_Update():

    update_confirm_window_block_entry.config(state="normal")
    update_confirm_window_block_entry.delete(0, END)
    update_confirm_window_block_entry.insert(0, admin_update_block_combobox.get())
    update_confirm_window_block_entry.config(state="disabled")
    update_confirm_window_unit_entry.config(state="normal")
    update_confirm_window_unit_entry.delete(0, END)
    update_confirm_window_unit_entry.insert(0, admin_update_unit_combobox.get())
    update_confirm_window_unit_entry.config(state="disabled")

    mydb = Create_Connection()
    mycursor = mydb.cursor()

    global update_confirm_occupants_table
    update_confirm_occupants_table.destroy()
    update_confirm_occupants_table = Frame(update_confirm_window, width=875, height=125, highlightbackground=color4, highlightthickness=2)
    update_confirm_occupants_table.place(x=60, y=210)
    Label(update_confirm_occupants_table, text="ID", font=("raleway", 10, "bold"), fg=color4, width=20).grid(row=0, column=0)
    Label(update_confirm_occupants_table, text="Name", font=("raleway", 10, "bold"), fg=color4, width=20).grid(row=0, column=1)
    Label(update_confirm_occupants_table, text="Age", font=("raleway", 10, "bold"), fg=color4, width=20).grid(row=0, column=2)
    Label(update_confirm_occupants_table, text="Sex", font=("raleway", 10, "bold"), fg=color4, width=20).grid(row=0, column=3)
    Label(update_confirm_occupants_table, text="Phone Number", font=("raleway", 10, "bold"), fg=color4, width=20).grid(row=0, column=4)
    
    try:
        mycursor.execute(f"SELECT occupant_id, occupant_name, occupant_age, occupant_sex, occupant_phone_number, move_in_date FROM _block join unit  on _block.block_id = unit.block_id join occupants on unit.unit_id = occupants.unit_id where unit.unit_id = {admin_update_unit_combobox.get()}")
        myresult = mycursor.fetchall()
        
        update_confirm_window_move_in_date_entry.config(state="normal")
        update_confirm_window_move_in_date_entry.delete(0, END)
        update_confirm_window_move_in_date_entry.insert(0, myresult[0][5])
        
        for x in range(len(myresult)):
            for y in range(5):
                Label(update_confirm_occupants_table, text=f"{myresult[x][y]}", font=("raleway", 10, "bold"), fg=color4, width=20).grid(row=x+1, column=y)
    except:
        pass

    global update_confirm_bill_table
    update_confirm_bill_table.destroy()
    update_confirm_bill_table = Frame(update_confirm_window, width=875, height=125, highlightbackground=color4, highlightthickness=2)
    update_confirm_bill_table.place(x=60, y=390)

    Label(update_confirm_bill_table, text="ID", font=("raleway", 10, "bold"), fg=color4, width=20).grid(row=0, column=0)
    Label(update_confirm_bill_table, text="Category", font=("raleway", 10, "bold"), fg=color4, width=20).grid(row=0, column=1)
    Label(update_confirm_bill_table, text="Amount", font=("raleway", 10, "bold"), fg=color4, width=20).grid(row=0, column=2)
    Label(update_confirm_bill_table, text="Billing Date", font=("raleway", 10, "bold"), fg=color4, width=20).grid(row=0, column=3)
    Label(update_confirm_bill_table, text="Status", font=("raleway", 10, "bold"), fg=color4, width=20).grid(row=0, column=4)

    try: 
        mycursor.execute(f"SELECT bill_id, bill_category, bill_amount, billing_date, bill_status FROM bills where unit_id = {admin_update_unit_combobox.get()}")
        myresult = mycursor.fetchall()
        for x in range(len(myresult)):
            for y in range(5):
                Label(update_confirm_bill_table, text=f"{myresult[x][y]}", font=("raleway", 10, "bold"), fg=color4, width=20).grid(row=x+1, column=y)
    except:
        pass
    update_confirm_window_move_in_date_entry.config(state="disabled")

def Update_Confirm():
    if(admin_update_block_combobox.get()!="" and admin_update_unit_combobox.get()!=""):
        Set_Update()
        admin_update_window.pack_forget()
        update_confirm_window.pack(pady=80)
    else:
        messagebox.showerror("Error", "Please fill-up all information properly")

def Update_Cancel():
    admin_update_block_combobox.set("")
    admin_update_unit_combobox.set("")
    admin_update_window.pack_forget()
    admin_window.pack(pady=100)

def Update_Block_Selected(e):
    admin_update_unit_combobox_choices.clear()
    admin_update_unit_combobox.set("")
    block_selected = admin_update_block_combobox.get()
    mydb = Create_Connection()
    mycursor = mydb.cursor()
    mycursor.execute(F"select * from unit where block_id = {block_selected}")
    myresult = mycursor.fetchall()
    for x in range(len(myresult)):
        admin_update_unit_combobox_choices.append(myresult[x][0])
    admin_update_unit_combobox.config(values=admin_update_unit_combobox_choices)

#====================Update Confirm Functions=============================
def Update_Return():

    update_confirm_bill_table.destroy()
    update_confirm_occupants_table.destroy()
    update_confirm_window.pack_forget()
    admin_update_window.pack(pady=80)
    
def Add_Occupant_Confirm():
    mydb = Create_Connection()
    mycursor = mydb.cursor()

    if(add_occupant_radio_var.get()==1):
        occupant_sex = "Male"
    elif(add_occupant_radio_var.get()==2):
        occupant_sex = "Female"
    try: 
        sql = "insert into occupants(unit_id, occupant_name, occupant_age, occupant_sex, occupant_phone_number, move_in_date) values(%s, %s, %s, %s, %s, %s)"
        val = (update_confirm_window_unit_entry.get(), add_occupant_name.get().title(), add_occupant_age.get(), occupant_sex, add_occupant_phone_number.get(), add_occupant_move_in_date.get())
        mycursor.execute(sql, val)
        mydb.commit()
        messagebox.showinfo("Success", "Occupant added successfully")
        add_occupant_window.destroy()
        Set_Update()
    except:
        messagebox.showerror("Error", "Please fill up information properly")

def Add_Occupant_Cancel():
    add_occupant_window.destroy()

def Add_Occupant():
    global add_occupant_window
    add_occupant_window = Toplevel()
    add_occupant_window.geometry("550x350")
    add_occupant_window.title("Add Occupant")

    Label(add_occupant_window).grid(row=0, column=0)
    Label(add_occupant_window, text="Enter Details:", font=("raleway", 15, "bold"), fg=color4, width=20).place(x=60, y=60)

    Label(add_occupant_window, text="Name:", font=("raleway", 11, "bold"), fg=color4, width=20).place(x=48, y=100)
    global add_occupant_name
    add_occupant_name = Entry(add_occupant_window, font=("raleway", 11, "bold"), fg=color4, width=26)
    add_occupant_name.place(x=200, y=100)

    Label(add_occupant_window, text="Age:", font=("raleway", 11, "bold"), fg=color4, width=20).place(x=45, y=140)
    global add_occupant_age
    add_occupant_age = Entry(add_occupant_window, font=("raleway", 11, "bold"), fg=color4, width=26)
    add_occupant_age.place(x=200, y=140)

    Label(add_occupant_window, text="Sex:", font=("raleway", 11, "bold"), fg=color4, width=20).place(x=45, y=180)
    global add_occupant_radio_var
    global add_occupant_r1
    global add_occupant_r2
    add_occupant_radio_var = IntVar()
    add_occupant_r1 = Radiobutton(add_occupant_window, text="Male", variable=add_occupant_radio_var, value=1, font=("raleway", 11, "bold"), fg=color4)
    add_occupant_r1.place(x=200, y=180)
    add_occupant_r2 =Radiobutton(add_occupant_window, text="Female", variable=add_occupant_radio_var, value=2, font=("raleway", 11, "bold"), fg=color4)
    add_occupant_r2.place(x=280, y=180)

    Label(add_occupant_window, text="Phone Number:", font=("raleway", 11, "bold"), fg=color4, width=20).place(x=83, y=220)
    global add_occupant_phone_number
    add_occupant_phone_number = Entry(add_occupant_window, font=("raleway", 11, "bold"), fg=color4, width=20)
    add_occupant_phone_number.place(x=250, y=220)    
    
    Label(add_occupant_window, text="Move-in-date:", font=("raleway", 11, "bold"), fg=color4, width=20).place(x=83, y=260)
    global add_occupant_move_in_date
    add_occupant_move_in_date = Entry(add_occupant_window, font=("raleway", 11, "bold"), fg=color4, width=20)
    add_occupant_move_in_date.delete(0, END)
    
    add_occupant_move_in_date.insert(0, f"{update_confirm_window_move_in_date_entry.get()}")
    add_occupant_move_in_date.place(x=250, y=260)    

    if(len(add_occupant_move_in_date.get())>1):
        add_occupant_move_in_date.config(state="disabled")

    Button(add_occupant_window, text="Confirm", font=("raleway",8, "bold"), bg=color4, fg=color3, width=8, command=Add_Occupant_Confirm).place(x=200, y=300)    
    Button(add_occupant_window, text="Cancel", font=("raleway",8, "bold"), bg=color4, fg=color3, width=8, command=Add_Occupant_Cancel).place(x=280, y=300)    

    add_occupant_window.mainloop()

def Add_Bill_Confirm():
    mydb = Create_Connection()
    mycursor = mydb.cursor()

    bill_status = 2
    if(add_bill_bill_status.get()=="Paid"):
        bill_status = 1
    else:
        bill_status = 0

    try: 
        sql = "insert into bills(unit_id, bill_category, bill_amount, billing_date, bill_status) values(%s, %s, %s, %s, %s)"
        val = (update_confirm_window_unit_entry.get(), add_bill_category.get().capitalize(), add_bill_amount.get(), add_bill_billing_date.get_date(), bill_status)
        mycursor.execute(sql, val)
        mydb.commit()
        messagebox.showinfo("Success", "Bill added successfully")
        Set_Update()
        add_bill_window.destroy()
    except:
        messagebox.showerror("Error", "Please fill up information properly")

def Add_Bill_Cancel():
    add_bill_window.destroy()

def Add_Bill():
    global add_bill_window
    add_bill_window = Tk()
    add_bill_window.geometry("550x350")
    add_bill_window.title("Add Bill")

    Label(add_bill_window).grid(row=0, column=0)
    Label(add_bill_window, text="Enter Details:", font=("raleway", 15, "bold"), fg=color4, width=20).place(x=60, y=60)

    Label(add_bill_window, text="Category:", font=("raleway", 11, "bold"), fg=color4, width=20).place(x=60, y=100)
    global add_bill_category
    add_bill_category = Entry(add_bill_window, font=("raleway", 11, "bold"), fg=color4, width=26)
    add_bill_category.place(x=200, y=100)

    Label(add_bill_window, text="Amount:", font=("raleway", 11, "bold"), fg=color4, width=20).place(x=58, y=140)
    global add_bill_amount
    add_bill_amount = Entry(add_bill_window, font=("raleway", 11, "bold"), fg=color4, width=26)
    add_bill_amount.place(x=200, y=140)

    Label(add_bill_window, text="Billing Date:", font=("raleway", 11, "bold"), fg=color4, width=20).place(x=60, y=180)
    global add_bill_billing_date
    add_bill_billing_date = DateEntry(add_bill_window, date_pattern = "yyyy-mm-dd", font=("raleway", 11, "bold"), fg=color4, width=20)
    add_bill_billing_date.place(x=200, y=180)    

    Label(add_bill_window, text="Status:", font=("raleway", 11, "bold"), fg=color4, width=20).place(x=60, y=220)
    global add_bill_bill_status
    add_bill_bill_status_choices = ["Paid", "Unpaid"]
    add_bill_bill_status = ttk.Combobox(add_bill_window, values=add_bill_bill_status_choices, font=("raleway", 11, "bold"), width=20, state="readonly")
    add_bill_bill_status.place(x=200, y=220)    

    Button(add_bill_window, text="Confirm", font=("raleway",8, "bold"), bg=color4, fg=color3, width=8, command=Add_Bill_Confirm).place(x=200, y=300)    
    Button(add_bill_window, text="Cancel", font=("raleway",8, "bold"), bg=color4, fg=color3, width=8, command=Add_Bill_Cancel).place(x=280, y=300)    

    add_bill_window.mainloop()

def Update_Occupant_Confirm():
    mydb = Create_Connection()
    mycursor = mydb.cursor()

    try: 
        sql = f"update occupants set occupant_age = %s, occupant_phone_number = %s where occupant_id = %s"
        val = (update_occupant_age.get(), update_occupant_phone_number.get(), occupant_id)
        mycursor.execute(sql, val)
        mydb.commit()
        messagebox.showinfo("Success", "Occupant updated successfully")
        update_occupant_window.destroy()
        Set_Update()
    except:
        messagebox.showerror("Error", "Please fill up information properly")
def Update_Occupant_Cancel():
    update_occupant_window.destroy()

def Update_Occupant():
    mydb = Create_Connection()
    mycursor = mydb.cursor()
    mycursor.execute(f"select * from occupants where unit_id = {update_confirm_window_unit_entry.get()}")
    myresult = mycursor.fetchall()

    global occupant_id
    occupant_id = askinteger("Update Occupant", "Enter Occupant ID")

    found = False
    for x in range(len(myresult)):
        if(int(myresult[x][0])==occupant_id):
            found = True
            global temp
            temp = x

    if(found):
        global update_occupant_window
        update_occupant_window = Toplevel()
        update_occupant_window.geometry("550x350")
        update_occupant_window.title("Update Occupant")

        Label(update_occupant_window).grid(row=0, column=0)
        Label(update_occupant_window, text="Enter Details:", font=("raleway", 15, "bold"), fg=color4, width=20).place(x=60, y=60)

        Label(update_occupant_window, text="Name:", font=("raleway", 11, "bold"), fg=color4, width=20).place(x=48, y=100)
        global update_occupant_name
        update_occupant_name = Entry(update_occupant_window, font=("raleway", 11, "bold"), fg=color4, width=26)
        update_occupant_name.insert(0, f"{myresult[temp][2]}")
        update_occupant_name.config(state="disabled")
        update_occupant_name.place(x=200, y=100)

        Label(update_occupant_window, text="Age:", font=("raleway", 11, "bold"), fg=color4, width=20).place(x=45, y=140)
        global update_occupant_age
        update_occupant_age = Entry(update_occupant_window, font=("raleway", 11, "bold"), fg=color4, width=26)
        update_occupant_age.place(x=200, y=140)
        update_occupant_age.insert(0, f"{myresult[temp][3]}")

        Label(update_occupant_window, text="Sex:", font=("raleway", 11, "bold"), fg=color4, width=20).place(x=45, y=180)
        global update_occupant_radio_var
        global update_occupant_r1
        global update_occupant_r2
        update_occupant_radio_var = IntVar()
        update_occupant_r1 = Radiobutton(update_occupant_window, text="Male", variable=update_occupant_radio_var, value=1, font=("raleway", 11, "bold"), fg=color4)
        update_occupant_r1.place(x=200, y=180)
        update_occupant_r2 =Radiobutton(update_occupant_window, text="Female", variable=update_occupant_radio_var, value=2, font=("raleway", 11, "bold"), fg=color4)
        update_occupant_r2.place(x=280, y=180)
        if(myresult[temp][4]=="Male"):
            update_occupant_r1.select()
        else:
            update_occupant_r2.select()
        update_occupant_r1.config(state="disabled")
        update_occupant_r2.config(state="disabled")

        Label(update_occupant_window, text="Phone Number:", font=("raleway", 11, "bold"), fg=color4, width=20).place(x=83, y=220)
        global update_occupant_phone_number
        update_occupant_phone_number = Entry(update_occupant_window, font=("raleway", 11, "bold"), fg=color4, width=20)
        update_occupant_phone_number.place(x=250, y=220)    
        update_occupant_phone_number.insert(0, f"{myresult[temp][5]}")
        
        Label(update_occupant_window, text="Move-in-date:", font=("raleway", 11, "bold"), fg=color4, width=20).place(x=83, y=260)
        global update_occupant_move_in_date
        update_occupant_move_in_date = Entry(update_occupant_window, font=("raleway", 11, "bold"), fg=color4, width=20)
        update_occupant_move_in_date.delete(0, END)
        
        update_occupant_move_in_date.insert(0, f"{update_confirm_window_move_in_date_entry.get()}")
        update_occupant_move_in_date.place(x=250, y=260)    
        update_occupant_move_in_date.config(state="disabled")

        Button(update_occupant_window, text="Confirm", font=("raleway",8, "bold"), bg=color4, fg=color3, width=8, command=Update_Occupant_Confirm).place(x=200, y=300)    
        Button(update_occupant_window, text="Cancel", font=("raleway",8, "bold"), bg=color4, fg=color3, width=8, command=Update_Occupant_Cancel).place(x=280, y=300)    

        update_occupant_window.mainloop()
    else:
        messagebox.showinfo("Occupant not found", "Please check the inputted value")

def Update_Bill_Confirm():
    mydb = Create_Connection()
    mycursor = mydb.cursor()

    bill_status = 2
    if(update_bill_bill_status.get()=="Paid"):
        bill_status = 1
    else:
        bill_status = 0
    try: 
        sql = f"update bills set bill_status = %s where bill_id = %s"
        val = (bill_status, bill_id)
        mycursor.execute(sql, val)
        mydb.commit()
        messagebox.showinfo("Success", "Bill updated successfully")
        update_bill_window.destroy()
        Set_Update()
    except:
        messagebox.showerror("Error", "Please fill up information properly")

def Update_Bill_Cancel():
    update_bill_window.destroy()

def Update_Bill():
    mydb = Create_Connection()
    mycursor = mydb.cursor()
    mycursor.execute(f"select * from bills where unit_id = {update_confirm_window_unit_entry.get()}")
    myresult = mycursor.fetchall()

    global bill_id
    bill_id = askinteger("Update Bill", "Enter Bill ID")

    found = False
    for x in range(len(myresult)):
        if(int(myresult[x][0])==bill_id):
            found = True
            global temp
            temp = x
    if(found):
        global update_bill_window
        update_bill_window = Tk()
        update_bill_window.geometry("550x350")
        update_bill_window.title("Update Bill")

        Label(update_bill_window).grid(row=0, column=0)
        Label(update_bill_window, text="Enter Details:", font=("raleway", 15, "bold"), fg=color4, width=20).place(x=60, y=60)

        Label(update_bill_window, text="Category:", font=("raleway", 11, "bold"), fg=color4, width=20).place(x=60, y=100)
        global update_bill_category
        update_bill_category = Entry(update_bill_window, font=("raleway", 11, "bold"), fg=color4, width=26)
        update_bill_category.place(x=200, y=100)
        update_bill_category.insert(0, f"{myresult[temp][2]}")
        update_bill_category.config(state="disabled")

        Label(update_bill_window, text="Amount:", font=("raleway", 11, "bold"), fg=color4, width=20).place(x=58, y=140)
        global update_bill_amount
        update_bill_amount = Entry(update_bill_window, font=("raleway", 11, "bold"), fg=color4, width=26)
        update_bill_amount.place(x=200, y=140)
        update_bill_amount.insert(0, f"{myresult[temp][3]}")
        update_bill_amount.config(state="disabled")

        Label(update_bill_window, text="Billing Date:", font=("raleway", 11, "bold"), fg=color4, width=20).place(x=60, y=180)
        global update_bill_billing_date
        update_bill_billing_date = Entry(update_bill_window, font=("raleway", 11, "bold"), fg=color4, width=26)
        update_bill_billing_date.place(x=200, y=180)  
        update_bill_billing_date.insert(0, f"{myresult[temp][4]}")
        update_bill_billing_date.config(state="disabled")

        Label(update_bill_window, text="Status:", font=("raleway", 11, "bold"), fg=color4, width=20).place(x=60, y=220)
        global update_bill_bill_status
        update_bill_bill_status_choices = ["Paid", "Unpaid"]
        update_bill_bill_status = ttk.Combobox(update_bill_window, values=update_bill_bill_status_choices, font=("raleway", 11, "bold"), width=20, state="readonly")
        update_bill_bill_status.place(x=200, y=220)  
        if(int(myresult[temp][5])==1):
            update_bill_bill_status.set("Paid")
        else:
            update_bill_bill_status.set("Unpaid")

        Button(update_bill_window, text="Confirm", font=("raleway",8, "bold"), bg=color4, fg=color3, width=8, command=Update_Bill_Confirm).place(x=200, y=300)    
        Button(update_bill_window, text="Cancel", font=("raleway",8, "bold"), bg=color4, fg=color3, width=8, command=Update_Bill_Cancel).place(x=280, y=300)    

        update_bill_window.mainloop()
    else:
        messagebox.showinfo("Occupant not found", "Please check the inputted value")

#====================Delete Functions=============================
def Set_Delete():
    delete_confirm_window_block_entry.config(state="normal")
    delete_confirm_window_block_entry.delete(0, END)
    delete_confirm_window_block_entry.insert(0, admin_delete_block_combobox.get())
    delete_confirm_window_block_entry.config(state="disabled")
    delete_confirm_window_unit_entry.config(state="normal")
    delete_confirm_window_unit_entry.delete(0, END)
    delete_confirm_window_unit_entry.insert(0, admin_delete_unit_combobox.get())
    delete_confirm_window_unit_entry.config(state="disabled")

    mydb = Create_Connection()
    mycursor = mydb.cursor()

    global delete_confirm_occupants_table
    delete_confirm_occupants_table.destroy()
    delete_confirm_occupants_table = Frame(delete_confirm_window, width=875, height=125, highlightbackground=color4, highlightthickness=2)
    delete_confirm_occupants_table.place(x=60, y=210)
    Label(delete_confirm_occupants_table, text="ID", font=("raleway", 10, "bold"), fg=color4, width=20).grid(row=0, column=0)
    Label(delete_confirm_occupants_table, text="Name", font=("raleway", 10, "bold"), fg=color4, width=20).grid(row=0, column=1)
    Label(delete_confirm_occupants_table, text="Age", font=("raleway", 10, "bold"), fg=color4, width=20).grid(row=0, column=2)
    Label(delete_confirm_occupants_table, text="Sex", font=("raleway", 10, "bold"), fg=color4, width=20).grid(row=0, column=3)
    Label(delete_confirm_occupants_table, text="Phone Number", font=("raleway", 10, "bold"), fg=color4, width=20).grid(row=0, column=4)

    try:
        mycursor.execute(f"SELECT occupant_id, occupant_name, occupant_age, occupant_sex, occupant_phone_number, move_in_date FROM _block join unit  on _block.block_id = unit.block_id join occupants on unit.unit_id = occupants.unit_id where unit.unit_id = {admin_delete_unit_combobox.get()}")
        myresult = mycursor.fetchall()

        delete_confirm_window_move_in_date_entry.config(state="normal")
        delete_confirm_window_move_in_date_entry.delete(0, END)
        delete_confirm_window_move_in_date_entry.insert(0, myresult[0][5])
        
        for x in range(len(myresult)):
            for y in range(5):
                Label(delete_confirm_occupants_table, text=f"{myresult[x][y]}", font=("raleway", 10, "bold"), fg=color4, width=20).grid(row=x+1, column=y)
    except:
        pass

    global delete_confirm_bill_table
    delete_confirm_bill_table.destroy()
    delete_confirm_bill_table = Frame(delete_confirm_window, width=875, height=125, highlightbackground=color4, highlightthickness=2)
    delete_confirm_bill_table.place(x=60, y=390)

    Label(delete_confirm_bill_table, text="ID", font=("raleway", 10, "bold"), fg=color4, width=20).grid(row=0, column=0)
    Label(delete_confirm_bill_table, text="Category", font=("raleway", 10, "bold"), fg=color4, width=20).grid(row=0, column=1)
    Label(delete_confirm_bill_table, text="Amount", font=("raleway", 10, "bold"), fg=color4, width=20).grid(row=0, column=2)
    Label(delete_confirm_bill_table, text="Billing Date", font=("raleway", 10, "bold"), fg=color4, width=20).grid(row=0, column=3)
    Label(delete_confirm_bill_table, text="Status", font=("raleway", 10, "bold"), fg=color4, width=20).grid(row=0, column=4)

    try: 
        mycursor.execute(f"SELECT bill_id, bill_category, bill_amount, billing_date, bill_status FROM bills where unit_id = {admin_delete_unit_combobox.get()}")
        myresult = mycursor.fetchall()

        for x in range(len(myresult)):
            for y in range(5):
                Label(delete_confirm_bill_table, text=f"{myresult[x][y]}", font=("raleway", 10, "bold"), fg=color4, width=20).grid(row=x+1, column=y)
    except:
        pass
    delete_confirm_window_move_in_date_entry.config(state="disabled")

def Delete_Confirm():
    if(admin_delete_block_combobox.get()!="" and admin_delete_unit_combobox.get()!=""):
        Set_Delete()
        admin_delete_window.pack_forget()
        delete_confirm_window.pack(pady=80)
    else:
        messagebox.showerror("Error", "Please fill-up all information properly")
def Delete_Cancel():
    admin_delete_block_combobox.set("")
    admin_delete_unit_combobox.set("")
    admin_delete_window.pack_forget()
    admin_window.pack(pady=100)
def Delete_Block_Selected(e):
    admin_delete_unit_combobox_choices.clear()
    admin_delete_unit_combobox.set("")
    block_selected = admin_delete_block_combobox.get()
    mydb = Create_Connection()
    mycursor = mydb.cursor()
    mycursor.execute(F"select * from unit where block_id = {block_selected}")
    myresult = mycursor.fetchall()

    for x in range(len(myresult)):
        admin_delete_unit_combobox_choices.append(myresult[x][0])
    admin_delete_unit_combobox.config(values=admin_delete_unit_combobox_choices)

#====================Delete Confirm Functions=============================
def Delete_Return():
    delete_confirm_bill_table.destroy()
    delete_confirm_occupants_table.destroy()
    delete_confirm_window.pack_forget()
    admin_delete_window.pack(pady=80)
    
def Delete_Occupant_Confirm():
    mydb = Create_Connection()
    mycursor = mydb.cursor()
    try:
        mycursor.execute(f"delete from occupants where occupant_id = {delete_occupant_id_combobox.get()}")
        mydb.commit()
        messagebox.showinfo("Success", "Occupant deleted successfully")
        delete_confirm_occupants_table.destroy()
        delete_occupant_window.destroy()
        Set_Delete()
    except:
        messagebox.showerror("Error", "Please fill-up all information properly")

def Delete_Occupant_Cancel():
    delete_occupant_window.destroy()
def Delete_Occupant():
    global delete_occupant_window
    delete_occupant_window = Tk()
    delete_occupant_window.geometry("550x200")
    delete_occupant_window.title("Delete Occupant")

    Label(delete_occupant_window, text="Occupant ID:", font=("raleway", 11, "bold"), fg=color4, width=20).place(x=60, y=60)
    global delete_occupant_id_combobox
    
    mydb = Create_Connection()
    mycursor = mydb.cursor()
    mycursor.execute(f"select occupant_id from occupants where unit_id = {delete_confirm_window_unit_entry.get()}")
    myresult = mycursor.fetchall()

    delete_occupant_id_combobox_choices = []
    for x in range(len(myresult)):
        delete_occupant_id_combobox_choices.append(myresult[x][0])
    delete_occupant_id_combobox = ttk.Combobox(delete_occupant_window, font=("raleway", 11, "bold"), width=26, values=delete_occupant_id_combobox_choices, state="readonly")
    delete_occupant_id_combobox.place(x=220, y=60)

    Button(delete_occupant_window, text="Confirm", font=("raleway",8, "bold"), bg=color4, fg=color3, width=8, command=Delete_Occupant_Confirm).place(x=220, y=100)    
    Button(delete_occupant_window, text="Cancel", font=("raleway",8, "bold"), bg=color4, fg=color3, width=8, command=Delete_Occupant_Cancel).place(x=300, y=100)    

    delete_occupant_window.mainloop()

def Delete_Bill_Confirm():
    mydb = Create_Connection()
    mycursor = mydb.cursor()
    try:
        try:
            mycursor.execute(f"delete from payment where bill_id = {delete_bill_id_combobox.get()}")
            mydb.commit()
        except:
            pass
        mycursor.execute(f"delete from bills where bill_id = {delete_bill_id_combobox.get()}")
        mydb.commit()
        messagebox.showinfo("Success", "bill deleted successfully")
        delete_confirm_bill_table.destroy()
        delete_bill_window.destroy()
        Set_Delete()
    except:
        messagebox.showerror("Error", "Please fill-up all information properly")

def Delete_Bill_Cancel():
    delete_bill_window.destroy()

def Delete_Bill():
    global delete_bill_window
    delete_bill_window = Tk()
    delete_bill_window.geometry("550x200")
    delete_bill_window.title("Delete Bill")

    Label(delete_bill_window, text="Bill ID:", font=("raleway", 11, "bold"), fg=color4, width=20).place(x=60, y=60)
    global delete_bill_id_combobox
    
    mydb = Create_Connection()
    mycursor = mydb.cursor()
    mycursor.execute(f"select bill_id from bills where unit_id = {delete_confirm_window_unit_entry.get()}")
    myresult = mycursor.fetchall()

    delete_bill_id_combobox_choices = []
    for x in range(len(myresult)):
        delete_bill_id_combobox_choices.append(myresult[x][0])
    delete_bill_id_combobox = ttk.Combobox(delete_bill_window, font=("raleway", 11, "bold"), width=26, values=delete_bill_id_combobox_choices, state="readonly")
    delete_bill_id_combobox.place(x=220, y=60)

    Button(delete_bill_window, text="Confirm", font=("raleway",8, "bold"), bg=color4, fg=color3, width=8, command=Delete_Bill_Confirm).place(x=220, y=100)    
    Button(delete_bill_window, text="Cancel", font=("raleway",8, "bold"), bg=color4, fg=color3, width=8, command=Delete_Bill_Cancel).place(x=300, y=100)    

    delete_bill_window.mainloop()

#=========================Initialization=============================
root = Tk()
root.geometry("1280x720")
root.title("Subdivision Management System")
background_picture = PhotoImage(file="bg4.png")
background = Label(root, image=background_picture)
background.pack(fill="both", expand=True, anchor="center")

#=========================Portal=============================
portal_window = Frame(background, width=550, height=500)
portal_window.pack(pady=100)

portal_label = Label(portal_window, text="PORTAL", font=("raleway", 50, "bold"), fg=color4).place(relx= 0.5, y=150, anchor="center")

login_button = Button(portal_window, text="Login", font=("raleway",14, "bold"), bg=color4, fg=color3, width=10, command=Show_Login).place(relx= 0.5, y=250, anchor="center")

signup_button = Button(portal_window, text="Signup", font=("raleway",14, "bold"), bg=color4, fg=color3, width=10, command=Show_Signup).place(relx= 0.5, y=300, anchor="center")
#=========================Login Window=============================
login_window = Frame(background, width=550, height=500)
#login_window.pack(pady=100)
login_label = Label(login_window, text="Login", font=("raleway", 45, "bold"), fg=color4).place(relx= 0.5, y=150, anchor="center")

login_type_combobox_label = Label(login_window, text="Login as:", font=("raleway", 11, "bold"), fg=color4).place(x=130, y=220)
login_type_choices = ["User", "Admin"]
login_type_combobox = ttk.Combobox(login_window, text="Name:", font=("raleway", 11, "bold"), state="readonly", width=33, values=login_type_choices)
login_type_combobox.place(x=130, y=250)

login_id_label = Label(login_window, text="ID:", font=("raleway", 11, "bold"), fg=color4).place(x=130, y=280)
login_id_entry = Entry(login_window, width=34, font=("raleway", 11), fg=color4)
login_id_entry.place(x=130, y=310)

login_button = Button(login_window, text="Login", font=("raleway",11, "bold"), bg=color4, fg=color3, width=30, command=Login).place(x=130, y=350)

return_button = Button(login_window, text="Return", font=("raleway",11, "bold"), bg=color4, fg=color3, width=8, command=Login_Return).place(x=450, y=20)
#=========================Signup Window=============================
signup_window = Frame(background, width=550, height=500)
#signup_window.pack(pady=100)
Label(signup_window, text="Signup", font=("raleway", 20, "bold"), fg=color4).place(x=40, y=50)

Label(signup_window, text="Name:", font=("raleway", 11, "bold"), fg=color4).place(x=60, y=120)
signup_name_entry = Entry(signup_window, width=35, font=("raleway", 11), fg=color4)
signup_name_entry.place(x=60, y=150)

Label(signup_window, text="Age:", font=("raleway", 11, "bold"), fg=color4).place(x=400, y=120)
signup_age_entry = Entry(signup_window, width=5, font=("raleway", 11), fg=color4)
signup_age_entry.place(x=400, y=150)

signup_sex_label = Label(signup_window, text="Sex:", font=("raleway", 11, "bold"), fg=color4).place(x=60, y=190)
signup_radio_var = IntVar()
r1 = Radiobutton(signup_window, text="Male", variable=signup_radio_var, value=1, font=("raleway", 11), fg=color4 )
r1.place(x=60, y=220)
r2 = Radiobutton(signup_window, text="Female", variable=signup_radio_var, value=2, font=("raleway", 11), fg=color4)
r2.place(x=120, y=220)

Label(signup_window, text="Phone Number:", font=("raleway", 11, "bold"), fg=color4).place(x=60, y=260)
signup_phone_number_entry = Entry(signup_window, width=24, font=("raleway", 11), fg=color4)
signup_phone_number_entry.place(x=60, y=290)

Label(signup_window, text="Move-in-date:", font=("raleway", 11, "bold"), fg=color4).place(x=60, y=330)
signup_move_in_date_dateentry = DateEntry(signup_window, date_pattern = "yyyy-mm-dd", font=("raleway", 11, "bold"), fg=color4)
signup_move_in_date_dateentry.place(x=60, y=360)

Label(signup_window, text="Unit ID:", font=("raleway", 11, "bold"), fg=color4).place(x=400, y=190)
signup_unit_id_combobox = ttk.Combobox(signup_window, font=("raleway", 11, "bold"), width=5, state="readonly")
signup_unit_id_combobox.place(x=400, y=220)

signup_button = Button(signup_window, text="Signup", font=("raleway",11, "bold"), bg=color4, fg=color3, width=45, command=Signup).place(x=60, y=410)
return_button = Button(signup_window, text="Return", font=("raleway",11, "bold"), bg=color4, fg=color3, width=8, command=Signup_Return).place(x=450, y=20)

#=========================User Window=============================
user_window = Frame(background, width=1000, height=800)
#user_window.pack(pady=80)

user_notebook = ttk.Notebook(user_window, width=900, height=450)
user_tab_1 = Frame(user_notebook)
user_tab_2 = Frame(user_notebook)
user_tab_3 = Frame(user_notebook)

user_notebook.add(user_tab_1, text="Home")
user_notebook.add(user_tab_2, text="Ocupant Details")
user_notebook.add(user_tab_3, text="Bills & Payments")
user_notebook.place(relx=0.5, rely=0.5, anchor="center")

user_tab1_label = Label(user_tab_1, text="Welcome", font=("raleway", 90, "bold"), fg=color4).place(relx=0.5, rely=0.5, anchor="center")
username_tab1_label = Label(user_tab_1, text="", font=("raleway", 20, "bold"), fg=color4)
username_tab1_label.place(relx=0.5, y=300, anchor="center")
user_tab2_label = Label(user_tab_2, text="Occupant Details:", font=("raleway", 20, "bold"), fg=color4).place(x=60, y=60)

user_id_label = Label(user_tab_2, text="ID:", font=("raleway", 18, "bold"), fg=color4).place(x=90, y=110)
user_id = Label(user_tab_2, text="placeholder", font=("raleway", 18), fg=color4)
user_id.place(x=180, y=110)

user_name_label = Label(user_tab_2, text="Name:", font=("raleway", 18, "bold"), fg=color4).place(x=90, y=150)
user_name = Label(user_tab_2, text="placeholder", font=("raleway", 18), fg=color4)
user_name.place(x=180, y=150)

user_age_label = Label(user_tab_2, text="Age:", font=("raleway", 18, "bold"), fg=color4).place(x=90, y=190)
user_age = Label(user_tab_2, text="placeholder", font=("raleway", 18), fg=color4)
user_age.place(x=180, y=190)

user_sex_label = Label(user_tab_2, text="Sex:", font=("raleway", 18, "bold"), fg=color4).place(x=90, y=230)
user_sex = Label(user_tab_2, text="placeholder", font=("raleway", 18), fg=color4)
user_sex.place(x=180, y=230)

user_phone_number_label = Label(user_tab_2, text="Phone Number:", font=("raleway", 18, "bold"), fg=color4).place(x=90, y=270)
user_phone_number = Label(user_tab_2, text="placeholder", font=("raleway", 18), fg=color4)
user_phone_number.place(x=300, y=270)

user_unit_label = Label(user_tab_2, text="Unit:", font=("raleway", 18, "bold"), fg=color4).place(x=550, y=110)
user_unit = Label(user_tab_2, text="placeholder", font=("raleway", 18), fg=color4)
user_unit.place(x=640, y=110)

user_move_in_date_label = Label(user_tab_2, text="Move-in-date:", font=("raleway", 18, "bold"), fg=color4).place(x=550, y=150)
user_move_in_date = Label(user_tab_2, text="placeholder", font=("raleway", 18), fg=color4)
user_move_in_date.place(x=550, y=190)

user_tab3_label = Label(user_tab_3, text="Bills & Payments", font=("raleway", 20, "bold"), fg=color4).place(x=60, y=60)

user_tab3_frame = Frame(user_tab_3, width=730, height=300, highlightbackground=color4, highlightthickness=2)
user_tab3_frame.place(x=80, y=110)

user_show_bills_label = Label(user_tab3_frame, text="Bills:", font=("raleway", 18, "bold"), fg=color4).place(x=30, y=10)
user_show_bills_button = Button(user_tab3_frame, text="Show Bills", font=("raleway",9, "bold"), bg=color4, fg=color3, width=8, command=Show_Bills)
user_show_bills_button.place(x=110, y=15)

user_tab3_divider = Frame(user_tab3_frame, width=900, height=2, bg=color4).place(x=0, y=50)

user_payments_label = Label(user_tab3_frame, text="Payment:", font=("raleway", 18, "bold"), fg=color4).place(x=30, y=60)

user_bill_id_label = Label(user_tab3_frame, text="Bill ID:", font=("raleway", 15, "bold"), fg=color4).place(x=60, y=120)
user_bill_id_entry = Entry(user_tab3_frame, width=24, font=("raleway", 11), fg=color4)
user_bill_id_entry.place(x=150, y=125)

user_payment_amount_label = Label(user_tab3_frame, text="Payment Amount:", font=("raleway", 15, "bold"), fg=color4).place(x=60, y=160)
user_payment_amount_entry = Entry(user_tab3_frame, width=24, font=("raleway", 11), fg=color4)
user_payment_amount_entry.place(x=260, y=165)

user_payment_method_label = Label(user_tab3_frame, text="Payment Method:", font=("raleway", 15, "bold"), fg=color4).place(x=60, y=200)
user_payment_amount_combobox_choices = ["G-cash", "Cash", "BDO"]
user_payment_method_combobox = ttk.Combobox(user_tab3_frame, width=24, font=("raleway", 11), values=user_payment_amount_combobox_choices, state="readonly")
user_payment_method_combobox.place(x=260, y=205)

user_payment_date_label = Label(user_tab3_frame, text="Payment Date:", font=("raleway", 15, "bold"), fg=color4).place(x=375, y=120)
user_payment_date_dateentry = DateEntry(user_tab3_frame, font=("raleway", 11, ), date_pattern = "yyyy-mm-dd")
user_payment_date_dateentry.place(x=520, y=125)

user_payment_submit_button = Button(user_tab3_frame, text="Submit", font=("raleway",12, "bold"), bg=color4, fg=color3, width=8, command=User_Payment_Submit)
user_payment_submit_button.place(relx=0.5, y=260, anchor="center")

user_logout_button = Button(user_window, text="Logout", font=("raleway",9, "bold"), bg=color4, fg=color3, width=8, command=User_Logout).place(x=880, y=20)

#=========================Admin Window=============================
admin_window = Frame(background, width=1000, height=800)
#admin_window.pack(pady=80)

admin_label = Label(admin_window, text="Welcome", font=("raleway", 90, "bold"), fg=color4).place(relx=0.5, y=250, anchor="center")
admin_name_label = Label(admin_window, text="Admin", font=("raleway", 20, "bold"), fg=color4).place(relx=0.5, y=320, anchor="center")

admin_create_button = Button(admin_window, text="Create", font=("raleway",12, "bold"), bg=color4, fg=color3, width=8, command=Create).place(x=300, y=350)
admin_read_button = Button(admin_window, text="Read", font=("raleway",12, "bold"), bg=color4, fg=color3, width=8, command=Read).place(x=400, y=350)
admin_update_button = Button(admin_window, text="Update", font=("raleway",12, "bold"), bg=color4, fg=color3, width=8, command=Update).place(x=500, y=350)
admin_delete_button = Button(admin_window, text="Delete", font=("raleway",12, "bold"), bg=color4, fg=color3, width=8, command=Delete).place(x=600, y=350)

admin_logout_button = Button(admin_window, text="Logout", font=("raleway",9, "bold"), bg=color4, fg=color3, width=8, command=Admin_Logout).place(x=880, y=20)
#=========================Create Window=============================
admin_create_window = Frame(background, width=550, height=500)
#admin_create_window.pack(pady=100)

admin_create_window_label = Label(admin_create_window, text="Create", font=("raleway", 50, "bold"), fg=color4).place(relx= 0.5, y=150, anchor="center")

admin_create_window_add_block_button = Button(admin_create_window, text="Add Block", font=("raleway",14, "bold"), bg=color4, fg=color3, width=10, command=Add_Block).place(relx= 0.5, y=250, anchor="center")
admin_create_window_add_unit_button = Button(admin_create_window, text="Add Unit", font=("raleway",14, "bold"), bg=color4, fg=color3, width=10, command=Add_Unit).place(relx= 0.5, y=300, anchor="center")

admin_create_cancel_button = Button(admin_create_window, text="Cancel", font=("raleway",11 , "bold"), bg=color4, fg=color3, width=8, command=Create_Cancel).place(x=450, y=20)
#=========================Read Window=============================
admin_read_window = Frame(background, width=550, height=500)
#admin_read_window.pack(pady=100)

admin_read_label = Label(admin_read_window, text="Read", font=("raleway", 50, "bold"), fg=color4).place(relx= 0.5, y=150, anchor="center")

admin_read_block_label = Label(admin_read_window, text="Block:", font=("raleway", 15, "bold"), fg=color4).place(x=210, y=200)
admin_read_block_combobox_choices = []
admin_read_block_combobox = ttk.Combobox(admin_read_window,values=admin_read_block_combobox_choices, font=("raleway",14, "bold"), width=10, state="readonly")
admin_read_block_combobox.bind("<<ComboboxSelected>>", Read_Block_Selected)
admin_read_block_combobox.place(relx= 0.5, y=250, anchor="center")

admin_read_unit_label = Label(admin_read_window, text="Unit:", font=("raleway", 15, "bold"), fg=color4).place(x=210, y=270)
admin_read_unit_combobox_choices = []
admin_read_unit_combobox = ttk.Combobox(admin_read_window,values=admin_read_unit_combobox_choices, font=("raleway",14, "bold"), width=10, state="readonly")
admin_read_unit_combobox.place(relx= 0.5, y=320, anchor="center")

admin_read_confirm_button = Button(admin_read_window, text="Confirm", font=("raleway",9, "bold"), bg=color4, fg=color3, width=8, command=Read_Confirm).place(x=200, y=400)
admin_read_cancel_button = Button(admin_read_window, text="Cancel", font=("raleway",9, "bold"), bg=color4, fg=color3, width=8, command=Read_Cancel).place(x=280, y=400)
#=========================Read Confirm Window=============================
read_confirm_window = Frame(background, width=1000, height=800)
#read_confirm_window.pack(pady=80)

read_confirm_window_block_label = Label(read_confirm_window, text="Block:", font=("raleway", 15, "bold"), fg=color4).place(x=60, y=50)
read_confirm_window_block_entry = Entry(read_confirm_window, width=10, font=("raleway", 15), fg=color4, state="disabled")
read_confirm_window_block_entry.place(x=150, y=50)

read_confirm_window_unit_label = Label(read_confirm_window, text="Unit:", font=("raleway", 15, "bold"), fg=color4).place(x=60, y=90)
read_confirm_window_unit_entry = Entry(read_confirm_window, width=10, font=("raleway", 15), fg=color4, state="disabled")
read_confirm_window_unit_entry.place(x=150, y=90)

read_confirm_window_move_in_date_label = Label(read_confirm_window, text="Move-in-date:", font=("raleway", 15, "bold"), fg=color4).place(x=60, y=130)
read_confirm_window_move_in_date_entry = Entry(read_confirm_window, width=20, font=("raleway", 15), fg=color4, state="disabled")
read_confirm_window_move_in_date_entry.place(x=200, y=130)

read_confirm_occupants_label = Label(read_confirm_window, text="Occupants:", font=("raleway", 15, "bold"), fg=color4).place(x=60, y=170)
read_confirm_bill_label = Label(read_confirm_window, text="Bills:", font=("raleway", 15, "bold"), fg=color4).place(x=60, y=350)

return_button = Button(read_confirm_window, text="Return", font=("raleway",11, "bold"), bg=color4, fg=color3, width=8, command=Read_Return).place(x=880, y=20)
#=========================Update Window=============================
admin_update_window = Frame(background, width=550, height=500)
#admin_update_window.pack(pady=100)

Label(admin_update_window, text="Update", font=("raleway", 50, "bold"), fg=color4).place(relx= 0.5, y=150, anchor="center")

Label(admin_update_window, text="Block:", font=("raleway", 15, "bold"), fg=color4).place(x=210, y=200)
admin_update_block_combobox_choices = []
admin_update_block_combobox = ttk.Combobox(admin_update_window,values=admin_update_block_combobox_choices, font=("raleway",14, "bold"), width=10, state="readonly")
admin_update_block_combobox.bind("<<ComboboxSelected>>", Update_Block_Selected)
admin_update_block_combobox.place(relx= 0.5, y=250, anchor="center")

Label(admin_update_window, text="Unit:", font=("raleway", 15, "bold"), fg=color4).place(x=210, y=270)
admin_update_unit_combobox_choices = []
admin_update_unit_combobox = ttk.Combobox(admin_update_window, values=admin_update_unit_combobox_choices, font=("raleway",14, "bold"), width=10, state="readonly")
admin_update_unit_combobox.place(relx= 0.5, y=320, anchor="center")

Button(admin_update_window, text="Confirm", font=("raleway",9, "bold"), bg=color4, fg=color3, width=8, command=Update_Confirm).place(x=200, y=400)
Button(admin_update_window, text="Cancel", font=("raleway",9, "bold"), bg=color4, fg=color3, width=8, command=Update_Cancel).place(x=280, y=400)

#=========================Update Confirm Window=============================
update_confirm_window = Frame(background, width=1000, height=800)
#update_confirm_window.pack(pady=80)

update_confirm_window_block_label = Label(update_confirm_window, text="Block:", font=("raleway", 15, "bold"), fg=color4).place(x=60, y=50)
update_confirm_window_block_entry = Entry(update_confirm_window, width=10, font=("raleway", 15), fg=color4, state="disabled")
update_confirm_window_block_entry.place(x=150, y=50)

update_confirm_window_unit_label = Label(update_confirm_window, text="Unit:", font=("raleway", 15, "bold"), fg=color4).place(x=60, y=90)
update_confirm_window_unit_entry = Entry(update_confirm_window, width=10, font=("raleway", 15), fg=color4, state="disabled")
update_confirm_window_unit_entry.place(x=150, y=90)

update_confirm_window_move_in_date_label = Label(update_confirm_window, text="Move-in-date:", font=("raleway", 15, "bold"), fg=color4).place(x=60, y=130)
update_confirm_window_move_in_date_entry = Entry(update_confirm_window, width=20, font=("raleway", 15), fg=color4, state="disabled")
update_confirm_window_move_in_date_entry.place(x=200, y=130)

update_confirm_occupants_label = Label(update_confirm_window, text="Occupants:", font=("raleway", 15, "bold"), fg=color4).place(x=60, y=170)
Button(update_confirm_window, text="Add Occupant", font=("raleway",8, "bold"), bg=color4, fg=color3, width=15, command=Add_Occupant).place(x=780, y=170)
Button(update_confirm_window, text="Update Occupant", font=("raleway",8, "bold"), bg=color4, fg=color3, width=15, command=Update_Occupant).place(x=650, y=170)
update_confirm_occupants_table = Frame(update_confirm_window)

update_confirm_bill_label = Label(update_confirm_window, text="Bills:", font=("raleway", 15, "bold"), fg=color4).place(x=60, y=350)
Button(update_confirm_window, text="Add Bill", font=("raleway",8, "bold"), bg=color4, fg=color3, width=15, command=Add_Bill).place(x=780, y=350)
Button(update_confirm_window, text="Update Bill", font=("raleway",8, "bold"), bg=color4, fg=color3, width=15, command=Update_Bill).place(x=650, y=350)
update_confirm_bill_table = Frame(update_confirm_window)

Button(update_confirm_window, text="Return", font=("raleway",11, "bold"), bg=color4, fg=color3, width=8, command=Update_Return).place(x=880, y=20)

#=========================Delete Window=============================
admin_delete_window = Frame(background, width=550, height=500)
#admin_delete_window.pack(pady=100)

Label(admin_delete_window, text="Delete", font=("raleway", 50, "bold"), fg=color4).place(relx= 0.5, y=150, anchor="center")

Label(admin_delete_window, text="Block:", font=("raleway", 15, "bold"), fg=color4).place(x=210, y=200)
admin_delete_block_combobox_choices = []
admin_delete_block_combobox = ttk.Combobox(admin_delete_window,values=admin_delete_block_combobox_choices, font=("raleway",14, "bold"), width=10, state="readonly")
admin_delete_block_combobox.bind("<<ComboboxSelected>>", Delete_Block_Selected)
admin_delete_block_combobox.place(relx= 0.5, y=250, anchor="center")

Label(admin_delete_window, text="Unit:", font=("raleway", 15, "bold"), fg=color4).place(x=210, y=270)
admin_delete_unit_combobox_choices = []
admin_delete_unit_combobox = ttk.Combobox(admin_delete_window, values=admin_delete_unit_combobox_choices, font=("raleway",14, "bold"), width=10, state="readonly")
admin_delete_unit_combobox.place(relx= 0.5, y=320, anchor="center")

Button(admin_delete_window, text="Confirm", font=("raleway",9, "bold"), bg=color4, fg=color3, width=8, command=Delete_Confirm).place(x=200, y=400)
Button(admin_delete_window, text="Cancel", font=("raleway",9, "bold"), bg=color4, fg=color3, width=8, command=Delete_Cancel).place(x=280, y=400)

#=========================Delete Confirm Window=============================
delete_confirm_window = Frame(background, width=1000, height=800)
#delete_confirm_window.pack(pady=80)

delete_confirm_window_block_label = Label(delete_confirm_window, text="Block:", font=("raleway", 15, "bold"), fg=color4).place(x=60, y=50)
delete_confirm_window_block_entry = Entry(delete_confirm_window, width=10, font=("raleway", 15), fg=color4, state="disabled")
delete_confirm_window_block_entry.place(x=150, y=50)

delete_confirm_window_unit_label = Label(delete_confirm_window, text="Unit:", font=("raleway", 15, "bold"), fg=color4).place(x=60, y=90)
delete_confirm_window_unit_entry = Entry(delete_confirm_window, width=10, font=("raleway", 15), fg=color4, state="disabled")
delete_confirm_window_unit_entry.place(x=150, y=90)

delete_confirm_window_move_in_date_label = Label(delete_confirm_window, text="Move-in-date:", font=("raleway", 15, "bold"), fg=color4).place(x=60, y=130)
delete_confirm_window_move_in_date_entry = Entry(delete_confirm_window, width=20, font=("raleway", 15), fg=color4, state="disabled")
delete_confirm_window_move_in_date_entry.place(x=200, y=130)

delete_confirm_occupants_label = Label(delete_confirm_window, text="Occupants:", font=("raleway", 15, "bold"), fg=color4).place(x=60, y=170)
Button(delete_confirm_window, text="Delete Occupant", font=("raleway",8, "bold"), bg=color4, fg=color3, width=15, command=Delete_Occupant).place(x=780, y=170)
delete_confirm_occupants_table = Frame(delete_confirm_window)

delete_confirm_bill_label = Label(delete_confirm_window, text="Bills:", font=("raleway", 15, "bold"), fg=color4).place(x=60, y=350)
Button(delete_confirm_window, text="Delete Bill", font=("raleway",8, "bold"), bg=color4, fg=color3, width=15, command=Delete_Bill).place(x=780, y=350)
delete_confirm_bill_table = Frame(delete_confirm_window)

Button(delete_confirm_window, text="Return", font=("raleway",11, "bold"), bg=color4, fg=color3, width=8, command=Delete_Return).place(x=880, y=20)

#=========================Delete Window=============================
#run
root.mainloop()