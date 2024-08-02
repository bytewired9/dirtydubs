import os
import sqlite3
import random
import string

from tree import review_tree, endings, required_continuations, prefixes


def generate_random_pack_name(length=10):
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=length))


# Prompt user for pack name and exclusivity
pack_name = (
        input("Enter the pack name (default is a random 10-character string): ")
        or generate_random_pack_name()
)
db_file = f"{pack_name}.db"
db_exists = os.path.exists(db_file)

conn = sqlite3.connect(db_file)


def initialize_database():
    cursor = conn.cursor()

    # Create tables if they don't exist
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS Phrases (
        id INTEGER PRIMARY KEY,
        phrase TEXT UNIQUE
    )
    """
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS PhraseRelations (
        parent_id INTEGER,
        child_id INTEGER,
        pack_name TEXT,
        FOREIGN KEY (parent_id) REFERENCES Phrases (id),
        FOREIGN KEY (child_id) REFERENCES Phrases (id),
        FOREIGN KEY (pack_name) REFERENCES config (pack_name)
    )
    """
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS Endings (
        id INTEGER PRIMARY KEY,
        ending TEXT UNIQUE,
        pack_name TEXT,
        FOREIGN KEY (pack_name) REFERENCES config (pack_name)
    )
    """
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS config (
        pack_name TEXT PRIMARY KEY,
        exclusive BOOLEAN
    )
    """
    )

    # Create table for required continuations
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS RequiredContinuations (
        id INTEGER PRIMARY KEY,
        phrase TEXT UNIQUE,
        pack_name TEXT,
        FOREIGN KEY (pack_name) REFERENCES config (pack_name)
    )
    """
    )

    # Create table for prefixes
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS Prefixes (
        id INTEGER PRIMARY KEY,
        prefix TEXT UNIQUE,
        pack_name TEXT,
        FOREIGN KEY (pack_name) REFERENCES config (pack_name)
    )
    """
    )

    exclusive_input = input(
        "Is this pack exclusive? (default is False) [y/N]: "
    ).lower()
    exclusive = True if exclusive_input == "y" else False

    cursor.execute(
        "INSERT OR IGNORE INTO config (pack_name, exclusive) VALUES (?, ?)",
        (pack_name, exclusive),
    )

    # Check if the tables are already populated
    cursor.execute("SELECT COUNT(*) FROM Phrases")
    if cursor.fetchone()[0] == 0:
        # Populate the Phrases table
        phrases = set()
        for key, values in review_tree.items():
            if isinstance(key, tuple):
                phrases.update(key)
            else:
                phrases.add(key)
            phrases.update(values)

        cursor.executemany(
            "INSERT OR IGNORE INTO Phrases (phrase) VALUES (?)",
            [(phrase,) for phrase in phrases],
        )

        # Populate the PhraseRelations table
        for parent, children in review_tree.items():
            if isinstance(parent, tuple):
                parent_ids = []
                for subkey in parent:
                    parent_id = cursor.execute(
                        "SELECT id FROM Phrases WHERE phrase = ?", (subkey,)
                    ).fetchone()[0]
                    parent_ids.append(parent_id)
            else:
                parent_id = cursor.execute(
                    "SELECT id FROM Phrases WHERE phrase = ?", (parent,)
                ).fetchone()[0]
                parent_ids = [parent_id]

            for child in children:
                child_id = cursor.execute(
                    "SELECT id FROM Phrases WHERE phrase = ?", (child,)
                ).fetchone()[0]
                for parent_id in parent_ids:
                    cursor.execute(
                        "INSERT INTO PhraseRelations (parent_id, child_id, pack_name) VALUES (?, ?, ?)",
                        (parent_id, child_id, pack_name),
                    )

    cursor.execute("SELECT COUNT(*) FROM Endings")
    if cursor.fetchone()[0] == 0:
        # Populate the Endings table
        cursor.executemany(
            "INSERT OR IGNORE INTO Endings (ending, pack_name) VALUES (?, ?)",
            [(ending, pack_name) for ending in endings],
        )

    cursor.execute("SELECT COUNT(*) FROM RequiredContinuations")
    if cursor.fetchone()[0] == 0:
        # Populate the RequiredContinuations table
        cursor.executemany(
            "INSERT OR IGNORE INTO RequiredContinuations (phrase, pack_name) VALUES (?, ?)",
            [(phrase, pack_name) for phrase in required_continuations],
        )

    cursor.execute("SELECT COUNT(*) FROM Prefixes")
    if cursor.fetchone()[0] == 0:
        # Populate the Prefixes table
        cursor.executemany(
            "INSERT OR IGNORE INTO Prefixes (prefix, pack_name) VALUES (?, ?)",
            [(prefix, pack_name) for prefix in prefixes],
        )

    conn.commit()


if not db_exists:
    initialize_database()

conn.close()
