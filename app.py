from flask import Flask, render_template, request, jsonify
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from slr_parser import SLRParser

app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), './templates'),
    static_folder=os.path.join(os.path.dirname(__file__), './static')
)

grammar = {}
parsing_table = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_grammar', methods=['POST'])
def upload_grammar():
    global grammar

    # ✅ Extract grammar correctly from JSON
    grammar_input = request.json.get("grammar", [])

    grammar = {}

    for rule in grammar_input:
        rule = rule.strip()
        if not rule or "->" not in rule:
            print(f"Skipping invalid rule: [{rule}] (possibly empty or missing '->')")
            continue

        parts = rule.split("->")

        if len(parts) != 2:
            print(f"Skipping invalid rule: [{rule}] (unexpected format)")
            continue  # Avoids crashing on bad input

        lhs, rhs = parts[0].strip(), parts[1].strip()

        print(f"Processed: LHS = [{lhs}], RHS = [{rhs}]")  # Debugging

        rhs_tokens = rhs.split()
        print(f"Final Stored Rule: {lhs} -> {rhs_tokens}")  # Debugging

        if lhs in grammar:
            grammar[lhs].append(rhs_tokens)
        else:
            grammar[lhs] = [rhs_tokens]

    print("\n✅ Uploaded Grammar:")
    for key, values in grammar.items():
        for value in values:
            print(f"{key} -> {' '.join(value)}")

    return jsonify({"message": "Grammar uploaded successfully", "grammar": grammar})

@app.route('/upload_table', methods=['POST'])
def upload_table():
    global parsing_table
    raw_table = request.json.get('table', {})

    parsing_table = {int(state): transitions for state, transitions in raw_table.items()}

    for state, transitions in parsing_table.items():
        for symbol, action in transitions.items():
            if isinstance(action[1], str) and action[1].isdigit():
                parsing_table[state][symbol][1] = int(action[1])

    print("\n✅ Uploaded Parsing Table:")
    for state, transitions in parsing_table.items():
        print(f"State {state}: {transitions}")

    return jsonify({"message": "Parsing table uploaded successfully", "table": parsing_table})


@app.route('/parse', methods=['POST'])
def parse():
    input_string = request.json['input_string']
    parser = SLRParser(grammar, parsing_table)
    result = parser.parse(input_string)
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
