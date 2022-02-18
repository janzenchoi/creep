# Description

The repository contains a program that uses the Visco-Plastic (V-P) model to predict the creep behaviour of Alloy 617. The V-P model contains 8 material parameters, which are determined using the Multi-Objective Genetic Algorithm (MOGA).

This `README.md` file was last updated on 18/02/2022.

# Instructions

The following are instructions to install and run the program. Running the program will read the experimental data and conditions from `creep/src/alloy_617.xlsx`, and execute the MOGA to optimise the parameters of the V-P model.

1) Open up a terminal and change to your desired directory.
2) Clone the repository by running `git clone https://github.com/jazzzmannn/creep/`.
3) Change to the directory with the code by running `cd creep/src/`.
4) Run the code by running `python main.py`.
5) The results will be stored in `creep/src/results/`.

# Configuration

You can easily change the settings of the optimisation.

* To include/exclude certain creep curves in the optimisation, go to `creep/src/alloy_617.xlsx`, and toggle TRUE/FALSE in the include column (of the `info` sheet).
* To change the hyperparameters of the MOGA, change the constant values in `creep/src/packages/genetic_algorithm.py`.
* To change which of the objective functions to use, change the constant array in `creep/src/packages/objective.py`.
* To change the input/output paths/names, change the constant strings in `creep/src/main.py`.

# Recorder Functionality

I have implemented a 'recorder' class, located at `creep/src/packages/io/recorder.py`.

* The class will store the results every 50 generations, so that a full run of the optimisation is not required to retrieve results.
* The class will also store the results of the latest generation, with a summary of the optimisation settings, and the general progress of the optimisation.
* The purpose of this class is to prevent the loss of results if the program were to halt (e.g., crash).
* When running multiple instances of `main.py`, the recorder will pipe the results for each optimisation into different directories.

# Running Multiple Instances

To run multiple instances of the program, run `nohup python3 <filename>.py &`.

* You will be able to check these instances by running `htop` in the terminal.
* You can close the terminal once you have run the `nohup` command - it will run in the background.
* You can run `kill -9 <pid>` to kill the instance, where `<pid>` is the PID of the instance/process.
