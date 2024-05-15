import re
import gurobipy as gp
from gurobipy import GRB, quicksum

class BlendingOptimizer:
    def __init__(self):
        self.model = gp.Model("Blending Optimization")
        self.vars = {}
        self.constraints = []

    def parse_expression(self, expr):
        pattern = re.compile(r'([-+]?\d*\.?\d+|\d+)?\s*([a-zA-Z]\w*)')
        matches = pattern.findall(expr)
        return [(float(coef) if coef else 1.0, var) for coef, var in matches]

    def add_variables(self, variable_names, variable_coefficients):
        self.variable_names = variable_names
        self.variable_coefficients = variable_coefficients
        for name in variable_names:
            self.vars[name] = self.model.addVar(name=name)
        self.model.update()

    def add_constraints(self, constraints):
        for expr, sense, rhs in constraints:
            lhs = quicksum(float(coeff) * self.vars[name] for coeff, name in self.parse_expression(expr) if name in self.vars)
            if sense == ">=":
                self.model.addConstr(lhs >= rhs)
            elif sense == "<=":
                self.model.addConstr(lhs <= rhs)
            elif sense == "=":
                self.model.addConstr(lhs == rhs)

    def set_objective(self):
        obj = quicksum(self.variable_coefficients[i] * self.vars[self.variable_names[i]] for i in range(len(self.variable_names)))
        self.model.setObjective(obj, GRB.MINIMIZE)

    def optimize(self):
        self.model.optimize()

        if self.model.status == GRB.OPTIMAL:
            results = {var.varName: var.x for var in self.model.getVars()}
            objective_value = self.model.objVal
            return results, objective_value
        else:
            print("Optimization was not successful.")
            return None, None

def solve_blending_problem(variable_names, variable_coefficients, constraints):
    optimizer = BlendingOptimizer()
    optimizer.add_variables(variable_names, variable_coefficients)
    optimizer.add_constraints(constraints)
    optimizer.set_objective()
    results, objective_value = optimizer.optimize()
    return results, objective_value
