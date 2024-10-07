# -*- coding: utf-8 -*-
"""pregunta7(a).ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/11IHS4zSmzQNr7Ta8Pd_goL0vZ51qxUoz
"""

!pip install deap

import random
from deap import base, creator, tools, algorithms
import math

# Eliminar las clases anteriores si ya han sido creadas
try:
    del creator.FitnessMax
    del creator.Individual
except AttributeError:
    pass

# Definir la función de evaluación: f(x) = (x^(2x)) - 1
def eval_function(individual):
    x = individual[0]
    try:
        result = (x ** (2 * x)) - 1
    except OverflowError:
        result = float('inf')  # Evitar el desbordamiento en grandes números
    return result,

# Configuración de DEAP
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("attr_int", random.randint, 1, 8)  # Limitar valores de x entre 1 y 8 para mayor variación
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_int, n=1)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Registro de las operaciones genéticas
toolbox.register("mate", tools.cxTwoPoint)         # Cruce
toolbox.register("mutate", tools.mutFlipBit, indpb=0.1)  # Mutación con probabilidad del 10%
toolbox.register("select", tools.selTournament, tournsize=3)  # Selección por torneo
toolbox.register("evaluate", eval_function)


# cxTwoPoint modificado para manejar individuos con tamaño 1

def cxTwoPoint(ind1, ind2):
    """Ejecuta un cruce de dos puntos en los individuos de entrada :term:`sequence`.
    Los dos individuos se modifican en el lugar y ambos mantienen
    su longitud original.

    :param ind1: El primer individuo que participa en el cruce.
    :param ind2: El segundo individuo que participa en el cruce.
    :returns: Una tupla de dos individuos.
    """
    size = min(len(ind1), len(ind2))
    if size > 1:  # Verifica si el individuo tiene más de un elemento para el cruce
        cxpoint1 = random.randint(1, size)
        cxpoint2 = random.randint(1, size - 1)
        if cxpoint2 >= cxpoint1:
            cxpoint2 += 1
    else:
        # Si el tamaño es 1, no se realiza el cruce
        cxpoint1, cxpoint2 = 0, 0

    ind1[cxpoint1:cxpoint2], ind2[cxpoint1:cxpoint2] \
        = ind2[cxpoint1:cxpoint2], ind1[cxpoint1:cxpoint2]

    return ind1, ind2

# Reemplaza el cxTwoPoint existente en la caja de herramientas con esta versión modificada
toolbox.register("mate", cxTwoPoint)

# Algoritmo principal
def main():
    population = toolbox.population(n=10)  # Población inicial de 10 individuos
    num_generations = 3

    for generation in range(num_generations):
        print(f"Generación {generation + 1}")

        # Evaluar individuos
        for ind in population:
            ind.fitness.values = toolbox.evaluate(ind)
            print(f"Individuo {ind[0]}: f(x) = {ind.fitness.values[0]}")

        # Selección de la nueva generación
        offspring = toolbox.select(population, len(population))
        offspring = list(map(toolbox.clone, offspring))

        # Aplicar cruce y mutación
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < 0.5:  # 50% probabilidad de cruce
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < 0.2:  # 20% probabilidad de mutación
                toolbox.mutate(mutant)
                # Asegurar que el mutante siga dentro del rango válido
                mutant[0] = max(1, min(8, mutant[0]))  # Limitar a rango 1-8
                del mutant.fitness.values

        # Re-evaluar los descendientes
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        for ind in invalid_ind:
            ind.fitness.values = toolbox.evaluate(ind)

        # Reemplazar la población con la nueva generación
        population[:] = offspring

    # Retornar la población final
    return population

# Ejecutar el algoritmo
final_population = main()