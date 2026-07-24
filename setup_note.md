# Setup Notes

This document describes how the local environment is configured to run this project. It's intended as a reference for reproducing the setup, not a full installation guide.

## Environment

- A single conda environment is used for the entire stack (Open Data Cube, Datacube Explorer, and datacube-ows).
- **Datacube Explorer** is pip-installed inside this environment.
- **datacube-ows** is installed in editable mode (`pip install -e`), to allow custom configuration and easier debugging.

## Open Data Cube Configuration

A datacube configuration file (`.datacube.conf` / environment-based config) connects the Open Data Cube to its PostgreSQL database. This is what `datacube` and `datacube-ows` both read to locate and query indexed products.

## datacube-ows Configuration

`datacube-ows` requires an environment variable pointing to the OWS configuration module:

```bash
export DATACUBE_OWS_CFG="<module>.ows_cfg"
export PYTHONPATH="$PYTHONPATH:/path/to/ows_config"
```

These are set so the OWS server loads the custom configuration file (`ows/ows_cfg_kerala_sentinel.py`) rather than any example or demo configuration bundled with the installed package. Both are persisted in `~/.bashrc` so they're available in every shell session.
