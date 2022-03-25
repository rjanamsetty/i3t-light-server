from lifxlan import LifxLAN

lifx = LifxLAN(1)


def on():
    """
    Turns on all lights
    :return: None
    """
    lifx.set_power_all_lights("on", rapid=True)


def off():
    """
    Turns off all lights
    :return: None
    """
    lifx.set_power_all_lights("off", rapid=True)


def power_state():
    """
    Gets the new state of the first light in the LifxLAN object
    :return: the new power state of the first light as a string
    """
    devices = lifx.get_lights()
    return 'off' if devices[0].get_power() == 0 else "on"


def set_brightness(brightness):
    """
    Sets the brightness of all lights to the given value
    :param brightness: the brightness value to set
    :return: None
    """
    devices = lifx.get_lights()
    for device in devices:
        device.set_brightness(brightness, rapid=True)


# Toggles power state of all lights based on current state of the first light
def toggle():
    """
    Toggles power state of all lights based on current state of the first light
    :return: the new, changed power state of the first light as a string
    """
    new_state = power_state()
    on() if power_state() == 'off' else off()
    return new_state


if __name__ == "__main__":
    set_brightness(2500)
