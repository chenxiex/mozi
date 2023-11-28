import random
import csv

#从文件中读取IP地址
with open(r"infected_nodes.txt","r") as f:
    infected_nodes=f.read().splitlines()
with open(r"uninfected_nodes.txt","r") as f:
    uninfected_nodes=f.read().splitlines()

#打开csv文件以写入感染流数据
with open('infection_flows.csv','w',newline='') as f:
    writer=csv.writer(f)
    #写入表头
    writer.writerow(['source_ip','target_ip','weight'])

    #逐行处理uninfected_nodes.txt中的IP地址
    for target_ip in uninfected_nodes:
        #遍历infected_nodes.txt中的IP地址
        for source_ip in infected_nodes:
            #随机生成感染流的数量
            weight=round(random.uniform(0.000001,0.00002),16)
            #将感染流数据写入csv文件
            writer.writerow([source_ip,target_ip,weight])

print("Infection flows generated and saved to 'infection_flows.csv'.")