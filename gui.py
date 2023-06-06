import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import pandas as pd

conn = sqlite3.connect('zawody.db')
c = conn.cursor()


def register_competitors():
    def save_competitor():
        imie = name_entry.get()
        nazwisko = surname_entry.get()
        data_urodzenia = dob_entry.get()
        pojazd = vehicle.get()
        nr_telefonu = phone_entry.get()
        dane_opiekuna = guardian_entry.get()

        c.execute(
            'INSERT INTO Zawodnik (imie, nazwisko, dataUrodzenia, nrTelefonu, daneOpiekuna, pojazd) VALUES (?, ?, ?, ?, ?, ?)',
            (imie, nazwisko, data_urodzenia, nr_telefonu, dane_opiekuna, pojazd))

        conn.commit()
        messagebox.showinfo("Informacja", "Zawodnik zarejestrowany pomyślnie!")
        register_window.destroy()


    register_window = tk.Toplevel(window)
    register_window.geometry('400x500')
    register_window.title("Rejestracja zawodników")

    name_label = tk.Label(register_window, text="Imię:")
    name_label.pack()
    name_entry = tk.Entry(register_window)
    name_entry.pack(padx=100, pady=10)

    surname_label = tk.Label(register_window, text="Nazwisko:")
    surname_label.pack()
    surname_entry = tk.Entry(register_window)
    surname_entry.pack(padx=100, pady=10)

    dob_label = tk.Label(register_window, text="Data urodzenia:")
    dob_label.pack()
    dob_entry = tk.Entry(register_window)
    dob_entry.pack(padx=100, pady=10)

    phone_label = tk.Label(register_window, text="Numer telefonu:")
    phone_label.pack()
    phone_entry = tk.Entry(register_window)
    phone_entry.pack(padx=100, pady=10)

    guardian_label = tk.Label(register_window, text="Dane opiekuna:")
    guardian_label.pack()
    guardian_entry = tk.Entry(register_window)
    guardian_entry.pack(padx=100, pady=10)

    vehicle = tk.StringVar()
    bike_radio = tk.Radiobutton(register_window, text="Rower", variable=vehicle, value="rower")
    bike_radio.pack()
    scooter_radio = tk.Radiobutton(register_window, text="Hulajnoga", variable=vehicle, value="hulajnoga")
    scooter_radio.pack()

    save_button = tk.Button(register_window, text="Zapisz", command=save_competitor)
    save_button.pack()


def modify_competitors():
    def update_competitor():
        id_zawodnika = id_entry.get()
        imie = name_entry.get()
        nazwisko = surname_entry.get()
        data_urodzenia = dob_entry.get()
        pojazd = vehicle_entry.get()
        nr_telefonu = phone_entry.get()
        dane_opiekuna = guardian_entry.get()
        c.execute('''
            UPDATE Zawodnik
            SET imie = ?, nazwisko = ?, dataUrodzenia = ?, nrTelefonu = ?, daneOpiekuna = ?, pojazd = ?
            WHERE id = ?
        ''', (imie, nazwisko, data_urodzenia, nr_telefonu, dane_opiekuna, pojazd, id_zawodnika))

        conn.commit()
        messagebox.showinfo("Informacja", "Dane zawodnika zaktualizowane pomyślnie!")
        modify_window.destroy()

    modify_window = tk.Toplevel(window)
    modify_window.geometry('400x450')
    modify_window.title("Modyfikacja zawodników")

    id_label = tk.Label(modify_window, text="ID zawodnika:")
    id_label.pack()
    id_entry = tk.Entry(modify_window)
    id_entry.pack(padx=100, pady=10)

    name_label = tk.Label(modify_window, text="Imię:")
    name_label.pack()
    name_entry = tk.Entry(modify_window)
    name_entry.pack(padx=100, pady=10)

    surname_label = tk.Label(modify_window, text="Nazwisko:")
    surname_label.pack()
    surname_entry = tk.Entry(modify_window)
    surname_entry.pack(padx=100, pady=10)

    dob_label = tk.Label(modify_window, text="Data urodzenia:")
    dob_label.pack()
    dob_entry = tk.Entry(modify_window)
    dob_entry.pack(padx=100, pady=10)

    vehicle_label = tk.Label(modify_window, text="Pojazd:")
    vehicle_label.pack()
    vehicle_entry = tk.Entry(modify_window)
    vehicle_entry.pack(padx=100, pady=10)

    phone_label = tk.Label(modify_window, text="Numer telefonu:")
    phone_label.pack()
    phone_entry = tk.Entry(modify_window)
    phone_entry.pack(padx=100, pady=10)

    guardian_label = tk.Label(modify_window, text="Dane opiekuna:")
    guardian_label.pack()
    guardian_entry = tk.Entry(modify_window)
    guardian_entry.pack(padx=100, pady=10)

    save_button = tk.Button(modify_window, text="Zapisz", command=update_competitor)
    save_button.pack(pady=20)


