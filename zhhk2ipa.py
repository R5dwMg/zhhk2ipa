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


def parse_ipa(text: str) -> []:
    """
    Sentence to ipa, validation text, unknown char
    """
    phrase_found = []
    ipa_list = []
    text_val = ""
    chunk = ""
    unknown_char = []
    text = text.strip()
    output = []

    for i in range(len(text)):
        c = text[i]
        if trie.char_search(c):
            chunk += c
        else:
            # c is not part of phrase or indicate end of phrase
            if len(chunk):
                # handle end of phrase, c triggered end of phrase
                if chunk in phrase_dict:
                    # chunk found in phrase dictionary
                    # append to phrase dict and clean up
                    phrase_found.append(chunk)
                    grp = (chunk, phrase_dict[chunk],)
                    output.append(grp)
                    text_val += chunk
                    chunk = ""
                    trie.reset_search()
                else:
                    for cc in chunk:
                        # chunk is not in phrase dict
                        if cc in word_dict:
                            # chunk is in word dict
                            grp = (cc, word_dict[cc],)
                            output.append(grp)
                            text_val += cc
                        else:
                            unknown = (cc, None,)
                            output.append(unknown)
                    chunk = ""
                    trie.reset_search()

                # handle character c
                # chat is c is part of another phrase
                if trie.char_search(c):
                    # c is part of phrase
                    chunk += c
                elif c in word_dict:
                    # c is not part of phrase
                    grp = (c, word_dict[c],)
                    output.append(grp)
                    text_val += c
                elif c in punctuation:
                    # c is punctuation
                    grp = (c, c,)
                    output.append(grp)
                    text_val += c
                else:
                    unknown = (c, None,)
                    output.append(unknown)
            else:
                # single word and chunk currently empty
                if c in word_dict:
                    grp = (c, word_dict[c],)
                    output.append(grp)
                    text_val += c
                elif c in punctuation:
                    # c is punctuation
                    grp = (c, c,)
                    output.append(grp)
                    text_val += c
                else:
                    unknown = (c, None,)
                    output.append(unknown)

    # iterated all characters
    # flush data in chunk
    remain_size = len(chunk)
    if remain_size == 1:
        # chunk is a character
        if chunk in word_dict:
            grp = (chunk, word_dict[chunk])
            output.append(grp)
            text_val += chunk
        elif chunk in word_dict:
            # chunk is not part of phrase
            grp = (chunk, word_dict[chunk],)
            output.append(grp)
            text_val += chunk
        elif chunk in punctuation:
            # chunk is punctuation
            grp = (chunk, chunk,)
            output.append(grp)
            text_val += chunk
        else:
            unknown = (chunk, None,)
            output.append(unknown)
    elif remain_size > 1:
        if chunk in phrase_dict:
            grp = (chunk, phrase_dict[chunk])
            output.append(grp)
            text_val += chunk
        else:
            for cc in chunk:
                if cc in word_dict:
                    # chunk is in word dict
                    grp = (cc, word_dict[cc],)
                    output.append(grp)
                    text_val += cc
                else:
                    unknown = (cc, None,)
                    output.append(unknown)
    trie.reset_search()

    # export ipa list, text for validation, unknown characters
    return output


def flatten(ipa_list) -> str:
    """
    Merge ipa to string
    """
    output = []
    for pair in ipa_list:
        output.extend(pair[1])
    ipa_text = " ".join(output).replace("/", "").replace("  ", " ")
    return ipa_text


def number_to_cantonese(text):
    return re.sub(r'\d+(?:\.?\d+)?', lambda x: cn2an.an2cn(x.group()), text)


def convert(text: str):
    # convert numbers to number reading
    text = number_to_cantonese(text)

    return parse_ipa(text)


def merge(path_1, path_2, output_path: str):
    """
    Merge 2 yue database, export new one
    """
    with open(path_1, "r", encoding="utf8") as f:
        f1 = f.read()

    with open(path_2, "r", encoding="utf8") as f:
        f2 = f.read()
    f2 = f2.replace("   ", "\2")

    output = (f1 + "\n" + f2).replace("\n\n", "\n").lower()
    with open(output_path, "w", encoding="utf8") as f:
        f.write(output)
    pass


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
            if word == "你好":
                pass
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
