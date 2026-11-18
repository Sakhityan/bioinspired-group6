# Name: Conway's game of life
# Dimensions: 2

# --- Set up executable path, do not edit ---
import sys
import inspect
this_file_loc = (inspect.stack()[0][1])
main_dir_loc = this_file_loc[:this_file_loc.index('ca_descriptions')]
sys.path.append(main_dir_loc)
sys.path.append(main_dir_loc + 'capyle')
sys.path.append(main_dir_loc + 'capyle/ca')
sys.path.append(main_dir_loc + 'capyle/guicomponents')
# ---

from capyle.ca import Grid2D, Neighbourhood, CAConfig, randomise2d
import capyle.utils as utils
import numpy as np


def transition_function(grid, neighbourstates, neighbourcounts):
    """Function to apply the transition rules
    and return the new grid"""
    # unpack state counts for all unique states
    Chaparral_neighbours, Lake_neighbours, Dense_Forest_neighbours, Scrubland_neighbours, Burning_c_neighbours, Burning_df_neighbours, Burning_s_neighbours, Burnt_down_neighbours = neighbourcounts
    burning_neighbours = Burning_c_neighbours + Burning_df_neighbours + Burning_s_neighbours
    # identifies what the tile is 
    is_chaparral = (grid == 0)
    is_dense_forest = (grid == 2)
    is_scrubland = (grid == 3)
    is_burning = (grid == 4) | (grid == 5) | (grid == 6)
    
    # states tansitioning from burning to burnt down is still incomplete
    burnt_out = False
    
    # starts_c_burning = is_chaparral and some function that used the number of neigbours burning to determine the likelyhood the tile goes on fire
    # starts_df_burning = is_dense_forest and some function that used the number of neigbours burning to determine the likelyhood the tile goes on fire
    # starts_s_burning = is_scrubland and some function that used the number of neigbours burning to determine the likelyhood the tile goes on fire
    grid[:, :] = 0
    grid[starts_c_burning] = 4
    grid[starts_df_burning] = 5
    grid[starts_s_burning] = 6
    grid[burnt_out] = 7
    return grid


def setup(args):
    """Set up the config object used to interact with the GUI"""
    config_path = args[0]
    config = utils.load(config_path)
    # -- THE CA MUST BE RELOADED IN THE GUI IF ANY OF THE BELOW ARE CHANGED --
    config.title = "Group Project: Forest Fire"
    config.dimensions = 2 
    Chaparral = 0
    Lake = 1 
    Dense_Forest = 2
    Scrubland = 3
    Burning_c = 4 # burning chaparral
    Burning_df = 5 # burning dense forest
    Burning_s = 6 # burning scubland
    Burnt_down = 7
    config.states = (Chaparral, Lake, Dense_Forest, Scrubland, Burning_c, Burning_df, Burning_s, Burnt_down)
    # -------------------------------------------------------------------------

    # ---- Override the defaults below (these may be changed at anytime) ----

    config.state_colors = [(0.58,0.58,0),(0,0,1),(0,0.24,0),(1,1,0),(0.55,0.18,0),(0.63,0,0),(0.92,0.4,0),(0,0,0)]
    config.grid_dims = (400,400)

    # ----------------------------------------------------------------------

    # the GUI calls this to pass the user defined config
    # into the main system with an extra argument
    # do not change
    if len(args) == 2:
        config.save()
        sys.exit()
    return config


def main():
    # Open the config object
    config = setup(sys.argv[1:])

    # Create grid object
    grid = Grid2D(config, transition_func)

    # Run the CA, save grid state every generation to timeline
    timeline = grid.run()

    # save updated config to file
    config.save()
    # save timeline to file
    utils.save(timeline, config.timeline_path)


if __name__ == "__main__":
    main()
