import random
import contextlib
import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

# Suppress NLTK download messages
with contextlib.redirect_stdout(open(os.devnull, 'w')):
    nltk.download('punkt', quiet=True)
    nltk.download('averaged_perceptron_tagger', quiet=True)

# Define the expanded tree structure with proper continuations
review_tree = {
    "start": [
        "I", "We", "My family", "Our friends", "A group of us", "My colleagues and I",
        "My partner and I", "The kids and I", "Our team", "My buddies and I",
        "My roommates", "My neighbors and I", "My classmates and I", "Our sports team",
        "The whole gang", "The entire office", "My best friend and I", "My siblings and I"
    ],
    "I": [
        "went", "had a great time", "loved", "enjoyed our visit", "visited",
        "experienced", "had an amazing dinner", "checked out", "tried", "decided to go",
        "spent the evening", "had a lunch", "decided to have a meal"
    ],
    "We": [
        "went", "had a fantastic experience", "enjoyed", "loved our time", "checked out",
        "decided to try", "had an incredible lunch", "experienced", "tried", "spent our evening",
        "had a fun time", "had a great night", "chose to dine"
    ],
    "My family": [
        "visited", "had a wonderful time", "loved", "enjoyed our outing", "went",
        "had an amazing day", "checked out", "tried", "decided to go", "spent our evening",
        "had a lunch", "had a great dinner", "spent a fantastic time"
    ],
    "Our friends": [
        "went", "had a great day", "enjoyed", "had a blast", "checked out",
        "experienced", "decided to try", "had a fun night", "tried", "spent our evening",
        "chose to dine", "had a great time", "had a fun day"
    ],
    "A group of us": [
        "went", "had a fun evening", "enjoyed our visit", "checked out",
        "loved", "tried out", "visited", "spent the evening", "had a blast", "decided to go",
        "had a great time", "tried", "chose to dine"
    ],
    "My colleagues and I": [
        "went", "had a team outing", "enjoyed", "loved our visit", "had a fantastic lunch",
        "checked out", "decided to try", "experienced", "had a great time", "spent our evening",
        "chose to dine", "tried", "spent a fun time"
    ],
    "My partner and I": [
        "went", "had a date night", "loved our evening", "enjoyed our dinner",
        "visited", "tried", "checked out", "had a fantastic time", "spent our night",
        "decided to go", "had a great time", "chose to dine"
    ],
    "The kids and I": [
        "went", "had a fun day", "loved", "enjoyed our visit", "checked out",
        "tried", "visited", "had a blast", "spent the day", "decided to go",
        "had a great time", "spent our evening"
    ],
    "Our team": [
        "went", "had a great outing", "enjoyed", "loved our time", "checked out",
        "decided to try", "experienced", "tried", "spent our evening", "had a fantastic time",
        "had a great night", "chose to dine", "spent the evening"
    ],
    "My buddies and I": [
        "went", "had a guys' night", "enjoyed", "loved our visit", "had a fantastic dinner",
        "checked out", "decided to try", "experienced", "had a great time", "spent our evening",
        "had a fun time", "tried", "chose to dine"
    ],
    "My roommates": [
        "went", "had a fun evening", "enjoyed our visit", "checked out",
        "loved", "tried out", "visited", "spent the evening", "had a blast", "decided to go",
        "had a great time", "tried", "chose to dine"
    ],
    "My neighbors and I": [
        "went", "had a great time", "enjoyed", "loved our visit", "checked out",
        "decided to try", "experienced", "tried", "spent the evening", "had a fantastic time",
        "had a fun night", "chose to dine"
    ],
    "My classmates and I": [
        "went", "had a study break", "enjoyed", "loved our visit", "checked out",
        "decided to try", "experienced", "tried", "spent our evening", "had a great time",
        "had a fun time", "chose to dine"
    ],
    "Our sports team": [
        "went", "had a team celebration", "enjoyed", "loved our time", "checked out",
        "decided to try", "experienced", "tried", "spent our evening", "had a fantastic time",
        "had a great night", "chose to dine", "spent the evening"
    ],
    "The whole gang": [
        "went", "had a fun evening", "enjoyed our visit", "checked out",
        "loved", "tried out", "visited", "spent the evening", "had a blast", "decided to go",
        "had a great time", "tried", "chose to dine"
    ],
    "The entire office": [
        "went", "had an office outing", "enjoyed", "loved our visit", "had a team lunch",
        "checked out", "decided to try", "experienced", "had a great time", "spent our evening",
        "chose to dine", "tried", "spent a fun time"
    ],
    "My best friend and I": [
        "went", "had a great time", "loved", "enjoyed our visit", "visited",
        "experienced", "had an amazing dinner", "checked out", "tried", "decided to go",
        "spent the evening", "had a lunch", "decided to have a meal"
    ],
    "My siblings and I": [
        "went", "had a sibling outing", "enjoyed", "loved our visit", "had a family dinner",
        "checked out", "decided to try", "experienced", "had a great time", "spent our evening",
        "chose to dine", "tried", "spent a fun time"
    ],

    "went": [
        "to Buffalo Wild Wings.", "to BWW.", "to B-Dubs.", "to the local Buffalo Wild Wings.",
        "to our favorite wing spot.", "to the new Buffalo Wild Wings in town.", "to the nearby BWW.",
        "to our go-to B-Dubs.", "to the Buffalo Wild Wings downtown.", "to the popular BWW nearby."
    ],
    "had a great time": [
        "at Buffalo Wild Wings.", "at BWW.", "at B-Dubs.", "at the local Buffalo Wild Wings.",
        "at our favorite wing spot.", "at the new Buffalo Wild Wings in town.", "at the nearby BWW.",
        "at our go-to B-Dubs.", "at the Buffalo Wild Wings downtown.", "at the popular BWW nearby."
    ],
    "loved": [
        "the food at Buffalo Wild Wings.", "the atmosphere at BWW.", "our experience at B-Dubs.",
        "the wings at the local Buffalo Wild Wings.",
        "the service at our favorite wing spot.", "everything about the new Buffalo Wild Wings in town.",
        "the drinks at the nearby BWW.",
        "the vibe at our go-to B-Dubs.", "the menu at the Buffalo Wild Wings downtown.",
        "the specials at the popular BWW nearby."
    ],
    "enjoyed our visit": [
        "to Buffalo Wild Wings.", "to BWW.", "to B-Dubs.", "to the local Buffalo Wild Wings.",
        "to our favorite wing spot.", "to the new Buffalo Wild Wings in town.", "to the nearby BWW.",
        "to our go-to B-Dubs.", "to the Buffalo Wild Wings downtown.", "to the popular BWW nearby."
    ],
    "had a fantastic experience": [
        "at Buffalo Wild Wings.", "at BWW.", "at B-Dubs.", "at the local Buffalo Wild Wings.",
        "at our favorite wing spot.", "at the new Buffalo Wild Wings in town.", "at the nearby BWW.",
        "at our go-to B-Dubs.", "at the Buffalo Wild Wings downtown.", "at the popular BWW nearby."
    ],
    "enjoyed": [
        "the wings at Buffalo Wild Wings.", "the atmosphere at BWW.", "our visit to B-Dubs.",
        "the drinks at the local Buffalo Wild Wings.",
        "the variety at our favorite wing spot.", "the vibe at the new Buffalo Wild Wings in town.",
        "the service at the nearby BWW.",
        "the menu at our go-to B-Dubs.", "the desserts at the Buffalo Wild Wings downtown.",
        "the appetizers at the popular BWW nearby."
    ],
    "loved our time": [
        "at Buffalo Wild Wings.", "at BWW.", "at B-Dubs.", "at the local Buffalo Wild Wings.",
        "at our favorite wing spot.", "at the new Buffalo Wild Wings in town.", "at the nearby BWW.",
        "at our go-to B-Dubs.", "at the Buffalo Wild Wings downtown.", "at the popular BWW nearby."
    ],
    "visited": [
        "Buffalo Wild Wings.", "BWW.", "B-Dubs.", "the local Buffalo Wild Wings.",
        "our favorite wing spot.", "the new Buffalo Wild Wings in town.", "the nearby BWW.",
        "our go-to B-Dubs.", "the Buffalo Wild Wings downtown.", "the popular BWW nearby."
    ],
    "had a wonderful time": [
        "at Buffalo Wild Wings.", "at BWW.", "at B-Dubs.", "at the local Buffalo Wild Wings.",
        "at our favorite wing spot.", "at the new Buffalo Wild Wings in town.", "at the nearby BWW.",
        "at our go-to B-Dubs.", "at the Buffalo Wild Wings downtown.", "at the popular BWW nearby."
    ],
    "enjoyed our outing": [
        "to Buffalo Wild Wings.", "to BWW.", "to B-Dubs.", "to the local Buffalo Wild Wings.",
        "to our favorite wing spot.", "to the new Buffalo Wild Wings in town.", "to the nearby BWW.",
        "to our go-to B-Dubs.", "to the Buffalo Wild Wings downtown.", "to the popular BWW nearby."
    ],
    "had a great day": [
        "at Buffalo Wild Wings.", "at BWW.", "at B-Dubs.", "at the local Buffalo Wild Wings.",
        "at our favorite wing spot.", "at the new Buffalo Wild Wings in town.", "at the nearby BWW.",
        "at our go-to B-Dubs.", "at the Buffalo Wild Wings downtown.", "at the popular BWW nearby."
    ],
    "had a blast": [
        "at Buffalo Wild Wings.", "at BWW.", "at B-Dubs.", "at the local Buffalo Wild Wings.",
        "at our favorite wing spot.", "at the new Buffalo Wild Wings in town.", "at the nearby BWW.",
        "at our go-to B-Dubs.", "at the Buffalo Wild Wings downtown.", "at the popular BWW nearby."
    ],
    "checked out": [
        "Buffalo Wild Wings.", "BWW.", "B-Dubs.", "the local Buffalo Wild Wings.",
        "our favorite wing spot.", "the new Buffalo Wild Wings in town.", "the nearby BWW.",
        "our go-to B-Dubs.", "the Buffalo Wild Wings downtown.", "the popular BWW nearby."
    ],
    "experienced": [
        "Buffalo Wild Wings.", "BWW.", "B-Dubs.", "the local Buffalo Wild Wings.",
        "our favorite wing spot.", "the new Buffalo Wild Wings in town.", "the nearby BWW.",
        "our go-to B-Dubs.", "the Buffalo Wild Wings downtown.", "the popular BWW nearby."
    ],
    "decided to try": [
        "Buffalo Wild Wings.", "BWW.", "B-Dubs.", "the local Buffalo Wild Wings.",
        "our favorite wing spot.", "the new Buffalo Wild Wings in town.", "the nearby BWW.",
        "our go-to B-Dubs.", "the Buffalo Wild Wings downtown.", "the popular BWW nearby."
    ],
    "had an amazing dinner": [
        "at Buffalo Wild Wings.", "at BWW.", "at B-Dubs.", "at the local Buffalo Wild Wings.",
        "at our favorite wing spot.", "at the new Buffalo Wild Wings in town.", "at the nearby BWW.",
        "at our go-to B-Dubs.", "at the Buffalo Wild Wings downtown.", "at the popular BWW nearby."
    ],
    "had an incredible lunch": [
        "at Buffalo Wild Wings.", "at BWW.", "at B-Dubs.", "at the local Buffalo Wild Wings.",
        "at our favorite wing spot.", "at the new Buffalo Wild Wings in town.", "at the nearby BWW.",
        "at our go-to B-Dubs.", "at the Buffalo Wild Wings downtown.", "at the popular BWW nearby."
    ],
    "had a fun night": [
        "at Buffalo Wild Wings.", "at BWW.", "at B-Dubs.", "at the local Buffalo Wild Wings.",
        "at our favorite wing spot.", "at the new Buffalo Wild Wings in town.", "at the nearby BWW.",
        "at our go-to B-Dubs.", "at the Buffalo Wild Wings downtown.", "at the popular BWW nearby."
    ],
    "tried out": [
        "Buffalo Wild Wings.", "BWW.", "B-Dubs.", "the local Buffalo Wild Wings.",
        "our favorite wing spot.", "the new Buffalo Wild Wings in town.", "the nearby BWW.",
        "our go-to B-Dubs.", "the Buffalo Wild Wings downtown.", "the popular BWW nearby."
    ],
    "tried": [
        "Buffalo Wild Wings.", "BWW.", "B-Dubs.", "the local Buffalo Wild Wings.",
        "our favorite wing spot.", "the new Buffalo Wild Wings in town.", "the nearby BWW.",
        "our go-to B-Dubs.", "the Buffalo Wild Wings downtown.", "the popular BWW nearby."
    ],
    "had a team outing": [
        "at Buffalo Wild Wings.", "at BWW.", "at B-Dubs.", "at the local Buffalo Wild Wings.",
        "at our favorite wing spot.", "at the new Buffalo Wild Wings in town.", "at the nearby BWW.",
        "at our go-to B-Dubs.", "at the Buffalo Wild Wings downtown.", "at the popular BWW nearby."
    ],
    "had a date night": [
        "at Buffalo Wild Wings.", "at BWW.", "at B-Dubs.", "at the local Buffalo Wild Wings.",
        "at our favorite wing spot.", "at the new Buffalo Wild Wings in town.", "at the nearby BWW.",
        "at our go-to B-Dubs.", "at the Buffalo Wild Wings downtown.", "at the popular BWW nearby."
    ],
    "had a fun day": [
        "at Buffalo Wild Wings.", "at BWW.", "at B-Dubs.", "at the local Buffalo Wild Wings.",
        "at our favorite wing spot.", "at the new Buffalo Wild Wings in town.", "at the nearby BWW.",
        "at our go-to B-Dubs.", "at the Buffalo Wild Wings downtown.", "at the popular BWW nearby."
    ],
    "had a great outing": [
        "at Buffalo Wild Wings.", "at BWW.", "at B-Dubs.", "at the local Buffalo Wild Wings.",
        "at our favorite wing spot.", "at the new Buffalo Wild Wings in town.", "at the nearby BWW.",
        "at our go-to B-Dubs.", "at the Buffalo Wild Wings downtown.", "at the popular BWW nearby."
    ],
    "had a guys' night": [
        "at Buffalo Wild Wings.", "at BWW.", "at B-Dubs.", "at the local Buffalo Wild Wings.",
        "at our favorite wing spot.", "at the new Buffalo Wild Wings in town.", "at the nearby BWW.",
        "at our go-to B-Dubs.", "at the Buffalo Wild Wings downtown.", "at the popular BWW nearby."
    ]
}

