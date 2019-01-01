import numpy as np
from utils import *
from RNN import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-e', '--epochs',
    type=int,
    default=10000,
    help='The number of epochs')

parser.add_argument('-lr', '--learning-rate',
    type=float,
    default=0.01,
    help='The number of epochs')

FLAGS, unparsed = parser.parse_known_args()


# Read the dataset
data = open('./dataset/dinosaurs.txt', 'r').read()
data = data.lower()
chars = list(set(data))
data_size, vocab_size = len(data), len(chars)
print ('There are %d total characters and %d unique characters in your data' % (data_size, vocab_size))

# Create the int2char and char2int dictionaries
char2int = {ch : i for i, ch in enumerate(chars)}
int2char = {i : ch for i, ch in enumerate(chars)}
print ('Integer to Character Mapping: ')
print (int2char)

# Initialize RNN
n_a = 50 # Number of RNN units
rnn = RNN(n_a, vocab_size, vocab_size, FLAGS.learning_rate)

# Sample Length
sample_length = 7

# Initialize Loss
loss = 0
loss = get_initial_loss(vocab_size, sample_length)

# Build list of all dinosaurs
with open('dataset/dinosaurs.txt', 'r') as f:
    dinos = f.readlines()
dinos = [dino.lower().strip() for dino in dinos]

# Initialize the hidden state
a_prev = np.zeros((n_a, 1))

# Optimization Loop
for i in range(1, FLAGS.epochs):
    # Create a training example
    idx = i % len(dinos)
    X = [None] + [char2int[ch] for ch in dinos[idx]]
    Y = X[1:] + [char2int['\n']]

    # Perform one optimization step
    curr_loss, gradients, a_prev = rnn.optimize(X, Y, a_prev)

    # Latency trick to keep the loss smooth
    loss = smooth_loss(loss, curr_loss)

    # Every n iterations generate samples
    if i % 2000 == 0:
        print ('Iteration: %d, Loss: %f' % (i, loss) + '\n')

        # Sample dino names
        parameters = rnn.get_weights()
        for name in range(sample_length):
            sampled_indices = sample(parameters, char2int)
            print_sample(sampled_indices, int2char)

        print ('\n')

# Save the weights
rnn.save_weights()
