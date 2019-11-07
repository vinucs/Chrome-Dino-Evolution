class Player:

    def __init__(self, dino, id_pop, sprite_time):
        self.dinosaur = dino
        self.id_population = id_pop
        self.sprite_time = sprite_time
        self.game_over = False

    def createNeuralNetwork(self, input_num, hidden_num, output_num):
        self.input_layer = Layer(input_num, input_num*hidden_num, hidden_num)
        self.hidden_layer = Layer(hidden_num, hidden_num*output_num, output_num)
        self.output_layer = Layer(output_num, 0, 0)

    def setNeuralNetworkWeights(self, weights):
        self.input_layer.setWeights(weights[:self.input_layer.numberOfConnections()])
        self.hidden_layer.setWeights(weights[self.input_layer.numberOfConnections():])

    def setBias(self, bias):
        self.bias = bias

    def updateInputValues(self, input_values):
        input_values.append(self.bias)
        self.input_layer.setValues(input_values)
    
    def calculateSigmoid(self, value):
        return (value)/(1 + abs(value))

    def makeDecision(self):
        decision = []
        for i in range (self.output_layer.number_of_neurons):
            hidden_sum = 0
            for j in range (self.hidden_layer.number_of_neurons):
                input_sum = 0
                for k in range (self.input_layer.number_of_neurons):
                    input_sum += (self.input_layer.neurons[k].weights[j] *self.input_layer.neurons[k].value)
                self.hidden_layer.neurons[j].value = input_sum
                # self.hidden_layer.neurons[j].value = self.calculateSigmoid(input_sum)
                hidden_sum += (self.hidden_layer.neurons[j].weights[i] *self.hidden_layer.neurons[j].value)
            # self.output_layer.neurons[i].value = self.calculateSigmoid(hidden_sum)
            self.output_layer.neurons[i].value = hidden_sum
            decision.append(self.output_layer.neurons[i].value)
        decision_made = decision.index(max(decision))
        if decision_made == 0:
            self.dinosaur.isJumping()
        elif decision_made == 1:
            self.dinosaur.isCrouch()
        elif decision_made == 2:
            self.dinosaur.isWalking()

    def setPlayerFitness(self, fitness):
        if self.game_over == False:
            self.fitness = fitness

    def getPlayerFitness(self):
        return self.fitness

    def gameOver(self):
        self.game_over = True

class Neuron:
    def __init__(self, connections):
        self.connections = connections
    
    def setNeuronWeights(self, weights):
        self.weights = weights
    
    def setNeuronValue(self, value):
        self.value = value

class Layer:
    def __init__(self, num_neurons, layer_connections, neuron_connections):
        self.number_of_neurons = num_neurons
        self.layer_connections = layer_connections
        self.neuron_connections = neuron_connections
        self.neurons = []
        for i in range(self.number_of_neurons):
            self.neurons.append(Neuron(self.neuron_connections))

    def numberOfConnections(self):
        return self.layer_connections

    def setWeights(self, weights):
        aux = 0
        for i in range(self.number_of_neurons):
            self.neurons[i].setNeuronWeights(weights[aux:(aux+self.neuron_connections)])
            aux += self.neuron_connections
    
    def setValues(self, values):
        for i in range(self.number_of_neurons):
            self.neurons[i].setNeuronValue(values[i])

    def getValues(self):
        values = []
        for i in range(self.number_of_neurons):
            values.append(neurons[i].getValue)


