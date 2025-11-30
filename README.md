# 2dynamics

A collection of machine-learning force field (MLFF) training sets for two-dimensional (2D) halide perovskites.  Among others, these training sets were used to train models to:
1. Explore the structural chirality of 2D halide perovskites at <i>T</i> = 0K and at finite temperatures. [DOI: [`10.1021/acs.jpclett.4c01629`](https://doi.org/10.1021/acs.jpclett.4c01629)]
2. Discover chiral phonons in chiral 2D halide perovskites [DOI: [`10.1021/acs.nanolett.5c01708`](https://doi.org/10.1021/acs.nanolett.5c01708)]
3. Investigate the effect of metal cations on the structural and dynamic chirality of 2D halide perovskites [DOI: [`10.1103/mxyl-tqjb`](https://doi.org/10.1103/mxyl-tqjb)]

## Computational settings

### Training procedure

All training sets were generated using the on-the-fly active learning scheme [1] as implemented in VASP [2-4]. The training sets include total energies, forces, and stresses and are computed with density functional theory (DFT) calculations. We used the following procedures for all training sets:

1. Training at <i>T</i> = 300 K for 50 ps from optimized crystal geometry ([`2database`](https://github.com/mikepols/2database))
2. Training at <i>T</i> = 100 K for 50 ps from final frame of previous run
3. Training at <i>T</i> = 450 K for 50 ps from final frame of previous run
4. Equilibration at <i>T</i> = 350 K for 10 ps
5. Training from <i>T</i> = 350 K to <i>T</i> = 50 K for 60 ps using equilibrated frame

During training the temperature and pressure (1 atm) were controlled using Parinello-Rahman dynamics [5, 6] using friction coefficients $\gamma$ = 5 ps$^{-1}$ and $\gamma_{\mathrm{L}}$ = 5 ps$^{-1}$ for the atomic and lattice degrees of freedom, respectively. A time step of $\Delta t$ = 2 fs was used together with an increased mass of the hydrogen atoms of $m_{\mathrm{H}}$ = 4 amu, to increase the sampling rate of new structures.

### Hyperparameters

Local atomic environments were described using an adaptation of the smooth overlap of atomic positions (SOAP) descriptor [7], for which we employed a cutoff for the two-body radial descriptor $\rho_{i}^{\left( 2 \right)}$ of 6.0 Å, and a 4.0 Å cutoff for the three-body angular descriptor $\rho_{i}^{\left( 3 \right)}$. The atomic positions were broadened using Gaussian distributions with a width of  0.5 Å. Both descriptors were expanded on a basis set of spherical Bessel functions and Legendre polynomials, using 8 and 6 Bessel functions for the two-body and three-body descriptors, respectively, with a maximum angular momentum quantum number of $l_{\mathrm{max}} = 2$. The expansion coefficients of this basis set constitute the descriptor for the local atomic environments. To measure the similarity between two local atomic environments, we employed a polynomial kernel function to a power 4, in which the two-body radial and three-body angular descriptor vectors were weighted by 0.1 and 0.9, respectively.

### Density functional theory

The reference data for the MLFFs was obtained using density functional theory (DFT) calculations. These DFT calculations were performed in the Vienna Ab-initio Simulation Package (VASP) [2-4]. The electron-electron exchange correlation (XC) interactions were modelled using a variety of XC functionals: SCAN [8] and PBE+D3(BJ) [9, 10]. The projector-augmented wave (PAW) pseudopotentials [11] treated the following electrons: H (1s<sup>1</sup>), C (2s<sup>2</sup>2p<sup>2</sup>), N (2s<sup>2</sup>2p<sup>3</sup>), Br (4s<sup>2</sup>4p<sup>5</sup>), Sn (5s<sup>2</sup>5p<sup>2</sup>), I (5s<sup>2</sup>5p<sup>5</sup>), Pb (6s<sup>2</sup>6p<sup>2</sup>) as valence electrons. The cutoff energy for the plane wave basis set was set to 500 eV in all calculations, combined with convergence criteria for the energies and forces of 10<sup>-5</sup> eV and 10<sup>-2</sup> eV/Å, respectively. The reciprocal space was sampled using 2 $\times$ 2 $\times$ 1 Γ-centered <i>k</i>-meshes [12], using a single <i>k</i>-point in the out-of-plane direction.

## Included data

### Training sets

The following training sets are included in this repository, every entry is grouped with the paper it is associated with.

- Pols *et al.*, *J. Phys. Chem. Lett.*, 15, 8057–8064 (2024), DOI: [`10.1021/acs.jpclett.4c01629`](https://doi.org/10.1021/acs.jpclett.4c01629).
	- (<i>S</i>-MBA)<sub>2</sub>PbI<sub>4</sub>
	- PEA<sub>2</sub>PbI<sub>4</sub>
	- BA<sub>2</sub>PbI<sub>4</sub>
- Pols *et al.*, *Phys. Rev. Mater.*, 9, 113601 (2025), DOI: [`10.1103/mxyl-tqjb`](https://doi.org/10.1103/mxyl-tqjb).
	- (<i>S</i>-MBA)<sub>2</sub>SnI<sub>4</sub>
	- (<i>S</i>-MBA)<sub>2</sub>Sn<sub>0.5</sub>Pb<sub>0.5</sub>I<sub>4</sub>
	- (<i>S</i>-MBA)<sub>2</sub>M</sub>I<sub>4</sub> (combined model)
- Others
	- (<i>S</i>-1NEA)<sub>2</sub>PbBr<sub>4</sub>
	- (<i>S</i>-2NEA)<sub>2</sub>PbBr<sub>4</sub>

### Merge data

The `merge` folder contains the `ml_ab_merge.py` script that can be used to combine separate VASP training sets (`ML_AB`) into a single training set that can be used to train an combined MLFF. The script can be used as:
```
ml_ab_merge.py -i ML_AB1 ML_AB2 ML_AB3 -o ML_ABN_NEW
```
This outputs a combined training set that has to be sampled using the `ML_MODE = SELECT` setting in VASP. As an example the folder contains the training sets (`ML_AB_S-MBA2PbI4_SCAN`, `ML_AB_S-MBA2SnI4_SCAN`, and `ML_AB_S-MBA2SnPbI4_SCAN`) that were used to create the mixed metal model (`ML_AB_S-MBA2MI4_SCAN`).

## Usage

The training sets can be freely used, however, it is greatly encouraged to reference the work these training sets were generated for.

## References

1. Jinnouchi *et al.*, *Phys. Rev. B*, 100, 014105 (2019), DOI: [`10.1103/PhysRevB.100.014105`](https://doi.org/10.1103/PhysRevB.100.014105).
2. Kresse *et al.*, *Phys. Rev. B*, 49, 14251 (1994), DOI: [`10.1103/PhysRevB.49.14251`](https://doi.org/10.1103/PhysRevB.49.14251).
3. Kresse *et al.*, *Comput. Mater. Sci.*, 6, 15-50 (1996), DOI: [`10.1016/0927-0256(96)00008-0`](https://doi.org/10.1016/0927-0256(96)00008-0).
4. Kresse *et al.*, *Phys. Rev. B*, 54, 11169 (1996), DOI: [`10.1103/PhysRevB.54.11169`](https://doi.org/10.1103/PhysRevB.54.11169).
5. Parrinello *et al.*, *Phys. Rev. Lett.*, 45, 1196 (1980), DOI: [`10.1103/PhysRevLett.45.1196`](https://doi.org/10.1103/PhysRevLett.45.1196).
6. Parrinello *et al.*, *J. Appl. Phys.*, 57, 7182-7190 (1981), DOI: [`10.1063/1.328693`](https://doi.org/10.1063/1.328693).
7. Bartók *et al.*, *Phys. Rev. B*, 87, 184115 (2013), DOI: [`10.1103/PhysRevB.87.184115`](https://doi.org/10.1103/PhysRevB.87.184115).
8. J. Sun. *et al.*, *Phys. Rev. Lett.*, 115, 036402 (2015) , DOI: [`10.1103/PhysRevLett.115.036402`](https://doi.org/10.1103/PhysRevLett.115.036402).
9. J.P. Perdew *et al.*, *Phys. Rev. Lett.*, 77, 3865 (1996) , DOI: [`10.1103/PhysRevLett.77.3865`](https://doi.org/10.1103/PhysRevLett.77.3865).
10. S. Grimme *et al.*, *J. Chem. Phys.*, 132, 154104 (2010) , DOI: [`10.1063/1.3382344`](https://doi.org/10.1063/1.3382344).
11. Kresse *et al.*, *Phys. Rev. B*, 59, 1758 (1999) , DOI: [`10.1103/PhysRevLett.115.036402`](https://doi.org/10.1103/PhysRevLett.115.036402).
12. H.J. Monkhorst *et al.*, *Phys. Rev. B*, 13, 5188 (1976) , DOI: [`10.1103/PhysRevB.13.5188`](https://doi.org/10.1103/PhysRevB.13.5188).
