# levels.py  -  Smart Kids Adventure
# Large question pools — the game randomly picks a subset each time you play.

import random

# ---------------------------------------------------------------
# PART 1  -  General Knowledge  (pool of 40 questions, pick 10)
# ---------------------------------------------------------------
POOL_PART1 = [
    # Letters
    {"question": "Catch the Letter  A", "options": ["A", "B", "C", "D"], "correct": "A"},
    {"question": "Catch the Letter  B", "options": ["D", "B", "F", "G"], "correct": "B"},
    {"question": "Catch the Letter  C", "options": ["C", "E", "K", "S"], "correct": "C"},
    {"question": "Catch the Letter  Z", "options": ["M", "N", "Z", "X"], "correct": "Z"},
    {"question": "Catch the Letter  M", "options": ["W", "M", "N", "H"], "correct": "M"},

    # Numbers
    {"question": "Catch the Number  5", "options": ["3", "5", "7", "9"], "correct": "5"},
    {"question": "Catch the Number  8", "options": ["6", "3", "8", "1"], "correct": "8"},
    {"question": "Catch the Number  2", "options": ["2", "7", "4", "9"], "correct": "2"},
    {"question": "Catch the Number  10", "options": ["10", "11", "12", "13"], "correct": "10"},
    {"question": "Catch the Number  0", "options": ["1", "0", "9", "5"], "correct": "0"},

    # Colors
    {"question": "Catch the Color  RED", "options": ["RED", "BLUE", "GREEN", "YELLOW"], "correct": "RED"},
    {"question": "Catch the Color  BLUE", "options": ["RED", "BLUE", "GREEN", "PINK"], "correct": "BLUE"},
    {"question": "Catch the Color  GREEN", "options": ["ORANGE", "GRAY", "GREEN", "BROWN"], "correct": "GREEN"},
    {"question": "Catch the Color  YELLOW", "options": ["WHITE", "YELLOW", "BLACK", "RED"], "correct": "YELLOW"},
    {"question": "Catch the Color  PINK", "options": ["PINK", "PURPLE", "RED", "BLUE"], "correct": "PINK"},

    # Animals
    {"question": "Catch the Animal  CAT", "options": ["DOG", "CAT", "COW", "LION"], "correct": "CAT"},
    {"question": "Catch the Animal  DOG", "options": ["DOG", "FISH", "ANT", "BAT"], "correct": "DOG"},
    {"question": "Catch the Animal  FISH", "options": ["BIRD", "LION", "FISH", "BEAR"], "correct": "FISH"},
    {"question": "Catch the Animal  BIRD", "options": ["ANT", "BIRD", "FROG", "BEE"], "correct": "BIRD"},
    {"question": "Catch the Animal  LION", "options": ["LION", "DEER", "WOLF", "FOX"], "correct": "LION"},

    # Shapes
    {"question": "Catch the Shape  CIRCLE", "options": ["SQUARE", "TRIANGLE", "CIRCLE", "STAR"], "correct": "CIRCLE"},
    {"question": "Catch the Shape  STAR", "options": ["STAR", "OVAL", "HEART", "LINE"], "correct": "STAR"},
    {"question": "Catch the Shape  SQUARE", "options": ["CIRCLE", "SQUARE", "DIAMOND", "CROSS"], "correct": "SQUARE"},
    {"question": "Catch the Shape  HEART", "options": ["ARROW", "HEART", "MOON", "RING"], "correct": "HEART"},

    # Math
    {"question": "Solve  2 + 3 = ?", "options": ["4", "5", "6", "7"], "correct": "5"},
    {"question": "Solve  1 + 1 = ?", "options": ["1", "2", "3", "4"], "correct": "2"},
    {"question": "Solve  4 + 2 = ?", "options": ["5", "6", "7", "8"], "correct": "6"},
    {"question": "Solve  5 - 3 = ?", "options": ["1", "2", "3", "4"], "correct": "2"},
    {"question": "Solve  3 + 4 = ?", "options": ["5", "6", "7", "8"], "correct": "7"},
    {"question": "Solve  10 - 5 = ?", "options": ["3", "4", "5", "6"], "correct": "5"},

    # Fruits
    {"question": "Catch the Fruit  APPLE", "options": ["BANANA", "APPLE", "MANGO", "ORANGE"], "correct": "APPLE"},
    {"question": "Catch the Fruit  BANANA", "options": ["GRAPE", "BANANA", "PEACH", "PLUM"], "correct": "BANANA"},
    {"question": "Catch the Fruit  MANGO", "options": ["MANGO", "LEMON", "CHERRY", "KIWI"], "correct": "MANGO"},
    {"question": "Catch the Fruit  GRAPE", "options": ["FIG", "GRAPE", "PEAR", "DATE"], "correct": "GRAPE"},

    # Vocabulary / Concepts
    {"question": "Catch the Word  BIG", "options": ["BIG", "SMALL", "SHORT", "THIN"], "correct": "BIG"},
    {"question": "Catch the Word  HAPPY", "options": ["SAD", "HAPPY", "ANGRY", "SHY"], "correct": "HAPPY"},
    {"question": "Catch  SUN", "options": ["MOON", "STAR", "SUN", "CLOUD"], "correct": "SUN"},
    {"question": "Catch  EARTH", "options": ["MARS", "EARTH", "VENUS", "JUPITER"], "correct": "EARTH"},
    {"question": "Catch  RAIN", "options": ["SNOW", "RAIN", "WIND", "FOG"], "correct": "RAIN"},
    {"question": "Catch  WATER", "options": ["FIRE", "WATER", "SAND", "ROCK"], "correct": "WATER"},
]

