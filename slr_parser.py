class SLRParser:
    def __init__(self, grammar, parsing_table):
        self.grammar = grammar
        self.parsing_table = parsing_table
        self.productions = self.extract_productions()

    def extract_productions(self):
        productions = []
        for lhs, rhs_list in self.grammar.items():
            for rhs in rhs_list:
                productions.append((lhs, rhs))  
        return productions

    def parse(self, input_string):
        stack = [0]  
        pointer = 0
        tokens = list(input_string) + ['$']  
        steps = []  

        while True:
            state = stack[-1]  
            symbol = tokens[pointer]  

            step = {
                "stack": stack[:],  
                "remaining_input": "".join(tokens[pointer:]),
                "action": "",
            }

            if state in self.parsing_table and symbol in self.parsing_table[state]:
                action, value = self.parsing_table[state][symbol]

                if action == 'shift':
                    step["action"] = f"SHIFT to state {value}"
                    stack.append(symbol)
                    stack.append(value)
                    pointer += 1

                elif action == 'reduce':
                    lhs, rhs = self.productions[value]
                    step["action"] = f"REDUCE using {lhs} -> {' '.join(rhs)}"

                    for _ in range(2 * len(rhs)):  
                        stack.pop()

                    prev_state = stack[-1]  
                    
                    stack.append(lhs)

                    if lhs in self.parsing_table[prev_state]:
                        new_state = self.parsing_table[prev_state][lhs][1]
                        stack.append(new_state)
                    else:
                        step["action"] = "❌ No GOTO action found"
                        steps.append(step)
                        return {"result": "Rejected", "steps": steps}

                elif action == 'accept':
                    step["action"] = "✅ Input Accepted!"
                    steps.append(step)
                    return {"result": "Accepted", "steps": steps}

            else:
                step["action"] = "❌ No valid action found"
                steps.append(step)
                return {"result": "Rejected", "steps": steps}

            steps.append(step)
