import sys
import pymongo
import random
import os
import math

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
db=myclient["codetrans"]

f1=open(t_lang+"_"+s_lang+"_pt.json","r")
pathtypelist=json.load(f1)
f1.close()
pathtypelist_len=len(pathtypelist)

lang_collection=["Python3","Java8","CPP14","JavaScript"]
for s_lang in lang_collection:
	lang_collection_tmp=lang_collection.remove("s_lang")
	for t_lang in lang_collection_tmp:	
		f1=open(t_lang+"_"+s_lang+"_rarity.json","r")
		ele_sta=json.load(f1)
		f1.close()
		mydb=db[s_lang][t_lang]
		for i in mydb.find():
			prog_id=i["_id"]
			vt=0
			feature_vec=i["feature_vector"]
			total_num=len(feature_vec)
			nonzero_num=0
			rarity=0
			vt+=random.randint(0,1)
			for j in range(total_num):
				if feature_vec[j] != 0:
					nonzero_num+=1
					if rarity == 0 :
						if ele_sta[j] == 1:
							rarity = 1
							vt+=1
						
			coverage=nonzero_num/total_num
			if coverage > 0.5:
				vt+=1
			
			path_list_new=[]
			pathnum_list_new=[]
			model=load_model("./model/"+t_lang+"_"+lang+".h5")
			feature_vec_new = model.predict_classes(feature_vec)
			
			for i in range(pathtypelist_len):
				if feature_vec_new[i] != 0:
					path_list_new.append(pathtypelist[i])
					pathnum_list_new.append(feature_vec_new[i])
			
			pathtoken_list_new=[[]]*len(path_list_new)	
			for j in range(pathtypelist_len,total_num):
				if feature_vec_new[j] != 0:
					cur_token=pathtokenlist[j-pathtypelist_len].split(' ')
					pathtoken_list_new[path_list_new.index(cur_token[0])].append([cur_token[1]]*feature_vec_new[j]))

			f1=open("./node/path.json","w")
			f2=open("./node/pathnmn.json","w")
			f3=open("./node/pathtokenn.json","w")
			json.dump(path_list_new,f1)
			json.dump(pathnum_list_new,f2)
			f3.write(str(pathtoken_list_new))
			f1.close()
			f2.close()
			f3.close()
			
			os.system("python3 retrieval.py "+s_lang+" "+t_lang)
			f=open("./max.txt","r")
			candidate=f.readlines()
			if candidate[1] > 0.75:
				vt+=1
			f.close()

			a=vt/4
			b=(4-vt)/4
			ve=-1*a*math.log(a,10)-b*math.log(b,10)
			newvalues = { "$set": { "ve": ve } }
			mydb.update_one({"_id": prog_id}, newvalues)

				
			
			