PART1_PICK = 10  # how many to pick each game


# ---------------------------------------------------------------
# PART 2  -  Python Programming  (pool of 20 questions, pick 5)
# ---------------------------------------------------------------
POOL_PART2 = [
    {"question": "What does  print()  do?", "options": ["DISPLAY", "DELETE", "SAVE", "CLOSE"], "correct": "DISPLAY"},
    {"question": "Which is a valid variable?", "options": ["my_name", "123abc", "if", "print("], "correct": "my_name"},
    {"question": "What is  2 ** 3  ?", "options": ["6", "8", "9", "5"], "correct": "8"},
    {"question": "Which is a Python type?", "options": ["int", "div", "run", "exe"], "correct": "int"},
    {"question": "len('Hello') = ?", "options": ["4", "5", "6", "3"], "correct": "5"},
    {"question": "True or False?  1 == 1", "options": ["TRUE", "FALSE", "MAYBE", "ERROR"], "correct": "TRUE"},
    {"question": "Which stores many items?", "options": ["list", "int", "bool", "None"], "correct": "list"},
    {"question": "What starts a comment?", "options": ["#", "//", "!", "@"], "correct": "#"},
    {"question": "What is  10 // 3 ?", "options": ["3", "3.33", "4", "10"], "correct": "3"},
    {"question": "Which is a loop keyword?", "options": ["for", "def", "class", "try"], "correct": "for"},
    {"question": "What is  type(42)  ?", "options": ["int", "str", "float", "bool"], "correct": "int"},
    {"question": "Which means NOT equal?", "options": ["!=", "==", "<=", ">="], "correct": "!="},
    {"question": "Range(3) gives how many?", "options": ["2", "3", "4", "1"], "correct": "3"},
    {"question": "What is  5 % 2  ?", "options": ["0", "1", "2", "3"], "correct": "1"},
    {"question": "Which creates a function?", "options": ["def", "var", "func", "let"], "correct": "def"},
    {"question": "What is  bool(0)  ?", "options": ["FALSE", "TRUE", "NONE", "ERROR"], "correct": "FALSE"},
    {"question": "Which is a string?", "options": ["'hello'", "123", "[1,2]", "True"], "correct": "'hello'"},
    {"question": "What does  input()  do?", "options": ["READ", "WRITE", "DELETE", "COPY"], "correct": "READ"},
    {"question": "Which keyword exits a loop?", "options": ["break", "stop", "end", "quit"], "correct": "break"},
    {"question": "What is  3 * 4  ?", "options": ["7", "10", "12", "14"], "correct": "12"},
]

PART2_PICK = 5  # how many to pick each game


# ---------------------------------------------------------------
# PART 3  -  Word Runner  (Subway-surfer style catch-the-word)
# Large pool of simple words; the game picks random targets.
# ---------------------------------------------------------------
POOL_PART3 = [
    # Animals
    "CAT", "DOG", "FISH", "BIRD", "FROG", "BEAR", "LION", "DUCK", "PIG", "COW",
    # Fruits
    "APPLE", "MANGO", "GRAPE", "PEACH", "PLUM", "LEMON", "KIWI", "PEAR",
    # Colors
    "RED", "BLUE", "GREEN", "PINK", "GOLD", "GRAY",
    # Body
    "HAND", "FOOT", "NOSE", "EYES", "EARS", "LEGS",
    # Nature
    "SUN", "MOON", "STAR", "RAIN", "SNOW", "TREE", "LEAF", "WIND",
    # Food
    "CAKE", "MILK", "RICE", "CORN", "SOUP", "BREAD",
    # Vehicles
    "CAR", "BUS", "VAN", "BIKE", "BOAT", "SHIP",
    # Clothing
    "HAT", "SHOE", "COAT", "BELT",
]

