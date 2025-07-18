# quantum_dsl_parser.py

import re
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import logging
import datetime
import textwrap

# Configurazione logging
logging.basicConfig(
    filename='qdsl_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class QuantumDSLInterpreter:
    """
    Interpreter esteso per Quantum DSL con:
    - Logging dettagliato
    - Modularizzazione in funzioni
    - Grafici multipli (grafo, probabilità)
    - Report PDF migliorato con wrapping del testo
    """
    def __init__(self):
        self.state_graph    = nx.DiGraph()
        self.registers      = {}
        self.probabilities  = {}
        self.normalized     = False
        self.events         = []  # lista di eventi per timeline

    def log(self, level, msg):
        print(msg)
        if level == 'info':    logging.info(msg)
        elif level == 'warning': logging.warning(msg)
        elif level == 'error':   logging.error(msg)

    def parse_line(self, line):
        line = line.strip()
        if not line or line.startswith('#'):
            return

        # observe(<symbol>)
        if m := re.match(r'observe\(([^)]+)\)', line):
            symbol = m.group(1)
            self.log('info', f"[OBSERVE] Sospensione collasso: {symbol}")
            self.events.append(('observe', symbol))
            return

        # intent -> collapse
        if m := re.match(r'intent\("(.+?)"\)\s*=>\s*collapse_to\(([^)]+)\)', line):
            intent_text, target = m.groups()
            self.log('info', f"[INTENT] '{intent_text}' -> {target}")
            self.state_graph.add_node(target)
            self.state_graph.add_edge(f"intent:{intent_text}", target)
            self.events.append(('intent', intent_text))
            return

        # event -> classify(state) = symbol
        if m := re.match(r'event\("(.+?)"\)\s*=>\s*classify\(([^)]+)\)\s*=\s*([^ ]+)', line):
            event_text, class_target, omega = m.groups()
            self.log('info', f"[EVENT] '{event_text}' classified {class_target} = {omega}")
            self.state_graph.add_edge(f"event:{event_text}", omega)
            self.events.append(('event', event_text))
            return

        # register state
        if m := re.match(r'register\s+([^\s=]+)\s*=\s*state\("(.+?)"\)', line):
            label, desc = m.groups()
            self.registers[label] = desc
            self.log('info', f"[REGISTER] {label} = '{desc}'")
            return

        # loop placeholder
        if m := re.match(r'while\s+not\s+in_state\(([^)]+)\):', line):
            label = m.group(1)
            self.log('info', f"[LOOP] fino a {label}")
            return

        # condition
        if m := re.match(r'if\s+\(([^ ]+)\s+(AND|OR|XOR|IMPLIES)\s+(NOT\s+)?([^)]+)\):', line):
            a, op, not_kw, b = m.groups()
            cond = f"{a} {op} {b}" if not not_kw else f"{a} {op} NOT {b}"
            self.log('info', f"[IF] {cond}")
            return

        # gate definition
        if m := re.match(r'gate\s+(\w+)\(([^)]+)\)\s*=\s*(.+)', line):
            gate_name, inp, expr = m.groups()
            self.log('info', f"[GATE] {gate_name} on {inp}: {expr}")
            return

        # use gate
        if m := re.match(r'use\s+gate\s+(\w+)\s+on\s+([^\s]+)', line):
            gate_name, target = m.groups()
            self.log('info', f"[USE] gate {gate_name} -> {target}")
            return

        # decoherence
        if m := re.match(r'decohere\(([^)]+)\)\s*->\s*([^\s]+)', line):
            src, tgt = m.groups()
            self.log('info', f"[DECOHERE] {src} -> {tgt}")
            self.state_graph.add_edge(src, tgt, label='decohere')
            return

        # multiverse jump
        if m := re.match(r'multiverse_jump\s+from\s+([^\s]+)\s+to\s+(.+)', line):
            src, dst = m.groups()
            self.log('info', f"[JUMP] {src} -> {dst}")
            self.state_graph.add_edge(src, dst, label='jump')
            return

        # entangle("A","B")
        if m := re.match(r'entangle\("([^"]+)"\s*,\s*"([^"]+)"\)', line):
            a, b = m.groups()
            self.log('info', f"[ENTANGLE] {a} entangled with {b}")
            self.state_graph.add_edge(a, b, label='entangle')
            return

        # hypothesis
        if m := re.match(r'hypothesis\("(.+?)"\s*,\s*([0-9]*\.?[0-9]+)\)', line):
            lbl, prob = m.groups()
            self.probabilities[lbl] = float(prob)
            self.log('info', f"[HYPOTHESIS] {lbl} = {prob}")
            return

        # normalize
        if line == 'normalize()':
            total = sum(self.probabilities.values()) or 1.0
            for k in self.probabilities:
                self.probabilities[k] /= total
            self.normalized = True
            self.log('info', f"[NORMALIZE] {self.probabilities}")
            return

        self.log('warning', f"Comando non riconosciuto: {line}")

    def plot_graph(self):
        pos = nx.circular_layout(self.state_graph)
        labels = nx.get_edge_attributes(self.state_graph, 'label')
        plt.figure(figsize=(8, 6))
        nx.draw(self.state_graph, pos, with_labels=True, node_size=800,
                node_color='lightgreen', font_size=10)
        nx.draw_networkx_edge_labels(self.state_graph, pos, edge_labels=labels)
        plt.title('Stati e Transizioni Quantistiche')

    def plot_probabilities(self):
        if not self.probabilities:
            return
        plt.figure(figsize=(6, 4))
        keys = list(self.probabilities.keys())
        vals = [self.probabilities[k] for k in keys]
        plt.bar(keys, vals)
        plt.xticks(rotation=45, ha='right')
        plt.title('Probabilità Ipotesi')
        plt.tight_layout()

    def save_report(self, pdf_path='report_qdsl.pdf'):
        wrap = lambda s: '\n'.join(textwrap.wrap(s, width=70))
        with PdfPages(pdf_path) as pdf:
            # Intro page
            fig = plt.figure(figsize=(8, 6))
            plt.axis('off')
            intro_text = (
                f"Report Generato: {datetime.datetime.now():%Y-%m-%d %H:%M}\n"
                "Quantum DSL Analysis\n\n"
                "Descrizione: Questo documento contiene il grafo degli stati mentali, "
                "le probabilità delle ipotesi inserite e il log degli eventi parsati."
            )
            plt.text(0.1, 0.5, wrap(intro_text), fontsize=11)
            pdf.savefig(fig)
            plt.close(fig)

            # Grafo
            self.plot_graph()
            pdf.savefig()
            plt.close()

            # Probabilità
            self.plot_probabilities()
            pdf.savefig()
            plt.close()

    def run(self, filename):
        self.log('info', f"Caricamento file: {filename}")
        with open(filename, encoding='utf-8') as f:
            for line in f:
                self.parse_line(line)
        # Genera grafici e report
        self.plot_graph()
        self.plot_probabilities()
        self.save_report()
        plt.show()


# ESEMPIO DI UTILIZZO
if __name__ == '__main__':
    qdsl = QuantumDSLInterpreter()
    esempio_1 = "esempio_1.qdsl"
    esempio_2 = "esempio_2.qdsl"
    esempio_3 = "esempio_3.qdsl"
    qdsl.run('esempio_3.qdsl')
