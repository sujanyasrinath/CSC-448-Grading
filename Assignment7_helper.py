from IPython.display import display
import numpy as np
import pandas as pd

import networkx as nx
import pandas as pd
import copy

import matplotlib.pyplot as plt

display_available = True
try:
    from IPython.display import Image
except:
    display_available = False
try:
    import pygraphviz
    graphviz_installed = True # Set this to False if you don't have graphviz
except:
    graphviz_installed = False

def draw(A):
    return Image(A.draw(format='png', prog='dot'))

patterns1 = ['ATAGA','ATC','GAT']
patterns2 = ['ananas','and','antenna','banana','bandana','nab','nana','pan']

# Inputs: G - networkx graph, current - node name, c - character on edge
# Output: a neighbor of current that is reached by an edge that has label==c; otherwise None
def find_edge(G,current,c): 
    for n in G.neighbors(current):
        if n is None:
            return None
        data = G.get_edge_data(current,n)
        if data['label'] == c:
            return n
    return None

def trie_construction(patterns):
    G = nx.DiGraph()
    G.add_node('root')

    node_count = 1  # Initialize a counter for naming nodes

    for pattern in patterns:
        current_node = 'root'

        for symbol in pattern:
            next_node = find_edge(G, current_node, symbol)

            if next_node is None:
                # If the edge with the current symbol doesn't exist, create a new node
                next_node = f'node{node_count}'
                node_count += 1
                G.add_node(next_node)
                G.add_edge(current_node, next_node, label=symbol)

            current_node = next_node

    return G

def trie_matching(text, trie):
    positions = []
    start_positions = []

    for i in range(len(text)):
        matched_patterns = prefix_trie_matching(text[i:], trie)  

        if matched_patterns:
            positions.append(i)
            start_positions.append(i)

    return start_positions



def prefix_trie_matching(text, trie):
    current_node = 'root'  
    matched_patterns = [] 
    previous_node =[]

    for symbol in text:
        next_node = find_edge(trie, current_node, symbol)
        #print(next_node)

        if next_node is None:
            break  

        current_node = next_node
        previous_node.append(symbol)
        #print(previous_node)
        
        
        #print(current_node)

        if trie.out_degree(current_node) == 0:
            #print(current_node)
            #matched_patterns.append(symbol)
            matched_patterns += previous_node 
            matched_patterns = ''.join(matched_patterns)

            #matched_patterns.append(text[:symbol])
        

    return matched_patterns if matched_patterns else None

def suffix_trie(text):
    G = nx.DiGraph()
    G.add_node('root')
    leaf_nodes =[]
    index_list = []
    num_dollar_nodes=0


    for i in range(len(text)):
        current_node = 'root'

        for symbol in text[i:]:
            #print("outer loop i is:",i)
            next_node = find_edge(G, current_node, symbol)
            #print(symbol)

            if next_node is None:
                
                if symbol == "$":
                    # print("fool")
                    # print("i is:",i)
                    dollar_node = '[' +str(i)+ ']'
                    #print("new_node", dollar_node)
                    G.add_node(dollar_node)
                    G.add_edge(current_node, dollar_node, label=symbol)
                    current_node = dollar_node   # G.add_node(new_node)
                    # G.add_edge(current_node, new_node, label=i)
                    # current_node = new_node
                    num_dollar_nodes+=1

                    
                else:
                    new_node = len (G.nodes) - num_dollar_nodes

                    #print("new_node", new_node)
                    G.add_node(new_node)
                    G.add_edge(current_node, new_node, label=symbol)
                    current_node = new_node        
                
            else:
                current_node = next_node
        
        #G.nodes[current_node]['position'] = i
        
        else:
            leaf_nodes.append(current_node)
    #print(leaf_nodes)

    # for x in leaf_nodes:
    #     index = leaf_nodes.index(x) 
    #     index_list.append(index)

    # if G.out_degree(current_node) == None:
    #     print("hello")
    #     for i, node in enumerate(leaf_nodes):
    #         G.nodes[node]['index'] = index_list[i]
            
            


    return G

# Inputs: G - networkx graph, current - node name, c - character on edge
# Output: a neighbor of current that is reached by an edge that has label==c; otherwise None
def modified_find_edge(G,current,c):
    cv,j = c.split(",")
    j = int(j)
    for n in G.neighbors(current):
        if n is None:
            return None
        data = G.get_edge_data(current,n)
        cw,i = data['label'].split(",")
        i = int(i)
        if cw == cv and j > i:
            return n
    return None