# Possible endings
endings = [
    "It was a memorable experience.",
    "We will definitely come back.",
    "Highly recommended!",
    "Can't wait to visit again!",
    "Best wings in town!",
    "A must-visit for wing lovers.",
    "Absolutely loved it!",
    "Perfect spot for any occasion.",
    "An unforgettable experience.",
    "Totally worth it!",
    "The best dining experience we've had.",
    "Will be visiting again soon!",
    "Five stars!",
    "Simply the best!",
    "An exceptional experience.",
    "Top-notch service and food.",
    "A wonderful place to dine.",
    "Can't wait to return!",
    "Our new favorite spot!",
    "Exceeded our expectations.",
    "Loved every moment.",
    "A great place to unwind.",
    "Perfect for family outings.",
    "A delightful dining experience.",
    "Ideal for casual dining.",
    "The staff was amazing.",
    "An all-around fantastic time.",
    "Great food and great service.",
    "Made our day special.",
    "A treat for the taste buds.",
    "Perfect for our weekend.",
    "A dining experience to remember.",
    "A five-star experience.",
    "Wonderful from start to finish.",
    "The highlight of our week.",
    "A fantastic choice for dinner.",
    "Left us wanting more.",
    "Made our evening delightful.",
    "The best place for wings.",
    "An enjoyable time, every time.",
    "Made our celebration special.",
    "A great addition to our night out.",
    "Can't get enough of this place.",
    "Perfect for our get-together.",
    "A memorable dining experience.",
    "Top of our list for dining out.",
    "Always a fantastic time.",
    "A delightful surprise.",
    "Best dining choice we've made."
]

def generate_review(tree, min_phrases=10, max_phrases=30):
    current_node = random.choice(tree["start"])
    review = [current_node]
    phrase_count = random.randint(min_phrases, max_phrases)

    for _ in range(phrase_count - 1):  # Subtract 1 since we already have the starting phrase
        if current_node not in tree:
            break
        next_phrase = random.choice(tree[current_node])
        review.append(next_phrase)
        current_node = next_phrase
        # Randomly decide to stop early to vary length, but ensure minimum length
        if random.random() > 0.8 and len(review) >= min_phrases:
            break

    # Ensure there is a period or comma before adding the ending
    last_word = review[-1]
    if not last_word.endswith(('.', ',')):
        review[-1] += '.'

    review.append(random.choice(endings))
    review_text = " ".join(review)

    # Check grammatical correctness using NLTK POS tagging
    tokens = word_tokenize(review_text)
    pos_tags = pos_tag(tokens)


    return review_text