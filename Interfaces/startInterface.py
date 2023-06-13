import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from raceInterface import RaceApp
from datetime import datetime

conn = sqlite3.connect('zawody.db')
c = conn.cursor()


def register_competitors():
    def save_competitor():
        imie = name_entry.get()
        nazwisko = surname_entry.get()
        data_urodzenia = dob_entry.get()
        kategoria = category_entry.get()
        pojazd = vehicle.get()
        nr_telefonu = phone_entry.get()
        dane_opiekuna = guardian_entry.get()

        c.execute('SELECT id FROM Kategoria WHERE nazwa = ?', (kategoria,))
        kategoria = c.fetchone()[0]

        c.execute(
            'INSERT INTO Zawodnik (imie, nazwisko, dataUrodzenia, nrTelefonu, daneOpiekuna, pojazd, Kategoria_id) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (imie, nazwisko, data_urodzenia, nr_telefonu, dane_opiekuna, pojazd, kategoria))

        conn.commit()
        messagebox.showinfo("Informacja", "Zawodnik zarejestrowany pomyślnie!")
        register_window.destroy()

    register_window = tk.Toplevel(window)
    register_window.geometry('400x600')
    register_window.title("Rejestracja zawodników")

    name_label = tk.Label(register_window, text="Imię:")
    name_label.pack()
    name_entry = tk.Entry(register_window)
    name_entry.pack(padx=100, pady=10)

    surname_label = tk.Label(register_window, text="Nazwisko:")
    surname_label.pack()
    surname_entry = tk.Entry(register_window)
    surname_entry.pack(padx=100, pady=10)

    dob_label = tk.Label(register_window, text="DB urodzenia:")
    dob_label.pack()
    dob_entry = tk.Entry(register_window)
    dob_entry.pack(padx=100, pady=10)

    category_label = tk.Label(register_window, text="Kategoria:")
    category_label.pack()
    category_entry = ttk.Combobox(register_window, values=get_categories())
    category_entry.pack(padx=100, pady=10)

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
        pojazd = vehicle.get()
        nr_telefonu = phone_entry.get()
        dane_opiekuna = guardian_entry.get()
        kategoria = category_entry.get()

        c.execute('SELECT id FROM Kategoria WHERE nazwa = ?', (kategoria,))
        kategoria = c.fetchone()[0]

        c.execute('''
            UPDATE Zawodnik
            SET imie = ?, nazwisko = ?, dataUrodzenia = ?, nrTelefonu = ?, daneOpiekuna = ?, pojazd = ?, Kategoria_id = ?
            WHERE id = ?
        ''', (imie, nazwisko, data_urodzenia, nr_telefonu, dane_opiekuna, pojazd, kategoria, id_zawodnika))

        conn.commit()
        messagebox.showinfo("Informacja", "Dane zawodnika zaktualizowane pomyślnie!")
        modify_window.destroy()

    modify_window = tk.Toplevel(window)
    modify_window.geometry('400x700')
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

    dob_label = tk.Label(modify_window, text="DB urodzenia:")
    dob_label.pack()
    dob_entry = tk.Entry(modify_window)
    dob_entry.pack(padx=100, pady=10)

    category_label = tk.Label(modify_window, text="Kategoria:")
    category_label.pack()
    category_entry = ttk.Combobox(modify_window, values=get_categories())
    category_entry.pack(padx=100, pady=10)

    vehicle = tk.StringVar()
    bike_radio = tk.Radiobutton(modify_window, text="Rower", variable=vehicle, value="rower")
    bike_radio.pack()
    scooter_radio = tk.Radiobutton(modify_window, text="Hulajnoga", variable=vehicle, value="hulajnoga")
    scooter_radio.pack()

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


def start_competition():
    root = tk.Toplevel(window)
    app = RaceApp(root)
    app.mainloop()

def set_category():
    def save_category():
        age_start = int(start_age_entry.get())
        age_end = int(end_age_entry.get())
        category_name = category_entry.get()
        current_year = datetime.now().year

        birth_year_start = current_year - age_end
        birth_year_end = current_year - age_start

        c.execute('INSERT INTO Kategoria (nazwa, rokUrodzeniaStart, rokUrodzeniaEnd) VALUES (?, ?, ?)',
                  (category_name, birth_year_start, birth_year_end))

        conn.commit()
        messagebox.showinfo("Informacja", "Kategoria dodana pomyślnie!")

        category_combobox['values'] = get_categories()

        category_window.destroy()

    category_window = tk.Toplevel(window)
    category_window.geometry('400x300')
    category_window.title("Ustawianie kategorii wiekowych")

    category_label = tk.Label(category_window, text="Nazwa kategorii:")
    category_label.pack()
    category_entry = tk.Entry(category_window)
    category_entry.pack(padx=100, pady=10)

    start_age_label = tk.Label(category_window, text="Wiek startowy:")
    start_age_label.pack()
    start_age_entry = tk.Entry(category_window)
    start_age_entry.pack(padx=100, pady=10)

    end_age_label = tk.Label(category_window, text="Wiek końcowy:")
    end_age_label.pack()
    end_age_entry = tk.Entry(category_window)
    end_age_entry.pack(padx=100, pady=10)

    save_button = tk.Button(category_window, text="Zapisz", command=save_category)
    save_button.pack(padx=100, pady=10)

def clear_competitors():
    delete_all_competitors = messagebox.askyesno("Potwierdzenie", "Czy na pewno chcesz usunąć wszystkich zawodników ich dane oraz kategorie?")
    if delete_all_competitors:
        c.execute("DELETE FROM Zaw odnik")
        c.execute("DELETE FROM Kategoria")
        c.execute("DELETE FROM Przejazd")
        conn.commit()
        messagebox.showinfo("Informacja", "Baza danych została wyczyszczona!")
    filter_table()

def get_categories():
    c.execute("SELECT nazwa FROM Kategoria")
    categories = c.fetchall()
    return [category[0] for category in categories]

def filter_by_category(event=None):
    for row in tree.get_children():
        tree.delete(row)

    category = category_combobox.get() or ''

    c.execute("""
        SELECT Zawodnik.id, Zawodnik.imie, Zawodnik.nazwisko, 
        Zawodnik.dataUrodzenia, Zawodnik.nrTelefonu, Zawodnik.daneOpiekuna, 
        Zawodnik.pojazd, Kategoria.nazwa
        FROM Zawodnik
        JOIN Kategoria 
        ON Kategoria_id = Kategoria.id
        WHERE Kategoria.nazwa = ?
    """, (category,))

    rows = c.fetchall()

    for index, row in enumerate(rows, start=1):
        tree.insert('', 'end', values=(index,) + row)


def filter_table(vehicle=None):
    for row in tree.get_children():
        tree.delete(row)

    if vehicle:
        c.execute("""
            SELECT Zawodnik.id, Zawodnik.imie, Zawodnik.nazwisko, 
            Zawodnik.dataUrodzenia, Zawodnik.nrTelefonu, Zawodnik.daneOpiekuna, 
            Zawodnik.pojazd, Kategoria.nazwa
            FROM Zawodnik
            JOIN Kategoria
            ON Kategoria_id = Kategoria.id
            WHERE pojazd=?
        """, (vehicle,))
    else:
        c.execute("""
            SELECT Zawodnik.id, Zawodnik.imie, Zawodnik.nazwisko,
            Zawodnik.dataUrodzenia, Zawodnik.nrTelefonu, Zawodnik.daneOpiekuna, 
            Zawodnik.pojazd, Kategoria.nazwa
            FROM Zawodnik
            JOIN Kategoria
            ON Kategoria_id = Kategoria.id
        """)

    rows = c.fetchall()

    for index, row in enumerate(rows, start=1):
        tree.insert('', 'end', values=(index,) + row)

def search_table():
    for row in tree.get_children():
        tree.delete(row)

    keyword = search_entry.get()

    c.execute("""
        SELECT Zawodnik.id, Zawodnik.imie, Zawodnik.nazwisko,
        Zawodnik.dataUrodzenia, Zawodnik.nrTelefonu, Zawodnik.daneOpiekuna, 
        Zawodnik.pojazd, Kategoria.nazwa
        FROM Zawodnik
        JOIN Kategoria
        ON Kategoria_id = Kategoria.id
        WHERE Zawodnik.imie LIKE ? OR Zawodnik.nazwisko LIKE ?
    """, (f'%{keyword}%', f'%{keyword}%'))

    rows = c.fetchall()

    for index, row in enumerate(rows, start=1):
        tree.insert('', 'end', values=(index,) + row)




window = tk.Tk()
window.geometry('1350x290')
window.resizable(False, False)
window.title("System do mierzenia czasu na zawodach rowerowych")

button_frame = tk.Frame(window)
button_frame.grid(row=0, column=0, sticky='ns')

register_button = tk.Button(button_frame, text="Rejestracja zawodników", command=register_competitors)
register_button.pack(padx=100, pady=(20,10))

modify_button = tk.Button(button_frame, text="Modyfikacja zawodników", command=modify_competitors)
modify_button.pack(padx=100, pady=10)

set_category_button = tk.Button(button_frame, text="Zarządzanie kategoriami", command=set_category)
set_category_button.pack(padx=100, pady=10)

start_button = tk.Button(button_frame, text="Start zawodów", command=start_competition)
start_button.pack(padx=100, pady=10)

clear_button = tk.Button(button_frame, text="Wyczyść", command=clear_competitors)
clear_button.pack(padx=100, pady=10)

table_frame = tk.Frame(window)
table_frame.grid(row=0, column=1, sticky='ns', pady=(20,0))


tree = ttk.Treeview(table_frame)
tree["columns"] = ("zero","one","two","three","four","five","six","seven","eight")
tree.column("#0", width=0)
tree.column("zero", width=50)
tree.column("one", width=50)
tree.column("two", width=100)
tree.column("three", width=100)
tree.column("four", width=100)
tree.column("five", width=100)
tree.column("six", width=250)
tree.column("seven", width=100)
tree.column("eight", width=100)

tree.heading("zero", text="Numer")
tree.heading("one", text="ID")
tree.heading("two", text="Imię")
tree.heading("three", text="Nazwisko")
tree.heading("four", text="DB urodzenia")
tree.heading("five", text="Nr telefonu")
tree.heading("six", text="Dane opiekuna")
tree.heading("seven", text="Pojazd")
tree.heading("eight", text="Kat. wiekowa")

tree.pack()

bike_button = tk.Button(table_frame, text="Rower", command=lambda: filter_table('rower'))
bike_button.pack(side='left')

scooter_button = tk.Button(table_frame, text="Hulajnoga", command=lambda: filter_table('hulajnoga'))
scooter_button.pack(side='left')

all_button = tk.Button(table_frame, text="Wszystko", command=filter_table)
all_button.pack(side='left')

search_label = tk.Label(table_frame, text="Szukaj:")
search_label.pack(side='left')

search_entry = tk.Entry(table_frame)
search_entry.pack(side='left')

search_button = tk.Button(table_frame, text="Szukaj", command=search_table)
search_button.pack(side='left')

category_label = tk.Label(table_frame, text="Filtruj po kategorii:")
category_label.pack(side='left')

category_combobox = ttk.Combobox(table_frame, values=get_categories())
category_combobox.bind("<<ComboboxSelected>>", filter_by_category)
category_combobox.pack(side='left')

window.mainloop()
