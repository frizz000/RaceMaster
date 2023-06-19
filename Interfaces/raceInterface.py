import os
import threading
import tkinter as tk
from tkinter import ttk
import sqlite3
from datetime import datetime
from MeasuringTime.cam import Camera

import cv2


class RaceInterface:
    def __init__(self, root):
        self.root = root
        self.conn = sqlite3.connect('zawody.db')
        self.cursor = self.conn.cursor()
        self.current_rider_id = None
        self.camera_active = False
        self.stop_button_clicked = False

        self.category_select = ttk.Combobox(root)
        self.category_select.grid(row=0, column=0)

        self.start_button = tk.Button(root, text='Aktywuj kamerę', command=self.start_timer, state='disabled')
        self.start_button.grid(row=0, column=1)

        self.next_button = tk.Button(root, text='Następny zawodnik', command=self.next_rider, state='disabled')
        self.next_button.grid(row=0, column=2)

        self.timer_label = tk.Label(root, text='00:00:00.000')
        self.timer_label.grid(row=0, column=3)

        self.table = ttk.Treeview(root, columns=('id', 'imie', 'nazwisko', 'kategoria', 'czas 1', 'czas 2'))
        self.table.grid(row=1, column=0, columnspan=4, pady=(10, 0), padx=(20, 0))

        self.table.column('#0', width=0, stretch='NO')
        self.table.heading('id', text='ID')
        self.table.column('id', anchor='center')
        self.table.heading('imie', text='Imię')
        self.table.column('imie', anchor='center')
        self.table.heading('nazwisko', text='Nazwisko')
        self.table.column('nazwisko', anchor='center')
        self.table.heading('kategoria', text='Kategoria')
        self.table.column('kategoria', anchor='center')
        self.table.heading('czas 1', text='Czas 1')
        self.table.column('czas 1', anchor='center')
        self.table.heading('czas 2', text='Czas 2')
        self.table.column('czas 2', anchor='center')

        self.current_rider_label = tk.Label(root, text='')
        self.current_rider_label.grid(row=2, column=0, columnspan=4)

        self.load_categories()

    def load_categories(self):
        categories = self.cursor.execute('SELECT nazwa FROM Kategoria').fetchall()
        categories = [x[0] for x in categories]
        self.category_select['values'] = categories
        self.category_select.bind('<<ComboboxSelected>>', self.on_category_selected)

    def on_category_selected(self, event):
        category = self.category_select.get()
        riders = self.cursor.execute(
            'SELECT Zawodnik.id, imie, nazwisko, Kategoria.nazwa '
            'FROM Zawodnik JOIN Kategoria ON Zawodnik.Kategoria_id = Kategoria.id '
            'WHERE Kategoria.nazwa = ?',
            (category,)
        ).fetchall()

        for row in self.table.get_children():
            self.table.delete(row)
        for rider in riders:
            self.table.insert('', 'end', values=rider)

        self.current_rider_id = riders[0][0] if riders else None
        self.update_current_rider_label()

        if riders:
            self.start_button['state'] = 'normal'
            self.next_button['state'] = 'normal'
        else:
            self.start_button['state'] = 'disabled'
            self.next_button['state'] = 'disabled'

    def start_timer(self):
        self.Camera = Camera(50)
        self.camera_active = True
        self.measure_time()
        self.next_button['state'] = 'normal'

    def measure_time(self):
        if self.camera_active:
            elapsed_time = self.Camera.start()
            self.cursor.execute(
                'INSERT INTO Przejazd (czasPrzejazdu, Zawodnik_id) VALUES (?, ?)',
                (elapsed_time, self.current_rider_id)
            )
            self.conn.commit()
            self.root.after(1000, self.measure_time)

    def next_rider(self):
        self.current_rider_id += 1
        self.update_current_rider_label()

        self.camera_active = False

        self.start_time = None

        self.next_button['state'] = 'disabled'

    def update_timer_label(self):
        elapsed_time = datetime.now() - self.start_time
        self.timer_label['text'] = str(elapsed_time).split('.')[0] + '.' + str(elapsed_time).split('.')[1][:3]
        self.timer_after_id = self.timer_label.after(1, self.update_timer_label)

    def update_current_rider_label(self):
        if self.current_rider_id is not None:
            rider = self.cursor.execute(
                'SELECT Zawodnik.id, imie, nazwisko, Kategoria.nazwa FROM Zawodnik '
                'JOIN Kategoria ON Zawodnik.Kategoria_id = Kategoria.id '
                'WHERE Zawodnik.id = ?',
                (self.current_rider_id,)
            ).fetchone()

            if rider is not None:
                self.current_rider_label['text'] = 'Aktualny Zawodnik: ' + ' '.join(map(str, rider))
            else:
                self.current_rider_label['text'] = 'Nie ma więcej zawodników w tej kategorii.'
        else:
            self.current_rider_label['text'] = 'Nie wybrano zawodnika.'

    def mainloop(self):
        self.root.mainloop()

