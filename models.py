import jajapy as ja
import numpy as np
import stormpy

def observations_to_file(training_set, model):
    filename = "experiments/scalability-experiment/observations/" +model.name + "_observations_cupaal.txt"
    with open(filename, "w") as file:
        for time, sequence in zip(training_set.times, training_set.sequences):
            for i in range(time):
                file.write(' '.join(sequence) + '\n')

def print_to_console(filename):
    with open(filename, "r") as file:
        for line in file:
            print(line, end='')

def write_to_file(model, name, i):
    filename = "experiments/scalability-experiment/initial-models/" + name + "_cupaal_run" + str(i) + ".txt"
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

def make_model(filepath):
    model = ja.loadPrism(filepath)
    model.name = "leader_sync" + str(model.nb_states)

    #training_set = model.generateSet(30, 10)
    #observations_to_file(training_set, model)
    #training_set.save("experiments/scalability-experiment/observations/" + model.name + "_observations_jajapy.txt")

    for i in range(5):
        initial_model = ja.MC_random(nb_states=model.nb_states-1, labelling=model.labelling[1:], random_initial_state=False, sseed=i)
        initial_model.save("experiments/scalability-experiment/initial-models/" + model.name + "_jajapy_run" + str(i) + ".txt")
        write_to_file(initial_model, model.name, i)

model = ja.loadPrism("experiments/original-models/tandem.v1.prism")
model.name = "tandem"
training_set = model.generateSet(30, 10, timed=False)
observations_to_file(training_set, model)
training_set.save("experiments/scalability-experiment/observations/" + model.name + "_observations_jajapy.txt")

make_model("experiments/original-models/tandem.v1.prism")
make_model("experiments/original-models/tandem.v1.2.prism")
make_model("experiments/original-models/tandem.v1.3.prism")
make_model("experiments/original-models/tandem.v1.4.prism")

#make_model("experiments/original-models/dtmc/leader_sync.3-2.v1.prism")
#make_model("experiments/original-models/dtmc/leader_sync.3-3.v1.prism")
#make_model("experiments/original-models/dtmc/leader_sync.3-4.v1.prism")
#make_model("experiments/original-models/dtmc/leader_sync.4-2.v1.prism")
#make_model("experiments/original-models/dtmc/leader_sync.4-3.v1.prism")
#make_model("experiments/original-models/dtmc/leader_sync.4-4.v1.prism")
#make_model("experiments/original-models/dtmc/leader_sync.5-2.v1.prism")
#make_model("experiments/original-models/dtmc/leader_sync.5-3.v1.prism")
#make_model("experiments/original-models/dtmc/brp.v1.prism", "brp")
#make_model("experiments/original-models/dtmc/crowds.v1.prism", "crowds")
#make_model("experiments/original-models/dtmc/oscillators.3-6-0.1-1.v1.prism", "oscillators1")
#make_model("experiments/original-models/dtmc/oscillators.6-6-0.1-1.v1.prism", "oscillators2")
#make_model("experiments/original-models/dtmc/oscillators.6-8-0.1-1.v1.prism", "oscillators3")

    

#original_model, results = ja.BW().fit(training_set, initial_model=model, nb_states=model.nb_states, pp=0, verbose=4, return_data=True)
#new_model, new_results = ja.BW().fit(training_set, initial_model=initial_model,nb_states=model.nb_states, pp=0,verbose=4, return_data=True)
#print(results['training_set_loglikelihood'])
#print(new_results['training_set_loglikelihood'])
#print(results['training_set_loglikelihood'] - new_results['training_set_loglikelihood'])
