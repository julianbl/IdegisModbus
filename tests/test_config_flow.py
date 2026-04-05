"""Tests for the Idegis Modbus config flow."""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

from homeassistant.const import CONF_HOST, CONF_NAME, CONF_PORT, CONF_TIMEOUT
import pytest

from custom_components.idegis_modbus.config_flow import _validate_connection
from custom_components.idegis_modbus.const import CONF_MESSAGE_WAIT_MS, CONF_SLAVE


@pytest.mark.asyncio
async def test_validate_connection_reads_probe_register() -> None:
    """Validation should connect and probe the device."""
    with patch(
        "custom_components.idegis_modbus.config_flow.IdegisModbusClient"
    ) as mock_client_cls:
        mock_client = mock_client_cls.return_value
        mock_client.async_connect = AsyncMock()
        mock_client.async_read_input_registers = AsyncMock(return_value=[1])
        mock_client.async_close = AsyncMock()

        await _validate_connection(
            {
                CONF_NAME: "Pool",
                CONF_HOST: "192.168.1.10",
                CONF_PORT: 4196,
                CONF_SLAVE: 1,
                CONF_TIMEOUT: 2,
                CONF_MESSAGE_WAIT_MS: 100,
            }
        )

        mock_client.async_connect.assert_awaited_once()
        mock_client.async_read_input_registers.assert_awaited_once_with(0x40, 1)
        mock_client.async_close.assert_awaited_once()

