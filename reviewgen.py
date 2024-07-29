import random
import re
import sqlite3
import nltk
from nltk.tokenize import word_tokenize
# Suppress NLTK download messages
nltk.download("punkt", quiet=True)
nltk.download("averaged_perceptron_tagger", quiet=True)


required_continuations = {
    "decided to try",
    "checked out",
    "loved",
    "planned a team outing",
    "chose to dine",
    "decided to dine",
    "spent the evening",
    "decided to visit",
    "had a great day"
}


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
        "ca n't": "can't",
        "wo n't": "won't",
        "ai n't": "ain't",
        "n't": "n't",
        "'ve": "'ve",
        "'ll": "'ll",
        "'re": "'re",
        "'d": "'d",
        "'s": "'s"
    }

    for contraction, fixed in contractions.items():
        text = text.replace(contraction, fixed)

    # Clean up spacing around punctuation
    text = re.sub(r'\s+([.,!?])', r'\1', text)  # Remove space before punctuation
    text = re.sub(r'([.,!?])\s+(?=[A-Z])', r'\1 ', text)  # Ensure space after punctuation
    text = re.sub(r'\s+(\')\s*', r'\1', text)  # Remove spaces around apostrophes

    return text

def generate_review(min_phrases=3, max_phrases=7):
    conn = sqlite3.connect('review_tree.db')
    cursor = conn.cursor()
    cursor.execute('SELECT phrase FROM Phrases WHERE id IN (SELECT child_id FROM PhraseRelations WHERE parent_id = (SELECT id FROM Phrases WHERE phrase = "start"))')
    current_node = random.choice(cursor.fetchall())[0]
    review = [current_node]
    phrase_count = random.randint(min_phrases, max_phrases)

    for _ in range(phrase_count - 1):
        cursor.execute('SELECT phrase FROM Phrases WHERE id IN (SELECT child_id FROM PhraseRelations WHERE parent_id = (SELECT id FROM Phrases WHERE phrase = ?))', (current_node,))
        possible_phrases = cursor.fetchall()
        if not possible_phrases:
            break
        next_phrase = random.choice(possible_phrases)[0]
        review.append(next_phrase)
        current_node = next_phrase.split()[0]

    # Ensure the review ends with proper punctuation
    if not review[-1].endswith((".", "!", "?")):
        review[-1] += "."

    # Check if the last phrase requires a continuation
    while review[-1] in required_continuations:
        cursor.execute('SELECT phrase FROM Phrases WHERE id IN (SELECT child_id FROM PhraseRelations WHERE parent_id = (SELECT id FROM Phrases WHERE phrase = ?))', (review[-1],))
        possible_phrases = cursor.fetchall()
        if not possible_phrases:
            break
        next_phrase = random.choice(possible_phrases)[0]
        review.append(next_phrase)
        if not next_phrase.endswith((".", "!", "?")):
            review[-1] += "."

    # Add an ending with 75% chance
    if random.random() > 0.25:
        cursor.execute('SELECT ending FROM Endings ORDER BY RANDOM() LIMIT 1')
        ending = cursor.fetchone()[0]
        review.append(ending)

    review_text = " ".join(review)
    review_text = replace_with_curated_synonyms(review_text)
    
    # Clean up the text, including fixing contractions
    review_text = clean_text(review_text)
    if random.random() < 0.10:
        review_text = review_text.lower()
    return review_text
