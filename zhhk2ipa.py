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


def number_to_cantonese(text):
    return re.sub(r'\d+(?:\.?\d+)?', lambda x: cn2an.an2cn(x.group()), text)


def convert(text: str):
    # convert numbers to number reading
    text = number_to_cantonese(text)
    return parse_ipa(text)


def parse_text(text: str) -> []:
    """
    Put data to dictionary
    """
    global word_dict, phrase_dict
    word_dict = {}
    phrase_dict = {}

    # clean up data
    data = re.sub(r'\[.*?\]', '', text)
    data = data.replace("/", "").replace("…", "").replace("，", "").replace("？", "").replace("！", "")
    data = data.lower()

    # split into lines
    data_lines = data.split("\n")
    idx = 1

    for line in data_lines:
        if len(line):
            line_data = line.split("\t")
            word = line_data[0]
            ipa_tag = line_data[1].split(", ")
            if len(ipa_tag) > 1:
                ipa_tag = [ipa_tag[0]]
            temp = []

            for t in ipa_tag:
                temp.extend(t.split(" "))
                ipa_tag = temp

            if len(word) == 1:
                word_dict[word] = ipa_tag
            else:
                phrase_dict[word] = ipa_tag
        idx += 1

    return word_dict, phrase_dict
