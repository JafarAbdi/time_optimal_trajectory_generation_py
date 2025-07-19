# Time-Optimal Trajectory Generation pybind11 binding

Python binding to https://github.com/tobiaskunz/trajectories/

## Installation

Use [pixi](pixi.sh)

```bash
pixi run install
```

## Example

```bash
pixi run python examples/example.py
```

## Test cibuildwheel locally

```bash
CIBW_BUILD_VERBOSITY=1 CIBW_BUILD="cp3{10,11,12}-macosx_{x86_64,arm64} cp3{9,10,11,12}-manylinux_x86_64" uv run cibuildwheel . --platform linux
```
