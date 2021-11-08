import sys
import json
from collections import Counter
from keras.models import Model, load_model

class creat_node:
	def __init__(self, pair, token_pair, pos, value, parent):
		self.pair=pair
		self.token_pair=token_pair
		self.pos=pos
		self.value=value
		self.parent=parent
		self.child=[]

def build_tree(cur_parent,cur_parent_class):
	#print(cur_parent,"\n",cur_parent_class,"\n", eval(cur_parent))
	global node_num,n1,terminal_node
	i=cur_parent_class.pos+1
	while i<list_len:
		if node_list[i]=="(":
			if node_list[i+1]=="(":
				cur_parent_class.token_pair=1
				i+=1
				continue
			elif node_list[i+1][0].isalnum() == False:
				i+=2
				cur_parent_class.token_pair=1
				continue
			else:
				cur_parent_class.pair=1
				i+=1
				node_num+=1 #num of nodes that has been processed so far
				exec("global "+"n"+str(node_num)+";"+"n"+str(node_num)+"=creat_node(0,0,i,node_list[i],cur_parent)")
				#print("n"+str(node_num)+"=creat_node(0,0,i,node_list[i],cur_parent)")
				cur_parent_temp="n"+str(node_num)
				cur_parent_class.child.append(cur_parent_temp)
				i=build_tree(cur_parent_temp,eval(cur_parent_temp))
		elif node_list[i]==")":
			if cur_parent_class.token_pair ==1:
				cur_parent_class.token_pair=0
			else:
				return i
		elif node_list[i][0].isalnum() == False:
			i+=1
			continue
		else:
			node_num+=1
			exec("global "+"n"+str(node_num)+";"+"n"+str(node_num)+"=creat_node(0,0,i,node_list[i],cur_parent)")
			cur_parent_class.child.append("n"+str(node_num))
			terminal_node.append("n"+str(node_num))	
		i+=1
	return i

def check_exist(path, list):
	for p in list:
		if p["top"]==path["top"] and ((p["end1"]==path["end1"] and p["end2"]==path["end2"]) or (p["end1"]==path["end2"] and p["end2"]==path["end1"])):
			return p
	return False

def check_literal(node):
	if ("iteral" in node) or (node == "number") or (node == "string"):
		return True
	else:
		return False
		
def tokenize(token):
	new_token=""
	for i in token:
		if i.isupper():
			new_token=new_token+" "+i
		elif i=="_":
			new_token=new_token+" "
		else:
			new_token=new_token+i
	return set(new_token.split())
	
def path_abstract(topv,end1v,end2v):
	abs_path={"top":[topv.value],"end1":[end1v.value],"end2":[end2v.value]}
	return abs_path

def is_exsit(path):
	if len(path["top"])!=0 and len(path["end1"])!=0 and len(path["end2"])!=0:
		return True
	else:
		return False
		
def token_sta(token_list):
	token=[]
	token_num=[]
	for t in token_list:
		if t in token:
			token_num[token.index(t)]+=1
		else:
			token.append(t)
			token_num.append(1)
	return token,token_num

