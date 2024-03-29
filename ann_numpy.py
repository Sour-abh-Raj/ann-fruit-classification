import numpy
import pickle

NUM_OF_ITERATIONS = 10
LEARNING_RATE = 0.01

def sigmoid(inpt):
    return 1.0 / (1 + numpy.exp(-1 * inpt))

def relu(inpt):
    result = inpt
    result[inpt < 0] = 0
    return result

def update_weights(weights, learning_rate):
    new_weights = []
    for weight_matrix in weights:
        new_weight_matrix = weight_matrix - learning_rate * weight_matrix
        # print("Updated weight matrix : ", new_weight_matrix)
        new_weights.append(new_weight_matrix)
    return new_weights


# def update_weights(weights, learning_rate):
#     print(weights)
#     new_weights = weights - learning_rate * weights
#     return new_weights

def train_network(num_iterations, weights, data_inputs, data_outputs, learning_rate, activation="relu"):
    for iteration in range(num_iterations):
        print("Itreation ", iteration)
        for sample_idx in range(data_inputs.shape[0]):
            r1 = data_inputs[sample_idx, :]
            for idx in range(len(weights) - 1):
                curr_weights = weights[idx]
                r1 = numpy.matmul(r1, curr_weights)
                if activation == "relu":
                    r1 = relu(r1)
                elif activation == "sigmoid":
                    r1 = sigmoid(r1)
            curr_weights = weights[-1]
            r1 = numpy.matmul(r1, curr_weights)
            predicted_label = numpy.where(r1 == numpy.max(r1))[0][0]
            desired_label = data_outputs[sample_idx]
            if predicted_label != desired_label:
                weights = update_weights(weights,
                                         learning_rate=0.001)
    return weights

def predict_outputs(weights, data_inputs, activation="relu"):
    predictions = numpy.zeros(shape=(data_inputs.shape[0]))
    for sample_idx in range(data_inputs.shape[0]):
        r1 = data_inputs[sample_idx, :]
        for curr_weights in weights:
            r1 = numpy.matmul(r1, curr_weights)
            if activation == "relu":
                r1 = relu(r1)
            elif activation == "sigmoid":
                r1 = sigmoid(r1)
        predicted_label = numpy.where(r1 == numpy.max(r1))[0][0]
        predictions[sample_idx] = predicted_label
    return predictions

def test_ann(weights, data_inputs):
    predictions = predict_outputs(weights, data_inputs)
    correct_predictions = numpy.where(predictions == data_outputs)[0]
    print("Correct Predictions ", correct_predictions.size)
    failed_predictions = numpy.where(predictions != data_outputs)[0]
    print("Failed Predictions ", failed_predictions.size)
    accuracy = (failed_predictions.size / (correct_predictions.size + failed_predictions.size)) * 100
    return accuracy

f = open("dataset_features.pkl", "rb")
data_inputs2 = pickle.load(f)
f.close()

features_STDs = numpy.std(a=data_inputs2, axis=0)
data_inputs = data_inputs2[:, features_STDs > 50]

f = open("outputs.pkl", "rb")
data_outputs = pickle.load(f)
f.close()

HL1_neurons = 150
HL2_neurons = 60
output_neurons = 4

input_HL1_weights = numpy.random.uniform(low=-0.1, high=0.1, size=(data_inputs.shape[1], HL1_neurons))
HL1_HL2_weights = numpy.random.uniform(low=-0.1, high=0.1, size=(HL1_neurons, HL2_neurons))
HL2_output_weights = numpy.random.uniform(low=-0.1, high=0.1, size=(HL2_neurons, output_neurons))

weights = [input_HL1_weights, HL1_HL2_weights, HL2_output_weights]


# HL1_neurons = 150
# input_HL1_weights = numpy.random.uniform(low=-0.1, high=0.1,
#                                          size=(data_inputs.shape[1], HL1_neurons))
# HL2_neurons = 60
# HL1_HL2_weights = numpy.random.uniform(low=-0.1, high=0.1,
#                                        size=(HL1_neurons, HL2_neurons))
# output_neurons = 4
# HL2_output_weights = numpy.random.uniform(low=-0.1, high=0.1,
#                                           size=(HL2_neurons, output_neurons))

# weights = numpy.array([input_HL1_weights,
#                        HL1_HL2_weights,
#                        HL2_output_weights])

weights = train_network(num_iterations=NUM_OF_ITERATIONS,
                        weights=weights,
                        data_inputs=data_inputs,
                        data_outputs=data_outputs,
                        learning_rate=LEARNING_RATE,
                        activation="relu")

accuracy = test_ann(weights=weights, data_inputs=data_inputs)

print("Accuracy : ", accuracy)


