import csv
import tkinter as tk
from tkinter import ttk

# Função para consultar os dados no arquivo CSV
def consultar_dados(condicoes):
    resultados = []
    with open(caminho_arquivo, 'r') as arquivo_csv:
        leitor_csv = csv.DictReader(arquivo_csv)
        for linha in leitor_csv:
            if all(condicao(linha) for condicao in condicoes.values()):
                resultados.append(linha)
    return resultados

class ConsultaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Consulta de Dados Profissional")
        self.root.geometry("1000x600")

        self.analista_label = tk.Label(self.root, text="Analista:")
        self.analista_combo = ttk.Combobox(self.root, values=["Analista 1", "Analista 2", "Analista 3"])
        self.conta_contabil_label = tk.Label(self.root, text="Conta Contábil:")
        self.conta_contabil_combo = ttk.Combobox(self.root, values=["Conta 1", "Conta 2", "Conta 3"])
        self.valor_label = tk.Label(self.root, text="Valor:")
        self.valor_entry = tk.Entry(self.root)
        self.filtro_button = tk.Button(self.root, text="Filtrar", command=self.exibir_resultados)

        self.resultados_tree = ttk.Treeview(self.root, columns=("Código Empresa", "Nome da Empresa", "Analista", "Conta Financeira", "Conta Contábil", "Data de Abertura", "Histórico", "Sinal Atual", "Valor Atual", "Status"), show="headings")
        self.resultados_tree.heading("Código Empresa", text="Código Empresa")
        self.resultados_tree.heading("Nome da Empresa", text="Nome da Empresa")
        self.resultados_tree.heading("Analista", text="Analista")
        self.resultados_tree.heading("Conta Financeira", text="Conta Financeira")
        self.resultados_tree.heading("Conta Contábil", text="Conta Contábil")
        self.resultados_tree.heading("Data de Abertura", text="Data de Abertura")
        self.resultados_tree.heading("Histórico", text="Histórico")
        self.resultados_tree.heading("Sinal Atual", text="Sinal Atual")
        self.resultados_tree.heading("Valor Atual", text="Valor Atual")
        self.resultados_tree.heading("Status", text="Status")

        self.analista_label.pack()
        self.analista_combo.pack()
        self.conta_contabil_label.pack()
        self.conta_contabil_combo.pack()
        self.valor_label.pack()
        self.valor_entry.pack()
        self.filtro_button.pack()
        self.resultados_tree.pack()

    def exibir_resultados(self):
        condicoes = {
            "Analista": lambda linha: linha['Analista'] == self.analista_combo.get(),
            "Conta Contábil": lambda linha: linha['Conta Contábil'] == self.conta_contabil_combo.get(),
            "Valor Atual": lambda linha: linha['Valor Atual'] == self.valor_entry.get()
        }
        resultados = consultar_dados(condicoes)

        for linha in self.resultados_tree.get_children():
            self.resultados_tree.delete(linha)

        for resultado in resultados:
            self.resultados_tree.insert("", "end", values=(resultado['Código Empresa'], resultado['Nome da Empresa'], resultado['Analista'], resultado['Conta Financeira'], resultado['Conta Contábil'], resultado['Data de Abertura'], resultado['Histórico'], resultado['Sinal Atual'], resultado['Valor Atual'], resultado['Status']))

if __name__ == "__main__":
    caminho_arquivo = 'caminho/para/o/arquivo.csv'

    root = tk.Tk()
    app = ConsultaApp(root)
    root.mainloop()
