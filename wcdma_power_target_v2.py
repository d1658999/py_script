import json

def power_target(band):
    file = 'wcdma_power_target.json'
    with open(file, 'r') as target:
        pwr_target = json.load(target)
    return pwr_target[str(int(band))]

def main():
    # test
    band = 5.0
    print(band, power_target(band))

if __name__ == '__main__':
    main()