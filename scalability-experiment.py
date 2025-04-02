import jajapy.jajapy as ja
import numpy as np
import stormpy

def run_experiment(model_name, states):
    file = open("experiments/scalability-experiment/results/" + model_name +"_output_jajapy.txt", "w")
    file.write("Results for " + model_name + "\n")
    file.write("states, run, iterations, time, log-likelihood, [log-likelihood per iteration]\n")
    training_set = ja.loadSet("experiments/scalability-experiment/observations/" + model_name + "_observations_jajapy.txt")
    states.sort()
    for i in range(len(states)):
        for j in range(5):
            initial_model = ja.loadMC("experiments/scalability-experiment/initial-models/" + model_name +str(states[i]) + "_jajapy_run" + str(j) + ".txt")
            new_model, new_results = ja.BW().fit(training_set, initial_model=initial_model,nb_states=initial_model.nb_states, pp=0,verbose=2, return_data=True)
            print(new_results)
            file.write(str(states[i]) + ',' +
                    str(i)+ ',' + 
                   str(new_results['learning_rounds'])+ ',' + 
                   str(new_results['learning_time']) + ','+ 
                   str(new_results['training_set_loglikelihood']) + ',' + 
                   str([val for _, val in new_results['additional_info']]) + '\n'
                   )
            new_model = ja.stormpyModeltoJajapy(h=new_model)
            new_model.save(file_path="experiments/results/" + model_name + "_jajapy_run" + str(i) + ".txt")
    file.close()

run_experiment("tandem", [66, 120, 496, 2016])
run_experiment("leader_sync", [26, 61, 69, 141, 147, 274, 812])