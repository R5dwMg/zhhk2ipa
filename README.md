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
output = zhhk2ipa.convert("運輸及物流局表示，清水灣道近坑口永隆路早前在特大暴雨下倒塌的斜坡，修復工程已經完成。")
print(output)

output = zhhk2ipa.convert("返屋企,樂而忘返。")
print(output)
```

### Example Output
```text
[('運輸', ['wɐn˨', 'sy:˥']), ...]
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

## Credits
The vocabulary for `zhhk2ipa` is adapted from data provided by [lotusfa/IPA-Translator](https://github.com/lotusfa/IPA-Translator/) with additional entries included for broader coverage.
