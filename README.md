# Idegis Modbus for Home Assistant

Local Home Assistant custom integration for Idegis pool controllers over a Modbus TCP bridge.

This integration is designed for devices such as the Idegis Domotic 2 LS and exposes:

- relay switches
- relay state binary sensors
- pH, ORP, free chlorine, temperature and salt sensors
- editable target numbers for pH, ORP, chlorine and electrolysis production
- UV status and counters
- digital inputs
- maintenance buttons for documented reset actions
- diagnostics download support

## Features

- Native Home Assistant integration with UI setup
- HACS-installable custom integration
- `Config Flow` and `Options Flow`
- `DataUpdateCoordinator` polling
- `sensor`, `binary_sensor`, `switch`, `number` and `button` entities
- local-only operation, no cloud required
- diagnostics support for troubleshooting

## Installation

### HACS

1. Open HACS.
2. Go to `Integrations`.
3. Add this repository as a custom repository.
4. Install `Idegis Modbus`.
5. Restart Home Assistant.

### Manual

Copy `custom_components/idegis_modbus` into your Home Assistant `custom_components` directory and restart Home Assistant.

## Configuration

After restart:

1. Go to `Settings -> Devices & Services`.
2. Click `Add Integration`.
3. Search for `Idegis Modbus`.
4. Enter:
   - bridge host
   - bridge port
   - Modbus slave
   - timeout
   - delay between Modbus requests

## Options

The integration also exposes an options flow where you can control:

- polling interval
- UV entities on/off
- digital input entities on/off
- diagnostics entities on/off
- maintenance buttons on/off

## Notes

- Relay control uses read-modify-write so schedule bits are preserved.
- Target values are implemented as native `number` entities.
- Diagnostics expose raw input and holding registers gathered by the coordinator.

## Development

Useful commands:

```bash
python3 -m compileall custom_components/idegis_modbus
pytest
```

## Disclaimer

This project is based on reverse engineering and field validation against local Idegis documentation and hardware behavior. Verify all write operations on your own equipment before relying on them in production pool automations.

