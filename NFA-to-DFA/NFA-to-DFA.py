import json
from itertools import chain, combinations


def read_nfa(file_path):
    
    with open(file_path, 'r') as f:
        return json.load(f)


def powerset(iterable):
    
    s = list(iterable)
    return list(chain.from_iterable(combinations(s, r) for r in range(len(s) + 1)))


def nfa_to_dfa(nfa):
    

    alphabet = nfa["alphabet"]
    transitions = nfa["transiction"]
    initial_state = nfa["initial_state"]
    end_states = nfa["end_state"]

    
    nfa_transitions = {}
    for t in transitions:
        init, symbol, end = t["initial"], t["symbol"], t["end"]
        if end == "null":
            end = []
        if (init, symbol) not in nfa_transitions:
            nfa_transitions[(init, symbol)] = set()
        nfa_transitions[(init, symbol)].update(end)

    
    dfa_states = []
    dfa_transitions = []
    dfa_start = frozenset([initial_state])
    dfa_states.append(dfa_start)

    visited = set()
    queue = [dfa_start]

    while queue:
        current = queue.pop(0)
        if current in visited:
            continue
        visited.add(current)

        for symbol in alphabet:
            new_state = set()
            for substate in current:
                new_state.update(nfa_transitions.get((substate, symbol), []))

            new_state = frozenset(new_state)
            if new_state:
                dfa_transitions.append({
                    "initial": ",".join(sorted(current)),
                    "symbol": symbol,
                    "end": [",".join(sorted(new_state))]
                })
                if new_state not in dfa_states:
                    dfa_states.append(new_state)
                    queue.append(new_state)

    
    dfa_final_states = []
    for state in dfa_states:
        if any(s in end_states for s in state):
            dfa_final_states.append(",".join(sorted(state)))

    
    dfa = {
        "alphabet": alphabet,
        "states": [",".join(sorted(s)) for s in dfa_states],
        "transiction": dfa_transitions,
        "initial_state": ",".join(sorted(dfa_start)),
        "end_state": dfa_final_states
    }

    return dfa


def save_dfa(dfa, file_path):
    
    with open(file_path, 'w') as f:
        json.dump(dfa, f, indent=4)


def print_dfa(dfa):
    
    print("\n=== DFA GERADO ===")
    print("Alfabeto:", dfa["alphabet"])
    print("Estados:", dfa["states"])
    print("Estado inicial:", dfa["initial_state"])
    print("Estados finais:", dfa["end_state"])
    print("\nTransições:")
    for t in dfa["transiction"]:
        print(f"  δ({t['initial']}, {t['symbol']}) → {t['end']}")


if __name__ == "__main__":
    
    input_file = "/home/italo/Área de trabalho/italo/avaliação/exemplo01.json"   #mudar o numero do exemplo para executar os outros json
    output_file = "dfa.json"  

    nfa = read_nfa(input_file)
    dfa = nfa_to_dfa(nfa)
    save_dfa(dfa, output_file)
    print_dfa(dfa)  

    print("\nConversão concluída! DFA salvo em", output_file)
