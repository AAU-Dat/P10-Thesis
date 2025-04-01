import jajapy.jajapy as ja
import numpy as np
import stormpy

def run_experiment(model_name):
    file = open("experiments/results/" + model_name +"_output_jajapy.txt", "w")
    file.write("Results for " + model_name + "\n")
    file.write("run, iterations, time, log-likelihood, [log-likelihood per iteration]\n")
    training_set = ja.loadSet("experiments/observations/" + model_name + "_observations_jajapy.txt")
    for i in range(10):
        initial_model = ja.loadMC("experiments/initial-models/" + model_name + "_jajapy_run" + str(i) + ".txt")
        new_model, new_results = ja.BW().fit(training_set, initial_model=initial_model,nb_states=initial_model.nb_states, pp=0,verbose=2, return_data=True)
        print(new_results)
        file.write(str(i)+ ',' + 
                   str(new_results['learning_rounds'])+ ',' + 
                   str(new_results['learning_time']) + ','+ 
                   str(new_results['training_set_loglikelihood']) + ',' + 
                   str([val for _, val in new_results['additional_info']]) + '\n'
                   )
        new_model = ja.stormpyModeltoJajapy(h=new_model)
        new_model.save(file_path="experiments/results/" + model_name + "_jajapy_run" + str(i) + ".txt")
    file.close()

run_experiment("oscillators1")
run_experiment("oscillators2")
run_experiment("oscillators3")
run_experiment("leader_sync")
run_experiment("brp")
run_experiment("crowds")
