## AI Powered Flappy Bird
A Pygame implementation of classic Flappy-Bird game controlled by Neuroevolutional AI.<br/>
*Images resources are found online, you may use them for any purposes.*

## GIFs
|![Screen 1](https://github.com/JasonFengGit/Flappy-Bird-AI-Powered/raw/master/GIFs/1.gif) |![Screen 2](https://github.com/JasonFengGit/Flappy-Bird-AI-Powered/raw/master/GIFs/2.gif)|
|---------------------------------------------|---------------------------------------------|
|![Screen 3](https://github.com/JasonFengGit/Flappy-Bird-AI-Powered/raw/master/GIFs/3.gif) |![Screen 4](https://github.com/JasonFengGit/Flappy-Bird-AI-Powered/raw/master/GIFs/4.gif)|

## Logistic
**This project uses the [NEAT(NeuroEvolution of Augmenting Topologies)](https://en.wikipedia.org/wiki/Neuroevolution) algorithm with [neat-python](https://neat-python.readthedocs.io/en/latest/neat_overview.html).<br/>
Check out the initial NEAT Paper [here](http://nn.cs.utexas.edu/downloads/papers/stanley.cec02.pdf).**

In our NEAT algorithm, each bird has its own genomes(weights of its neural network), and birds that performs well get to pass their genomes to the next generation. Our idea is to evolve the "best" set of genome through generations to make the birds master the game.

## Dependencies
`neat-python`:
```
pip install neat-python
```

`pygame`:
```
pip install pygame
```

## How To Run
Clone this project and run `flappy-bird.py`.

## Sample Stats of A Generation
```
 ****** Running generation 1 ****** 

Population's average fitness: 192.69333 stdev: 98.08002
Best fitness: 812.60000 - size: (3, 7) - species 2 - id 35
Average adjusted fitness: 0.010
Mean genetic distance 3.222, standard deviation 0.580
Population of 75 members in 31 species:
   ID   age  size  fitness  adj fit  stag
  ====  ===  ====  =======  =======  ====
     1    1     8    751.6    0.181     0
     2    1     9    812.6    0.073     0
     3    1     2    175.4    0.000     0
     4    1     2    175.6    0.000     0
     5    1     2    175.6    0.000     0
     6    1     2    175.2    0.000     1
     7    1     2    175.2    0.000     1
     8    1     2    175.4    0.000     1
     9    1     2    175.8    0.000     0
    10    1     2    251.4    0.040     1
    11    1     2    175.4    0.000     0
    12    1     2    175.6    0.001     1
    13    1     2    175.6    0.000     0
    14    1     2    175.8    0.000     0
    15    1     2    175.4    0.000     0
    16    1     2    175.6    0.000     1
    17    1     2    176.0    0.001     0
    18    1     2    175.4    0.000     1
    19    1     2    175.4    0.000     0
    20    1     2    175.4    0.000     1
    21    1     2    175.6    0.000     0
    22    1     2    175.4    0.000     0
    23    1     2    175.8    0.000     0
    24    1     2    175.6    0.000     0
    25    1     2    175.4    0.000     0
    26    1     2    175.6    0.000     0
    27    1     2    175.4    0.000     1
    28    1     2    175.4    0.000     0
    29    1     2    176.0    0.001     0
    30    1     2    176.2    0.001     0
    31    1     2    175.4    0.000     0
Total extinctions: 0
Generation time: 6.907 sec (6.901 average)
```

## Potential Improvements 
- increase the difficulty along with game progress
- try different model architectures
- add random rewards and punishments(such as fruits and bombs) in the game
- ...

