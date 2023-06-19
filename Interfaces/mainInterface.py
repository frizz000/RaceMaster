import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from raceInterface import RaceInterface
from datetime import datetime

conn = sqlite3.connect('zawody.db')
c = conn.cursor()


class MainInterface:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry('1350x290')
        self.window.resizable(False, False)
        self.window.title("System do mierzenia czasu na zawodach rowerowych")

        self.button_frame = tk.Frame(self.window)
        self.button_frame.grid(row=0, column=0, sticky='ns')

        self.register_button = tk.Button(self.button_frame, text="Rejestracja zawodników",
                                         command=self.register_competitors)
        self.register_button.pack(padx=100, pady=(20, 10))

        self.modify_button = tk.Button(self.button_frame, text="Modyfikacja zawodników",
                                       command=self.modify_competitors)
        self.modify_button.pack(padx=100, pady=10)

        self.set_category_button = tk.Button(self.button_frame, text="Zarządzanie kategoriami",
                                             command=self.set_category)
        self.set_category_button.pack(padx=100, pady=10)

        self.start_button = tk.Button(self.button_frame, text="Start zawodów", command=self.start_competition)
        self.start_button.pack(padx=100, pady=10)

        self.clear_button = tk.Button(self.button_frame, text="Wyczyść", command=self.clear_competitors)
        self.clear_button.pack(padx=100, pady=10)

        self.table_frame = tk.Frame(self.window)
        self.table_frame.grid(row=0, column=1, sticky='ns', pady=(20, 0))

        self.tree = ttk.Treeview(self.table_frame)
        self.tree["columns"] = ("zero", "one", "two", "three", "four", "five", "six", "seven", "eight")
        self.tree.column("#0", width=0)
        self.tree.column("zero", width=50)
        self.tree.column("one", width=50)
        self.tree.column("two", width=100)
        self.tree.column("three", width=100)
        self.tree.column("four", width=100)
        self.tree.column("five", width=100)
        self.tree.column("six", width=250)
        self.tree.column("seven", width=100)
        self.tree.column("eight", width=100)

        self.tree.heading("zero", text="Numer")
        self.tree.heading("one", text="ID")
        self.tree.heading("two", text="Imię")
        self.tree.heading("three", text="Nazwisko")
        self.tree.heading("four", text="DB urodzenia")
        self.tree.heading("five", text="Nr telefonu")
        self.tree.heading("six", text="Dane opiekuna")
        self.tree.heading("seven", text="Pojazd")
        self.tree.heading("eight", text="Kat. wiekowa")

        self.tree.pack()

        self.bike_button = tk.Button(self.table_frame, text="Rower", command=lambda: self.filter_table('rower'))
        self.bike_button.pack(side='left')

        self.scooter_button = tk.Button(self.table_frame, text="Hulajnoga",
                                        command=lambda: self.filter_table('hulajnoga'))
        self.scooter_button.pack(side='left')

        self.all_button = tk.Button(self.table_frame, text="Wszystko", command=self.filter_table)
        self.all_button.pack(side='left')

        self.search_label = tk.Label(self.table_frame, text="Szukaj:")
        self.search_label.pack(side='left')

        self.search_entry = tk.Entry(self.table_frame)
        self.search_entry.pack(side='left')

        self.search_button = tk.Button(self.table_frame, text="Szukaj", command=self.search_table)
        self.search_button.pack(side='left')

        self.category_label = tk.Label(self.table_frame, text="Filtruj po kategorii:")
        self.category_label.pack(side='left')

        self.category_combobox = ttk.Combobox(self.table_frame, values=self.get_categories())
        self.category_combobox.bind("<<ComboboxSelected>>", self.filter_by_category)
        self.category_combobox.pack(side='left')

    def register_competitors(self):
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

        register_window = tk.Toplevel(self.window)
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
        category_entry = ttk.Combobox(register_window, values=self.get_categories())
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

    def modify_competitors(self):
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

        modify_window = tk.Toplevel(self.window)
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
        category_entry = ttk.Combobox(modify_window, values=self.get_categories())
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

    def start_competition(self):
        root = tk.Toplevel(self.window)
        root.geometry('1350x270')
        root.resizable(False, False)
        app = RaceInterface(root)
        app.mainloop()

    def set_category(self):
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

            self.category_combobox['values'] = self.get_categories()

            category_window.destroy()

        category_window = tk.Toplevel(self.window)
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

    def clear_competitors(self):
        delete_all_competitors = messagebox.askyesno("Potwierdzenie",
                                                     "Czy na pewno chcesz usunąć wszystkich zawodników ich dane oraz kategorie?")
        if delete_all_competitors:
            c.execute("DELETE FROM Zawodnik")
            c.execute("DELETE FROM Kategoria")
            c.execute("DELETE FROM Przejazd")
            conn.commit()
            messagebox.showinfo("Informacja", "Baza danych została wyczyszczona!")
        self.filter_table()

    def get_categories(self):
        c.execute("SELECT nazwa FROM Kategoria")
        categories = c.fetchall()
        return [category[0] for category in categories]

    def filter_by_category(self, event=None):
        for row in self.tree.get_children():
            self.tree.delete(row)

        category = self.category_combobox.get() or ''

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
            self.tree.insert('', 'end', values=(index,) + row)

    def filter_table(self, vehicle=None):
        for row in self.tree.get_children():
            self.tree.delete(row)

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
            self.tree.insert('', 'end', values=(index,) + row)

    def search_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        keyword = self.search_entry.get()

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
            self.tree.insert('', 'end', values=(index,) + row)


program = MainInterface()
program.window.mainloop()
