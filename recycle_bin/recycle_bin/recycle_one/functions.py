from .models import Material
import pulp

def materials_filter(materials):
    """
    Estafuncion filtra la lista de materiales
    utilizando la una lista con los nombres de los materiales que pueden reciclarse
    """
    #crea una lista con los materiales pueden reciclarse
    selectable_materials = Material.objects.values_list('name')

    #obtener los materiales aptos paa recickado
    selected_materials = []
    for material in materials:
        if material['name'] in selectable_materials:
            selected_materials.append(material)
    return selected_materials


def materials_value(materials):
    values =[]
    for material in materials:
        values.append(material['weight'] * material['value'])
    return values

def materials_weights(materials):
    weights = []
    for material in materials:
        weights.append(material['weight'])
    return weights


def optimal_materials_calculator(materials, limit_weight):

    materials = materials_filter(materials)

    problem = pulp.LpProblem("Maximizar_Z", pulp.LpMaximize)

    n = len(materials)
    variables = [pulp.LpVariable(f"x{i}", lowBound=0, upBound=1, cat="Integer") for i in range(1, n+1)]
    c = materials_value(materials)
    problem += pulp.lpSum(c[i] * variables[i] for i in range(n)), "Z"
    A = []
    A.append(materials_weights(materials))
    b = [limit_weight]

    for row in A:
        problem += pulp.lpSum(row[i] * variables[i] for i in range(n)) <= b[A.index(row)], f"Restriccion{A.index(row)}"

    problem.solve()

    selecteds = []

    for variable in variables:
        selecteds.append(variable.varValue)

    result = []
    iter = 0
    for n in selecteds:
        if n == 1.0:
            result.append(materials[iter])
            iter += 1
        else:
            iter += 1

    return result


        



