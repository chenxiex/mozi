#随机生成数据

import random

#传染节点数量
num_infected_nodes = 10
#未被传染的节点数量
num_uninfected_nodes = 60

#生成合法的IPv4地址
def generate_ipv4_address():
    ip_parts = [str(random.randint(0, 255)) for _ in range(4)]
    return ".".join(ip_parts)

def generate_unique_ipv4_address(num_addresses):
    unique_addresses=set()
    while len(unique_addresses) < num_addresses:
        unique_addresses.add(generate_ipv4_address())
    return list(unique_addresses)

#生成所有IPv4地址
all_ip_addresses=generate_unique_ipv4_address(num_infected_nodes+num_uninfected_nodes)

#随机排列所有IPv4地址
random.shuffle(all_ip_addresses)

#分配传染结点和未传染结点的IP地址
infected_nodes=all_ip_addresses[:num_infected_nodes]
uninfected_nodes=all_ip_addresses[num_infected_nodes:]

#将传染结点的IP地址写入文件
with open("infected_nodes.txt","w") as f:
    for ip_address in infected_nodes:
        f.write(ip_address+"\n")

#将未传染结点的IP地址写入文件
with open("uninfected_nodes.txt","w") as f:
    for ip_address in uninfected_nodes:
        f.write(ip_address+"\n")

print(f"Generated and saved {num_infected_nodes} infected nodes to 'infected_nodes.txt'.")
print(f"Generated and saved {num_uninfected_nodes} uninfected nodes to 'uninfected_nodes.txt'.")