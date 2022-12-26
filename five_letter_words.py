import json
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor


class TrieNode:
    """
    A TrieNode represents a node in a Trie (prefix tree).

    Each TrieNode represents a letter in a word. The root TrieNode represents an empty
    string and the child TrieNodes represent the letters in the word. The TrieNode has a
    flag called 'is_word' that indicates whether the word represented by the path from
    the root TrieNode to the current TrieNode is a word in the set.

    The TrieNode also has a dictionary called 'children' that stores the child TrieNodes
    for each letter in the word.

    Attributes
    ----------
    children : dict
        A dictionary that stores the child TrieNodes for each letter in the word.
    is_word : bool
        A flag that indicates whether the word represented by the path from the root
        TrieNode to the current TrieNode is a word in the set.
    """

    def __init__(self):
        self.children = {}
        self.is_word = False


class Trie:
    """
    A Trie (prefix tree) is a tree-like data structure that is used to store a set of words.

    Each node in the Trie represents a letter in a word. The root node represents an empty
    string and the child nodes represent the letters in the word. The Trie has a flag called
    'is_word' that indicates whether the word represented by the path from the root node to
    the current node is a word in the set.

    The Trie data structure is useful for searching for words in a large dataset because it
    allows you to search for words that start with a given prefix.

    Attributes
    ----------
    root : TrieNode
        The root node of the Trie.
    """

    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        current = self.root
        for letter in word:
            if letter not in current.children:
                current.children[letter] = TrieNode()
            current = current.children[letter]
        current.is_word = True


def find_combinations(trie, prefix, current_word, current_combination, combinations):
    """
    Find all combinations of 5 words that do not share any common letters.

    This function searches for combinations of 5 words using a depth-first search.
    It starts from the given prefix and checks if it is a word. If it is a word,
    it is added to the current combination. If the current combination has 5 words,
    it is added to the list of combinations. If the current combination does not
    have 5 words, the search continues by adding each letter of the current prefix
    to the current word and recursively calling the function. If the current prefix
    is not a word, the search continues by adding each letter of the current prefix
    to the current word and recursively calling the function.

    Parameters
    ----------
    trie : Trie
        The Trie data structure that stores the words.
    prefix : str
        The current prefix being searched.
    current_word : str
        The current word being searched.
    current_combination : tuple
        The current combination of words.
    combinations : list
        The list of combinations of words.

    Returns
    -------
    list
        The list of combinations of words.
    """

    # Get the TrieNode for the current prefix
    node = trie.root
    for letter in prefix:
        if letter not in node.children:
            return
        node = node.children[letter]

    # Check if the current prefix is a word
    if len(prefix) == 5 and node.is_word:
        # The current prefix is a word, so add it to the current combination
        current_combination = current_combination + (prefix,)
        if len(current_combination) == 5:
            # The current combination has 5 words, so add it to the list of combinations
            combinations.append(current_combination)
        else:
            # The current combination does not have 5 words, so continue the search
            for letter, child in node.children.items():
                # Check if the letter is in the current word
                if letter not in current_word:
                    # The letter is not in the current word, so add it to the current word
                    # and recursively call the function
                    new_word = current_word + letter
                    find_combinations(
                        trie, "", new_word, current_combination, combinations
                    )
    else:
        # The current prefix is not a word, so continue the search
        for letter, child in node.children.items():
            # Check if the letter is in the current word
            if letter not in current_word:
                # The letter is not in the current word, so add it to the current word
                # and recursively call the function
                new_word = current_word + letter
                new_prefix = prefix + letter
                find_combinations(
                    trie, new_prefix, new_word, current_combination, combinations
                )
    return combinations


if __name__ == "__main__":
    # Load the English words from the file
    with open("five_letter_english_words.json", "r") as f:
        words_dict = json.load(f)

    words = list(words_dict.keys())

    # Create a Trie data structure to store the words
    trie = Trie()
    for word in words:
        trie.insert(word)

    # Create a ProcessPoolExecutor to use multiple CPU cores
    with ProcessPoolExecutor() as executor:
        # Initialize the list of combinations and the progress bar
        combinations = []
        progress_bar = tqdm(total=len(trie.root.children))

        # Find all combinations of 5 words
        for letter, child in trie.root.children.items():
            # Update the progress bar
            progress_bar.update(1)

            # Find all combinations starting from the given letter
            combinations = find_combinations(trie, letter, letter, (), combinations)

        # Close the progress bar
        progress_bar.close()

    # Print the combinations
    print(f"Number of combinations: {len(combinations)}")
    for combination in combinations:
        print(combination)
