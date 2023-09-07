# Bachelor's thesis @ Unimi

This repository contains the LaTeX source code and some scripts for my bachelor's thesis in computer science at University of Milan (Unimi).
You can read the full thesis [here](https://github.com/r-carissimi/bachelor-thesis/blob/main/thesis.pdf) or read the useful [abstract](https://github.com/r-carissimi/bachelor-thesis/blob/main/abstract.pdf).



## Goal

This thesis aims to design and implement an emulation environment for 5G networks and edge computing systems, further analyzing the various proposed scheduling algorithms to understand their characteristics and evaluate their impact on the architecture.

## Results achieved

The validity of the designed and implemented architecture was evaluated through simulations of real applications, thanks to which we were able to confirm the achievement of the set goals.

We also paid great attention to the analysis of the scheduling algorithms implemented by IPVS, which Kubernetes relies on. Thus, we were able to derive characteristics and peculiarities of the main scheduling algorithms in order to enable their proper use depending on the desired behavior of the emulation environment.

<p align="center">
    <img src="https://raw.githubusercontent.com/r-carissimi/bachelor-thesis/main/latex/images/15_grafico_scheduler.png" width="800" />
</p>

Based on the test results and from the collected data, we can state that in a geographically distributed environment the shortest expected delay algorithm is generally better performing. On the contrary, the Round-Robin and least connections algorithms are better suited in realities where the computation nodes are in a single geographic area, as they offer better performance for the same number of requests and delays between nodes.

However, it is important to note that the environment allows analysis of any network configuration and scheduling algorithm. This is a very important result that shows the great flexibility of the designed and implemented emulation environment.

An important evolution of the work done so far would be the use of the OMNeT++ simulation system and its Simu5G framework. Through these it would be possible to generate requests from simulated user equipment to the real application, allowing the 5G network to also be considered in the simulation.
