# Time-Optimal Trajectory Generation pybind11 binding

Python binding to https://github.com/tobiaskunz/trajectories/

## Installation

Use [pixi](pixi.sh)

```bash
pixi run install
```

## Example

```bash
pixi run python example.py
```

## Releasing a new version to conda

```bash
pixi run conda-build
pixi run upload pixi run upload --api-key <key> .build/conda/linux-64/XXX.conda
```
