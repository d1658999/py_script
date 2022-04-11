import json

def mchs(band):
    file = './wcdma_mch.json'
    with open(file, 'r') as ltemch:
        mchs = json.load(ltemch)
    return mchs[str(int(band))]

def main():
    # test
    band = 5.0
    print(band, mchs(band))

if __name__ == '__main__':
    main()