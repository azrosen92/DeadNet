from keras.layers import Input, Dense
from keras.models import Model
import os

def load_data():
	music_files = [file for file in os.listdir("data")]

def build_model(data_chunk_size):
	X_input = Input(shape=(data_chunk_size,))
	X = Dense(64, activation='relu')(X_input)
	X = Dense(64, activation='relu')(X)
	Y = Dense(10, activation='softmax')(X)

	model = Model(inputs=X_input, outputs=Y)
	model.compile(optimizer='rmsprop',
	              loss='categorical_crossentropy',
	              metrics=['accuracy'])
	return model

if __name__ == '__main__':
	data, labels = load_data()
	model = build_model(data.size[0])
	model.fit(data, labels)

