from tkinter import *
from tkinter import ttk
from tkcalendar import *
import sqlite3
from datetime import datetime, timedelta
import math
from appointments.database import conn, drop_and_create_db, insert_db_data, insert_client, delete_clients, get_client, alter_client, get_appointments, get_client_combobox
drop_and_create_db()
insert_db_data()

master = Tk()
master.title('Pacientu arhīvs')
master.iconbitmap()
master.geometry('1272x600+0+0')
master.resizable(width=True, height=True)

for i in range(2):
    master.rowconfigure(i, weight=1, uniform=1)

calendar_frame = Frame(master)
calendar_frame.grid(row=0, column=0, padx=5, pady=5)
cal = Calendar(calendar_frame, selectmode='day')
cal.pack(ipady=52, ipadx=50, side=TOP)




appointment_treeview_frame = LabelFrame(master)
appointment_treeview_frame.grid(row=0, column=2, rowspan=2, padx=0, pady=5)

create_entry_button = Button(appointment_treeview_frame, text='Pievienot', width=12, command=lambda:add_new_appointment_window())
create_entry_button.grid(row=0, column=0, padx=0, sticky=W)

edit_button = Button(appointment_treeview_frame, text='Rediģēt', width=12, relief=SUNKEN)
edit_button.grid(row=0, column=1, padx=0, sticky=W)

del_button = Button(appointment_treeview_frame, text='Dzēst', width=12, relief=SUNKEN)
del_button.grid(row=0, column=2, padx=0, sticky=W)

appointment_list = ttk.Treeview(appointment_treeview_frame)
appointment_list.grid(row=1, column=0, columnspan=100, ipady=166)


def dis_resize(event):
    if appointment_list.identify_region(event.x, event.y) == 'separator':
        return 'break'


def dis_dbl_arrw(event):
    if appointment_list.identify_region(event.x, event.y) == 'separator':
        return 'break'


appointment_list.bind('<Button-1>', dis_resize)
appointment_list.bind('<Motion>', dis_dbl_arrw)

appointment_list['columns'] = ('time_from', 'time_to', 'first_name', 'last_name', 'age', 'number')
appointment_list.heading('#0', text='', anchor='w')
appointment_list.column('#0', anchor='center', width=0, stretch=FALSE)
appointment_list.heading('time_from', text='No:', anchor='w')
appointment_list.column('time_from', width='70', minwidth='70', anchor='center', stretch=FALSE)
appointment_list.heading('time_to', text='Līdz:', anchor='w')
appointment_list.column('time_to', width='70', minwidth='70', anchor='center', stretch=FALSE)
appointment_list.heading('first_name', text='Vārds', anchor='w')
appointment_list.column('first_name', width='130', minwidth='130', anchor='center', stretch=FALSE)
appointment_list.heading('last_name', text='Uzvārds', anchor='w')
appointment_list.column('last_name', width='130', minwidth='130', anchor='center', stretch=FALSE)
appointment_list.heading('age', text='Vecums', anchor='w')
appointment_list.column('age', width='55', minwidth='55', anchor='center', stretch=FALSE)
appointment_list.heading('number', text='Telefona nr.', anchor='w')
appointment_list.column('number', width='140', minwidth='140', anchor='center', stretch=FALSE)

client_list_frame = LabelFrame(master)
client_list_frame.grid(row=0, column=3, rowspan=2)

client_add = Button(client_list_frame, width=13, text='Pievienot', command=lambda: add_new_client_window())

client_edit = Button(client_list_frame, width=13, text='Rediģēt', command=lambda: [
    edit_client_window(),
])

