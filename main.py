import sys
from PySide6 import QtWidgets, QtCore
from PySide6.QtGui import QIcon
from rdkit import Chem
from rdeditor.rdEditor import MainWindow

class AppWindow(MainWindow):
    def __init__(self, fileName=None, loglevel="WARNING"):
        super().__init__(fileName=fileName, loglevel=loglevel)
        self.setWindowIcon(QIcon("app-icon.png"))
        
        # Break before adding our new toolbars to push them below the existing ones
        self.addToolBarBreak(QtCore.Qt.TopToolBarArea)

        # SMILES Toolbar
        self.smilesToolBar = QtWidgets.QToolBar("SMILES Input")
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.smilesToolBar)
        
        self.smilesInput = QtWidgets.QLineEdit()
        self.smilesInput.setPlaceholderText("Paste SMILES here...")
        self.smilesInput.textChanged.connect(self.on_smiles_changed)
        
        self.smilesToolBar.addWidget(QtWidgets.QLabel(" SMILES: "))
        self.smilesToolBar.addWidget(self.smilesInput)

        # Break again to stack the SMARTS toolbar below SMILES
        self.addToolBarBreak(QtCore.Qt.TopToolBarArea)
        
        # SMARTS Toolbar
        self.smartsToolBar = QtWidgets.QToolBar("SMARTS Input")
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.smartsToolBar)

        self.smartsInput = QtWidgets.QLineEdit()
        self.smartsInput.setPlaceholderText("Enter SMARTS here...")
        self.smartsInput.textChanged.connect(self.on_smarts_changed)
        
        self.prevMatchBtn = QtWidgets.QPushButton()
        self.prevMatchBtn.setIcon(self.style().standardIcon(QtWidgets.QStyle.StandardPixmap.SP_ArrowLeft))
        self.prevMatchBtn.setToolTip("Previous Match")
        self.prevMatchBtn.clicked.connect(self.prev_match)
        
        self.nextMatchBtn = QtWidgets.QPushButton()
        self.nextMatchBtn.setIcon(self.style().standardIcon(QtWidgets.QStyle.StandardPixmap.SP_ArrowRight))
        self.nextMatchBtn.setToolTip("Next Match")
        self.nextMatchBtn.clicked.connect(self.next_match)
        
        self.matchLabel = QtWidgets.QLabel("0/0")
        self.matchLabel.setMargin(5)
        
        self.smartsToolBar.addWidget(QtWidgets.QLabel(" SMARTS: "))
        self.smartsToolBar.addWidget(self.smartsInput)
        self.smartsToolBar.addWidget(self.prevMatchBtn)
        self.smartsToolBar.addWidget(self.matchLabel)
        self.smartsToolBar.addWidget(self.nextMatchBtn)
        
        self.matches = []
        self.current_match_idx = -1
        
        # Keep track of the original molecule text so we don't unnecessarily re-parse
        self._last_smiles = ""

    def on_smiles_changed(self, text):
        text = text.strip()
        if text == self._last_smiles:
            return
        
        self._last_smiles = text
        if not text:
            self.editor.mol = None
            self.statusBar().showMessage("Cleared molecule.")
            return
            
        mol = Chem.MolFromSmiles(text, sanitize=False)
        if mol:
            try:
                Chem.SanitizeMol(mol)
                # Assign stereo
                self.editor.assign_stereo_atoms(mol)
                Chem.rdmolops.SetBondStereoFromDirections(mol)
                
                self.editor.mol = mol
                self.statusBar().showMessage("SMILES loaded successfully.")
                
                # Re-run SMARTS search if any
                self.on_smarts_changed(self.smartsInput.text())
            except Exception as e:
                self.statusBar().showMessage(f"Error sanitizing SMILES: {e}")
        else:
            self.statusBar().showMessage("Invalid SMILES.")

    def on_smarts_changed(self, text):
        text = text.strip()
        self.matches = []
        self.current_match_idx = -1
        
        if not text or self.editor.mol is None:
            self.editor.selectedAtoms = []
            self.update_match_label()
            return
            
        smarts_mol = Chem.MolFromSmarts(text)
        if smarts_mol:
            # Find all matches
            matches = self.editor.mol.GetSubstructMatches(smarts_mol)
            if matches:
                self.matches = matches
                self.current_match_idx = 0
                self.highlight_current_match()
                self.statusBar().showMessage(f"Found {len(self.matches)} matches.")
            else:
                self.editor.selectedAtoms = []
                self.statusBar().showMessage("No SMARTS matches found.")
        else:
            self.editor.selectedAtoms = []
            self.statusBar().showMessage("Invalid SMARTS.")
            
        self.update_match_label()

    def prev_match(self):
        if not self.matches:
            return
            
        self.current_match_idx = (self.current_match_idx - 1) % len(self.matches)
        self.highlight_current_match()
        self.update_match_label()

    def next_match(self):
        if not self.matches:
            return
            
        self.current_match_idx = (self.current_match_idx + 1) % len(self.matches)
        self.highlight_current_match()
        self.update_match_label()

    def highlight_current_match(self):
        if 0 <= self.current_match_idx < len(self.matches):
            match = self.matches[self.current_match_idx]
            # match is a tuple of atom indices
            self.editor.selectedAtoms = list(match)
            # RDKit editor draw function uses self.editor.selectedAtoms

    def update_match_label(self):
        if self.matches:
            self.matchLabel.setText(f"{self.current_match_idx + 1}/{len(self.matches)}")
        else:
            self.matchLabel.setText("0/0")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = AppWindow()
    window.show()
    sys.exit(app.exec())
