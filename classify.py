import matplotlib.pyplot as plt
f=open("items.txt","r")
e=open("Entertainment","r")
fo=open("Food","r")
sh=open("shopping","r")
uti=open("utilities","r")
ent=e.readlines()
food=fo.readlines()
shop=sh.readlines()
util=uti.readlines()
items=f.readlines()
en=fn=sn=un=ms=0
print(util,items)
for i in items:
	if i.lower() in map(lambda x:x.lower(), ent):
		en+=1
	elif i.lower() in map(lambda x:x.lower(), food):
		fn+=1
	elif i.lower() in map(lambda x:x.lower(), shop):
		sn+=1
	elif i.lower() in map(lambda x:x.lower(), util):
		un+=1
	else:
		ms+=1
labels="Entertainment","Food","Shopping","Utilities","Miscellaneous"
sizes=[en,fn,sn,un,ms]
print(sizes)
fig1, ax1 = plt.subplots()
ax1.pie(sizes, labels=labels, autopct='%1.1f%%',shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.savefig("piechart.jpg")


