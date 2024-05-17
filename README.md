# zhhk2ipa
Convert Hong Kong Chinese sentences to the International Phonetic Alphabet (IPA).

## Introduction
The `zhhk2ipa` project provides tools to convert text from Hong Kong Chinese into the International Phonetic Alphabet (IPA). It supports phrase-level and word-level transcription based on a comprehensive vocabulary table.

## Installation
Install the required dependencies by running:
```commandline
pip install -r requirements.txt
```

## Usage
To use `zhhk2ipa`, follow these steps:
```python
import zhhk2ipa

# Load the vocabulary table
zhhk2ipa.init("data/zhhk_ipa.txt")

# Convert text to IPA
output = zhhk2ipa.convert("同朕check吓")
print(output)

output = zhhk2ipa.convert("返屋企,樂而忘返。")
print(output)
```

### Example Output
```text
[('同', ['tʰʊŋ˨˩']), ('朕', ['tsɐm˨']), ('check吓', ['tsʰɛ:k˥', 'ha:˩˧'])]
[('返屋企', ['fa:n˥', 'ŋʊk˥', 'kʰei˧˥']), (',', ','), ('樂而忘返', ['lɔ:k˨', 'ji:˨˩', 'mɔ:ŋ˨˩', 'fa:n˧˥']), ('。', '。')]
```

### Handling Tokens Not in Vocabulary
If a token is not in the vocabulary table, it will be marked as `None` in the output:
```python
output = zhhk2ipa.convert("我ABCD你")
print(output)
```
```text
[('我', ['ŋɔ:˩˧']), ('A', None), ('B', ['pi:˥']), ('C', None), ('D', None), ('你', ['nei˩˧'])]
```

## Disclaimer

### Reliability and Testing
Please note that the functionality of this software has been tested with a limited number of test cases. While preliminary results are promising, the reliability across diverse and extensive datasets has not been fully established. Users are encouraged to conduct their own tests and report any issues or discrepancies they encounter. This will assist in improving the tool and extending its reliability for broader usage.

### Credits
The vocabulary for `zhhk2ipa` is adapted from data provided by [lotusfa/IPA-Translator](https://github.com/lotusfa/IPA-Translator/) with additional entries included for broader coverage.
