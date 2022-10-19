# Sensitivity analysis on a model the social consequences of testimonial norms

[![Build Status](https://github.com/Jannetty/science_cliques/workflows/build/badge.svg)](https://github.com/Jannetty/science_cliques/actions?query=workflow%3Abuild)
[![codecov](https://codecov.io/gh/Jannetty/science_cliques/branch/main/graph/badge.svg?token=p46b5eTAyy)](https://codecov.io/gh/Jannetty/science_cliques)
[![Lint Status](https://github.com/Jannetty/science_cliques/workflows/lint/badge.svg)](https://github.com/Jannetty/science_cliques/actions?query=workflow%3Alint)
[![Documentation](https://github.com/Jannetty/science_cliques/workflows/documentation/badge.svg)](https://jannetty.github.io/science_cliques/)
[![Code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

This repo contains a python implementation of [Kevin J. S. Zollman's](https://www.kevinzollman.com/)
"Science Cliques" agent based model.
The original model was published in 
[Zollman, Kevin J.
S. “Modeling the Social Consequences of 
Testimonial Norms.”](https://www.kevinzollman.com/uploads/5/0/3/6/50361245/zollman_-_modeling_the_social_consequence_of_testimonial_norms.pdf)
(Zollman, Kevin J. S. “Modeling the Social Consequences of Testimonial Norms.” Philosophical Studies 172, no. 9 (2015): 2371–83. doi:10.1007/s11098-014-0416-7.)
Original source code in netlogo can be found [here](https://www.kevinzollman.com/uploads/5/0/3/6/50361245/sciencecliquesv2.nlogo)
with original data output files [here](https://www.kevinzollman.com/uploads/5/0/3/6/50361245/testimonydata.qti) and [here](https://www.kevinzollman.com/uploads/5/0/3/6/50361245/polymorphictestimony.qti) 
(original data files in [QtiPlotformat](http://www.qtiplot.com/))

Final write up for this project can be read in [Science_Cliques_writeup.pdf](Science_Cliques_writeup.pdf).

Note that the displayed code coverage is inflated. This was a course project that I used as an opportunity to experiment with [Codecov](https://about.codecov.io/). Most tests I wrote do not actually test anything, thus the effective coverage is lower than the coverage displayed.

## Motivation
Philosophers of science use Agent Based Models (ABMs) to study how 
collaboration and communication network structures emerge from decisions and 
actions made by individual scientists. While models in this field have allowed 
researchers to generate new hypotheses relating individuals' behaviors to 
emergent network structures, researchers rarely discuss the robustness of 
their results to changes in (parametric and non parametric) model elements, 
nor do researchers frequently characterize which elements have the greatest 
impact on emergent behavior.

Here I present an example of how a simple sensitivity analysis can be 
conducted on a philosophy ABM and what additional information can be gleaned 
from sensitivity analysis.

## Model overview
number_of_individuals individuals exist in the model. Each individual 
has a reliability(which is pulled from a beta distrubution and averages .6 
over the entire population). num_facts number of facts exist in the
model. Individuals have a correct belief, an incorrect belief, or no 
belief about each fact. Individuals begin with a starting_knowledge number 
of beliefs. The accuracy of these initial beliefs is proportional to the 
individual's reliability (an individual with a reliability of .6 will have 
roughly 60% true beliefs and 40% false beliefs).

The model is advanced 500 time steps per run. At each time step, each 
individual progresses through three phases.
1. **Investigate**: With probability investigation_probability, independently 
   generate a new belief about a fact the individual previously had no 
   opinion about. The probability of this new belief being true is the 
   individual's reliability.
2. **Select Teachers**: Select a set of number_of_neighbors unique individuals 
   from whom to solicit testimony. Each teacher presents a random fact and 
   opinion about that fact. Teachers only present facts about which they 
   have an opinion.
3. **Learn**: Adopt the opinions of teachers if they offer an opinion about 
   a fact this individual does not currently have an opinion about, 
   otherwise ignore new teacher and keep previous opinion.

All individuals in a model follow one of four philosophies; skeptical, reid, 
direct, and indirect. The individuals' philosophy determines each 
individual's behavior in each phase. Skeptical individuals do not 
select teachers nor learn from teachers. They only learn new facts through 
investigation. Reid individuals select teachers randomly. Direct individuals 
select the individuals who have the highest percentage of true beliefs as 
their teachers, calculated using the equation below.

![\Small x=\frac{\mathrm{truebeliefs}}{(\textrm{truebeliefs}&space;&plus;
&space;\textrm{falsebeliefs})}](https://latex.codecogs.com/svg.image?\frac{\mathrm{truebeliefs}}{(\textrm{truebeliefs}&space;&plus;&space;\textrm{falsebeliefs})}) 

Indirect individuals select individuals who have the most beliefs 
in common with themselves as their teachers. All ties when direct or indirect
individuals are selecting teachers are broken randomly.

## Sensitivity Analysis
The sensitivity analysis implemented here is a simple one-at-a-time method.
The parameters selected for sensitivity analysis are as follows:
- number_of_individuals: the total number of individuals in the model. 
  - Values tested: [8, 20, 40, 60, 80, 100]
- number_of_facts: the total number of facts in the model.
  - Values tested: [16, 300, 600, 900, 1200, 1500]
- investigation_probability: the probability an individual investigates and 
  generates a new belief about an unknown fact each run
  - Values tested: [0, .2, .4, .6, .8, 1]
- philosophy: the philosophy guiding individual behavior 
  - Values tested: 
    ['skeptical', 'reid', 'direct', 'indirect']

The model was run 10 times with each permutation of parameters. 
number_of_neighbors was set to 8 for all runs.

The output measured for each run were as follows:
- truth_mean: the percent of facts agents' have opinions about that are true 
  (calculated using equation above for all agents' beliefs in the model)
- truth_total: the total number of true opinions held by all agents in the model
- false_mean: the percent of facts agents' have opinions about that are false
- false_total: the total number of false opinions held by all agents in the 
  model

Correlation coefficients were calculated between parameters and outputs.

## Implementation Details
Brief overview of python tools implemented in directory (thanks to [Jessica 
Yu's](https://github.com/jessicasyu) python template):
- [Poetry](https://python-poetry.org/) for packaging and dependency management
- [Tox](https://tox.readthedocs.io/en/latest/) for automated testing
- [Black](https://black.readthedocs.io/en/stable/) for code formatting
- [Pylint](https://www.pylint.org/) for linting
- [Mypy](http://mypy-lang.org/) for type checking
- [Sphinx](https://www.sphinx-doc.org/) for automated documentation

This model is built using the python package [mesa](https://github.com/projectmesa/mesa).