def edit_client_window(width=300, height=300):
    client_id = client_list.item(client_list_selected_clients)['values'][0]
    client = get_client(client_id)

    edit_client = Toplevel()
    edit_client.title('Klienta labošana')
    edit_client.iconbitmap()
    edit_client.geometry(f'{width}x{height}')
    edit_client.resizable(width=False, height=False)
    edit_client.grab_set()
    entry_frame = LabelFrame(edit_client, width=width, height=height)
    entry_frame.grid(row=0, column=0, ipadx=5, ipady=10)

    first_name_entry_label = Label(entry_frame, text='Vārds')
    first_name_entry_label.grid(row=0, column=0, sticky='w')
    first_name_entry = Entry(entry_frame)
    first_name_entry.insert(0, client[1])
    first_name_entry.grid(row=0, column=1, ipadx=25)

    last_name_entry_label = Label(entry_frame, text='Uzvārds')
    last_name_entry_label.grid(row=1, column=0, sticky='w')
    last_name_entry = Entry(entry_frame)
    last_name_entry.insert(0, client[2])
    last_name_entry.grid(row=1, column=1, ipadx=25)

    age_entry_label = Label(entry_frame, text='Vecums')
    age_entry_label.grid(row=2, column=0, sticky='w')
    age_entry = Entry(entry_frame)
    age_entry.insert(0, client[3])
    age_entry.grid(row=2, column=1, ipadx=25)

    tel_entry_label = Label(entry_frame, text='Telefona nr.')
    tel_entry_label.grid(row=3, column=0, sticky='w')
    tel_entry = Entry(entry_frame)
    tel_entry.insert(0, client[4])
    tel_entry.grid(row=3, column=1, ipadx=25)

    edit_client_button = Button(
        edit_client,
        text='Saglabāt',
        width=12,
        command=lambda: [
            alter_client(client[0], first_name_entry.get(), last_name_entry.get(), age_entry.get(), tel_entry.get()),
            draw_client_tree_view(),
            client_list.event_generate('<<TreeviewSelect>>'),
            edit_client.destroy()
        ]
    )
    edit_client_button.grid(row=4, column=0, columnspan=2)


client_edit['state'] = 'disabled'
client_delete = Button(client_list_frame, width=13, text='Izdzēst', command=lambda: [
    client_list_delete_clients(),
    draw_client_tree_view()
])
client_delete['state'] = 'disabled'


def client_list_delete_clients():
    client_ids = []
    for selected_client in client_list_selected_clients:
        client_id = client_list.item(selected_client)['values'][0]
        client_ids.append(client_id)

    delete_clients(client_ids)


client_add.grid(row=0, column=0)
client_edit.grid(row=0, column=1)
client_delete.grid(row=0, column=2)

client_list = ttk.Treeview(client_list_frame)
client_list.grid(row=1, column=0, columnspan=100, ipady=166)

client_list['columns'] = ('id', 'first_name', 'last_name')
client_list.heading('#0', text='', anchor='w')
client_list.column('#0', anchor='center', width=0, stretch=FALSE)
client_list.heading('id', text='id', anchor='w')
client_list.column('id', width='100', anchor='center', stretch=FALSE)
client_list.heading('first_name', text='Vārds', anchor='w')
client_list.column('first_name', width='100', anchor='center', stretch=FALSE)
client_list.heading('last_name', text='Uzvārds', anchor='w')
client_list.column('last_name', width='100', anchor='center', stretch=FALSE)


# def draw_appointment_tree_view():
def add_new_client_window(width=300, height=300):
    add_new_client = Toplevel()
    add_new_client.title('Pieraksta pievienošana')
    add_new_client.iconbitmap()
    add_new_client.geometry(f'{width}x{height}')
    add_new_client.resizable(width=False, height=False)
    add_new_client.grab_set()
    entry_frame = LabelFrame(add_new_client, width=400, height=400)
    entry_frame.grid(row=0, column=0, ipadx=5, ipady=10)
    first_name_entry_label = Label(entry_frame, text='Vārds')
    first_name_entry_label.grid(row=0, column=0, sticky='w')
    first_name_entry = Entry(entry_frame)
    first_name_entry.grid(row=0, column=1, ipadx=25)
    last_name_entry_label = Label(entry_frame, text='Uzvārds')
    last_name_entry_label.grid(row=1, column=0, sticky='w')
    last_name_entry = Entry(entry_frame)
    last_name_entry.grid(row=1, column=1, ipadx=25)
    age_entry_label = Label(entry_frame, text='Vecums')
    age_entry_label.grid(row=2, column=0, sticky='w')
    age_entry = Entry(entry_frame)
    age_entry.grid(row=2, column=1, ipadx=25)
    tel_entry_label = Label(entry_frame, text='Telefona nr.')
    tel_entry_label.grid(row=3, column=0, sticky='w')
    tel_entry = Entry(entry_frame)
    tel_entry.grid(row=3, column=1, ipadx=25)
    client_add_button = Button(
        add_new_client,
        text='Pievienot',
        width=12,
        command=lambda: [
            insert_client(first_name_entry.get(), last_name_entry.get(), age_entry.get(), tel_entry.get()),
            draw_client_tree_view(),
            add_new_client.destroy()
        ]
    )
    client_add_button.grid(row=4, column=0, columnspan=2)


