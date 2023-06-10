from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    conn = sqlite3.connect('../zawody.db')
    c = conn.cursor()

    query = 'SELECT imie, nazwisko, Kategoria.nazwa, Przejazd.czasPrzejazdu FROM Zawodnik JOIN Przejazd ON Zawodnik.id = Przejazd.Zawodnik_id JOIN Kategoria ON Zawodnik.Kategoria_id = Kategoria.id'
    c.execute(query)
    data = c.fetchall()

    return render_template('data.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
