from keras.layers import Input, Dense
from keras.models import Model, load_model, Sequential
import numpy as np
import pymongo

#train autoencoder
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
db=myclient["codetrans"]
lang_collection=["Python3","Java8","CPP14","JavaScript"]
for s_lang in lang_collection:
	lang_collection_tmp=lang_collection.remove("s_lang")
	for t_lang in lang_collection_tmp:
		mydb=db[s_lang][t_lang]
		x=[]
		size=0
		for i in mydb.find():
			x.append(i["feature_vector"])
			size+=1
		split_size=int(size*0.8)
		vec_size=len(x[0])
		x_train=np.array(x[:split_size])
		x_test=np.array(x[split_size:])
		
		# construct model
		encoding_dim = 3000

		input_prog = Input(shape=(vec_size,))
		encoded = Dense(encoding_dim, activation='relu')(input_prog)
		decoded = Dense(vec_size, activation='sigmoid')(encoded)

		autoencoder = Model(input=input_prog, output=decoded)

		encoder = Model(input=input_prog, output=encoded)

		encoded_input = Input(shape=(encoding_dim,))
		decoder_layer = autoencoder.layers[-1]
		decoder = Model(input=encoded_input, output=decoder_layer(encoded_input))
		
		autoencoder.fit(x_train, x_train,
				nb_epoch=50,
				batch_size=256,
				shuffle=True,
				validation_data=(x_test, x_test))
		
		encoder.save("./model/"+t_lang+"_"+s_lang+"_encoder.h5")
		decoder.save("./model/"+t_lang+"_"+s_lang+"_decoder.h5")

#build qtm		
lang_collection=["Python3","Java8","CPP14","JavaScript"]
for s_lang in lang_collection:
	lang_collection_tmp=lang_collection.remove("s_lang")
	for t_lang in lang_collection_tmp:
	
		encoder=load_model("./model/"+t_lang+"_"+s_lang+"_encoder.h5")
		decoder=load_model("./model/"+s_lang+"_"+t_lang+"_decoder.h5")
		
		model = Sequential()
		model.add(encode.layers[-1])
		model.add(decode.layers[-1])
		model.save("./model/"+t_lang+"_"+s_lang+".h5")
