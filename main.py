from timeit import default_timer as timer  # To calculate elapsed time


class UcsNode:
    """
    Represents a tree node. Takes arguments suitable for solving
    the pancake flipping sort problem using UCS algorithm
    """

    def __init__(self, stack, backwards_cost, path):
        self.stack = stack  # List which represents a pancake stack state
        self.backwards_cost = backwards_cost  # Cost from root to current node
        self.path = path  # Path from root to current node(list of stacks)

    def __eq__(self, other):
        """
        Defines if current node and other node are equal based on their stack list.
        :param other: UcsNode:Represent the other node with which the current node
        is compared
        :return: True if nodes stacks are equal, False otherwise
        """
        if isinstance(other, UcsNode):
            return self.stack == other.stack


class AStarNode(UcsNode):
    """
    Inherits all  methods and properties from UcsNode class. Takes arguments
    suitable for solving the pancake flipping sort problem using A* algorithm
    """

    def __init__(self, stack, backwards_cost, path, heuristic_value):
        super().__init__(stack, backwards_cost, path)
        self.heuristic_cost = heuristic_value  # Heuristic cost
        # Total cost(backwards + heuristic)
        self.total_cost = self.heuristic_cost + self.backwards_cost


class Ucs:
    """
    Implements the Uniform Cost Search algorithm to solve
    the pancake flipping sort problem.
    """

    def __init__(self, starting_stack):
        self.root = UcsNode(starting_stack, 0, [starting_stack])  # Root node
        self.expanded = []  # List with expanded but not yet traversed nodes(Ανοικτές)
        self.traversed = []  # List with nodes that have been traversed(Κλειστές)
        self.goal_stack = sorted(self.root.stack)  # Goal stack
        self.nodes_expanded = 1  # Number of expanded nodes

    def get_lowest_cost_node(self):
        """
        Returns lowest cost node found in self.expanded list
        """
        self.expanded.sort(key=lambda x: x.backwards_cost)
        return self.expanded[0]

    def get_node_by_stack(self, stack):
        """
        Returns node found in self.expanded list based on node stack
        """
        for node in self.expanded:
            if node.stack == stack:
                return node
        return 0

    @staticmethod
    def flip(stack, n):
        """
        Inverts "n" first elements of stack(list)
        """
        return stack[:n][::-1] + stack[n:]

    def start_search(self):
        """
        Starts UCS search
        """
        self.expanded.append(self.root)

        while True:
            # Set lowest cost node in expanded list as current node
            current_node = self.get_lowest_cost_node()
            # Remove current node from expanded and append it to traversed
            self.expanded.remove(current_node)
            self.traversed.append(current_node)

            # Goal node traversed as termination criterion:
            # If current node is goal-node then end search and return node
            if current_node.stack == self.goal_stack:
                return current_node

            # Expand all sub nodes of current node
            for i in range(2, len(current_node.stack) + 1):
                self.nodes_expanded += 1
                stack = self.flip(current_node.stack, i)
                path = current_node.path.copy()
                path.append(stack)
                new_node = UcsNode(stack, current_node.backwards_cost + 1, path)
                # # Uncomment to set goal node expansion as termination criterion
                # if new_node.stack == self.goal_stack:
                #     return new_node
                if new_node not in self.expanded and new_node not in self.traversed:
                    self.expanded.append(new_node)
                elif new_node in self.expanded:
                    old_node = self.get_node_by_stack(new_node.stack)
                    if new_node.backwards_cost < old_node.backwards_cost:
                        self.expanded.remove(old_node)
                        self.expanded.append(new_node)


