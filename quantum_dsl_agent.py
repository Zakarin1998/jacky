# quantum_dsl_agent.py

import re
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import logging
import datetime
import textwrap
import json

# Configurazione logging
logging.basicConfig(
    filename='qdsl_agent_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class KnowledgeBase:
    """
    KB minimale con formule e descrizioni.
    """
    def __init__(self):
        self.formulas = {
            'Bohr': 'E_n = -13.6 eV / n^2',
            'PhotonEnergy': 'E = h * f',
            'TunnelProb': 'T ≈ exp(-2 * κ * d)',
        }
        self.descriptions = {
            'Bohr': "Livelli discreti di energia nell'atomo di idrogeno",
            'PhotonEnergy': "Energia di un fotone in funzione della frequenza",
            'TunnelProb': "Probabilità di tunneling attraverso barriera di potenziale",
        }

    def get_all(self):
        return self.formulas, self.descriptions


class QuantumDSLInterpreter:
    def __init__(self):
        self.state_graph = nx.DiGraph()
        self.registers = {}
        self.probabilities = {}
        self.events = []

    def log(self, msg):
        print(msg)
        logging.info(msg)

    def parse_line(self, line):
        line = line.strip()
        if not line or line.startswith('#'):
            return
        patterns = [
            (r'observe\(([^)]+)\)', lambda m: self._obs(m.group(1))),
            (r'intent\("(.+?)"\)\s*=>\s*collapse_to\(([^)]+)\)',
             lambda m: self._intent(m.group(1), m.group(2))),
            (r'event\("(.+?)"\)\s*=>\s*classify\(([^)]+)\)\s*=\s*([^ ]+)',
             lambda m: self._event(m.group(1), m.group(3))),
            (r'register\s+([^\s=]+)\s*=\s*state\("(.+?)"\)',
             lambda m: self._register(m.group(1), m.group(2))),
            (r'decohere\(([^)]+)\)\s*->\s*([^\s]+)',
             lambda m: self._decohere(m.group(1), m.group(2))),
            (r'multiverse_jump\s+from\s+([^\s]+)\s+to\s+(.+)',
             lambda m: self._jump(m.group(1), m.group(2))),
            (r'entangle\("([^"]+)"\s*,\s*"([^"]+)"\)',
             lambda m: self._entangle(m.group(1), m.group(2))),
            (r'hypothesis\("(.+?)"\s*,\s*([0-9]*\.?[0-9]+)\)',
             lambda m: self._hypothesis(m.group(1), m.group(2))),
            (r'normalize\(\)', lambda m: self._normalize()),
        ]
        for pattern, action in patterns:
            m = re.match(pattern, line)
            if m:
                action(m)
                return
        self.log(f"[WARN] Comando non riconosciuto: {line}")

    # Handlers
    def _obs(self, symbol):
        self.log(f"[OBSERVE] {symbol}")
        self.events.append(('observe', symbol))

    def _intent(self, text, tgt):
        self.log(f"[INTENT] '{text}' -> {tgt}")
        self.state_graph.add_edge(f"intent:{text}", tgt)

    def _event(self, text, omega):
        self.log(f"[EVENT] '{text}' = {omega}")
        self.state_graph.add_edge(f"event:{text}", omega)

    def _register(self, label, desc):
        self.log(f"[REGISTER] {label} = '{desc}'")
        self.registers[label] = desc

    def _decohere(self, src, tgt):
        self.log(f"[DECOHERE] {src} -> {tgt}")
        self.state_graph.add_edge(src, tgt, label='decohere')

    def _jump(self, src, dst):
        self.log(f"[JUMP] {src} -> {dst}")
        self.state_graph.add_edge(src, dst, label='jump')

    def _entangle(self, a, b):
        self.log(f"[ENTANGLE] {a} <-> {b}")
        self.state_graph.add_edge(a, b, label='entangle')
        self.state_graph.add_edge(b, a, label='entangle')

    def _hypothesis(self, lbl, prob):
        self.probabilities[lbl] = float(prob)
        self.log(f"[HYPOTHESIS] {lbl} = {prob}")

    def _normalize(self):
        total = sum(self.probabilities.values()) or 1.0
        for k in self.probabilities:
            self.probabilities[k] /= total
        self.log(f"[NORMALIZE] {self.probabilities}")

    # Plotting
    def plot_graph(self, ax=None):
        if ax is None:
            fig, ax = plt.subplots(figsize=(6, 5))
        pos = nx.circular_layout(self.state_graph)
        nx.draw(self.state_graph, pos, ax=ax, with_labels=True,
                node_size=600, node_color='lightblue')
        labels = nx.get_edge_attributes(self.state_graph, 'label')
        nx.draw_networkx_edge_labels(self.state_graph, pos, edge_labels=labels, ax=ax)
        ax.set_title('Grafo Stati Quantistici')

    def plot_probabilities(self, ax=None):
        if not self.probabilities:
            return
        if ax is None:
            fig, ax = plt.subplots(figsize=(5, 3))
        keys, vals = zip(*self.probabilities.items())
        ax.bar(keys, vals)
        ax.set_xticklabels(keys, rotation=45, ha='right')
        ax.set_title('Probabilità Ipotesi')
        ax.grid(True)

    def generate_formula_graphs(self, kb, ax_list):
        # Grafico di esempio: valori di energia fotone vs frequenza
        f = [1e14 * i for i in range(1, 6)]
        h = 6.626e-34
        E = [h * freq for freq in f]
        ax = ax_list[0]
        ax.plot(f, E)
        ax.set_xlabel('Frequenza (Hz)')
        ax.set_ylabel('Energia (J)')
        ax.set_title('E = h·f')

        # Dummy grafico tunnel
        d = [1, 2, 3, 4]
        T = [0.1 * (0.5**x) for x in d]
        ax = ax_list[1]
        ax.plot(d, T)
        ax.set_xlabel('Spessore barriera')
        ax.set_ylabel('Probabilità Tunnel')
        ax.set_title('Tunneling quantistico')

    # Report V2
    def save_report_v2(self, pdf_path='report_v2_qdsl.pdf'):
        wrap = lambda s: '\n'.join(textwrap.wrap(s, width=70))
        kb = KnowledgeBase()
        formulas, descs = kb.get_all()

        with PdfPages(pdf_path) as pdf:
            # Intro
            fig, ax = plt.subplots(figsize=(8,6))
            ax.axis('off')
            intro = (
                f"Report V2: {datetime.datetime.now():%Y-%m-%d %H:%M}\n"
                "Quantum DSL Agent comprehensive analysis\n\n"
                "Contenuto:\n"
                "- Grafi di stati\n"
                "- Probabilità delle ipotesi\n"
                "- Grafici di formule base da KB\n"
            )
            ax.text(0.1,0.5, wrap(intro), fontsize=12)
            pdf.savefig()
            plt.close(fig)

            # Stati + Probabilità
            fig, axs = plt.subplots(1,2, figsize=(12,5))
            self.plot_graph(ax=axs[0])
            self.plot_probabilities(ax=axs[1])
            pdf.savefig()
            plt.close(fig)

            # Formule e descrizioni
            fig, ax = plt.subplots(figsize=(8,6))
            ax.axis('off')
            text = "Formule dalla Knowledge Base:\n"
            for k,v in formulas.items():
                text += f"\n{k}: {v}  ({descs[k]})"
            ax.text(0.05,0.95, wrap(text), va='top', fontsize=10)
            pdf.savefig()
            plt.close(fig)

            # Grafici di formule
            fig, axs = plt.subplots(1,2, figsize=(12,5))
            self.generate_formula_graphs(kb, axs)
            pdf.savefig()
            plt.close(fig)

    def run(self, filename):
        self.log(f"Caricamento file: {filename}")
        with open(filename, encoding='utf-8') as f:
            for line in f:
                self.parse_line(line)
        # Report v1
        self.plot_graph()
        self.plot_probabilities()
        PdfPages('report_v1_qdsl.pdf').savefig()
        plt.show()

    def run_v2(self, filename):
        self.log(f"Caricamento file: {filename}")
        with open(filename, encoding='utf-8') as f:
            for line in f:
                self.parse_line(line)
        self.save_report_v2()
        plt.show()

# MAIN
if __name__ == '__main__':
    agent = QuantumDSLInterpreter()
    agent.run_v2('esempio_3.qdsl')   # Report v2  
