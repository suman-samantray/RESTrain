# RESTrain

**RESTrain** is a flexible tool for automating partial REST (Replica Exchange with Solute Tempering) molecular dynamics simulations. It enables selective acceleration of conformational sampling in targeted regions—ideal for enhancing the dynamics of protein loops, binding sites, or disordered regions without globally heating the system.

## 🔍 Features
- Supports **partial REST region definition** via index files
- Compatible with **GROMACS** setups and topologies
- Generates `.mdp` files, index groups, and exchange configurations
- Includes templates for submission scripts on HPC clusters

## ⚙️ Requirements
- Python 3.x
- GROMACS (tested on 2019+)
- NumPy

## 🚀 Usage
```bash
python restrain.py -f topol.top -pmd base.mdp -i rest_regions.ndx -o run/
