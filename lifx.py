from lifxlan import LifxLAN

lifx = LifxLAN(1)


# Turns on all lights
def on():
    lifx.set_power_all_lights("on", rapid=True)


# Turns off all lights
def off():
    lifx.set_power_all_lights("off", rapid=True)


# Returns the power state of the first light obtained from the LifxLAN object
def power_state():
    devices = lifx.get_lights()
    return 'off' if devices[0].get_power() == 0 else "on"


# Toggles power state of all lights based on current state of the first light
def toggle():
    new_state = power_state()
    on() if power_state() == 'off' else off()
    return new_state


if __name__ == "__main__":
    toggle()
