import threading
from dotenv import load_dotenv
import psycopg2
import os

class ThreadLocalCursor:
    """Daje svakom threadu zaseban cursor nad postojećom konekcijom."""

    def __init__(self, konekcija):
        self.konekcija = konekcija
        self.lokalni_podaci = threading.local()

    def _cursor(self):
        if not hasattr(self.lokalni_podaci, "kursor"):
            self.lokalni_podaci.kursor = self.konekcija.cursor()
        return self.lokalni_podaci.kursor

    def __getattr__(self, naziv):
        return getattr(self._cursor(), naziv)

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


if DATABASE_URL:
    konekcija1 = psycopg2.connect(DATABASE_URL)
else:
    konekcija1 = psycopg2.connect(
        dbname="korisnici_db",
        user="postgres",
        password= os.getenv("SIFRA"),
        host=os.getenv("DB_HOST", "localhost"),
        port="5432"
        )
kursor1 = ThreadLocalCursor(konekcija1)

kursor1.execute("""
    CREATE TABLE IF NOT EXISTS korisnici (
        id SERIAL PRIMARY KEY,
        korisnicko_ime TEXT UNIQUE,
        lozinka_hash TEXT
    )
""")
konekcija1.commit()