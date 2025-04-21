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

def BuildStateLabeling(h):
	state_labelling = stormpy.storage.StateLabeling(h.nb_states)
	for o in h.getAlphabet():
		state_labelling.add_label(o)
	for s in range(h.nb_states):
		state_labelling.add_label_to_state(h.labelling[s],s)
	return state_labelling    

def calculate_props(model_name):
    #STEP 1: load stormpy model
    if model_name == "leader_sync":
        prism_model = stormpy.parse_prism_program("experiments/original-models/dtmc/leader_sync.4-3.v1.prism")
        props = ['"eventually_elected": P>=1 [ F "elected" ]', 'R{"num_rounds"}=? [ F "elected" ]']
    elif model_name == "brp":
        prism_model = stormpy.parse_prism_program("experiments/original-models/dtmc/brp.v1.prism")
        props = ['"p1": P=? [ F s=5 ]', '"p2": P=? [ F s=5 & srep=2 ]', '"p4": P=? [ F !(srep=0) & !recv ]']
    elif model_name == "crowds":
        prism_model = stormpy.parse_prism_program("experiments/original-models/dtmc/crowds.v1.prism")
        props = ['"positive": P=? [ F observe0>1  ]']
    elif model_name == "oscillators1":
        prism_model = stormpy.parse_prism_program("experiments/original-models/dtmc/oscillators.3-6-0.1-1.v1.prism")
        props = ['"time_to_synch": R{"time_to_synch"}=?[F order_parameter >= lambda]', '"power_consumption": R{"power_consumption"}=?[F order_parameter >= lambda]']	
    elif model_name == "oscillators2":
        prism_model = stormpy.parse_prism_program("experiments/original-models/dtmc/oscillators.6-6-0.1-1.v1.prism")
        props = ['"time_to_synch": R{"time_to_synch"}=?[F order_parameter >= lambda]', '"power_consumption": R{"power_consumption"}=?[F order_parameter >= lambda]']	
    elif model_name == "oscillators3":
        prism_model = stormpy.parse_prism_program("experiments/original-models/dtmc/oscillators.6-8-0.1-1.v1.prism")
        props = ['"time_to_synch": R{"time_to_synch"}=?[F order_parameter >= lambda]', '"power_consumption": R{"power_consumption"}=?[F order_parameter >= lambda]']	
    else:
        raise ValueError("Unknown model name: " + model_name)
    
    stormpy_model = stormpy.build_model(prism_model)

    #STEP 2: pluk reward modellen ud
    print("Loading model: " + model_name)
    rewards = stormpy_model.reward_models

    #step 3: Model check på stormpy model
    original_result = []
    for prop in props:
        property = stormpy.parse_properties(prop, prism_model)
        model = stormpy.build_model(prism_model, property)
        new_result = stormpy.model_checking(model, property[0])
        print("Result for original model: " + str(new_result))
        original_result.append(str(new_result))

    #STEP 5: train
    training_set = ja.loadSet("experiments/observations/" + model_name + "_observations_jajapy.txt")
    result = []
    for i in range(10):
        initial_model = ja.loadMC("experiments/initial-models/" + model_name + "_jajapy_run" + str(i) + ".txt")
        new_model = ja.BW().fit(training_set, initial_model=initial_model,nb_states=initial_model.nb_states, pp=0,verbose=2)
        print(type(new_model))
        trained_model = ja.stormpyModeltoJajapy(h=new_model)

        state_labelling = BuildStateLabeling(trained_model)
        transition_matrix = trained_model.matrix
        transition_matrix =  stormpy.build_sparse_matrix(transition_matrix)
        components = stormpy.SparseModelComponents(transition_matrix=transition_matrix, state_labeling=state_labelling, reward_models=rewards)
        mc = stormpy.storage.SparseDtmc(components)

        for prop in props:
            property = stormpy.parse_properties(prop, prism_model)
            model = stormpy.build_model(prism_model, property)
            result_new = stormpy.model_checking(mc, property[0])
            print("Result for new model: " + str(result_new))
            result.append(str(result_new))
        
    #STEP 6: save results
    file = open("experiments/results/" + model_name + "_error_jajapy.txt", "w")
    file.write("Results for " + model_name + "\n")
    file.write("original_result: \n")
    for prop in props:
         file.write(original_result[props.index(prop)] + ",")
    file.write("\n")
    file.write("run, new_result\n")
    for i in range(10):
        for prop in props:
            file.write(str(i) + "," + result[props.index(prop)] + ",")
        file.write("\n") 
    file.close()




