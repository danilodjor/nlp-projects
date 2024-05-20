def backward(self):
        self.derivative = {}
        
        # Go through all nodes and set all  backwards values to 0
        for key in self.graph.keys():
          self.graph[key]['backwards'] = 0

        # 1. Go through nodes in reverse topological order (starting from the back). Last variable has backwards value = 1.
        # 2. For all children of the current node, find calculate the product of the corresponding gradient multiplied by the current node value
        # 3. Add the value to the children node backwards_value
        # (No need for recursion - just do it iteratively)

        output_flag = 0

        for key in reversed(list(self.graph.keys())):

            # Set the derivative of output wrt itself to 1 (backwards value)
            if not output_flag:
                self.graph[key]['backwards'] = 1
                output_flag = 1

            # Calculate the gradient of current node wrt its parent nodes
            fun_to_use = self.graph[key]['function']

            parent_values = []

            operands = self.graph[key]['operands']
            if operands is not None:
              for operand in operands:
                if type(operand) is str:
                  parent_values.append(self.graph[operand]['value'])
                elif operand is not None:
                  parent_values.append(operand)
            
            if fun_to_use is not None:
              gradient = self.fn_map[fun_to_use].df(*parent_values)

            # Do the rest of the variables
            if self.graph[key]['operands'] is not None:
                for i, parent in enumerate(self.graph[key]['operands']):
                  if (parent is not None) and (type(parent) is str):  
                    self.graph[parent]['backwards'] += self.graph[key]['backwards']*gradient[i]

        # Final output
        for input_var in self.in_vars:
          self.derivative[input_var] = self.graph[input_var]['backwards']