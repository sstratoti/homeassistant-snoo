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
        self._state = SnooState.NONE
        self._client = Client()

    @property
    def name(self):
        """Return the name of the sensor."""
        return "Snoo state"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state.value

    def update(self):
        """Fetch new state data for the sensor."""
        session = self._client.get_current_session()
        if session["end_time"]:
            self._state = SnooState.AWAKE
        elif session["level"] in ["BASELINE", "WEANING_BASELINE"]:
            self._state = SnooState.ASLEEP
        else:
            self._state = SnooState.SOOTHING


class SnooState(Enum):
    NONE = "None"
    AWAKE = "Awake"
    ASLEEP = "Asleep"
    SOOTHING = "Soothing"
