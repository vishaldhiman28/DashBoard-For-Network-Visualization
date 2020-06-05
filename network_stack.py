# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import networkx as nx


class GraphStack():
  #reading files
  def __init__(self):

    self.stack_network_links=pd.read_csv("./stack_network_links.csv") 
    self.stack_network_nodes=pd.read_csv("./stack_network_nodes.csv")

  def get_links_data(self):
    return self.stack_network_links

  def get_nodes_data(self):
    return self.stack_network_nodes

  def make_graph(self):
    
    graph=nx.Graph()
    #adding nodes
    for row in range(self.stack_network_nodes.shape[0]):
      graph.add_node(self.stack_network_nodes.iloc[row]["name"],group=self.stack_network_nodes.iloc[row]["group"],nodesize=self.stack_network_nodes.iloc[row]["nodesize"])
    
    #adding eges  
    for row in range(self.stack_network_links.shape[0]):
      graph.add_edge(self.stack_network_links.iloc[row]["source"],self.stack_network_links.iloc[row]["target"],weight=self.stack_network_links.iloc[row]["value"])
    
    return graph

  def make_group_graph(self,gp,graph):

    #neighbors=graph.neighbors(gp)
    group_n=list(self.stack_network_nodes[self.stack_network_nodes['group']==gp]['name'])
    p_subg=graph.subgraph(set(group_n))
    return p_subg


  def make_spanning_tree_graph(self,tree_min):
    span_graph=nx.Graph()

    #adding nodes
    for row in range(self.stack_network_nodes.shape[0]):
      span_graph.add_node(self.stack_network_nodes.iloc[row]["name"],group=self.stack_network_nodes.iloc[row]["group"],nodesize=self.stack_network_nodes.iloc[row]["nodesize"])
    #adding eges  
    for row in range(len(tree_min)):
      span_graph.add_edge(tree_min[row][0],tree_min[row][1],weight=tree_min[row][2]['weight'])
    return span_graph 
 

  def position_of_nodes(self,graph,n=60):
    #defines coordinate of nodes 
    pos = nx.drawing.spring_layout(graph,k=0.70,iterations=n)
    return pos

  def get_coordinate(self,pos,graph,opt):
    if opt=="Main Network":

      node_x=[]
      node_y=[]
      
      #getting x_corrdinate and y_coordinates of nodes in list
      for key in sorted(pos.keys()):
        node_x.append(pos[key][0])
        node_y.append(pos[key][1])

    elif opt=="Minimum Spannining Tree":
      nodelist=list(graph)
      xy = np.asarray([pos[v] for v in nodelist])
      node_x=xy[:,0]
      node_y=xy[:,1]

      
    edge_x=[]
    edge_y=[]

    #getting start-end coordinated of nodes in the list
    for edge in sorted(graph.edges()):
      edge_x.append(pos[edge[0]][0])
      edge_y.append(pos[edge[0]][1])
      edge_x.append(pos[edge[1]][0])
      edge_y.append(pos[edge[1]][1])
      edge_x.append(None)
      edge_y.append(None)
     
    return node_x,node_y,edge_x,edge_y

  def span_tree(self,graph):
    span_tree=nx.minimum_spanning_tree(graph)
    tree_min=list(span_tree.edges(data=True))
    span_graph=self.make_spanning_tree_graph(tree_min)
    return span_graph

  def get_color_text(self,graph):
    #setting color and text of each node 
    node_color=[]
    hover_text=[]
    text=[]
    size=[]

    d=self.stack_network_nodes.sort_values('name')
    for _ , r in d.iterrows():
      node_color.append(r['group']*100)
      t= "Tag Name: "+r['name']+" , "+"Tag Group: "+str(r['group'])
      text.append(r['name'])
      hover_text.append(t)
      size.append(abs((r['nodesize']-self.stack_network_nodes['nodesize'].mean())*25/self.stack_network_nodes['nodesize'].std()))
    return node_color,text,size,hover_text
  
  def group_visual(self):
    number_of_group=len(self.stack_network_nodes['group'].unique())
    group_info={}
    for i in range(number_of_group):
      data_g=self.stack_network_nodes[self.stack_network_nodes['group']==(i+1)]['nodesize'].argmax()
      group_info[i+1]=self.stack_network_nodes.iloc[data_g]['name']
    return group_info
  
