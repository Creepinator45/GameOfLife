
# GameOfLife

This is an implementation of Conway's Game of Life in which cells manage themselves locally as opposed to globally.

If you don't know what Conway's Game of Life is, here's the [wiki](https://conwaylife.com/wiki/Conway%27s_Game_of_Life).

## Instructions

Just run main.py to simulate the GameOfLife, you may need to install python. 

To input your own starting cell arrangement see the demoStartingCellsFile for instructions on how the file should be formatted. 

The variables defined in the first few lines of main() in main.py are adjustable parameters. Change them to add the path to your own starting cells file or change simulation parameters.

## Why it's interesting

Most implementations of the Game of Life I've seen use a shared grid structure that's responsible for managing cells and rules. This implementation offloads that to the cells, which are each only given information from their immediate neighbors. This reflects an interesting aspect of the Game of Life, which is that all of the intricacies of the game arise emergently out of simple rules which apply only on a local scale. I find this implementation of the game to be more mathematically satisfying.

Cells only exist if they're alive or are directly adjacent to a living cell. Each cell will notify their neighbors when they change state. When a cell becomes alive they will generate cells next if those cells don't yet exist.

Only 2 aspects of the simulation are managed globally:
- A hashmap of weak references to all cells that currently exist. This is necassary so that cells can lookup if a cell already exists before generating a new cell. 

    These are weak references so that dead cells with no living neighbors can be automatically garbage collected, though by default dead cells are set to automatically delete themselves if they have no living neighbors.
- Global functions for alerting cells to update. This is necassary so that cells stay synchronized with each other between iterations.
