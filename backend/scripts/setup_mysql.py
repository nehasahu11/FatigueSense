from sqlalchemy import text

from app.database.mysql.connection import (
    engine
)

from app.database.mysql.models import (
    Base
)


def create_database():

    database_name = "fatiguesense"

    root_url = (
        "mysql+pymysql://root:password@localhost:3306"
    )

    print(
        "Creating FatigueSense database..."
    )

    try:

        # Connect without selecting database
        from sqlalchemy import create_engine

        root_engine = create_engine(
            root_url,
            isolation_level="AUTOCOMMIT"
        )

        with root_engine.connect() as connection:

            connection.execute(
                text(
                    f"CREATE DATABASE IF NOT EXISTS "
                    f"{database_name}"
                )
            )

        root_engine.dispose()

        print(
            "Database created successfully."
        )

    except Exception as e:

        print(
            f"Database creation failed: {e}"
        )

        return


def create_tables():

    try:

        Base.metadata.create_all(
            bind=engine
        )

        print(
            "Tables created successfully."
        )

    except Exception as e:

        print(
            f"Table creation failed: {e}"
        )


if __name__ == "__main__":

    create_database()

    create_tables()

    print(
        "MySQL setup completed."
    )