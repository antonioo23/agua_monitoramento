import tkinter as tk
from tkinter import messagebox


class MonitoramentoConsumoAgua:
    def __init__(self):
        self.usuarios = {}

    def cadastrar_usuario(self, nome):
        if nome in self.usuarios:
            return f"Erro: Usuário '{nome}' já está cadastrado."
        self.usuarios[nome] = []
        return f"Usuário '{nome}' cadastrado com sucesso!"

    def registrar_consumo(self, nome, consumo):
        if nome not in self.usuarios:
            return f"Erro: Usuário '{nome}' não encontrado."
        if consumo < 0:
            return "Erro: Consumo inválido."
        self.usuarios[nome].append(consumo)
        historico = self.usuarios[nome]
        media = sum(historico) / len(historico)
        if consumo > media:
            alerta = "Consumo acima da média!"
        elif consumo < media:
            alerta = "Consumo abaixo da média."
        else:
            alerta = "Consumo dentro da média."
        return f"Histórico: {historico}, Média: {media:.1f}, Alerta: {alerta}"


class App:
    def __init__(self, root):
        self.monitor = MonitoramentoConsumoAgua()

        root.title("Cadastro de Usuários e Consumo")
        root.geometry("500x500")

        self.label_usuario = tk.Label(root, text="Digite o nome do usuário:")
        self.label_usuario.pack(pady=10)

        self.entry_usuario = tk.Entry(root)
        self.entry_usuario.pack(pady=10)

        self.botao_cadastrar = tk.Button(
            root, text="Cadastrar Usuário", command=self.cadastrar_usuario
        )
        self.botao_cadastrar.pack(pady=10)

        self.label_consumo = tk.Label(root, text="Digite o consumo:")
        self.label_consumo.pack(pady=10)

        self.entry_consumo = tk.Entry(root)
        self.entry_consumo.pack(pady=10)

        self.botao_registrar = tk.Button(
            root, text="Registrar Consumo", command=self.registrar_consumo
        )
        self.botao_registrar.pack(pady=10)

        self.label_historico = tk.Label(root, text="Selecione um usuário:")
        self.label_historico.pack(pady=10)

        self.listbox_usuarios = tk.Listbox(root, height=5)
        self.listbox_usuarios.pack(pady=10)
        self.listbox_usuarios.bind("<<ListboxSelect>>", self.mostrar_historico)

        self.historico_texto = tk.Label(root, text="", justify="left", wraplength=450)
        self.historico_texto.pack(pady=20)

    def cadastrar_usuario(self):
        nome = self.entry_usuario.get().strip()
        if not nome:
            messagebox.showerror("Erro", "O nome do usuário não pode ser vazio.")
            return
        resultado = self.monitor.cadastrar_usuario(nome)
        self.listbox_usuarios.insert(tk.END, nome)
        messagebox.showinfo("Cadastro", resultado)
        self.entry_usuario.delete(0, tk.END)

    def registrar_consumo(self):
        nome = self.get_usuario_selecionado()
        if not nome:
            messagebox.showerror("Erro", "Selecione um usuário para registrar consumo.")
            return
        try:
            consumo = int(self.entry_consumo.get())
            resultado = self.monitor.registrar_consumo(nome, consumo)
            if "Erro" in resultado:
                messagebox.showerror("Erro", resultado)
            else:
                messagebox.showinfo("Registro", resultado)
                self.mostrar_historico()
        except ValueError:
            messagebox.showerror("Erro", "Digite um valor numérico válido para o consumo.")
        finally:
            self.entry_consumo.delete(0, tk.END)

    def mostrar_historico(self, event=None):
        nome = self.get_usuario_selecionado()
        if not nome:
            return
        historico = self.monitor.usuarios[nome]
        if historico:
            media = sum(historico) / len(historico)
            texto = f"Histórico de Consumo: {historico}\nMédia: {media:.1f}"
        else:
            texto = "Histórico de consumo vazio."
        self.historico_texto.config(text=texto)

    def get_usuario_selecionado(self):
        try:
            index = self.listbox_usuarios.curselection()[0]
            return self.listbox_usuarios.get(index)
        except IndexError:
            return None


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
