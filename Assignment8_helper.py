import networkx as nx
import pandas as pd
import numpy as np
import copy
from IPython.display import Image

import matplotlib.pyplot as plt

a_mass = {
    "G": 57,
    "A": 71,
    "S": 87,
    "P": 97,
    "V": 99,
    "T": 101,
    "C": 103,
    "I": 113,
    "L": 113,
    "N": 114,
    "D": 115,
    "K": 128,
    "Q": 128,
    "E": 129,
    "M": 131,
    "H": 137,
    "F": 147,
    "R": 156,
    "Y": 163,
    "W": 186
}

mass_a = {}
for key in a_mass.keys():
    mass = a_mass[key]
    if mass not in mass_a:
        mass_a[mass] = []
    mass_a[mass].append(key)

def spectrum_graph_construction(spectrum, mass_a=mass_a):
    spectrum = copy.copy(spectrum)
    spectrum.insert(0, 0)
    G = nx.DiGraph()
    
    for i, s in enumerate(spectrum):  # i is the index, s is the value
        G.add_node(s)
        for mass, amino_acids in mass_a.items():
            #print(amino_acids)
            for source_mass in spectrum[:i]:
                mass_diff = s - source_mass
                if mass_diff == mass:
                    matching_amino_acids = "/".join(amino_acids)
                    G.add_edge(source_mass, s, label=matching_amino_acids)
    
    return G


# fragments is for debugging purposes
def ideal_spectrum(peptide, a_mass=a_mass, prefix=True, suffix=True, fragments=None):
    if fragments is None:
        fragments = []
    
    ideal = [0]
    
    # Calculate the masses of prefix and suffix peptides
    peptide_mass = 0
    for amino_acid in peptide:
        peptide_mass += a_mass[amino_acid]
    
    if prefix:
        for i in range(1, len(peptide)):
            prefix_mass = 0
            for j in range(i):
                prefix_mass += a_mass[peptide[j]]
            ideal.append(prefix_mass)
    
    if suffix:
        for i in range(1, len(peptide)):
            suffix_mass = 0
            for j in range(i, len(peptide)):
                suffix_mass += a_mass[peptide[j]]
            ideal.append(suffix_mass)
    
    ideal.append(peptide_mass)
    
    
    # For debugging, collect fragments
    if fragments is not None:
        for i in range(1,len(peptide)):
            if prefix:
                fragments.append(peptide[:i])
            if suffix:
                fragments.append(peptide[i:])
    ideal.sort()
    return ideal

def decoding_ideal_spectrum(spectrum,a_mass=a_mass,debug=False):
    mass_a = {}
    for key in a_mass.keys():
        mass = a_mass[key]
        if mass not in mass_a:
            mass_a[mass] = []
        mass_a[mass].append(key)
    G = spectrum_graph_construction(spectrum,mass_a=mass_a)
    if debug:
        show(G)
    # Your solution here
    matches = []
    return matches

def construct_peptide_vector(peptide,a_mass={"X":4,"Z":5},verbose=False):
    total_mass = sum([a_mass[c] for c in peptide])
    vector = np.zeros((total_mass),dtype=int)
    # Your solution here
    return vector

def construct_peptide_from_vector(p,a_mass={"X":4,"Z":5}):
    peptides = []
    # Your solution here
    return peptides

def max_peptide(s, a_mass={"X": 4, "Z": 5}, debug=False):
    n = len(s)
    
    # Initialize a score matrix with zeros
    score_matrix = [0] * (n + 1)
    peptide_matrix = ["" for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        max_score = float("-inf")
        max_peptide = ""
        
        # For each amino acid mass, calculate the score
        for mass, aa in a_mass.items():
            if i - aa >= 0:
                score = score_matrix[i - aa] + s[i - 1]
                if score > max_score:
                    max_score = score
                    max_peptide = peptide_matrix[i - aa] + mass
        
        # Update the score and peptide matrices
        score_matrix[i] = max_score
        peptide_matrix[i] = max_peptide
    
    # Trace back to find the peptide with the maximum score
    max_peptide = peptide_matrix[n]
    
    if debug:
        print("Score Matrix:")
        print(score_matrix)
    
    return max_peptide





def draw(A):
    return Image(A.draw(format='png', prog='dot'))

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
    # same layout using matplotlib with no labels
    pos = nx.drawing.nx_agraph.graphviz_layout(G, prog='neato')
    #print(edge_labels)
    # Modify node fillcolor and edge color.
    #D.node_attr.update(color='blue', style='filled', fillcolor='yellow')
    #D.edge_attr.update(color='blue', arrowsize=1)
    A = nx.nx_agraph.to_agraph(G)
    A.graph_attr["rankdir"] = "LR"
    # draw it in the notebook
    display(draw(A))