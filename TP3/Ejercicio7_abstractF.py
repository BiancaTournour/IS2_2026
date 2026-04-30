#Imagine una situación donde pueda ser de utilidad el patrón “abstract factory”

from abc import ABC, abstractmethod

#En este ejemplo, se implementa el patrón Abstract Factory para crear interfaces gráficas de usuario (GUI) para diferentes sistemas operativos (Windows y Linux)
#La fábrica abstracta define métodos para crear componentes de la GUI, como botones y ventanas, y las fábricas concretas implementan estos métodos para cada sistema operativo específico
class Button(ABC):
    @abstractmethod
    def render(self):
        pass

class Window(ABC):
    @abstractmethod
    def render(self):
        pass

#Productos concretos Windows
class WindowsButton(Button):
    def render(self):
        return "Renderizando botón de Windows"
    
class WindowsWindow(Window):
    def render(self):
        return "Renderizando ventana de Windows"    
    
#Productos Concretos LINUX
class LinuxButton(Button):
    def render(self):
        return "Renderizando botón de Linux"
    
class LinuxWindow(Window):
    def render(self):
        return "Renderizando ventana de Linux"
    
#ABSTRACT FACTOTY USO
class GUIFactory(ABC):
    @abstractmethod
    def create_button(self):
        pass
    
    @abstractmethod
    def create_window(self):
        pass

class WindowsFactory(GUIFactory):
    def create_button(self):
        return WindowsButton()
    
    def create_window(self):
        return WindowsWindow()

class LinuxFactory(GUIFactory):
    def create_button(self):
        return LinuxButton()
    
    def create_window(self):
        return LinuxWindow()

def render_ui(factory: GUIFactory):
    button = factory.create_button()
    window = factory.create_window()
    print(button.render())
    print(window.render())

#se elige una o la otra dependiendo del sistema operativo
render_ui(WindowsFactory())
render_ui(LinuxFactory()) 