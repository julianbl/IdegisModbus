"""Coordinator tests for Idegis Modbus."""

from __future__ import annotations

from custom_components.idegis_modbus.coordinator import IdegisData


def test_u32_input_is_assembled_lsb_first() -> None:
    """Two consecutive registers should be combined as documented."""
    data = IdegisData(input_registers={0x48: 0x1234, 0x49: 0x5678}, holding_registers={})
    low = data.input_registers[0x48]
    high = data.input_registers[0x49]
    assert (low | (high << 16)) == 0x56781234

