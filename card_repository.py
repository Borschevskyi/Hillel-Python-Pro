import os

import psycopg2
from dotenv import load_dotenv

from card import Card

load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


class CardRepository:
    def __init__(self):
        self.password = os.getenv("PASSWORD")
        self.connection = self.connect_to_db()

    def connect_to_db(self):
        db_pass = str(input("Please enter the password: "))
        if self.password != db_pass:
            raise Exception("Wrong password")
        connection = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
        )
        return connection

    def create_table_cards(self, name: str = "cards"):
        query = f"""
            CREATE TABLE IF NOT EXISTS {name} (
                id SERIAL PRIMARY KEY,
                pan TEXT,
                expiration_date TEXT,
                cvv TEXT,
                issue_date TEXT,
                owner_id TEXT UNIQUE,
                status TEXT
            )
        """
        self.connection.cursor().execute(query)
        self.connection.commit()

    def save_card(self, card):
        existing_card = self.get_card_by_pan(card.pan)
        if existing_card:
            raise ValueError("A card with the same PAN already exists.")
        try:
            query = """
                INSERT INTO cards (pan, expiration_date, cvv, issue_date, owner_id, status)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
            self.connection.cursor().execute(
                query,
                (
                    card.pan,
                    card.expiration_date,
                    card.cvv,
                    card.issue_date,
                    card.owner_id,
                    str(card.status),
                ),
            )
            self.connection.commit()
        except psycopg2.Error as e:
            print(f"Error occurred while saving card: {e}")

    def get_cards(self) -> list:
        query = """
            SELECT * FROM cards
            """
        cursor = self.connection.cursor()
        cursor.execute(query)
        cards = []
        for row in cursor:
            card = Card(row[1], row[2], row[3], row[4], row[5], row[6])
            cards.append(card)
        return cards

    def get_card_by_pan(self, pan: str):
        query = """
            SELECT * FROM cards WHERE pan = %s
            """
        cursor = self.connection.cursor()
        cursor.execute(query, (pan,))
        row = cursor.fetchone()
        if row:
            card = Card(row[1], row[2], row[3], row[4], row[5], row[6])
            return card
        return None

    def update_card(self, card):
        try:
            query = """
                UPDATE cards SET expiration_date = %s, cvv = %s, issue_date = %s, owner_id = %s, status = %s
                WHERE pan = %s
                """
            cursor = self.connection.cursor()
            cursor.execute(
                query,
                (
                    card.expiration_date,
                    card.cvv,
                    card.issue_date,
                    card.owner_id,
                    str(card.status),
                    card.pan,
                ),
            )
            self.connection.commit()
        except psycopg2.Error as e:
            print(f"Error occurred while updating card: {e}")

    def get_card_by_uuid(self, user_id):
        query = """
                    SELECT * FROM cards WHERE owner_id = %s
                    """
        cursor = self.connection.cursor()
        cursor.execute(query, (user_id,))
        row = cursor.fetchone()
        if row:
            card = Card(row[1], row[2], row[3], row[4], row[5], row[6])
            return card
        return None

    def close(self):
        self.connection.close()
