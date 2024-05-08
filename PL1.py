import gurobipy as gp
from gurobipy import *
from read_files import load_products, load_resources, add_product, add_resource

class solve_optimization():
    # Liste des noms des cultures
    def __init__(self):
        self.products = load_products()
        self.resources = load_resources()

        # TODO: Change this to read from file
        self.nb_employees = 200
        self.nb_machines = 100

        self.model = None

    def setup_model(self):
        self.model = Model("Production Optimization")
        # Initialize decision variables
        x = []
        for i in self.products:
            x.append(self.model.addVar(lb=0, vtype=GRB.CONTINUOUS, name=i['name']))

        # Objective Function: Maximize total sales
        self.model.setObjective(quicksum(self.products[i]["Price"] * x[i] for i in range(len(self.products))),
                                GRB.MAXIMIZE)

        # Human work time constraint
        self.model.addConstr(quicksum(
            self.products[i]["Worker_time"] * x[i] for i in range(len(self.products))) <= 8 * self.nb_employees,
                             "HumanWorkTimeLimit")

        # Machine time constraint
        self.model.addConstr(quicksum(
            self.products[i]["Machine_time"] * x[i] for i in range(len(self.products))) <= 16 * 60 * self.nb_machines,
                             "MachineTimeLimit")

        for resource in self.resources:
            available_quantity = resource["quantity_available"]
            resource_name = resource["name"]

            # Sum the usage across all products for this resource
            total_usage = quicksum(x[i] * (
                next((res["quantity"] for res in self.products[i]["resources_needed"] if res["name"] == resource_name),
                     0)) for i in range(len(self.products)))
            self.model.addConstr(total_usage <= available_quantity, f"resource_limit_{resource_name}")

    def optimize(self):
        if not self.model:
            self.setup_model()

        self.model.optimize()

        if self.model.status == GRB.OPTIMAL:
            results = {var.varName: var.x for var in self.model.getVars()}
            objective_value = self.model.objVal
            return results, objective_value
        else:
            print("Optimization was not successful.")
            return None

    def run_optimization(self):
        results, objective_value = self.optimize()
        if results is not None:
            print("Optimization Results:")
            for product, quantity in results.items():
                print(f"{product} = {quantity}")
            print(f"Objective value = {objective_value}")
        else:
            print("No results to display.")

if __name__ == "__main__":
    opt_manager = solve_optimization()
    opt_manager.run_optimization()