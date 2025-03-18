import jajapy as ja
from random import uniform, randint
import stormpy
from ast import literal_eval
import numpy as np
from numpy.random import seed

def write_to_file(model, filename):
    with open(filename, "w") as file:
        file.write('states\n')
        for i in range(model.nb_states):
            file.write(str(i) + ' ')
        file.write("\nlabels\n")
        
        unique_labels = list(set(model.labelling))
        for label in unique_labels:
            file.write(label + ' ')
        file.write("\ninitial\n")
        
        initial_state_str = ' '.join(map(str, model.initial_state.tolist()))
        file.write(initial_state_str)
        file.write("\ntransitions\n")
        
        #normalize the transition matrix to each row to sum to 1
        for i in range(model.nb_states):
            row_sum = sum(model.matrix[i])
            for j in range(model.nb_states):
                model.matrix[i][j] = model.matrix[i][j] / row_sum
        for i in range(model.nb_states):
            for j in range(model.nb_states):
                file.write(f"{model.matrix[i][j]} ")
            file.write("\n")
        file.write("\nemissions\n")
        
        for j in range(len(unique_labels)):
            for i in range(model.nb_states):
                if model.labelling[i] == unique_labels[j]:
                    file.write("1 ")
                else:
                    file.write("0 ")
            file.write("\n")

def print_to_console(filename):
    with open(filename, "r") as file:
        for line in file:
            print(line, end='')

def normalize(arr, t_min, t_max):
    norm_arr = []
    diff = t_max - t_min
    diff_arr = max(arr) - min(arr)
    for i in arr:
        temp = (((i - min(arr))*diff)/diff_arr) + t_min
        norm_arr.append(temp)
    return norm_arr

def observations_to_file(model):
    training_set = model.generateSet(10, 30)
    filename = "experiments/observations/" + model.name + "_observations.txt"
    with open(filename, "w") as file:
        for time, sequence in zip(training_set.times, training_set.sequences):
            for i in range(time):
                file.write(' '.join(sequence) + '\n')

def MC_random(nb_states: int, sseed:int=None):
	if sseed != None:
		seed(sseed)
	matrix = []
	for _ in range(nb_states):
		matrix.append((randomProbabilities(nb_states)))
	matrix = np.array(matrix)
	seed() # reset seed
	return matrix

def randomProbabilities(length, decimals=5):
    # Generate random numbers
    random_numbers = np.random.rand(length)
    # Normalize the random numbers so they sum to 1
    normalized_probabilities = random_numbers / random_numbers.sum()

    #formatted_probabilities = [float(f"{p:.{decimals}f}") for p in normalized_probabilities]
    formatted_probabilities = [round(p, decimals) for p in normalized_probabilities]
    return formatted_probabilities

def generate_random_model(model):
    filename = "experiments/initial-models/" + model.name + "_run"
    for i in range(10):
        model.matrix = MC_random(model.nb_states)
        write_to_file(model, filename + str(i) + ".txt")
        print("Done! with "+ filename + str(i) + ".txt")

# Usage example
print("Creating model...")
leader_sync = ja.loadPrism("experiments/original-models/dtmc/leader_sync.4-3.v1.prism")
brp = ja.loadPrism("experiments/original-models/dtmc/brp.v1.prism")
crowds = ja.loadPrism("experiments/original-models/dtmc/crowds.v1.prism")
oscilltor_1 = ja.loadPrism("experiments/original-models/dtmc/oscillators.3-6-0.1-1.v1.prism")
oscilltor_2 = ja.loadPrism("experiments/original-models/dtmc/oscillators.6-6-0.1-1.v1.prism")
oscilltor_3 = ja.loadPrism("experiments/original-models/dtmc/oscillators.6-8-0.1-1.v1.prism")
oscilltor_4 = ja.loadPrism("experiments/original-models/dtmc/oscillators.6-10-0.1-1.v1.prism")
leader_sync.name = "leader_sync"
brp.name = "brp"
crowds.name = "crowds"
oscilltor_1.name = "oscilltor_1"
oscilltor_2.name = "oscilltor_2"
oscilltor_3.name = "oscilltor_3"
oscilltor_4.name = "oscilltor_4"

print("Writing to file...")
observations_to_file(leader_sync)
observations_to_file(brp)
observations_to_file(crowds)
observations_to_file(oscilltor_1)
observations_to_file(oscilltor_2)
observations_to_file(oscilltor_3)
observations_to_file(oscilltor_4)

print("Done!")

generate_random_model(leader_sync)
generate_random_model(brp)
generate_random_model(crowds)
generate_random_model(oscilltor_1)
generate_random_model(oscilltor_2)
generate_random_model(oscilltor_3)
generate_random_model(oscilltor_4)

1.0/0.5