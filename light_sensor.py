from waveshare_TSL2591 import TSL2591

sensor = TSL2591.TSL2591()


def get_lux():
    try:
        luxsum = 0
        iterations = 5
        for _ in range(iterations):
            luxsum += sensor.TSL2591_SET_LuxInterrupt(50, 200)
        return luxsum / iterations
    except KeyboardInterrupt:
        sensor.Disable()
        exit()


if __name__ == '__main__':
    print('Lux: %.2f' % get_lux())
