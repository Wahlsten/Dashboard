import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
from transformers import AutoTokenizer
import pickle
import numpy as np
import pandas as pd

seq_length  = 20  # Adjusted for dataset consistency

def InitializeModel(seq_length, d_model, num_heads, num_classes, num_layers):

    # Input Layer
    inputs = tf.keras.Input(shape=(seq_length,))  # Input shape matches tokenized sequences
    
    # Embedding Layer
    embedding_layer = tf.keras.layers.Embedding(input_dim=10000, output_dim=d_model, input_length=seq_length)
    x = embedding_layer(inputs)  # Convert integer sequences to embeddings
    
    # Add Positional Encoding
    x += positional_encoding(seq_length, d_model)
    
    # Transformer Encoder Layers
    for _ in range(num_layers):
        # Multi-Head Attention
        attn_output = tf.keras.layers.MultiHeadAttention(num_heads=num_heads, key_dim=d_model)(x, x, x)
        x = tf.keras.layers.Add()([x, attn_output])  # Residual connection
        x = tf.keras.layers.LayerNormalization(epsilon=1e-6)(x)
    
        # Feed-Forward Network
        ffn = tf.keras.Sequential([
            tf.keras.layers.Dense(4 * d_model, activation="relu"),
            tf.keras.layers.Dense(d_model)
        ])
        ffn_output = ffn(x)
        x = tf.keras.layers.Add()([x, ffn_output])  # Residual connection
        x = tf.keras.layers.LayerNormalization(epsilon=1e-6)(x)
    
    # Classification Head
    x = tf.keras.layers.GlobalAveragePooling1D()(x)
    outputs = tf.keras.layers.Dense(num_classes, activation="softmax")(x)
    
    # Define Model
    model = tf.keras.Model(inputs=inputs, outputs=outputs)
    
    # Compile Model
    model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    
    # Summary of the Model
    model.summary()
    
    return model

def positional_encoding(seq_length, d_model):

    angle_rads = np.arange(seq_length)[:, np.newaxis] / np.power(
        10000, (2 * (np.arange(d_model)[np.newaxis, :] // 2)) / np.float32(d_model)
    )
    angle_rads[:, 0::2] = np.sin(angle_rads[:, 0::2])  # Apply sin to even indices
    angle_rads[:, 1::2] = np.cos(angle_rads[:, 1::2])  # Apply cos to odd indices
    pos_encoding = angle_rads[np.newaxis, :, :]  # Shape: (1, seq_length, d_model)

    return tf.cast(pos_encoding, dtype=tf.float32)

def PreTokenize(seq):

    auto_tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
    tokens = [auto_tokenizer.tokenize(s) for s in seq]

    return tokens

def InitializeTokenizer(seq):

    tokens = PreTokenize(seq)

    tokenizer = Tokenizer(num_words=10000)  # Define max vocabulary size
    tokenizer.fit_on_texts(tokens)

    # Save tokenizer to a file
    with open('tokenizer.pickle', 'wb') as handle:
        pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

def GetTokenizer():

    # Load tokenizer from the file
    with open('tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

    return tokenizer

def Tokenize(seq):

    tokenizer = GetTokenizer()
    tokens    = PreTokenize(seq)
    sequences = tokenizer.texts_to_sequences(tokens)
    padded_sequences = pad_sequences(sequences, maxlen=seq_length, padding="post")

    return padded_sequences

def LoadTransformer():
    
    load_file_name = r'C:\Users\Quake\OneDrive\Dokument\Coding\Python\Other\Dashboard\saved_model\budget_transformer_model.keras'
    loaded_model   = load_model(load_file_name)

    return loaded_model

def PredictCategory(model, seq):

    mapping = {
        'Inkomst': 1, 'Hyra': 2, 'Mat': 3, 'Ovrig': 4,
        'Ovrig fast': 5, 'Transport': 6, 'RAnta': 7,
        'Amortering': 8, 'KlAder': 0
    }
    
    predicted_output = model.predict(seq)
    predicted_class = np.argmax(predicted_output, axis=-1)  # Get the class index
    
    # Step 3: Map the predicted class to the category
    reverse_mapping = {v: k for k, v in mapping.items()}  # Reverse the mapping dictionary
    predicted_category = [reverse_mapping[k] for k in predicted_class]  # Get the human-readable category
    
    return predicted_category

if __name__ == '__main__':

    # Input Parameters
    d_model     = 8      # Dimension of the model
    num_heads   = 2    # Number of attention heads
    num_classes = 9  # Number of output classes
    num_layers  = 2   # Number of Transformer encoder layers
    
    model = InitializeModel(seq_length, d_model, num_heads, num_classes, num_layers)

    # File Path
    ouput_file_name = r'C:\Users\Quake\OneDrive\Dokument\Coding\Python\Other\Dashboard\BudgetCSVBackup.csv'
    
    # Load Data
    df = pd.read_csv(ouput_file_name, encoding='cp1252', sep=',')
    
    # Map categories to integers
    mapping = {
        'Inkomst': 1, 'Hyra': 2, 'Mat': 3, 'Ovrig': 4,
        'Ovrig fast': 5, 'Transport': 6, 'RAnta': 7,
        'Amortering': 8, 'KlAder': 0
    }
    
    y_train = df['category'].map(mapping).to_numpy()

    df = df.map(lambda x: x.replace(' ', '') if isinstance(x, str) else x)

    X_train = df['description'].astype(str).to_numpy()
    
    # Initialize tokenizer
    InitializeTokenizer(X_train)

    # Tokenization
    padded_sequences = Tokenize(X_train)
    
    # Train the Model
    model.fit(padded_sequences, y_train, epochs=30)
    
    #df['description2'] = predicted_category
    #df.to_csv(ouput2_file_name, mode='w', index=False, header=True)
    save_file = r'C:\Users\Quake\OneDrive\Dokument\Coding\Python\Other\Dashboard\saved_model\budget_transformer_model.keras'

    model.save(save_file)
