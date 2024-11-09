# Traveling Salesman Problem Solver

This project implements three different formulations to solve the Traveling Salesman Problem (TSP):
- DFJ (Dantzig-Fulkerson-Johnson)
- MTZ (Miller-Tucker-Zemlin)
- GG (Gavish-Graves)

## Project Structure

- `data/`: Contains input files
  - `atsp/`: TSPLIB format instances
  - `txt/`: Text format instances
- `src/`: Source code
  - `proyecto2.py`: Main implementation with all formulations
  - `generar_matrices.py`: Matrix generation utilities

## Requirements

- Python 3.x
- Required packages:
  - numpy
  - networkx
  - pulp
  - tsplib95

## Usage

1. Run the main program:
```bash
python src/proyecto2.py
```
2. Choose input format:
- Enter `1` for text matrix format
- Enter `2` for TSPLIB format

## Input Formats

### Text Matrix Format
- Files: ins10.txt through ins18.txt
- Simple distance matrix format

### TSPLIB Format
- Files: ftv35.atsp, ftv38.atsp, ftv44.atsp
- Standard TSPLIB ATSP format

## Formulations

### DFJ (Dantzig-Fulkerson-Johnson)
- Classic TSP formulation
- Uses subtour elimination constraints

### MTZ (Miller-Tucker-Zemlin)
- Uses additional variables to prevent subtours
- More compact than DFJ

### GG (Gavish-Graves)
- Alternative formulation
- Uses flow variables for subtour elimination