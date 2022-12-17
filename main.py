import kivy
kivy.require("2.0.0")
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.utils import get_color_from_hex
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
import sqlite3

# Alterar a cor do fundo
Window.clearcolor = get_color_from_hex("#F4F7F5")

# Animação ao ocultar ou exibir o teclado
Window.keyboard_anim_args = {'d':0.2, 't': 'in_out_expo'}
# Reajusta a tela ao exibir o teclado
Window.softinput_mode = "resize"

# Classe do gerenciador de telas
class Gerenciador(ScreenManager):
    pass

# Classe da tela sobre
class TelaSobre(Screen):
    pass


# Classe da TelaTarefas
class TelaTarefas(Screen):

    # Método que adiciona o widget NovoItem no widget de id=box
    def addWidget(self):
        txt = self.ids.txt.text
        status = "False"
        # Connect to database and insert a record
        con = sqlite3.connect("tarefas.db")
        c = con.cursor()
        c.execute("INSERT INTO tarefas VALUES(:txt, :status)",
                  {
                      "txt": txt,
                      "status": status
                  })
        con.commit()
        con.close()
        # Add widget Item to GridLayout
        self.ids.box.add_widget(NovoItem(texto=txt))
        self.ids.txt.text = ""

# Classe do Item da lista de tarefas
class NovoItem(BoxLayout):
    # Método Builder
    def __init__(self, texto="", status="False"):
        super().__init__()
        self.ids.txtlabel.text = texto

        con = sqlite3.connect("tarefas.db")
        c = con.cursor()
        c.execute("SELECT * FROM tarefas WHERE tarefa = (:tarefa)",
                  {
                      "tarefa": texto
                  })
        records = c.fetchall()
        if records[0][1] == "True":
            self.ids.cb.active = True
        con.commit()
        con.close()


    # Método para alterar a cor da label de acordo com o CheckBox
    def changeColor(self):
        tarefa = self.ids.txtlabel.text
        if self.ids.cb.active == True:
            self.ids.txtlabel.color = get_color_from_hex("#268C20")

            status = "True"

            con = sqlite3.connect("tarefas.db")
            c = con.cursor()
            c.execute("UPDATE tarefas SET status = (:status) WHERE tarefa = (:tarefa)",
                      {
                          "status": status,
                          "tarefa": tarefa
                      })
            con.commit()
            con.close()
        else:
            self.ids.txtlabel.color = 0,0,0,1

            status = "False"

            con = sqlite3.connect("tarefas.db")
            c = con.cursor()
            c.execute("UPDATE tarefas SET status = (:status) WHERE tarefa = (:tarefa)",
                      {
                          "status": status,
                          "tarefa": tarefa
                      })
            con.commit()
            con.close()

    # DELETE RECORD FROM DATABASE
    def delTarefa(self):
        txt = self.ids.txtlabel.text
        # Connect to database and delete a record
        con = sqlite3.connect("tarefas.db")
        c = con.cursor()
        c.execute("DELETE FROM tarefas WHERE tarefa = (?)", (txt,))
        con.commit()
        con.close()

class tela_tarefas(App):
    def build(self):
        return Gerenciador()

    def on_start(self):
        # CREATE A DATABASE TABLE IF NOT EXIST
        con = sqlite3.connect("tarefas.db")
        c = con.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS tarefas(
            tarefa text,
            status text
        )""")
        con.commit()
        con.close()

        # LOAD DATABASE AND CREATE WIDGETS ITEM
        con = sqlite3.connect("tarefas.db")
        c = con.cursor()
        c.execute("SELECT DISTINCT tarefa FROM tarefas")
        records = c.fetchall()
        for record in records:
            i = 0
            self.root.get_screen("TelaTarefas").ids.box.add_widget(NovoItem(texto="%s" % record[i]))
            i += 1
        con.commit()
        con.close()


if __name__ == "__main__":
    tela_tarefas().run()
