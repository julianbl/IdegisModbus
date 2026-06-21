"""Tests for the Idegis Modbus client helpers."""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from custom_components.idegis_modbus.client import IdegisModbusClient


@pytest.mark.asyncio
async def test_async_write_relay_state_preserves_schedule_bits() -> None:
    """Turning a relay on/off should preserve unrelated bits."""
    client = IdegisModbusClient("127.0.0.1", 4196, 1, 2, 100)
    client.async_read_holding_registers = AsyncMock(return_value=[0b0000_0001_0000_1111])
    client.async_write_register = AsyncMock()

    await client.async_write_relay_state(0x110, True)
    client.async_write_register.assert_awaited_once_with(0x110, 0b0100_0001_0000_1111)


@pytest.mark.asyncio
async def test_async_write_relay_state_forces_manual_mode_off_bit15() -> None:
    """Turning a relay off should also clear auto mode."""
    client = IdegisModbusClient("127.0.0.1", 4196, 1, 2, 100)
    client.async_read_holding_registers = AsyncMock(return_value=[0b1100_0000_0000_0000])
    client.async_write_register = AsyncMock()

    await client.async_write_relay_state(0x110, False)
    client.async_write_register.assert_awaited_once_with(0x110, 0)


@pytest.mark.asyncio
async def test_async_write_register_bit_preserves_unrelated_bits() -> None:
    """Writing a control-word bit should preserve every other bit."""
    client = IdegisModbusClient("127.0.0.1", 4196, 1, 2, 100)
    client.async_read_holding_registers = AsyncMock(return_value=[0b0000_0000_0000_0101])
    client.async_write_register = AsyncMock()

    await client.async_write_register_bit(0x56, 6, True)
    client.async_write_register.assert_awaited_once_with(0x56, 0b0000_0000_0100_0101)


@pytest.mark.asyncio
async def test_async_write_register_bit_can_clear_bit() -> None:
    """Clearing a control-word bit should preserve every other bit."""
    client = IdegisModbusClient("127.0.0.1", 4196, 1, 2, 100)
    client.async_read_holding_registers = AsyncMock(return_value=[0b0000_0000_0100_0101])
    client.async_write_register = AsyncMock()

    await client.async_write_register_bit(0x56, 6, False)
    client.async_write_register.assert_awaited_once_with(0x56, 0b0000_0000_0000_0101)
