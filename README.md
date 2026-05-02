# RDKit Render

Chemical structure editor and viewer built as a wrapper around [`rdeditor`](https://github.com/EBjerrum/rdeditor). This project leverages RDKit and PySide6 to provide an addition that allows for easier smiles pasting and SMARTS highlighting for debugging SMARTS.

## Features

This application preserves all the comprehensive drawing and editing capabilities of `rdeditor` while introducing  new search and rendering tools:

*   **Dynamic SMILES & Reaction SMILES Rendering:** A dedicated toolbar allows you to paste or type a SMILES string (or Reaction SMILES containing `>>` or `>`). The molecule is rendered in the editor canvas instantly as you type.
*   **Round-Trip Synchronization:** Modifying the molecule on the visual canvas automatically regenerates the SMILES string and updates the SMILES input box in real time.
*   **Interactive SMARTS & SMIRKS Search:** A SMARTS input box allows you to perform substructure searches directly on the currently drawn or loaded molecule. It fully supports matching Reaction SMIRKS against Reaction SMILES. 
*   **Match Highlighting & Toggling:** Found a substructure match? The matching atoms are highlighted dynamically. Use the convenient `<-` and `->` buttons to cycle through all occurrences of the SMARTS pattern within your molecule.
*   **Full `rdeditor` Integration:** Modify atoms, bonds, rings, adjust stereochemistry, and clean up 2D coordinates natively—all SMARTS highlights will track with the underlying RDKit molecule representation seamlessly.

## Installation

This project uses [`uv`](https://github.com/astral-sh/uv) for fast, reliable Python dependency management.

1.  Make sure you have `uv` installed on your system.
2.  Clone the repository and navigate to the project directory:
    ```bash
    cd rdkit-render
    ```
3.  The project dependencies are already defined in `pyproject.toml`. You can sync/install them by running:
    ```bash
    uv sync
    ```

## Usage

To launch the application, run the `main.py` script using `uv`:

```bash
uv run python main.py
```

### Navigating the Interface

*   **SMILES Input Toolbar:** Located just below the main toolbars. Enter a valid SMILES or Reaction SMILES string here to load it onto the canvas.
*   **SMARTS Input Toolbar:** Located just below the SMILES toolbar. Enter a valid SMARTS or SMIRKS pattern to highlight matching atoms in the current structure.
*   **Match Navigation:** Use the left (`<-`) and right (`->`) arrow buttons on the SMARTS toolbar to step through multiple matches.

## License

This project is open-source. See the `LICENSE` file for more details. Since it builds upon `rdeditor`, it inherits compatibility with the LGPL-3.0 license.
