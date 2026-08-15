import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()


class HistoryStore:

    def __init__(self):
        self.config = {
            "host": os.getenv("MYSQL_HOST", "localhost"),
            "port": int(os.getenv("MYSQL_PORT", "3306")),
            "user": os.getenv("MYSQL_USER", "root"),
            "password": os.getenv("MYSQL_PASSWORD", ""),
            "database": os.getenv("MYSQL_DATABASE", "fatiguesense")
        }

    def get_connection(self):
        return mysql.connector.connect(**self.config)

    def save_result(
        self,
        user_id,
        image_name,
        fatigue_score,
        risk_level,
        recommendation
    ):
        connection = None
        cursor = None

        try:
            connection = self.get_connection()
            cursor = connection.cursor()

            query = """
                INSERT INTO fatigue_history
                (
                    user_id,
                    image_name,
                    fatigue_score,
                    risk_level,
                    recommendation
                )
                VALUES (%s, %s, %s, %s, %s)
            """

            values = (
                user_id,
                image_name,
                fatigue_score,
                risk_level,
                recommendation
            )

            cursor.execute(query, values)
            connection.commit()

            return True

        except Error as e:
            print(f"MySQL error while saving result: {e}")
            return False

        finally:
            if cursor:
                cursor.close()

            if connection:
                connection.close()

    def get_history(self, user_id):
        connection = None
        cursor = None

        try:
            connection = self.get_connection()
            cursor = connection.cursor(dictionary=True)

            query = """
                SELECT
                    id,
                    user_id,
                    image_name,
                    fatigue_score,
                    risk_level,
                    recommendation,
                    timestamp
                FROM fatigue_history
                WHERE user_id = %s
                ORDER BY timestamp ASC
            """

            cursor.execute(query, (user_id,))

            results = cursor.fetchall()

            return results

        except Error as e:
            print(f"MySQL error while fetching history: {e}")
            return []

        finally:
            if cursor:
                cursor.close()

            if connection:
                connection.close()