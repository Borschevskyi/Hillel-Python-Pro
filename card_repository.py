import os
import sqlite3

from dotenv import load_dotenv

from card import Card

load_dotenv()


class CardRepository:
    def __init__(self, db_file: str = "card.db"):
        self.db_path = os.path.join(os.getcwd(), db_file)
        self.password = os.getenv("PASSWORD")
        self.connection = self.connect_to_db()

    def connect_to_db(self):
        db_pass = str(input("Please enter the password: "))
        if self.password != db_pass:
            raise Exception("Wrong password")
        self.connection = sqlite3.connect(self.db_path)
        return self.connection

    def create_table(self, name: str = "cards"):
        query = f"""
            CREATE TABLE IF NOT EXISTS {name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pan TEXT,
                expiration_date TEXT,
                cvv TEXT,
                issue_date TEXT,
                owner_id TEXT,
                status TEXT
            )
        """
        self.connection.execute(query)
        self.connection.commit()

    def save_card(self, card):
        existing_card = self.get_card_by_pan(card.pan)
        if existing_card:
            raise ValueError("A card with the same PAN already exists.")
        try:
            query = """
                INSERT INTO cards (pan, expiration_date, cvv, issue_date, owner_id, status)
                    VALUES (?, ?, ?, ?, ?, ?)
                """
            self.connection.execute(
                query,
                (
                    card.pan,
                    card.expiration_date,
                    card.cvv,
                    card.issue_date,
                    card.user_id,
                    str(card.status),
                ),
            )
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error occurred while saving card: {e}")

    def get_cards(self) -> list:
        query = """
                SELECT * FROM cards
                """
        cursor = self.connection.execute(query)
        cards = []
        for row in cursor:
            card = Card(row[1], row[2], row[3], row[4], row[5], row[6])
            cards.append(card)
        return cards

    def get_card_by_pan(self, pan: str):
        query = """
            SELECT * FROM cards WHERE pan = ?
            """
        cursor = self.connection.execute(query, (pan,))
        row = cursor.fetchone()
        if row:
            card = Card(row[1], row[2], row[3], row[4], row[5], row[6])
            return card
        return None

    def update_card(self, card):
        try:
            query = """
                UPDATE cards SET expiration_date = ?, cvv = ?, issue_date = ?, owner_id = ?, status = ?
                WHERE pan = ?
                """
            self.connection.execute(
                query,
                (
                    card.expiration_date,
                    card.cvv,
                    card.issue_date,
                    card.user_id,
                    str(card.status),
                    card.pan,
                ),
            )
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error occurred while updating card: {e}")

    def close(self):
        self.connection.close()
