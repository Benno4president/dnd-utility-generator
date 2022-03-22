# uses second virtural environment (lmenv) for testing.
import os, sys
import time
import glob
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers.experimental import preprocessing


EPOCHS = 50
OUTPUT_LENGTH = 5000
MODEL_TEMPERATURE = 1.0
BATCH_SIZE = 64
BUFFER_SIZE = 10000
EMBEDDING_DIM = 256
RNN_UNITS = 1024
START_STRING = 'Dungeons & Dragons\n'


text = ''
for fp in glob.iglob('data/*.txt'):
    # Read in the text:
    print(fp)
    with open(fp, 'r') as f:
        text += f'{f.read()}\n\n'

# Count the unique characters in the file
vocabulary = sorted(set(text))

# Vectorize text
example_texts = ['abcdefg', 'xyz']
chars = tf.strings.unicode_split(example_texts, input_encoding='UTF-8')

# Create the StringLookup layer.
ids_from_chars = preprocessing.StringLookup(vocabulary=list(vocabulary))
ids = ids_from_chars(chars)


chars_from_ids = preprocessing.StringLookup(
    vocabulary=ids_from_chars.get_vocabulary(),
    invert=True
)

class Gru_Model(tf.keras.Model):
    def __init__(self, vocabulary_size, embedding_dim, rnn_units):
        super().__init__(self)
        self.embedding = tf.keras.layers.Embedding(vocabulary_size, embedding_dim)
        self.gru = tf.keras.layers.GRU(rnn_units, return_sequences=True, return_state=True)
        self.dense = tf.keras.layers.Dense(vocabulary_size)

    def call(self, inputs, states=None, return_state=False, training=False):
        i = inputs
        i = self.embedding(i, training=training)
        if states is None:
            states = self.gru.get_initial_state(i)
        i, states = self.gru(i, initial_state=states, training=training)
        i = self.dense(i, training=training)

        if return_state:
            return i, states
        else:
            return i

if 't' in sys.argv:
    # This layer recovers characters from the vectors of IDs and returns them as a RaggedTensor of characters:
    chars = chars_from_ids(ids)

    # Join the characters back into strings. 
    tf.strings.reduce_join(chars, axis=-1).numpy()


    all_ids = ids_from_chars(tf.strings.unicode_split(text, 'UTF-8'))

    # Convert the text vector into a stream of indices.
    ids_dataset = tf.data.Dataset.from_tensor_slices(all_ids)

    sequence_length = 100
    examples_per_epoch = len(text) // (sequence_length + 1)

    # Convert these individual characters to sequences of the desired size.
    sequences = ids_dataset.batch(sequence_length + 1, drop_remainder=True)


    # Takes a sequence as input, duplicates, and shifts it to align the input and label for each timestep:
    def split_input_target(sequence):
        input_text = sequence[:-1]
        target_text = sequence[1:]
        return input_text, target_text

    dataset = sequences.map(split_input_target)


    dataset = (
        dataset
        .shuffle(BUFFER_SIZE)
        .batch(BATCH_SIZE, drop_remainder=True)
        .prefetch(tf.data.experimental.AUTOTUNE)
    )


    model = Gru_Model(len(ids_from_chars.get_vocabulary()), EMBEDDING_DIM, RNN_UNITS)


    for input_example_batch, target_example_batch in dataset.take(1):
        example_batch_predictions = model(input_example_batch)
        print(example_batch_predictions.shape, "# (batch_size, sequence_length, vocab_size)")

    model.summary()

    # Gives us a prediction of the next character index at each timestep
    sampled_indices = tf.random.categorical(example_batch_predictions[0], num_samples=1)
    sampled_indices = tf.squeeze(sampled_indices, axis=-1).numpy()

    loss = tf.losses.SparseCategoricalCrossentropy(from_logits=True)
    example_batch_loss = loss(target_example_batch, example_batch_predictions)
    mean_loss = example_batch_loss.numpy().mean()
    print("Prediction shape: ", example_batch_predictions.shape, " # (batch_size, sequence_length, vocab_size)")
    print("Mean loss:        ", mean_loss)

    # Configure the training procedure.
    model.compile(optimizer='adam', loss=loss)

    history = model.fit(dataset, epochs=EPOCHS)
    model.save('model')
    print('Model saved')
    exit()



class OneStep(tf.keras.Model):
  def __init__(self, model, chars_from_ids, ids_from_chars, temperature):
    super().__init__()
    self.temperature = temperature
    self.model = model
    self.chars_from_ids = chars_from_ids
    self.ids_from_chars = ids_from_chars

    # Create a mask to prevent "" or "[UNK]" from being generated.
    skip_ids = self.ids_from_chars(['', '[UNK]'])[:, None]
    sparse_mask = tf.SparseTensor(
        values=[-float('inf')] * len(skip_ids),  # Put a -inf at each bad index.
        indices=skip_ids,
        dense_shape=[len(ids_from_chars.get_vocabulary())]  # Match the shape to the vocabulary
    )
    self.prediction_mask = tf.sparse.to_dense(sparse_mask, validate_indices=False)

  @tf.function
  def generate_one_step(self, inputs, states=None):
    # Convert strings to token IDs.
    input_chars = tf.strings.unicode_split(inputs, 'UTF-8')
    input_ids = self.ids_from_chars(input_chars).to_tensor()

    # Run the model.
    # predicted_logits.shape is [batch, char, next_char_logits]
    predicted_logits, states = self.model(
        inputs=input_ids,
        states=states,
        return_state=True,
    )
    # Only use the last prediction.
    predicted_logits = predicted_logits[:, -1, :]
    predicted_logits = predicted_logits / self.temperature
    # Apply the prediction mask: prevent "" or "[UNK]" from being generated.
    predicted_logits = predicted_logits + self.prediction_mask

    # Sample the output logits to generate token IDs.
    predicted_ids = tf.random.categorical(predicted_logits, num_samples=1)
    predicted_ids = tf.squeeze(predicted_ids, axis=-1)

    # Convert from token ids to characters
    predicted_chars = self.chars_from_ids(predicted_ids)

    # Return the characters and model state.
    return predicted_chars, states

model = keras.models.load_model('model', custom_objects={'gru_model':Gru_Model})
one_step_model = OneStep(model, chars_from_ids, ids_from_chars, MODEL_TEMPERATURE)

start = time.time()
states = None
next_char = tf.constant([START_STRING])
result = [next_char]

# Generate text with the model.
for n in range(OUTPUT_LENGTH):
    next_char, states = one_step_model.generate_one_step(next_char, states=states)
    result.append(next_char)

result = tf.strings.join(result)
end = time.time()
print(result[0].numpy().decode('utf-8'))

