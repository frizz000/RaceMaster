from flask import Flask, render_template
import sqlite3

app = Flask(__name__, template_folder='../templates')


@app.route('/')
def home():
    conn = sqlite3.connect('../zawody.db')
    c = conn.cursor()

    c.execute('''
        SELECT Zawodnik.imie, Zawodnik.nazwisko, Zawodnik.dataUrodzenia, Kategoria.nazwa, Przejazd.czasPrzejazdu
        FROM Zawodnik
        JOIN Kategoria ON Zawodnik.Kategoria_id = Kategoria.id
        JOIN Przejazd ON Zawodnik.id = Przejazd.Zawodnik_id
        ''')
    zawodnicy = c.fetchall()

    return render_template('index.html', zawodnicy=zawodnicy)


if __name__ == '__main__':
    app.run(debug=True)
