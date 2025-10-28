import numpy as np

class NN():
    def __init__(self, sizes):
        self.weights = []
        self.baiases = []
        self.outputs = []
        self.sizes = sizes
        self.size = len(self.sizes) - 1
        self.acts = lambda x: x if x > 0 else 0
        self.act = np.vectorize(self.acts)

        self.outputs.append(np.zeros(self.sizes[0]))
        for i in range(self.size):
            self.weights.append(np.random.randn(self.sizes[i], self.sizes[i + 1]) - 0.5)
            self.baiases.append(np.zeros(self.sizes[i + 1]))
            self.outputs.append(np.zeros(self.sizes[i + 1]))

    def feed(self, inputs):
        self.outputs[0] = inputs
        for i in range(self.size):
            self.outputs[i + 1] = self.act(np.dot(self.outputs[i], self.weights[i]) + self.baiases[i])
        return self.outputs[-1]