client_list_selected_clients = None


def toggle_client_list_button_state(event):
    selected_clients = event.widget.selection()
    global client_list_selected_clients
    client_list_selected_clients = selected_clients

    if len(selected_clients) == 1:
        client_edit['state'] = 'active'
    else:
        client_edit['state'] = 'disabled'

    if len(selected_clients) >= 1:
        client_delete['state'] = 'active'
    else:
        client_delete['state'] = 'disabled'


client_list.bind('<<TreeviewSelect>>', toggle_client_list_button_state)


def draw_client_tree_view():
    c = conn.cursor()
    c.execute('SELECT id, first_name, last_name FROM clients')
    clients = c.fetchall()

    # for client_id in range(len(clients)):
    #     client = clients[client_id]
    #     client_list.insert('', END, values=(client[0], client[1]))

    for idx in client_list.get_children():
        client_list.delete(idx)

    for client in clients:
        client_list.delete()
        client_list.insert('', END, values=(client[0], client[1], client[2]))
    c.close()


def draw_app_tree_view():
    get_appointments()

    for appointment in appointment_list.get_children():
        appointment_list.delete(appointment)
    for appointment in appointments():
        appointment_list.insert('', END, values=(appointment[0:6]))

option_buttons = LabelFrame()
option_buttons.grid(row=1, column=0, ipadx=2, ipady=2)

def calendar_reset():
   for calendar_destroy in calendar_frame.winfo_children():
       calendar_destroy.destroy()
       Calendar(calendar_frame, selectmode='day').pack(ipady=52, ipadx=50, side=TOP)

def add_new_appointment_window(width=620, height=500):
    add_new_appointment = Toplevel()
    add_new_appointment.title('Pieraksta pievienošana')
    add_new_appointment.iconbitmap()
    add_new_appointment.geometry(f'{width}x{height}')
    #add_new_appointment.resizable(width=False, height=False)
    add_new_appointment.grab_set()

    calendar_chosen_date = cal.get_date()

    times_from = [
            ('09:00'), ('09:30'), ('10:00'), ('10:30'), ('11:00'),('11:30'),('12:00'),('12:30'),
            ('13:00'), ('13:30'), ('14:00'), ('14:30'), ('15:00'), ('15:30'), ('16:00'), ('16:30'),
            ('17:00'), ('17:30'), ('18:00'), ('18:30'), ('19:00'), ('19:30'), ('20:00')
            ]
    times_to = [
            ('09:30'), ('10:00'), ('10:30'), ('11:00'),('11:30'),('12:00'),('12:30'), ('13:00'),
            ('13:30'), ('14:00'), ('14:30'), ('15:00'), ('15:30'), ('16:00'), ('16:30'),
            ('17:00'), ('17:30'), ('18:00'), ('18:30'), ('19:00'), ('19:30'), ('20:00')
            ]
    chosen_date_label = Label(add_new_appointment, text='Datums:', padx=10)
    chosen_date_label.grid(row=0, column=0)
    chosen_date = Label(add_new_appointment, text=calendar_chosen_date)
    chosen_date.grid(row=1, column=0)
    time_from_text = Label(add_new_appointment, text='Laiks no:')
    time_from_text.grid(row=0, column=1)
    time_from_text = Label(add_new_appointment, text='Laiks līdz:')
    time_from_text.grid(row=0, column=2)
    time_from = ttk.Combobox(add_new_appointment, values=times_from)
    time_from.grid(row=1, column=1)
    time_to = ttk.Combobox(add_new_appointment, values=times_to)
    time_to.grid(row=1, column=2)
    patient_label = Label(add_new_appointment, text='Pacients')
    patient_label.grid(row=0, column=3)
    patient = ttk.Combobox(add_new_appointment)
    patient.grid(row=1, column=3, ipadx=60)


reset_date = Button(option_buttons, text='Tekošais datums', width=42, command=lambda:calendar_reset())
reset_date.grid(row=0, column=0, columnspan=2, padx=2, pady=2)
choose_date_button = Button(option_buttons, text='Parādīt pierakstus', width=20, relief=SUNKEN)
choose_date_button.grid(row=1, column=0, padx=2)
random_button = Button(option_buttons, width=20, relief=SUNKEN)
random_button.grid(row=1, column=1, padx=2)

draw_client_tree_view()

master.mainloop()
