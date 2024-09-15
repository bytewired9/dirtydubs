import os
import random
import re
import sqlite3
import nltk
from nltk.tokenize import word_tokenize

def replace_with_curated_synonyms(sentence):
    synonym_dict = {
        "went": ["visited", "checked out", "explored"],
        "great": ["fantastic", "wonderful", "excellent"],
        "experience": ["time", "visit", "outing"],
        "friendly": ["welcoming", "hospitable", "cordial"],
        "delicious": ["tasty", "savory", "flavorful"],
        "enjoyed": ["loved", "appreciated", "relished"],
        "time": ["evening", "night", "day"],
        "food": ["meal", "dishes", "cuisine"],
        "perfect": ["ideal", "flawless", "excellent"],
        "memorable": ["unforgettable", "remarkable", "noteworthy"],
        "favorite": ["preferred", "beloved", "top choice"],
        "service": ["assistance", "help", "support"],
        "definitely": ["certainly", "surely", "undoubtedly"],
        "staff": ["team", "crew", "personnel"],
    }
    tokens = word_tokenize(sentence)
    new_sentence = []
    for word in tokens:
        if word.lower() in synonym_dict and random.random() < 0.2:  # 20% chance to replace with a curated synonym
            new_word = random.choice(synonym_dict[word.lower()])
            new_sentence.append(new_word)
        else:
            new_sentence.append(word)
    return " ".join(new_sentence)


def clean_text(text):
    # Fix common contractions
    contractions = {
        " n't": "n't",
        " 've": "'ve",
        " 'll": "'ll",
        " 're": "'re",
        " 'd": "'d",
        "' s": "'s",
    }

    for contraction, fixed in contractions.items():
        text = text.replace(contraction, fixed)

    # Clean up spacing around punctuation
    text = re.sub(r"\s+([.,!?])", r"\1", text)  # Remove space before punctuation
    text = re.sub(r"([.,!?])\s+(?=[A-Z])", r"\1 ", text)  # Ensure space after punctuation
    text = re.sub(r"\s+(\')\s*", r"\1", text)  # Remove spaces around apostrophes

    return text


def find_db_files(directory):
    return [file for file in os.listdir(os.path.abspath(directory)) if file.endswith(".db")]


def table_exists(cursor, table_name):
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    return bool(cursor.fetchone())


def select_pack(cursor):
    if table_exists(cursor, "config"):
        cursor.execute("PRAGMA table_info(config)")
        columns = [info[1] for info in cursor.fetchall()]
        if "pack_name" in columns and "exclusive" in columns:
            cursor.execute("SELECT pack_name, exclusive FROM config")

            cursor.execute("SELECT pack_name FROM config WHERE exclusive = 1")
            exclusive_packs = cursor.fetchall()
            if exclusive_packs:
                exclusive_packs = [pack[0] for pack in exclusive_packs]
                selected_pack = sorted(exclusive_packs)[-1]
            else:
                cursor.execute("SELECT pack_name FROM config")
                all_packs = cursor.fetchall()
                if all_packs:
                    all_packs = [pack[0] for pack in all_packs]
                    selected_pack = random.choice(all_packs)
                else:
                    raise Exception("No packs available in the config table.")
            return selected_pack
        else:
            raise Exception("The config table does not contain the required fields.")
    else:
        raise Exception("No config table found in the database.")


def generate_review(review_chance, min_phrases=3, max_phrases=5):
    db_files = find_db_files(os.path.join(os.path.dirname(__file__), "../../language_packs"))
    if not db_files:
        raise Exception("No .db files found in the directory.")

    selected_db = None
    selected_pack = None

    for db_file in db_files:
        db_path = os.path.join(os.path.dirname(__file__), "../../language_packs", db_file)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        try:
            pack = select_pack(cursor)
            if pack:
                if selected_pack is None or (selected_pack is not None and selected_pack < pack):
                    selected_db = db_path
                    selected_pack = pack
        except Exception as e:
            print(f"Skipping {db_file} due to error: {e}")
        finally:
            conn.close()

    if not selected_db or not selected_pack:
        raise Exception("No suitable pack found in any .db files.")

    conn = sqlite3.connect(selected_db)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT phrase FROM Phrases 
        WHERE id IN (
            SELECT child_id FROM PhraseRelations 
            WHERE parent_id = (
                SELECT id FROM Phrases WHERE phrase = "start"
            )
        )
    """
    )
    current_node = random.choice(cursor.fetchall())[0]
    review = [current_node]
    phrase_count = random.randint(min_phrases, max_phrases)

    while len(review) < phrase_count:
        cursor.execute(
            """
            SELECT phrase FROM Phrases 
            WHERE id IN (
                SELECT child_id FROM PhraseRelations 
                WHERE parent_id = (
                    SELECT id FROM Phrases WHERE phrase = ?
                )
            )
        """,
            (current_node,),
        )
        possible_phrases = cursor.fetchall()
        if not possible_phrases:
            break
        next_phrase = random.choice(possible_phrases)[0]
        review.append(next_phrase)
        current_node = next_phrase

    if len(review) < min_phrases:
        raise Exception(f"Unable to generate review with the minimum number of phrases. \n {review}")

    while True:
        cursor.execute(
            """
            SELECT phrase FROM RequiredContinuations WHERE pack_name = ?
        """,
            (selected_pack,),
        )
        required_continuations = [row[0] for row in cursor.fetchall()]
        if review[-1] not in required_continuations:
            break
        cursor.execute(
            """
            SELECT phrase FROM Phrases 
            WHERE id IN (
                SELECT child_id FROM PhraseRelations 
                WHERE parent_id = (
                    SELECT id FROM Phrases WHERE phrase = ?
                )
            )
        """,
            (review[-1],),
        )
        possible_phrases = cursor.fetchall()
        if not possible_phrases:
            break
        next_phrase = random.choice(possible_phrases)[0]
        review.append(next_phrase)
        if not next_phrase.endswith((".", "!", "?")):
            review[-1] += "."

    if not review[-1].endswith((".", "!", "?")):
        review[-1] += "."

    if random.random() > 0.25:
        cursor.execute("SELECT ending FROM Endings ORDER BY RANDOM() LIMIT 1")
        ending = cursor.fetchone()[0]
        review.append(ending)

    review_text = " ".join(review)

    if random.random() < 0.3:
        cursor.execute("SELECT prefix FROM Prefixes ORDER BY RANDOM() LIMIT 1")
        prefix = cursor.fetchone()[0]
        review_text = prefix + " " + review_text

    review_text = replace_with_curated_synonyms(review_text)

    review_text = clean_text(review_text)
    if random.random() < 0.10:
        review_text = review_text.lower()

    if random.random() > float(review_chance):
        review_text = ""

    conn.close()
    return review_text

# Suppress NLTK download messages
nltk.download("punkt", quiet=True)
nltk.download("averaged_perceptron_tagger", quiet=True)