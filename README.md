# homeassistant-snoo

This is a [Home Assistant][1] custom component to retreive the status of
a [SNOO Smart Bassinet][2]. It creates a sensor showing the current
session status (awake, asleep or soothing), as well as the current soothe
level when soothing.

[1]: https://www.home-assistant.ai/
[2]: https://www.happiestbaby.com/products/snoo-smart-bassinet

This component is made possible by the [`snoo` Python module][3]. Note
that it is only possible to read the current status. Sending commands is
not supported, and won't be in the forseeable future.

[3]: https://github.com/maebert/snoo

## Installation

Copy the contents of the `custom_components` directory to the
`custom_components` directory in your Home Assistant configuration
directory, and restart Home Assistant.

## Usage

The component does not (yet) support YAML configuration. Create a new
integration through the Home Assistant UI. The component requires your
username and password for your Happiest Baby account.

If successful, the component adds a new `sensor.snoo_state` sensor. This
will have one of these states:

* `Awake`: The SNOO is inactive.
* `Asleep`: The SNOO is active, and baby is calm.
* `Soothing`: The SNOO has detected baby is unsettled, and is attempting
  to soothe.

Additionally, the sensor exposes these attributes:

* `level`: When state is `Soothing`, this attribute will be a number
  indicating the soothing level, between 1 and 4. At all other times
  `level` is 0.
* `session_start_time`: The time since the last session started, reported
  by the API in UTC. Note that this only updates when transitioning to or
  from the `Awake` state. Going from `Asleep` to `Soothing` or back again
  does not change this time.
