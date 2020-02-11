"""Snoo sensor."""
import logging

from enum import Enum

from homeassistant.helpers.entity import Entity

from snoo import Client

_LOGGER = logging.getLogger(__name__)

async def async_setup_platform(
        hass, config, async_add_entries, discovery_info=None):
    """Set up the sensor platform."""
    async_add_entities([SnoostateSensor()])

async def async_setup_entry(
        hass, config_entry, async_add_devices):
    """Set up the sensor platform"""
    async_add_devices([SnooStateSensor()])

class SnooStateSensor(Entity):
    """Representation of the Snoo status."""

    def __init__(self):
        self._setup_state()
        self._setup_attributes()
        self._client = Client()

    @property
    def name(self):
        """Return the name of the sensor."""
        return "Snoo state"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state.value

    @property
    def device_state_attributes(self):
        """Return device specific state attributes."""
        return self._attributes

    def _setup_state(self):
        self._state = SnooState.NONE

    def _setup_attributes(self):
        # level:
        #   When awake or asleep, this is 0. When soothing,
        #   this is the soothing level between 1 and 4.
        # session_start_time::
        #   Contains the time the current wake or sleep session started.
        #   Note that only changes to or from awake are tracked here;
        #   transitions between soothing and sleep phases are ignored.
        self._attributes = {
            "level": 0,
            "session_start_time": ""
        }

    def update(self):
        """Fetch new state data for the sensor."""
        session = self._client.get_current_session()
        if session["end_time"]:
            self._attributes["level"] = 0
            self._attributes["session_start_time"] = session["end_time"]
            self._state = SnooState.AWAKE
        elif session["level"] in ["BASELINE", "WEANING_BASELINE"]:
            self._attributes["session_start_time"] = session["start_time"]
            self._attributes["level"] = 0
            self._state = SnooState.ASLEEP
        elif session["level"] == "LEVEL1":
            self._attributes["level"] = 1
            self._state = SnooState.SOOTHING
        elif session["level"] == "LEVEL2":
            self._attributes["level"] = 2
            self._state = SnooState.SOOTHING
        elif session["level"] == "LEVEL3":
            self._attributes["level"] = 3
            self._state = SnooState.SOOTHING
        elif session["level"] == "LEVEL4":
            self._attributes["level"] = 4
            self._state = SnooState.SOOTHING
        else:
            # TODO: Raise an exception here?
            self._state = SnooState.NONE


class SnooState(Enum):
    NONE = "None"
    AWAKE = "Awake"
    ASLEEP = "Asleep"
    SOOTHING = "Soothing"