# How many target words per runner level  (level 1-5)
RUNNER_TARGETS_PER_LEVEL = {1: 4, 2: 5, 3: 6, 4: 7, 5: 8}


def get_runner_level(level_num: int) -> list[str]:
    """Return a random list of target words for the given runner level (1-5)."""
    count = RUNNER_TARGETS_PER_LEVEL.get(level_num, 5)
    return random.sample(POOL_PART3, min(count, len(POOL_PART3)))


# ---------------------------------------------------------------
# Helper function  -  call this to get a shuffled level set
# ---------------------------------------------------------------

def get_random_levels(part: int) -> list:
    """Return a randomly sampled and shuffled list of levels for the given part."""
    if part == 0:
        pool, pick = POOL_PART1, PART1_PICK
    else:
        pool, pick = POOL_PART2, PART2_PICK
    chosen = random.sample(pool, min(pick, len(pool)))
    random.shuffle(chosen)
    return chosen


# Backward compatibility aliases  (used by PARTS definition in main.py)
LEVELS_PART1 = POOL_PART1
LEVELS_PART2 = POOL_PART2


# ---------------------------------------------------------------
# PART 1  -  PANDA GAME  Separated Category Word Lists
# Each list contains enough words for the correct answer + distractors.
# The game picks the correct word and fills remaining slots from the
# SAME category — guaranteeing no cross-category mixing.
# ---------------------------------------------------------------

WORD_CATEGORIES = {
    "Colors": {
        "words": ["RED", "BLUE", "GREEN", "YELLOW", "PINK", "ORANGE", "PURPLE", "WHITE", "BLACK", "BROWN", "GRAY", "GOLD"],
        "article": "the Color",
    },
    "Animals": {
        "words": ["CAT", "DOG", "FISH", "BIRD", "FROG", "BEAR", "LION", "DUCK", "PIG", "COW", "FOX", "WOLF", "DEER", "ANT", "BEE"],
        "article": "the Animal",
    },
    "Numbers": {
        "words": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
        "article": "the Number",
    },
    "Fruits": {
        "words": ["APPLE", "BANANA", "MANGO", "GRAPE", "PEACH", "PLUM", "LEMON", "KIWI", "PEAR", "CHERRY", "ORANGE", "FIG"],
        "article": "the Fruit",
    },
    "Shapes": {
        "words": ["CIRCLE", "SQUARE", "STAR", "HEART", "TRIANGLE", "OVAL", "DIAMOND", "MOON", "CROSS", "ARROW"],
        "article": "the Shape",
    },
    "Letters": {
        "words": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
                  "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"],
        "article": "the Letter",
    },
}

# Map each panda level (1-10) to a category name and the specific correct word.
# Using a fixed correct word per level keeps the game predictable for children
# while the distractors are shuffled fresh each round.
PANDA_LEVEL_MAP = {
    1:  {"category": "Colors",   "correct": "RED"},
    2:  {"category": "Colors",   "correct": "BLUE"},
    3:  {"category": "Animals",  "correct": "CAT"},
    4:  {"category": "Animals",  "correct": "LION"},
    5:  {"category": "Numbers",  "correct": "5"},
    6:  {"category": "Numbers",  "correct": "8"},
    7:  {"category": "Fruits",   "correct": "APPLE"},
    8:  {"category": "Fruits",   "correct": "MANGO"},
    9:  {"category": "Shapes",   "correct": "CIRCLE"},
    10: {"category": "Shapes",   "correct": "STAR"},
}


def get_panda_level_data(level_num: int) -> dict:
    """Return level data for the panda catch-game.

    Returns a dict with:
        category     - e.g. "Colors"
        instruction  - e.g. "Catch the Color: RED"
        correct      - the word the player must catch
        distractors  - list of same-category wrong words
    """
    mapping = PANDA_LEVEL_MAP.get(level_num, PANDA_LEVEL_MAP[1])
    cat_name = mapping["category"]
    cat_data = WORD_CATEGORIES[cat_name]
    article  = cat_data["article"]

    # Randomly choose one word from this array as the target word
    all_words = list(cat_data["words"])
    correct = random.choice(all_words)

    # Build distractor pool: all words in the category EXCEPT the correct word
    pool = [w for w in all_words if w != correct]
    random.shuffle(pool)
    # We want ~4 distractors so up to 5 bubbles total on screen
    distractors = pool[:4]

    return {
        "category":    cat_name,
        "instruction": f"Catch {article}:  {correct}",
        "correct":     correct,
        "distractors": distractors,
    }
