"""Switch platform for Idegis Modbus."""

from __future__ import annotations

from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .descriptions import SWITCH_DESCRIPTIONS, SwitchDescription
from .entity import IdegisEntity


class IdegisSwitch(IdegisEntity, SwitchEntity):
    """Representation of an Idegis relay."""

    def __init__(self, entry: ConfigEntry, description: SwitchDescription) -> None:
        coordinator = entry.runtime_data
        super().__init__(coordinator, entry, description.key, description.name)
        self.description = description
        self._attr_icon = description.icon
        self._attr_entity_category = description.entity_category

    @property
    def is_on(self) -> bool | None:
        """Return the switch state."""
        if self.description.value_fn is not None:
            return self.description.value_fn(self.coordinator)
        return self.coordinator.get_relay_state(self.description.key)

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on the switch."""
        if self.description.write_address is not None and self.description.bit is not None:
            await self.coordinator.async_set_holding_bit(
                self.description.write_address, self.description.bit, True
            )
            return
        await self.coordinator.async_set_relay(self.description.key, True)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off the switch."""
        if self.description.write_address is not None and self.description.bit is not None:
            await self.coordinator.async_set_holding_bit(
                self.description.write_address, self.description.bit, False
            )
            return
        await self.coordinator.async_set_relay(self.description.key, False)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Idegis switches."""
    async_add_entities([IdegisSwitch(entry, description) for description in SWITCH_DESCRIPTIONS])