if __name__ == '__main__':
	f=open(sys.argv[3],'r') 
	lisp_tree = f.read() 
	f.close() 
	lisp_tree = lisp_tree.replace("("," ( ").replace(")"," ) ").replace("'"," ").replace('"',' ') 
	node_list = lisp_tree.split()[1:-1] 
	list_len = len(node_list) 
	node_num=1
	ROOT=creat_node(0,0,-1,"ROOT","") 
	n1=creat_node(0,0,0,node_list[0],"ROOT") 
	terminal_node=[]
	build_tree("n1",n1) 
	
	#prune rule 2
	for x in terminal_node:
		tmp=eval(eval(x).parent)
		if len(tmp.child)>1:
			terminal_node.remove(x)		
	
	#extract path
	path_list=[]
	abs_path_list=[]
	pathnum_list=[]
	pathtoken_list=[]
	#print(len(terminal_node))
	for p in range(len(terminal_node)-1):
		for q in range(p+1,len(terminal_node)):
			x=eval(terminal_node[p]).parent
			y=eval(terminal_node[q]).parent
			px=[x]
			py=[y]
			temp_list=[]
			while True:
				if x!="ROOT":
					x=eval(x).parent
					px.append(x)
				if x!="ROOT" and (x in temp_list):
					cur_abs_path=path_abstract(eval(x),eval(px[0]),eval(py[0]))
					cp=check_exist(cur_abs_path,abs_path_list)
					if cp:
						tmp=abs_path_list.index(cp)
						pathnum_list[tmp]+=1
						pathtoken_list[tmp]=pathtoken_list[tmp]|tokenize(eval(eval(px[0]).child[0]).value)
						pathtoken_list[tmp]=pathtoken_list[tmp]|tokenize(eval(eval(py[0]).child[0]).value)
					else:
						abs_path_list.append(cur_abs_path)
						pathnum_list.append(1)
						tmp_token=set()
						tmp_token=tmp_token|tokenize(eval(eval(px[0]).child[0]).value)
						tmp_token=tmp_token|tokenize(eval(eval(py[0]).child[0]).value)						
						pathtoken_list.append(tmp_token)
					break
				else:
					temp_list.append(x)
					if y!="ROOT":
						y=eval(y).parent
						py.append(y)
					if y!="ROOT" and (y in temp_list):
						cur_abs_path=path_abstract(eval(y),eval(px[0]),eval(py[0]))
						cp=check_exist(cur_abs_path,abs_path_list)
						if cp:
							tmp=abs_path_list.index(cp)
							pathnum_list[tmp]+=1
							pathtoken_list[tmp]=pathtoken_list[tmp]|tokenize(eval(eval(px[0]).child[0]).value)
							pathtoken_list[tmp]=pathtoken_list[tmp]|tokenize(eval(eval(py[0]).child[0]).value)							
						else:
							abs_path_list.append(cur_abs_path)
							pathnum_list.append(1)
							tmp_token=set()
							tmp_token=tmp_token|tokenize(eval(eval(px[0]).child[0]).value)
							tmp_token=tmp_token|tokenize(eval(eval(py[0]).child[0]).value)						
							pathtoken_list.append(tmp_token)												
						break
					else:
						temp_list.append(y)
	
	
	lang=sys.argv[1]
	t_lang=sys.argv[2]
	f=open("./node/"+lang+".json","r") 
	node_list=json.load(f)
	f.close()

	#generalize path
	path_list=[]
	path_list_new=[]
	pathnum_list_new=[]
	for p in abs_path_list:
		p1={"top":[],"end1":[],"end2":[]}
		for i in p["top"]:
			if (i in node_list) and (t_lang in node_list[i]):
				p1["top"]=list(set(p1["top"]+node_list[i][t_lang]))
		for i in p["end1"]:
			if (i in node_list) and (t_lang in node_list[i]):
				p1["end1"]=list(set(p1["end1"]+node_list[i][t_lang]))		
		for i in p["end2"]:
			if (i in node_list) and (t_lang in node_list[i]):
				p1["end2"]=list(set(p1["end2"]+node_list[i][t_lang]))
		path_list.append(p1)
		
		
	f1=open(t_lang+"_"+s_lang+"_pt.json","r")
	pathtypelist=json.load(f1)
	f1.close()

	f2=open(t_lang+"_"+s_lang+"_tk.json","r")
	pathtokenlist=json.load(f2)
	f2.close()
	
	f3=open("./pathtype/"+t_lang+"_"+s_lang+".json","r")
	pathtype=json.load(f3)
	f3.close()

	pathtypelist_len=len(pathtypelist)
	vec_len=pathtypelist_len+len(pathtokenlist)
	feature_vec=[0]*vec_len
	
	#remove mismatched path
	ll=len(abs_path_list)
	for i in range(ll):
		cur_path=path_list[i]
		if is_exsit(cur_path):
			path={"top":cur_path["top"][0],"end1":cur_path["end1"][0],"end2":cur_path["end2"][0]}
			path1={"top":cur_path["top"][0],"end1":cur_path["end2"][0],"end2":cur_path["end1"][0]}
			if path in pathtype["path"]:
				path_name=pathtype["name"][pathtype["path"].index(path)]
			elif path1 in pathtype["path"]:
				path_name=pathtype["name"][pathtype["path"].index(path1)]
			else:
				break
			feature_vec[pathtypelist.index(path_name)]=pathnum_list[i]
			token,token_num=token_sta(pathtoken_list[i])
			#record[path_name]=[pathnum_list[i],token,token_num]
			
			token_depend=[]
			for j in range(len(token)):
				token_name=path_name+" "+t
				if token_name in pathtokenlist:
					feature_vec[pathtokenlist.index(token_name)+pathtypelist_len]=token_num[j]
	
	model=load_model("./model/"+t_lang+"_"+lang+".h5")
	feature_vec_new = model.predict_classes(feature_vec)
	
	for i in range(pathtypelist_len):
		if feature_vec_new[i] != 0:
			path_list_new.append(pathtypelist[i])
			pathnum_list_new.append(feature_vec_new[i])
	
	pathtoken_list_new=[[]]*len(path_list_new)	
	for j in range(pathtypelist_len,vec_len):
		if feature_vec_new[j] != 0:
			cur_token=pathtokenlist[j-pathtypelist_len].split(' ')
			add_token_idx=path_list_new.index(cur_token[0])
			add_token=cur_token[1]
			for i in range(feature_vec_new[j]):
				pathtoken_list_new[add_token_idx].append(add_token)

	f1=open("./node/path.json","w")
	f2=open("./node/pathnmn.json","w")
	f3=open("./node/pathtokenn.json","w")
	if sys.argv[3] == "./test.txt":
		f4=open("./node/vector.json","w")
	else:
		f4=open("./node/vector_fb.json","w")
	json.dump(path_list_new,f1)
	json.dump(pathnum_list_new,f2)
	f3.write(str(pathtoken_list_new))
	json.dump(feature_vec_new,f4)
	f1.close()
	f2.close()
	f3.close()
	f4.close()
