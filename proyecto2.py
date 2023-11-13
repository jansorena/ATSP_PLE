import numpy as np
import networkx as nx
import tsplib95
import pulp
from itertools import combinations

def matriz_texto(path):
    c = []

    with open(path, 'r') as archivo:
        lines = archivo.readlines()

    for i in range(0, len(lines)):
        row = list(map(int, lines[i].split()))
        c.append(row)
    
    return c

def matriz_atsp(path):
    problem = tsplib95.load(path)

    G = problem.get_graph()
    nodes = sorted(G.nodes())
    c = []

    for node1 in nodes:
        row = []
        for node2 in nodes:
            if node1 == node2:
                row.append(0)
            else:
                weight = int(G.get_edge_data(node1, node2, default={'weight': 0})['weight'])
                row.append(weight)
        c.append(row)
    #print(c)
    return c
####################################################################################
# Formulacion DFJ
def f_DFJ(c):
    # Conjuntos de nodos y aristas
    n = len(c)
    V = range(n)  # Donde 'n' es el número de nodos
    A = [(i, j) for i in V for j in V if i != j]

    problema_DFJ = pulp.LpProblem("Problema_Vendedor_Viajero_Asimetrico",pulp.LpMinimize) # Problema de minimización

    subtours = []
    for i in range(1, n):
        subtours.extend(combinations(V, i))

    # Variables binarias x_ij
    x = pulp.LpVariable.dicts("x", A, 0, 1, pulp.LpBinary)

    # Función objetivo
    problema_DFJ += pulp.lpSum(c[i][j] * x[(i, j)] for (i, j) in A)

    # Restricciones
    for i in V:
        problema_DFJ += pulp.lpSum(x[(i, j)] for j in V if i != j) == 1

    for j in V:
        problema_DFJ += pulp.lpSum(x[(i, j)] for i in V if i != j) == 1

    for S in subtours:
        problema_DFJ += pulp.lpSum(x[(i, j)] for i in S for j in S if i != j) <= len(S) - 1

    # Resolver el problema
    print("DFJ: ", instancia)
    problema_DFJ.solve(pulp.PULP_CBC_CMD(msg=False))
    print("Status: ",pulp.LpStatus[problema_DFJ.status])
    print("CPU Time: ",problema_DFJ.solutionCpuTime)
    print("Optimal Value: ",pulp.value(problema_DFJ.objective))
    print()
####################################################################################
# Formulacion MTZ
def f_MTZ(c):
    # Conjuntos de nodos y aristas
    n = len(c)
    V = range(n)  # Donde 'n' es el número de nodos
    A = [(i, j) for i in V for j in V if i != j]
    problema_MTZ = pulp.LpProblem("Problema_Vendedor_Viajero_Asimetrico",pulp.LpMinimize) # Problema de minimización

    # Variables binarias x_ij
    x = pulp.LpVariable.dicts("x", A, 0, 1, pulp.LpBinary)
    # Variable auxiliar u_i
    u = pulp.LpVariable.dicts("u", V, 0, n, pulp.LpInteger )

    # Función objetivo
    problema_MTZ += pulp.lpSum(c[i][j] * x[(i, j)] for (i, j) in A)

    # Restricciones
    for i in V:
        problema_MTZ += pulp.lpSum(x[(i, j)] for j in V if i != j) == 1

    for j in V:
        problema_MTZ += pulp.lpSum(x[(i, j)] for i in V if i != j) == 1

    for i in V:
        for j in V:
            if(i!=j and i>=1):
                #problema_MTZ += u[i]-u[j]+1<=n*(1-x[(i,j)])
                problema_MTZ += u[i]-u[j]+(n -1)*x[(i,j)]<= n - 2

    # Resolver el problema
    print("MTZ: ", instancia)
    problema_MTZ.solve(pulp.PULP_CBC_CMD(msg=False))
    print("Status: ",pulp.LpStatus[problema_MTZ.status])
    print("CPU Time: ",problema_MTZ.solutionCpuTime)
    print("Optimal Value: ",pulp.value(problema_MTZ.objective))
    print()

####################################################################################
#Formulacion GG
def f_GG(c):
    # Conjuntos de nodos y aristas
    n = len(c)
    V = range(n)  # Donde 'n' es el número de nodos
    A = [(i, j) for i in V for j in V if i != j]

    # Formulacion GG
    problema_gg = pulp.LpProblem("ATSP_GG", pulp.LpMinimize)

    # Variables binarias x_ij
    x = pulp.LpVariable.dicts("x", A, 0, 1, pulp.LpBinary)
    # Variable auxiliar g_i
    g = pulp.LpVariable.dicts("g", A, 0, n-1, pulp.LpContinuous)

    # Definir la función objetivo para GG
    problema_gg += pulp.lpSum(c[i][j] * x[(i, j)] for (i, j) in A)

    # Restricciones
    for i in V:
        problema_gg += pulp.lpSum(x[(i, j)] for j in V if i != j) == 1

    for j in V:
        problema_gg += pulp.lpSum(x[(i, j)] for i in V if i != j) == 1

    for i in V[1:]:
        problema_gg += pulp.lpSum(g[(i, j)] for j in V if j != i) - pulp.lpSum(g[(j, i)] for j in V if j != i) == 1

    # Restricciones para g_ij
    for i in V:
        for j in V:
            if i != j:
                problema_gg += g[(i, j)] >= 0
                problema_gg += g[(i, j)] <= (n - 1) * x[(i, j)]

    # Resolver el problema
    print("GG: ", instancia)
    problema_gg.solve(pulp.PULP_CBC_CMD(msg=False))
    print("Status: ",pulp.LpStatus[problema_gg.status])
    print("CPU Time: ",problema_gg.solutionCpuTime)
    print("Optimal Value: ",pulp.value(problema_gg.objective))
    print()

var_input = input("Ingrese 1 para matriz texto o 2 para instancia TSPLIB: ")

if var_input == '1':
    nombre_instancia = ['ins10.txt','ins11.txt','ins12.txt','ins13.txt','ins14.txt','ins15.txt','ins16.txt','ins17.txt',
                        'ins18.txt',]
    for instancia in nombre_instancia:
        c = matriz_texto(instancia)
        f_DFJ(c)
        f_MTZ(c)
        f_GG(c)

elif var_input == '2':
    nombre_instancia = ['ftv35.atsp','ftv38.atsp','ftv44.atsp']
    for instancia in nombre_instancia:
        c = matriz_atsp(instancia)
        f_MTZ(c)
        f_GG(c)