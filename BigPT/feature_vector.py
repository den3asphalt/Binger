import sys
import json
import pymongo
import unicodedata


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
db=myclient["codetrans"]
lang_collection=["Python3","Java8","CPP14","JavaScript"]
for s_lang in lang_collection:
	lang_collection_tmp=lang_collection.remove("s_lang")
	for t_lang in lang_collection_tmp:
		f1=open(t_lang+"_"+s_lang+"_pt.json","r")
		pathtypelist=json.load(f1)
		f1.close()

		f2=open(t_lang+"_"+s_lang+"_tk.json","r")
		pathtokenlist=json.load(f2)
		f2.close()

		pathtypelist_len=len(pathtypelist)
		vec_len=pathtypelist_len+len(pathtokenlist)

		ele_sta=[0]*vec_len
		prog_sta=0
		
		mydb=db[s_lang][t_lang]
		for i in mydb.find():
			prog_sta+=0
			feature_vec=[0]*vec_len
			prog_id=i["_id"]
			prog_feature=i["feature"]
			for key,value in prog_feature.items():
				feature_vec[pathtypelist.index(key)]=value[0]
				ele_sta[pathtypelist.index(key)]+=1
				for j in range(len(value[3])):
					token=value[3][j]
					token_num=value[2][j]
					feature_vec[j+pathtypelist_len]=token_num
					ele_sta[j+pathtypelist_len]+=1
			
			newvalues = { "$set": { "feature_vector": feature_vec } }
			mydb.update_one({"_id": prog_id}, newvalues)
		
		for x in range(len(ele_sta)):
			if ele_sta[x]/prog_sta < 0.1: # rarity threshold
				ele_sta[x]=1
			else:
				ele_sta[x]=0
		
		f3=open(t_lang+"_"+s_lang+"_rarity.json","w")
		json.dump(ele_sta,f3)
		f3.close()