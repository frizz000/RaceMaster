from flask import Flask, render_template
import sqlite3

class TableWWW:
    def __init__(self):
        self.app = Flask(__name__, template_folder='../templates', static_folder='../static')
        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/')
        def home():
            conn = sqlite3.connect('../zawody.db')
            c = conn.cursor()

            c.execute('''
                    SELECT Zawodnik.id, imie, nazwisko, dataUrodzenia, Kategoria.nazwa, GROUP_CONCAT(Przejazd.czasPrzejazdu)
                    FROM Zawodnik
                    JOIN Kategoria ON Zawodnik.Kategoria_id = Kategoria.id
                    LEFT JOIN Przejazd ON Zawodnik.id = Przejazd.Zawodnik_id
                    GROUP BY Zawodnik.id
                ''')
            zawodnicy = c.fetchall()

            zawodnicy = [(id, imie, nazwisko, dataUrodzenia, nazwa, "brak czasu" if czasy is None else czasy) for id, imie, nazwisko, dataUrodzenia, nazwa, czasy in zawodnicy]

            max_przejazdy = max(len(zawodnik[5].split(',')) for zawodnik in zawodnicy)

            return render_template('index.html', zawodnicy=zawodnicy, max_przejazdy=max_przejazdy)

    def run(self):
        self.app.run(debug=True)

if __name__ == '__main__':
    my_app = TableWWW()
    my_app.run()