def view_competitors():
    def filter_by_vehicle(vehicle_type):
        nonlocal df
        df = original_df[original_df['pojazd'] == vehicle_type]
        update_label()

    def reset_data():
        nonlocal df
        df = original_df.copy()
        update_label()

    def update_label():
        data_label.config(text=df.to_string(index=False))

    view_window = tk.Toplevel(window)
    view_window.geometry('600x600')
    view_window.title("Zawodnicy")

    original_df = pd.read_sql_query(
        "SELECT id, imie, nazwisko, dataUrodzenia, nrTelefonu, daneOpiekuna, pojazd FROM Zawodnik",
        conn)

    df = original_df.copy()

    bike_button = tk.Button(view_window, text="Pokaż zawodników na rowerach", command=lambda: filter_by_vehicle('rower'))
    bike_button.pack()

    scooter_button = tk.Button(view_window, text="Pokaż zawodników na hulajnogach", command=lambda: filter_by_vehicle('hulajnoga'))
    scooter_button.pack()

    all_button = tk.Button(view_window, text="Pokaż wszystkich zawodników", command=reset_data)
    all_button.pack()

    data_label = tk.Label(view_window, text=df.to_string(index=False), justify='left')
    data_label.pack()



def start_competition():
    messagebox.showinfo("Informacja", "Funkcja startu zawodów jeszcze nie została zaimplementowana.")


def quit_app():
    window.quit()


def refresh_table():
    for row in tree.get_children():
        tree.delete(row)

    c.execute("SELECT * FROM Zawodnik")
    rows = c.fetchall()

    for row in rows:
        tree.insert('', 'end', values=row)


window = tk.Tk()
window.geometry('1200x400')
window.title("System do mierzenia czasu na zawodach rowerowych")

button_frame = tk.Frame(window)
button_frame.grid(row=0, column=0, sticky='ns')

register_button = tk.Button(button_frame, text="Rejestracja zawodników", command=register_competitors)
register_button.pack(padx=100, pady=20)

modify_button = tk.Button(button_frame, text="Modyfikacja zawodników", command=modify_competitors)
modify_button.pack(padx=100, pady=20)

view_button = tk.Button(button_frame, text="Zawodnicy", command=view_competitors)
view_button.pack(padx=100, pady=20)

start_button = tk.Button(button_frame, text="Start zawodów", command=start_competition)
start_button.pack(padx=100, pady=20)

exit_button = tk.Button(button_frame, text="Wyjście", command=quit_app)
exit_button.pack(padx=100, pady=20)

table_frame = tk.Frame(window)
table_frame.grid(row=0, column=1, sticky='ns', pady=(20,0))


tree = ttk.Treeview(table_frame)
tree["columns"]=("one","two","three","four","five","six","seven")
tree.column("#0", width=0)
tree.column("one", width=50)
tree.column("two", width=100)
tree.column("three", width=100)
tree.column("four", width=100)
tree.column("five", width=100)
tree.column("six", width=150)
tree.column("seven", width=100)

tree.heading("one", text="ID")
tree.heading("two", text="Imię")
tree.heading("three", text="Nazwisko")
tree.heading("four", text="Data urodzenia")
tree.heading("five", text="Numer telefonu")
tree.heading("six", text="Dane opiekuna")
tree.heading("seven", text="Pojazd")

tree.pack()

refresh_button = tk.Button(table_frame, text="Odśwież", command=refresh_table)
refresh_button.pack(pady=20)

window.mainloop()