def modified_find_edge(G,current,c):
    cv,j = c.split(",")
    j = int(j)
    for n in G.neighbors(current):
        if n is None:
            return None
        data = G.get_edge_data(current,n)
        cw,i = data['label'].split(",")
        i = int(i)
        if cw == cv and j > i:
            return n
    return None

def modified_suffix_trie(text):
    G = nx.DiGraph()
    G.add_node('root')
    leaf_nodes =[]
    num_dollar_nodes=0


    for i in range(len(text)):
        current_node = 'root'

        for symbol_idx,symbol in enumerate(text[i:]):
            #print("outer loop i is:",i)
            next_node = modified_find_edge(G, current_node, f"{symbol},{i+symbol_idx}")

            #print(symbol)

            if next_node is None:
                
                if symbol == "$":
                    # print("fool")
                    # print("i is:",i)
                    dollar_node = '[' +str(i)+ ']'
                    #print("new_node", dollar_node)
                    G.add_node(dollar_node)
                    G.add_edge(current_node, dollar_node, label=f"{symbol},{i+symbol_idx}")
                    current_node = dollar_node   # G.add_node(new_node)
                    # G.add_edge(current_node, new_node, label=i)
                    # current_node = new_node
                    num_dollar_nodes+=1

                    
                else:
                    new_node = len (G.nodes) - num_dollar_nodes

                    #print("new_node", new_node)
                    G.add_node(new_node)
                    G.add_edge(current_node, new_node, label=f"{symbol},{i+symbol_idx}")
                    current_node = new_node        
                
            else:
                current_node = next_node
        
        #G.nodes[current_node]['position'] = i
        
        else:
            leaf_nodes.append(dollar_node)
    #print(leaf_nodes)

    # for x in leaf_nodes:
    #     index = leaf_nodes.index(x) 
    #     index_list.append(index)

    # if G.out_degree(current_node) == None:
    #     print("hello")
    #     for i, node in enumerate(leaf_nodes):
    #         G.nodes[node]['index'] = index_list[i]
            
            


    return G,leaf_nodes

import numpy as np

def suffix_tree_construction(text):
    trie= suffix_trie(text)
    root_node = 'root'
    converged_array = []

    def traverse_loop(trie, current_node, next_node):
            
            print ("-----------------------------")
            print("current_node", current_node)
            print("next_node", next_node)
            successors = trie.successors(next_node)
            successors_list = list(trie.successors(next_node))


            if len (successors_list) >= 1:
                data = trie.get_edge_data(current_node,next_node)
                print("symbol on edge", data)
                converged_array.append(data['label'])
                current_node = next_node
                for each_successor in successors:
                    traverse_loop(trie,current_node,each_successor)

            elif len (successors_list) < 1: 
                data = trie.get_edge_data(current_node, next_node)
                print("symbol on edge", data)
                converged_array.append(data['label'])
                print("answer:",converged_array)
                print ("---------------------")
            return None
    
   
    for each_node in trie.successors(root_node):
         traverse_loop(trie,root_node,each_node)
         converged_array = []
    return trie


def to_adj(T):
    df = pd.DataFrame(nx.adjacency_matrix(T).todense(),index=T.nodes(),columns=T.nodes())
    for i in range(len(df)):
        for j in range(len(df)):
            if df.iloc[i,j] == 1:
                data = T.get_edge_data(df.index[i],df.columns[j])
                df.iloc[i,j] = data['label']
            else:
                df.iloc[i,j] = ""
    return df

def show(G):
    if graphviz_installed:
        # same layout using matplotlib with no labels
        pos = nx.drawing.nx_agraph.graphviz_layout(G, prog='dot')
        #print(edge_labels)
        # Modify node fillcolor and edge color.
        #D.node_attr.update(color='blue', style='filled', fillcolor='yellow')
        #D.edge_attr.update(color='blue', arrowsize=1)
        A = nx.nx_agraph.to_agraph(G)
        # draw it in the notebook
        if display_available:
            display(draw(A))
        else:
            print(A)
    else:
        if display_available:
            display(to_adj(G))
        else:
            print(to_adj(G))
            
            