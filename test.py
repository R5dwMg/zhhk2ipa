import zhhk2ipa

if __name__ == "__main__":
    zhhk2ipa.init("data/zhhk_ipa.txt")

    while True:
        text = input()
        output = zhhk2ipa.convert(text)
        print(output)
    pass