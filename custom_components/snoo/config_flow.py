"""Config flow for Happiest Baby Snoo Smart Bassinet integration."""
import logging

import voluptuous as vol

from snoo import Client as snoo_client
from snoo.client import APIError as APIError

from homeassistant import config_entries, core, exceptions

from .const import DOMAIN # pyline:disable=unused-import

_LOGGER = logging.getLogger(__name__)

DATA_SCHEMA = vol.Schema({"username": str, "password": str})

# Synchronous class to actually attempt a log in.
# Returns a valid token, or an APIError.
def fetch_token(username: str, password: str):
    client = snoo_client()
    client.auth["username"] = username
    client.auth["password"] = password
    client.auth["token"] = ""
    try:
        res = client.get_token()
    except APIError as e:
        res = e
    return res

async def validate_input(hass: core.HomeAssistant, data):
    """Validate the user input allows us to connect.

    Data has the keys from DATA_SCHEMA with values provided by the user.
    """

    result = await hass.async_add_executor_job(
        fetch_token, data["username"], data["password"])
    if isinstance(result, APIError):
        raise InvalidAuth

    return {"title": "Snoo"}

class SnooConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)

                return self.async_create_entry(title=info["title"], data=user_input)
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except Exception: # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )

class InvalidAuth(exceptions.HomeAssistantError):
    """Error to indicate there is invalid auth."""
