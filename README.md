# mozi僵尸网络传播模拟
一个随机生成mozi僵尸网络并模拟其传播过程的程序

## 文件说明
- `data_generate.py`用于生成合法的节点存入`infected_nodes.txt`和`uninfected_nodes.txt`
- `attack_generate.py`用于生成攻击流存入`infection_flows.csv`
- `analysis.py`用于模拟攻击过程并生成统计数据存入`top_10_infected_nodes.csv`和`top_10_infection_flows.csv`