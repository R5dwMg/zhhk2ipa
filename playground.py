import zhhk2ipa

if __name__ == "__main__":
    # load vocab table
    zhhk2ipa.init("data/zhhk_ipa.txt")

    while True:
        text = input()
        # convert text to ipa
        output = zhhk2ipa.convert(text)
        print(output)
