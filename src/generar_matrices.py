import numpy as np

tamano_matriz = 18
c = np.random.randint(0, 100, size=(tamano_matriz, tamano_matriz), dtype=int)
np.fill_diagonal(c, 9999)

# Guardar la matriz en un archivo de texto
np.savetxt('matriz18.txt', c, fmt='%d', delimiter='\t')