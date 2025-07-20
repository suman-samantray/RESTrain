# RESTrain

**RESTrain** is a flexible tool for automating scaling in REST (Replica Exchange with Solute Tempering) molecular dynamics simulations that selectively accelerate sampling of user-chosen regions using PLUMED + GROMACS. It enables selective acceleration of conformational sampling in targeted regions—ideal for enhancing the dynamics of protein loops, binding sites, or disordered regions without globally heating the system.

## 🔍 Features
- Supports **partial REST region definition** via index files
- Compatible with **GROMACS** setups and topologies
- Generates `.mdp` files, index groups, and exchange configurations
- Includes templates for submission scripts on HPC clusters

## ⚙️ Requirements
- Python 3.x
- GROMACS (tested on 2019+)
- NumPy

## 🔧 Scripts

- `partial_tempering.sh`: Applies REST scaling factors (e.g., 1.0, 0.926, 0.856…) to Amber-style `.top` files via PLUMED.
- `partial_tempering-charmm.py`: Applies REST scaling factors (e.g., 1.0, 0.926, 0.856…) to Charmm-style `.top` files via PLUMED.

---

## 🚀 Example Usage

### Amber-based REST:
```bash
./partial_tempering.sh 1.00   < processed_new.top > abeta16-22_amber_rest0.top
./partial_tempering.sh 0.926  < processed_new.top > abeta16-22_amber_rest1.top
./partial_tempering.sh 0.856  < processed_new.top > abeta16-22_amber_rest2.top
...

