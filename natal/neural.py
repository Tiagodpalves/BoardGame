import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np

# 1. Dataset: Exemplos de desafios engraçados
data = [
    "Beba tudo e imite um pato depois.",
    "Fale algo que rime ou beba dois goles.",
    "Faça uma careta sem piscar por 10 segundos.",
    "Grite 'Sou o rei das bebidas!' antes de beber.",
    "Imite um animal até alguém acertar.",
    "Troque seu copo com o vizinho por um turno.",
    "Fale 'eu nunca' sem rir. Se rir, beba!",
    "Dance algo inédito por 15 segundos.",
    "Conte uma piada engraçada ou beba dois goles.",
    "Cante como um galo por 10 segundos sem parar.",
    "Faça uma pose engraçada na frente do espelho.",
    "Recite 3 fatos aleatórios sobre você."
]

# Garantir UTF-8 na entrada de texto
data = [text.encode("utf-8").decode("utf-8") for text in data]

# 2. Pré-processamento dos dados
tokenizer = Tokenizer(filters='', lower=False)
tokenizer.fit_on_texts(data)
total_words = len(tokenizer.word_index) + 1

# Gerar sequências de treinamento
input_sequences = []
for line in data:
    token_list = tokenizer.texts_to_sequences([line])[0]
    for i in range(1, len(token_list)):
        n_gram_sequence = token_list[:i + 1]
        input_sequences.append(n_gram_sequence)

# Padronizar o comprimento das sequências
max_sequence_len = max(len(x) for x in input_sequences)
input_sequences = pad_sequences(input_sequences, maxlen=max_sequence_len, padding='pre')

# Separar entradas (X) e saídas (y)
X = input_sequences[:, :-1]
y = input_sequences[:, -1]
y = tf.keras.utils.to_categorical(y, num_classes=total_words)

# 3. Modelo da rede neural aprimorado
model = Sequential([
    Embedding(total_words, 128, input_length=max_sequence_len - 1),
    LSTM(256, return_sequences=True),
    Dropout(0.2),
    LSTM(256),
    Dropout(0.2),
    Dense(128, activation='relu'),
    Dense(total_words, activation='softmax')
])

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
print(model.summary())

# 4. Treinamento
model.fit(X, y, epochs=50, verbose=1)

# 5. Função para gerar novas descrições de desafios
def generate_description(seed_text, max_words=50, temperature=0.8):
    generated_text = seed_text
    generated_words = set()  # Conjunto para rastrear palavras já geradas

    for _ in range(max_words):
        token_list = tokenizer.texts_to_sequences([generated_text])[0]
        token_list = pad_sequences([token_list], maxlen=max_sequence_len - 1, padding='pre')
        predictions = model.predict(token_list, verbose=0)[0]

        # Ajustar distribuição com temperatura
        predictions = np.log(predictions + 1e-9) / temperature
        predictions = np.exp(predictions)
        predictions = predictions / np.sum(predictions)

        # Filtrar palavras já geradas
        for word_idx in generated_words:
            predictions[word_idx] = 0  # Zera a probabilidade de palavras já usadas

        # Re-normalizar após filtrar
        predictions = predictions / np.sum(predictions)

        # Escolher a próxima palavra
        predicted_id = np.random.choice(len(predictions), p=predictions)

        # Encerrar se nenhuma palavra for prevista
        if predicted_id == 0:
            break

        output_word = tokenizer.index_word[predicted_id]
        generated_text += " " + output_word
        generated_words.add(predicted_id)  # Adiciona a palavra ao conjunto de palavras geradas

    return generated_text.strip()


# 6. Testando a geração
seed_texts = ["Beba", "Fale", "Faça", "Grite"]
for seed in seed_texts:
    description = generate_description(seed, temperature=0.8)
    print(f"Descrição Gerada: {description}\n")
