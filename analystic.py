import networkx as nx
import random
import csv
import matplotlib.pyplot as plt

graph = nx.DiGraph()

#读取数据集
with open(r'infection_flows.csv','r',encoding='utf-8') as f:
    reader=csv.reader(f)
    next(reader)
    for row in reader:
        source_ip,target_ip,weight=row
        graph.add_edge(source_ip,target_ip,weight=float(weight))

def simulation_si(graph,seed,iter_num=100):
    for node in graph:
        graph.nodes[node]['state']=0
    graph.nodes[seed]['state']=1
    all_infect_nodes=[seed]
    all_infect_nodes_round=[]

    infect_graph=nx.DiGraph()
    infect_graph.add_node(seed)

    for i in range(iter_num):
        new_infect=[]
        for v in all_infect_nodes:
            for nbr in graph.neighbors(v):
                edge_data=graph.get_edge_data(v,nbr)
                if random.uniform(0,1)<10000*float(edge_data['weight']):
                    graph.nodes[nbr]['state']=1
                    new_infect.append(nbr)
                    infect_graph.add_edge(v,nbr)
        all_infect_nodes.extend(new_infect)
        all_infect_nodes_round.append(list(set(all_infect_nodes)))
    return all_infect_nodes,all_infect_nodes_round

si = []

#迭代处理每个节点
for node in graph:
    all_infect_nodes_round=[]
    for i in range(1,11):
        #获取在第i轮的感染节点数量
        all_infect_nodes,_=simulation_si(graph,node,iter_num=i)
        all_infect_nodes_round.append(len(all_infect_nodes))
    si.append([node]+all_infect_nodes_round)

#按照总感染节点数排序
top_10 = sorted(si,key=lambda x:x[-1],reverse=True)[:10]
formatted_top_10=[(node[0],node[1:]) for node in top_10]
for item in formatted_top_10:
    print(item)

##生成top_10需要的文件
#1.从infection_flows.csv中找出所有source_ip在top_10中的数据，并写入top10_infection_flows.csv

#获取top_10中的source_ip
top_10_source_ip=[item[0] for item in top_10]

#打开infection_flows.csv读取数据
with open(r'infection_flows.csv','r',newline='',encoding='utf-8') as f:
    reader=csv.reader(f)
    header=next(reader)

    #找出所有top_10中的数据
    top_10_data=[row for row in reader if row[0] in top_10_source_ip]

#写入top_10_infection_flows.csv
with open(r'top_10_infection_flows.csv','w',newline='',encoding='utf-8') as f:
    writer=csv.writer(f)
    writer.writerow(header)
    writer.writerows(top_10_data)

#2.计算top_10中每个source_ip的weight的平均值，并写入top_10_infected_nodes.csv

#创建一个字典来存储每个source_ip对应的weight总和和计数
ip_weight_sum={ip:[0,0] for ip in top_10_source_ip}

#重新打开infection_flows.csv读取数据
with open(r'infection_flows.csv','r',newline='',encoding='utf-8') as f:
    reader=csv.reader(f)
    next(reader)
    for row in reader:
        source_ip,target_ip,weight=row
        if source_ip in top_10_source_ip:
            ip_weight_sum[source_ip][0]+=float(weight)
            ip_weight_sum[source_ip][1]+=1

#计算每个source_ip的weight平均值
ip_weight_average={ip: sum_count[0]/sum_count[1] for ip,sum_count in ip_weight_sum.items()}

#将数据写入top_10_infected_nodes.csv
with open(r'top_10_infected_nodes.csv','w',newline='',encoding='utf-8') as f:
    writer=csv.writer(f)
    writer.writerow(['Id','weight'])
    writer.writerows(ip_weight_average.items())

#根据生成的top10进行图表绘制

#设置随机颜色
def random_color():
    colorArr=['1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
    color=''
    for i in range(6):
        color+=colorArr[random.randint(0,14)]
    return '#'+color

plt.rcParams['axes.unicode_minus']=False
plt.figure(figsize=(16,9))
marker=['.',',','v','^','>','*','+','d','x','p']

for node in top_10[:3]:
    ip=node[0]
    x=[i for i in range(11)]
    y=[0]
    y.extend(node[1:])
    plt.plot(x,y,marker=marker[top_10.index(node)],label=ip,color=random_color(),linewidth=2.5)

plt.xlim(0,len(x))
plt.ylim(0,max(y))
plt.xlabel('Round',fontsize=25)
plt.ylabel('Number',fontsize=25)
plt.legend(fontsize=20,loc="upper right",bbox_to_anchor=(1.13,1.0),borderaxespad=0.)
plt.show()
