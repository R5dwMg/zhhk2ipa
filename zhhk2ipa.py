# load data
import re
import cn2an
from trie import Trie

word_dict = {}
phrase_dict = {}
punctuation = "\'\",.:；–—-－?!．，、。‧·…⋯《》「」（）()/:︰：;！？﹖ ﹔~～／”“⠀"
trie = Trie()


def init(data_path: str):
    global word_dict, phrase_dict
    # load file
    with open(data_path, "r", encoding="utf8") as f:
        word_dict, phrase_dict = parse_text(f.read())

    for key, word in phrase_dict.items():
        trie.insert(key)


def process_chunk(chunk, output, text_val):
    """
    Processes chunks of text that may or may not correspond to phrases or words in the dictionaries.
    """
    chunk_origin = chunk
    chunk = chunk.lower()
    if chunk in phrase_dict:
        output.append((chunk_origin, phrase_dict[chunk]))
        text_val += chunk_origin
    else:
        for cc in chunk:
            cc_origin = cc
            cc = cc.lower()
            if cc in word_dict:
                output.append((cc_origin, word_dict[cc]))
                text_val += cc_origin
            else:
                output.append((cc_origin, None))
    return text_val


def process_character(c, output, text_val):
    """
    Processes individual characters, managing punctuation and unknown characters.
    """
    c_origin = c
    c = c.lower()
    if c in word_dict:
        output.append((c_origin, word_dict[c]))
        text_val += c_origin
    elif c in punctuation:
        output.append((c_origin, c_origin))
        text_val += c_origin
    else:
        output.append((c_origin, None))
    return text_val


def parse_ipa(text: str):
    """
    Converts a given text to International Phonetic Alphabet (IPA) notation.
    Handles continuous phrases and individual characters, managing punctuation and unknowns.
    """
    text = text.strip()
    output = []
    text_val = ""
    chunk = ""
    trie.reset_search()

    for c in text:
        if trie.char_search(c):
            chunk += c
        else:
            if chunk:
                text_val = process_chunk(chunk, output, text_val)
                chunk = ""  # Reset chunk after processing
                trie.reset_search()

            # Handle the current character if the chunk is interrupted or empty
            text_val = process_character(c, output, text_val)
            trie.reset_search()  # Reset after a failed trie search

    # Handle any remaining data in 'chunk' after processing all characters in 'text'
    if chunk:
        text_val = process_chunk(chunk, output, text_val)
        chunk = ""  # Clear the chunk after processing
        trie.reset_search()

    return output


def number_to_reading(text: str) -> str:
    """
    Converts numerical values in the text to their Chinese character readings.

    Args:
        text (str): The input text containing numerical values.

    Returns:
        str: The modified text where all numbers are converted to their Chinese numeral readings.
    """
    # Regex to find all numerical expressions in the text and replace them using cn2an.
    return re.sub(r'\d+(?:\.?\d+)?', lambda x: cn2an.an2cn(x.group()), text)


def convert(text: str) -> []:
    """
    Converts a given text into IPA notation after converting all numerical values
    to their Chinese character readings.

    Args:
        text (str): The input text possibly containing numerical values.

    Returns:
        tuple: Returns two dictionaries containing the IPA mappings for single characters and phrases.
    """
    # First convert numbers in the text to their Chinese numeral readings.
    text = number_to_reading(text)

    # Then parse the text to extract IPA notations for words and phrases.
    return parse_ipa(text)


def parse_text(text: str) -> tuple:
    """
    Parses a given text string to populate dictionaries for individual words and phrases with their
    corresponding IPA (International Phonetic Alphabet) notations.

    Args:
        text (str): The raw input text containing words or phrases and their IPA notations,
                    typically separated by tabs and different entries by newlines.

    Returns:
        tuple: A tuple containing two dictionaries:
            - word_dict: Dictionary for single character words.
            - phrase_dict: Dictionary for multiple character phrases.
    """
    global word_dict, phrase_dict
    word_dict = {}
    phrase_dict = {}

    # Remove unwanted characters and normalize the data.
    data = re.sub(r'\[.*?\]', '', text)  # Remove bracketed content.
    # Remove various punctuation and special characters, then convert to lower case.
    data = re.sub(r"[\/…，？！]", "", data).lower()

    # Split the cleaned data into lines.
    data_lines = data.split("\n")

    # Process each line to extract words and their corresponding IPA.
    for line in data_lines:
        if line:
            line_data = line.split("\t")
            if len(line_data) < 2:
                continue  # Skip lines that don't have the expected format.

            word, ipa_tag = line_data[0], line_data[1].split(", ")
            # If multiple IPA entries exist, select only the first one.
            ipa_tag = [ipa_tag[0]]

            # Split IPA tags by spaces to handle multiple IPA components.
            ipa_tag = [item for sub_tag in ipa_tag for item in sub_tag.split(" ")]

            # Assign the parsed data to the appropriate dictionary.
            if len(word) == 1:
                word_dict[word] = ipa_tag
            else:
                phrase_dict[word] = ipa_tag

    return word_dict, phrase_dict
