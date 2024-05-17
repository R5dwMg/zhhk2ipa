# Definition of a TrieNode, which is an element of the Trie structure.
class TrieNode:
    def __init__(self):
        # Dictionary to hold child nodes, where keys are characters and values are TrieNode instances.
        self.children = {}
        # Boolean flag to indicate if this node marks the end of a word in the Trie.
        self.is_end_of_word = False

# Definition of the Trie class, a data structure for efficient string handling and retrieval.
class Trie:
    def __init__(self):
        # The root node of the Trie from which all words originate.
        self.root = TrieNode()
        # Helper attribute to manage the state of incremental search operations.
        self.current = None

    # Method to insert a word into the Trie.
    def insert(self, word):
        # Start from the root node.
        current = self.root
        # Iterate over each character in the word.
        for char in word:
            # If the character is not already a child of the current node, create a new TrieNode.
            if char not in current.children:
                current.children[char] = TrieNode()
            # Move to the child node associated with the character.
            current = current.children[char]
        # After inserting all characters, mark the last node as the end of the word.
        current.is_end_of_word = True

    # Method to search for a complete word in the Trie.
    def search(self, word):
        # Start from the root node.
        current = self.root
        # Iterate over each character in the word.
        for char in word:
            # If a character does not lead to a child node, the word is not in the Trie.
            if char not in current.children:
                return False
            # Move to the child node associated with the character.
            current = current.children[char]
        # Return True if the last character node is marked as end of the word, otherwise False.
        return current.is_end_of_word

    # Method to search the Trie incrementally character by character.
    def char_search(self, char):
        # Start from the root if no current search is ongoing.
        if not self.current:
            self.current = self.root
        # Check if the character is in the children of the current node.
        if char not in self.current.children:
            return False
        else:
            # Move to the child node associated with the character.
            self.current = self.current.children[char]
            return True

    # Method to reset the incremental search to start over from the root node.
    def reset_search(self):
        self.current = None
