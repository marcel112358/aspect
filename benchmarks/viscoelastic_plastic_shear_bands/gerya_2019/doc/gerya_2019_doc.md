(sec:benchmarks:gerya_2019-shortening_block)=
# Shortening of a visco-elasto-plastic block

*This section was contributed by Marcel Saaro, Cedric Thieulot and John Naliboff.*

This benchmark originates in {cite:t}`Ger10`. 
In the first edition of the book the domain is a square of size $L=1000~\text{km}$, while it is of size $L=100~\text{km}$ in the second edition, which is the dimension we use in this benchmark. The boundary conditions and material layout are shown in {numref}`fig:gerya_2019_shortening_block_setup`.


```{figure-md} fig:gerya_2019_shortening_block_setup
<img src="./gerya_2019_shortening_block_setup.*" alt="shortening_block" width="80%"/>

Shortening of visco-(elasto-)plastic block benchmark. Boundary conditions and material layout. The red, green and blue lines correspond to angles of $63.5\text{°}$, $45\text{°}$ and $26.5\text{°}$ respectively.
```


The thickness of the top and bottom weak layer
as well as the dimensions of the square inclusion have been slightly modified so 
that element edges align with these material interfaces 
for uniformly refined meshes of level 4 and up: The size of the inclusion is then $L/8=12.5~\text{km}$ and the block has a thickness of $50~\text{km}$.

The velocity on the boundaries is $v_{bc}=5 \times 10^{-9}~\text{m s}^{-1}$ so that the background strain rate is $2 v_{bc}/L = 1 \times 10^{-13}~\text{s}^{-1}$.
The weak medium and the weak inclusion have a viscosity 
$\eta=1 \times 10^{17}~\text{Pa s}$ while 
the block is visco-plastic with $c=100~\text{MPa}$ and $\phi=37\text{°}$. 
Gravity is set to zero (material density values are then irrelevant) and pressure is normalised so that its volume average is zero.

In the case of the von Mises ($\phi=0\text{°}$) failure criterion we expect the shear bands at $\frac{\pi}{4}=45\text{°}$ (see green line in Figure~\ref{fig:shortening_vp_block}). 
When $\phi=37\text{°}$, we expect the shear band angle to be given by the Coulomb angle $\frac{\pi}{4} +\pm \frac{\phi}{2}$, i.e. $26.5\text{°}$ in compression and $63.5\text{°}$ in extension
represented by the blue and red lines in {numref}`fig:gerya_2019_shortening_block_setup` respectively. 

There are 3 input files in `/benchmarks/viscoelastic_plastic_shear_bands/gerya_2019`.

The `gerya_2019_vp.prm` file corresponds to the visco-plastic case, while `gerya_2019_vep.prm` corresponds to the visco-elasto-plastic case and `gerya_2019_vp_damper.prm` 
corresponds to the visco-plastic case which makes use of the so-called plastic damper.
In order to easily compare results between models, the strain rate is measured on the purple dashed line (see {numref}`fig:gerya_2019_shortening_block_setup`) and plotted with the help of the included `gerya_2019_analysis.py` script.



```{figure-md} fig:gerya_2019_vep_result
<img src="./gerya_2019_vep.*" width="100%"/>

The strain rate field and its profile at the height $\frac{5}{16}$ of the shortening block in the *visco-elasto-plastic case* from {cite:t}`Ger10`.
```

```{figure-md} fig:gerya_2019_vp_result
<img src="./gerya_2019_vp.*" width="100%"/>

The strain rate field and its profile at the height $\frac{5}{16}$ of the shortening block in the *visco-plastic case* from {cite:t}`Ger10`.
```

```{figure-md} fig:gerya_2019_vp_damper_result
<img src="./gerya_2019_vp_damper.*" width="100%"/>

The strain rate field and its profile at the height $\frac{5}{16}$ of the shortening block in the *visco-plastic case using the damper* from {cite:t}`Ger10`.
```