def test(model_name):
    #STEP 1: load stormpy model
    prism_model = stormpy.parse_prism_program("experiments/original-models/dtmc/leader_sync.4-3.v1.prism")
    #print(stormpy_model)
    stormpy_model = stormpy.build_model(prism_model)
    print(stormpy_model)
    print("done")

    #STEP 2: pluk reward modellen ud
    print(stormpy_model.reward_models)
    rewards = stormpy_model.reward_models

    #STEP 3: load ja model
    jajapy_model = ja.loadPrism("experiments/original-models/dtmc/leader_sync.4-3.v1.prism")
    #original_model = ja.jajapyModeltoStormpy(h=original_model)
    #print(original_model)
    print("done")

    #STEP 4: model check på stormpy model
    prop = 'R{"num_rounds"}=? [ F "elected" ]'
    property = stormpy.parse_properties(prop, prism_model)
    model = stormpy.build_model(prism_model, property)

    result = stormpy.model_checking(model, property[0])
    print("Result for original model: " + str(result))

    #STEP 5: lav en ny stormpy model baseret på jajapy model
    state_labelling = BuildStateLabeling(jajapy_model)
    transition_matrix = jajapy_model.matrix
    transition_matrix =  stormpy.build_sparse_matrix(transition_matrix)
    components = stormpy.SparseModelComponents(transition_matrix=transition_matrix, state_labeling=state_labelling, reward_models=rewards)
    mc = stormpy.storage.SparseDtmc(components)

    #STEP 6: lav en ny stormpy model baseret på jajapy model
    training_set = ja.loadSet("experiments/observations/" + model_name + "_observations_jajapy.txt")
    initial_model = ja.loadMC("experiments/initial-models/" + model_name + "_jajapy_run1.txt")
    new_model = ja.BW().fit(training_set, initial_model=initial_model,nb_states=initial_model.nb_states, pp=0,verbose=2)
    trained_model = ja.stormpyModeltoJajapy(h=new_model)

    state_labelling = BuildStateLabeling(trained_model)
    transition_matrix = trained_model.matrix
    transition_matrix =  stormpy.build_sparse_matrix(transition_matrix)
    components = stormpy.SparseModelComponents(transition_matrix=transition_matrix, state_labeling=state_labelling, reward_models=rewards)
    mc = stormpy.storage.SparseDtmc(components)

    #STEP 7: model check på den nye stormpy model
    prop = 'R{"num_rounds"}=? [ F "elected" ]'
    result_new = stormpy.model_checking(mc, property[0])
    print("Result for new model: " + str(result_new))


#run_experiment("oscillators1")
#run_experiment("oscillators2")
#run_experiment("oscillators3")
#run_experiment("leader_sync")
#run_experiment("brp")
#run_experiment("crowds")

#calculate_props("leader_sync")
#calculate_props("brp") DOES NOT WORK
#calculate_props("crowds") DOES NOT WORK
#calculate_props("oscillators1")
#calculate_props("oscillators2")
#calculate_props("oscillators3")

def calculate_absolute_errors(true_values, measured_values):
    if len(true_values) != len(measured_values):
        raise ValueError("Both lists must have the same length.")

    absolute_errors = [abs(t - m) for t, m in zip(true_values, measured_values)]
    return absolute_errors

def calculate_average_error(errors):
    if not errors:
        return 0
    return sum(errors) / len(errors)

# Example usage
true_values = [1.35, 1.35, 1.35, 1.35, 1.35, 1.35, 1.35, 1.35, 1.35, 1.35]
measured_values = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

# Calculate absolute errors
errors = calculate_absolute_errors(true_values, measured_values)
print("Absolute Errors:", errors)

# Calculate average absolute error
average_error = calculate_average_error(errors)
print("Average Absolute Error:", average_error)

