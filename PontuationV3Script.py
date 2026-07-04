import tkinter as tk
import random as rng
import pygame as pg

root = tk.Tk()
root.geometry("400x300")
pg.init()
pg.mixer.init()
volume = 50
winSFX = pg.mixer.Sound("WinEffect.mp3")

# Começa com o Light Mode (1) selecionado por padrão
V1 = tk.IntVar(value=1)

# Definições de Cores
WhiteBG = "#ffffff"
WhiteFG = "#1e1e1e"
WhiteBTN_BG = "#f0f0f0"

BlackBG = "#1e1e1e"
BlackFG = "#ffffff"
BlackBTN_BG = "#2e2e2e"

# FUNÇÃO NOVA: Garante que tudo que for criado na tela adote o tema atual
def applyTheme(widget=None):
    if widget is None:
        widget = root
        
    bg, fg, btn_bg = getTheme()
    
    # Aplica a cor de fundo na janela principal ou frames
    if widget == root:
        root.configure(bg=bg)
        
    # Verifica o tipo de componente para aplicar a cor certa
    if isinstance(widget, (tk.Label, tk.Message, tk.Radiobutton, tk.Scale)):
        widget.configure(bg=bg, fg=fg)
    elif isinstance(widget, tk.Button):
        widget.configure(bg=btn_bg, fg=fg, activebackground=btn_bg, activeforeground=fg)
    elif isinstance(widget, tk.Entry):
        widget.configure(bg=btn_bg, fg=fg, insertbackground=fg) # insertbackground muda a cor do cursor piscando

    # Passa recursivamente por todos os componentes filhos
    for child in widget.winfo_children():
        applyTheme(child)

def getTheme():
    if V1.get() == 2:
        return BlackBG, BlackFG, BlackBTN_BG
    return WhiteBG, WhiteFG, WhiteBTN_BG

def clean():
    for widget in root.winfo_children():
        widget.destroy()

def TelaInfo():
    clean()
    info = "This is a simple game made by Wellington, powered by Python 3.13."
    tk.Label(root, text=info, wraplength=300).pack(pady=20)
    tk.Button(root, text="Return", command=menu).pack()
    applyTheme() # Atualiza o tema dos novos elementos

def GameScreen():
    clean()
    tk.Label(root, text="[Gamemodes]").pack()
    tk.Button(root, text="Normal", command=Normal).pack()
    applyTheme() # Atualiza o tema dos novos elementos

def Settings():
    clean()
    tk.Label(root, text="[Settings]").pack()
    global volume
    scale = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, label="Volume")
    scale.pack()
    scale.set(volume)

    def saveVolume():
        global volume
        volume = scale.get()
        menu()

    # Mudamos o comando para aplicar o tema assim que clicar no Radiobutton
    tk.Radiobutton(root, text="Light Mode", variable=V1, value=1, command=applyTheme).pack()
    tk.Radiobutton(root, text="Dark Mode", variable=V1, value=2, command=applyTheme).pack()
    tk.Button(root, text="Save", command=saveVolume).pack()
    tk.Button(root, text="Return", command=menu).pack()
    applyTheme() # Atualiza o tema dos novos elementos

def Normal():
    clean()
    pg.mixer.music.stop()
    valor = rng.randint(1, 100)
    Call = "I chosen a number between 1 and 100. Try to guess it!"
    Enun = tk.Message(root, text=Call, width=300)
    Enun.pack()
    answer = tk.Entry(root)
    answer.pack()

    resultado_label = tk.Label(root, text="")
    resultado_label.pack()
    print(valor)  
    returnButton = tk.Button(root, text="Return", command=menu)
    pg.mixer.music.load("MainGameTheme.mp3")
    pg.mixer.music.play(-1)  

    def verify():
        try:
            tentativa = int(answer.get())
        except ValueError:
            resultado_label.config(text="Please enter a valid number.")
            return
        if tentativa < valor:
            resultado = "Too low! Try again."
        elif tentativa > valor:
            resultado = "Too high! Try again."
        else:
            resultado = "Congratulations! You got it right!"
            returnButton.pack()
            verifyButton.destroy()
            pg.mixer.music.stop()
            winSFX.play()
        resultado_label.config(text=resultado)
        applyTheme() 

    verifyButton = tk.Button(root, text="Verify", command=verify)
    verifyButton.pack()
    applyTheme() # Atualiza o tema dos novos elementos

def menu():
    clean()
    bg, _, _ = getTheme()
    root.configure(bg=bg)
    
    tk.Label(root, text="[Pontuation V2.3]").pack(pady=20)
    tk.Button(root, text="Start", command=GameScreen).pack()
    tk.Button(root, text="Info", command=TelaInfo).pack()
    tk.Button(root, text="Settings", command=Settings).pack()
    tk.Button(root, text="Quit", command=root.quit).pack()
    
    pg.mixer.music.load("MenuTheme.mp3")
    pg.mixer.music.set_volume(volume / 100)
    pg.mixer.music.play(-1)
    applyTheme() # Aplica o tema em tudo do menu

menu()
root.mainloop()