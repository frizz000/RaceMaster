import tkinter as tk
from tkinter import messagebox
import sqlite3
import pandas as pd

conn = sqlite3.connect('zawody.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS zawodnicy (
        id INTEGER PRIMARY KEY,
        imie TEXT,
        nazwisko TEXT,
        data_urodzenia Date,
        pojazd TEXT
    )
''')
conn.commit()


def register_competitors():
    def save_competitor():
        imie = name_entry.get()
        nazwisko = surname_entry.get()
        data_urodzenia = dob_entry.get()
        pojazd = vehicle.get()

        c.execute('INSERT INTO zawodnicy (imie, nazwisko, data_urodzenia, pojazd) VALUES (?, ?, ?, ?)',
                  (imie, nazwisko, data_urodzenia, pojazd))
        conn.commit()
        messagebox.showinfo("Informacja", "Zawodnik zarejestrowany pomyślnie!")
        register_window.destroy()

    register_window = tk.Toplevel(window)
    register_window.geometry('400x500')
    register_window.title("Rejestracja zawodników")
    #register_window.configure(bg='blue')

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

        c.execute('''
            UPDATE zawodnicy
            SET imie = ?, nazwisko = ?, data_urodzenia = ?, pojazd = ?
            WHERE id = ?
        ''', (imie, nazwisko, data_urodzenia, pojazd, id_zawodnika))
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

    original_df = pd.read_sql_query("SELECT * FROM zawodnicy", conn)
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


window = tk.Tk()
window.geometry('400x300')
window.title("System do mierzenia czasu na zawodach rowerowych")

frame1 = tk.Frame(window)
frame1.pack(fill=tk.X)
register_button = tk.Button(frame1, text="Rejestracja zawodników", command=register_competitors)
register_button.pack(padx=100, pady=20)

frame2 = tk.Frame(window)
frame2.pack(fill=tk.X)
modify_button = tk.Button(frame2, text="Modyfikacja zawodników", command=modify_competitors)
modify_button.pack(padx=100, pady=20)

frame3 = tk.Frame(window)
frame3.pack(fill=tk.X)
view_button = tk.Button(frame3, text="Zawodnicy", command=view_competitors)
view_button.pack(padx=100, pady=20)

frame4 = tk.Frame(window)
frame4.pack(fill=tk.X)
start_button = tk.Button(frame4, text="Start zawodów", command=start_competition)
start_button.pack(padx=100, pady=20)

frame5 = tk.Frame(window)
frame5.pack(fill=tk.X)
exit_button = tk.Button(frame5, text="Wyjście", command=quit_app)
exit_button.pack(padx=100, pady=20)

window.mainloop()