class Astar(Ucs):
    """
    Implements the A* algorithm to solve the pancake flipping sort problem.
    Inherits all methods and properties from Ucs class.
    """

    def __init__(self, starting_stack):
        super().__init__(starting_stack)
        self.root = AStarNode(starting_stack, 0, [starting_stack],
                              self.calculate_heuristic_value(starting_stack))

    def get_lowest_cost_node(self):
        """
        Returns lowest total cost node found in self.expanded list
        """
        self.expanded.sort(key=lambda x: x.total_cost)
        return self.expanded[0]

    @staticmethod
    def calculate_heuristic_value(stack):
        """
        Calculates and returns heruistic value of stack
        """
        heuristic_value = 0
        i = 0
        while i < len(stack) - 1:
            current_pancake = stack[i]
            current_plus_one = current_pancake - 1
            current_minus_one = current_pancake + 1
            # If next pancake's value isn't one number above or bellow current pancake
            if (stack[i + 1] != current_minus_one) and \
                    (stack[i + 1] != current_plus_one):
                heuristic_value += 1  # Increment Nodes heuristic value
            i += 1
        return heuristic_value

    def start_search(self):
        """
        Starts A* search
        """
        self.root.heuristic_cost = self.calculate_heuristic_value(self.root.stack)
        self.expanded.append(self.root)
        while True:
            # Set lowest cost node in expanded list as current node
            current_node = self.get_lowest_cost_node()
            # Remove current node from expanded and append it to traversed
            self.expanded.remove(current_node)
            self.traversed.append(current_node)

            # If current node is goal-node then end search and return node
            if current_node.stack == self.goal_stack:
                return current_node

            # Expand all sub nodes of current node
            for i in range(2, len(current_node.stack) + 1):
                self.nodes_expanded += 1
                stack = self.flip(current_node.stack, i)
                path = current_node.path.copy()
                path.append(stack)
                heuristic_value = self.calculate_heuristic_value(stack)
                new_node = AStarNode(stack, current_node.backwards_cost + 1,
                                     path, heuristic_value)
                if new_node not in self.expanded and new_node not in self.traversed:
                    self.expanded.append(new_node)
                elif new_node in self.expanded:
                    old_node = self.get_node_by_stack(new_node.stack)
                    if new_node.total_cost < old_node.total_cost:
                        self.expanded.remove(old_node)
                        self.expanded.append(new_node)


class FlippingSort:
    """
    Implements helper function to get and validate user input and to print results
    """
    @staticmethod
    def get_user_input():
        return input("\nPlease select the starting stack.\nStack must contain "
                     "all integers from 1 to the desired number separated by "
                     "comma. E.g. 4,1,5,2,3.\nFirst number inputted represents"
                     " the pancake that will be on the top of the stack.\n")

    @staticmethod
    def parse_user_input(user_input):
        user_input = user_input.split(",")
        starting_stack = []
        for num in user_input:
            num = int(num)
            starting_stack.append(num)
        return starting_stack

    @staticmethod
    def is_stack_valid(starting_stack):
        """
        Validates that stack contains numbers 1 to n
        :return: True if stack is valid, False otherwise
        """
        starting_stack_set = set(starting_stack)
        # Check if stack contains duplicates
        if len(starting_stack) != len(starting_stack_set):
            print(f"Error: Stack contains duplicates. "
                  f"You inputted: {' '.join(str(x) for x in starting_stack)}. "
                  f"Try again")
            return False
        # Check if stack contains all integers from 1 to stack length
        for i in range(1, len(starting_stack) + 1):
            if i not in starting_stack:
                print(f"Error: Numbers missing from stack. "
                      f"You inputted: {' '.join(str(x) for x in starting_stack)}. "
                      f"Try again")
                return False
        return True

    @staticmethod
    def print_results(target_node, nodes_expanded, time_elapsed):
        """
        Prints results of search
        """

        print("Optimal path:")
        for stack in target_node.path:
            if stack != target_node.path[0]:
                print(" -> ")
            print(stack, end="")
        print(f"\nPath cost: {target_node.backwards_cost}.\n"
              f"Number of expanded nodes: {nodes_expanded}.\n"
              f"Time elapsed: {time_elapsed} sec.")

    def validate_user_input(self):
        while True:  # Prompt user for input until input is valid
            user_input = self.get_user_input()
            starting_stack = self.parse_user_input(user_input)
            if self.is_stack_valid(starting_stack):
                print(starting_stack)
                return starting_stack


def main():

    fs = FlippingSort()  # Create FlippingSort instance
    starting_stack = fs.validate_user_input()

    # Run Ucs search
    ucs = Ucs(starting_stack)
    start_time = timer()
    target_node = ucs.start_search()
    ucs_elapsed_time = timer() - start_time
    print("\nUCS results:")
    fs.print_results(target_node, ucs.nodes_expanded, ucs_elapsed_time)

    # Run A* search
    a_star = Astar(starting_stack)
    start_time = timer()
    target_node = a_star.start_search()
    astar_elapsed_time = timer() - start_time
    print("\nA* results:")
    fs.print_results(target_node, a_star.nodes_expanded, astar_elapsed_time)

    print(f"\nA* was {ucs_elapsed_time - astar_elapsed_time} "
          f"seconds faster than UCS.")
    print(f"A* expanded {ucs.nodes_expanded - a_star.nodes_expanded}"
          f" less nodes to find the solution.")


if __name__ == "__main__":
    main()
