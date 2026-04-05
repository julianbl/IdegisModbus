"""Diagnostics support for Idegis Modbus."""

from __future__ import annotations

from homeassistant.components.diagnostics import async_redact_data
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from . import IdegisConfigEntry

TO_REDACT = {"host"}


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: IdegisConfigEntry
) -> dict:
    """Return diagnostics for a config entry."""
    coordinator = entry.runtime_data
    return {
        "entry": async_redact_data(dict(entry.data), TO_REDACT),
        "options": dict(entry.options),
        "last_update_success": coordinator.last_update_success,
        "input_registers": coordinator.data.input_registers if coordinator.data else {},
        "holding_registers": coordinator.data.holding_registers if coordinator.data else {},
    }

