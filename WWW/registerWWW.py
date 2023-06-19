from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__, template_folder='../templates', static_folder='../static')

@app.route('/', methods=['GET', 'POST'])
def register():
    conn = sqlite3.connect('../zawody.db')
    c = conn.cursor()

    if request.method == 'POST':
        imie = request.form['imie']
        nazwisko = request.form['nazwisko']
        dataUrodzenia = request.form['dataUrodzenia']
        nrTelefonu = request.form['nrTelefonu']
        daneOpiekuna = request.form['daneOpiekuna']
        pojazd = request.form['pojazd']
        Kategoria_nazwa = request.form['Kategoria']

        c.execute("SELECT id FROM Kategoria WHERE nazwa=?", (Kategoria_nazwa,))
        Kategoria_id = c.fetchone()[0]

        c.execute('''
            INSERT INTO Zawodnik (imie, nazwisko, dataUrodzenia, nrTelefonu, daneOpiekuna, pojazd, Kategoria_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (imie, nazwisko, dataUrodzenia, nrTelefonu, daneOpiekuna, pojazd, Kategoria_id))
        conn.commit()

        return redirect('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
    else:
        c.execute("SELECT nazwa FROM Kategoria")
        kategorie = [row[0] for row in c.fetchall()]
        return render_template('register.html', kategorie=kategorie)

if __name__ == '__main__':
    app.run(debug=True)
