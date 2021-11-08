from keras.models import Model, load_model, Sequential
from keras.optimizers import SGD
from keras.losses import categorical_crossentropy
from keras.optimizers import Adam
import numpy as np
import sys

def load_data(datapath):
	data = np.load(datapath)
	X, Y = data["X"], data["Y"]
    print('X_shape:{}\nY_shape:{}'.format(X.shape, Y.shape))
    return X, Y

if __name__ == '__main__':
	lang_collection=["Python3","Java8","CPP14","JavaScript"]
	s_lang=sys.argv[1]
	t_lang=sys.argv[2]
	for s_lang in lang_collection:
		lang_collection_tmp=lang_collection.remove("s_lang")
		for t_lang in lang_collection_tmp:
			datapath="./labeled_data/"+t_lang+"_"+s_lang+".npz"
			X_train, Y_train = load_data(datapath)
			
			model=load_model("./model/"+t_lang+"_"+s_lang+".h5")
			
			sgd = SGD(lr=0.001, decay=1e-6, momentum=0, nesterov=True)

			model.compile(loss=categorical_crossentropy, optimizer=Adam(), metrics=['accuracy'])
			model.summary()
			
			history = model.fit(X_train, Y_train, batch_size=2, epochs=10,
							validation_data=(X_test, Y_test), verbose=1, shuffle=True)
			
			model.save("./model/"+t_lang+"_"+s_lang+".h5")
