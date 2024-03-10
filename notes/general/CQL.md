# CQL



### 学习参考资料

[Neo4j和知识图谱：从基础入门到精通全栈教程](https://www.bilibili.com/video/BV1MR4y1L7zG)



### 前言

neo4j启动：bin目录下cmd输入neo4j console



#### 1 CQL 特点

- Neo4j图形数据库查询语言
- 声明性模式匹配语言
- 遵循SQL语法



#### 2 CQL语句

<table>
    <tr>
    	<th>CQL命令</th>
        <th>用法</th>
    </tr>
    <tr>
    	<td>CREATE</td>
        <td>创建节点、关系、属性</td>
    </tr>
    <tr>
    	<td>MATCH</td>
        <td>查询节点、关系、属性</td>
    </tr>
    <tr>
    	<td>RETURN</td>
        <td>返回查询结果</td>
    </tr>
    <tr>
    	<td>WHERE</td>
        <td>条件查询</td>
    </tr>
    <tr>
    	<td>DELETE</td>
        <td>删除节点、关系</td>
    </tr>
    <tr>
    	<td>REMOVE</td>
        <td>移除节点、关系的属性</td>
    </tr>
    <tr>
    	<td>ORDER BY</td>
        <td>排序</td>
    </tr>
    <tr>
    	<td>SET</td>
        <td>添加、更新数据</td>
    </tr>
</table>




###### （1）CREATE

创建节点、关系、属性，例如

```CQL
/*创建单一节点*/
CREATE (变量)
/*创建多节点*/
CREATE (变量1),(变量2)
/*创建带标签的节点*/
CREATE (n:类1:类2)
/*创建带属性的节点*/
CREATE (n:类名 {属性名:"字符串", 属性名:数字})
/*创建关系*/
CREATE (Entity1)<-[:Relation]-(Entity2)-[:Relation]->(Entity3)	/*可以直接打，也可先查询后用变量创建*/
```




###### （2）MATCH

查询关系，例如

```CQL
/*查询全部*/
MATCH (N:类) RETURN N
/*查询匹配的关系*/
MATCH p=()-[:类]->() RETURN p
/*查询一节点和一节点的关系*/
MATCH (:类 {属性})-[r]->(:类 {属性})
	RETURN type(r)
/*查询一节点和其他节点的全部关系*/
MATCH (:类 {属性})-[r]->()
	RETURN type(r)
```



###### （3）DELETE

删除节点，例如

```CQL
/*删除某标签下的所有节点*/
MATCH (n:标签)
	DELETE n
/*删除所有节点*/
MATCH (n)
	DELETE n
/*删除两节点间的关系*/
MATCH (:类 {属性})-[r]->(:类 {属性})
	DELETE r
/*删除一节点和其他节点的所有关系*/
MATCH (:类 {属性})-[r]->()
	DELETE r
```



###### （4）SET

添加、更新某一属性，例如

```CQL
/*添加、更新某一属性*/
MATCH(n:类) WHERE a.属性=属性值
	SET a.属性=属性值	/*若有则更新，若无添加*/
	RETURN a
```



###### （5）REMOVE

删除某一属性，例如

```CQL
/*删除某一属性*/
MATCH(n:类) WHERE a.属性=属性值
	REMOVE a.属性=属性值	/*删除a的一个属性*/
	RETURN a
```



###### （6）ORDER BY



#### 3  Neo4j与python

##### 3.1 相关包

```python
from py2neo import Graph
from py2neofun import CreateNode
```

##### 3.2 连接与使用

```python
# 连接数据库
g = Graph('http://localhost:7474/', username='neo4j', password='12345678')
# 执行CQL
graph.run('CQL命令')
# 获取CQL return结果
graph.run('CQL命令').data()
```



#### 4 Neo4j与Linux

##### 4.1 前置准备工作

###### （1）准备Linux工具

安装JDK并设置环境变量

libasound2

neo4j并修改相关配置

###### （2）准备windows工具

Putty 或 Xshell：Telnet、ssh和rlogin客户端（win10及以上可用powershell）

WinSCP：远程ssh文件传输工具（win10及以上可用powershell）

