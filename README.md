# Sensitivity analysis on a model the social consequences of testimonial norms

[![Build Status](https://github.com/Jannetty/science_cliques_sensitivity_analysis/workflows/build/badge.svg)](https://github.com/Jannetty/science_cliques_sensitivity_analysis/actions?query=workflow%3Abuild)
[![codecov](https://codecov.io/gh/Jannetty/science_cliques_sensitivity_analysis/branch/main/graph/badge.svg?token=ZK8G71CJUU)](https://codecov.io/gh/Jannetty/science_cliques_sensitivity_analysis)
[![Lint Status](https://github.com/Jannetty/science_cliques_sensitivity_analysis/workflows/lint/badge.svg)](https://github.com/Jannetty/science_cliques_sensitivity_analysis/actions?query=workflow%3Alint)
[![Documentation](https://github.com/bagherilab/python_project_template/workflows/documentation/badge.svg)](https://bagherilab.github.io/python_project_template/)
[![Code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Original model implemented by [Kevin J. S. Zollman](https://www.kevinzollman.com/) in [Zollman, Kevin J. S. “Modeling the Social Consequences of 
Testimonial Norms.” Philosophical Studies 172, no. 9 (2015): 2371–83. doi:10.
1007/s11098-014-0416-7.](https://www.kevinzollman.com/uploads/5/0/3/6/50361245/zollman_-_modeling_the_social_consequence_of_testimonial_norms.pdf).
Original source code in netlogo can be found [here](https://www.kevinzollman.com/uploads/5/0/3/6/50361245/sciencecliquesv2.nlogo)
with original data output files [here](https://www.kevinzollman.com/uploads/5/0/3/6/50361245/testimonydata.qti) and [here](https://www.kevinzollman.com/uploads/5/0/3/6/50361245/polymorphictestimony.qti) 
(original data files in [QtiPlotformat](http://www.qtiplot.com/))

Overview of tools implemented in directory:
- [Poetry](https://python-poetry.org/) for packaging and dependency management
- [Tox](https://tox.readthedocs.io/en/latest/) for automated testing
- [Black](https://black.readthedocs.io/en/stable/) for code formatting
- [Pylint](https://www.pylint.org/) for linting
- [Mypy](http://mypy-lang.org/) for type checking
- [Sphinx](https://www.sphinx-doc.org/) for automated documentation


### Sophia is adding things now

Potential ranges of parameters
```python
import numpy as np
# Possible ranges of parameters
possible_number_of_individuals = range(1, 101)
possible_number_of_facts = range(1, 1501)
possible_investigation_probability = np.arange(0, 1, 0.01)
only_new_facts = bool
possible_starting_knowledge = range(0, 1501)
believe_most_recent = bool
possible_reliability_alpha = range(1, 101)
possible_reliability_beta = np.arange(0.001, 0.991, 0.01)
possible_rewire_probability = np.arange(0, 1, 0.01)
direct_calibration = bool
possible_proportion_alternative_rewire = np.arange(0, 1, 0.01)
possible_alternative_rewire_probability = np.arange(0, 1, 0.01)
use_random_seed = bool
parameter_randomize = bool
```

### Notes on Zollman's described ABM

#### Setup
- 100 individuals
- can solicit 2, 4, 6, or 8 people for testimony (information)
- "very large number of logically independent propositions" they'd like to learn
  - 1500 for all runs
- start life with info about small number of propositions they believe or 
  disbelieve, abstain from all others
  - 15 for all runs
  - correct initial beliefs is correlated to individual's reliability (see 
    below)
- for each proposition, individual can believe, disbelieve, or abstain 
  ("withold judgement")
- each individual has intrinsic reliability that determines likelihood in 
  believing true propositions and disbelieving false propositions 

#### Overview of parameters
- individual reliability (random but averages to 60% over all individuals)
  - average reliability of all individuals was never varied
- direct calibration: true and false (from looking at parameters)
  - true for directhume, false for indirecthume, false for reid
- neighbor percent = percent of number of neighbors (2 neighbors, 2 percent,
   8 neighbors, 8 percent)
- reid wire probability = 0, Hume wire probability = 1
- investigation probability = .1
- only_newfacts = false
- believe_most_recent = false
- reliability determined by drawing from beta distribution
  - reliability beta = 1
  - reliability alpha = 1.5
- parameter randomize = fals
- step[Y] = 500
- outputs:
  - meantruth - mean of individuals[Y]
  - variancetruth - mean of individuals[Y]
  - meantruth - total of individuals[Y]
  - variancetruth - total of individuals[Y]
  - paper also talks about sizes of communities so probably some statistics 
    about community size
  
#### At each time step each individual
- observes something true about the world with 10% chance
- chooses a group of people with which to solicit testimony
- asks each member of the group to tell them something that member either 
  believes or disbelieves
- receives honest replies from the asked individuals
- if told somethign about which they currently have no opinion, they believe 
  what they are told. Otherwise they donnot change their belief
  - "This means that in this model there is no ‘‘belief revision.’’ This is certainly an idealization, which has been made for two reasons. First, following the literature on testimony this model focuses primarily on the acquisition of new beliefs not on belief revision. The later issue, called peer disagreement, has an extensive literature which will not be addressed here. Second, there is no uncontroversial way to model belief revision especially in the context of qualitative beliefs. Important future work should tackle this question directly to determine how robust the findings are to modifications of this assumption."
Process is repeated 500 times