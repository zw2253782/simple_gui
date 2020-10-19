import os

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.loader import Loader
from kivy.uix.button import Button 
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.lang.builder import Builder
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.graphics import Rectangle, Color,Rotate
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout

firstImagePath = ""

class LoadScreen(Screen):
    pass

class DisplayScreen(Screen):
    def on_enter(self):
        child = self.children[0]
        child.state = 1
        child.update_rect()
    pass

class ScreenTransition(ScreenManager):
    pass
    
class Home(FloatLayout):
    def __init__(self, **kwargs):
        super(Home, self).__init__(**kwargs)

        self.menuLayout = GridLayout(cols=1,pos_hint= {'x':0.25,'y':0.25}, size_hint =(0.5, 0.5),row_force_default = True, row_default_height = 40,padding = 20,spacing=[10,10])
        self.add_widget(self.menuLayout)
        
        self.menuLayout.add_widget(Label(text='Welcome to use the Image File Loader.\nValid file types include \"*.jpg\" and \"*.png\"',font_size = 30, color = (1,0,1,0.6)))

        self.menuLayout.add_widget(Label(text='Enter the file path below and click the button:',font_size = 20))
        self.inputText = TextInput()
        self.menuLayout.add_widget(self.inputText)

        self.loadButton = Button(text='Load A New File')
        self.menuLayout.add_widget(self.loadButton)
        self.loadButton.bind(on_press=self.loadButtonPressed)
        
    def loadButtonPressed(self, instance):
        path = self.inputText.text
        fileType = path.split(".")[-1]
        if not os.path.isfile(path):
            self.popup_invalid_path()
        elif (fileType != "jpg") and (fileType != "png"):
            self.popup_invalid_fileType()
        else:
            layout = self.parent.parent.get_screen("display").children[0].children[0]
            image = Image(source=path)
            imageRatio = image.image_ratio
            with layout.canvas:
                layout.rect = Rectangle(texture=image.texture, size=(layout.height * imageRatio, layout.height))
                layout.rect.pos = (layout.center[0] - layout.rect.size[0] / 2, layout.center[1] - layout.rect.size[1] / 2)
            self.parent.parent.current = "display"



    def popup_invalid_path(self):
        layout = GridLayout(cols = 1, padding = 10) 
  
        popupLabel = Label(text = "Can't find the file path!") 
        closeButton = Button(text = "Close",size_hint=(0.3,0.2)) 
  
        layout.add_widget(popupLabel) 
        layout.add_widget(closeButton)        
  
        popup = Popup(title ='Invalid File Path', 
                      content = layout, 
                      size_hint =(None, None), size =(400, 400))   
        popup.open()     
        closeButton.bind(on_press=popup.dismiss)
        
    def popup_invalid_fileType(self):
        layout = GridLayout(cols = 1, padding = 10) 
  
        popupLabel = Label(text = "Please enter either a png or a jpg file!") 
        closeButton = Button(text = "Close",size_hint=(0.3,0.2)) 
  
        layout.add_widget(popupLabel) 
        layout.add_widget(closeButton)        
  
        popup = Popup(title ='Invalid File Type', 
                      content = layout, 
                      size_hint =(None, None), size =(400, 400))   
        popup.open()    
        closeButton.bind(on_press=popup.dismiss)


class Display(FloatLayout):
    def __init__(self, **kwargs):
        super(Display, self).__init__(**kwargs)
        
        # left side: controlling interfaces
        self.menuLayout = GridLayout(cols=1,size_hint =(0.2, 1),row_force_default = True, row_default_height = 30,padding = 10,spacing=[5,5])
        self.add_widget(self.menuLayout)
        self.menuLayout.add_widget(Label(text='Enter a file path below:'))
        self.inputText = TextInput()
        self.menuLayout.add_widget(self.inputText)

        self.loadButton = Button(text='Load A New File')
        self.menuLayout.add_widget(self.loadButton)
        self.loadButton.bind(on_press=self.loadButtonPressed)
        
        self.resizeLayout = GridLayout(cols=2, size_hint_x=0.2, row_force_default=True, row_default_height=50, padding=10, spacing=[10,10])
        self.menuLayout.add_widget(self.resizeLayout)
        self.inButton = Button(text="+", font_size=50)
        self.inButton.bind(on_press=self.zoonIn)
        self.resizeLayout.add_widget(self.inButton)
        self.outButton = Button(text = "-",font_size = 50)
        self.resizeLayout.add_widget(self.outButton)
        self.outButton.bind(on_press=self.zoomOut)

        # right side: displaying an image
        self.imageLayout = GridLayout(cols=1, size_hint=(0.8, 1),pos_hint={"right":1})
        self.add_widget(self.imageLayout)                

        self.imageLayout.bind(pos=self.update_rect, size=self.update_rect)
        
        self.state = 0
        

    def loadButtonPressed(self, instance):
        path = self.inputText.text
        fileType = path.split(".")[-1]
        if not os.path.isfile(path):
            self.popup_invalid_path()
        elif (fileType != "jpg") and (fileType != "png"):
            self.popup_invalid_fileType()
        else:
            image = Image(source=path)
            self.imageRatio = image.image_ratio
            with self.imageLayout.canvas:
                # if (len(self.imageLayout.canvas.children) != 0):
                #     self.imageLayout.canvas.remove(self.imageLayout.rect)
                self.imageLayout.canvas.clear()
                self.imageLayout.rect = Rectangle(texture=image.texture, size=(self.imageLayout.height / 2 * self.imageRatio, self.imageLayout.height / 2))
                self.imageLayout.rect.pos = (self.imageLayout.center[0] - self.imageLayout.rect.size[0] / 2, self.imageLayout.center[1] - self.imageLayout.rect.size[1] / 2)
            self.state = 1
    
    def update_rect(self, *args): 
        if self.state == 1:
            with self.imageLayout.canvas:
                self.imageLayout.rect.pos = (self.imageLayout.center[0] - self.imageLayout.rect.size[0] / 2, self.imageLayout.center[1] - self.imageLayout.rect.size[1] / 2)


    def popup_invalid_path(self):
        layout = GridLayout(cols = 1, padding = 10) 
  
        popupLabel = Label(text = "Can't find the file path!") 
        closeButton = Button(text = "Close",size_hint=(0.3,0.2)) 
  
        layout.add_widget(popupLabel) 
        layout.add_widget(closeButton)        
  
        popup = Popup(title ='Invalid File Path', 
                      content = layout, 
                      size_hint =(None, None), size =(400, 400))   
        popup.open()    
  
        closeButton.bind(on_press=popup.dismiss)
        
    def popup_invalid_fileType(self):
        layout = GridLayout(cols = 1, padding = 10) 
  
        popupLabel = Label(text = "Please enter either png or jpg file!") 
        closeButton = Button(text = "Close",size_hint=(0.3,0.2)) 
  
        layout.add_widget(popupLabel) 
        layout.add_widget(closeButton)        
  
        popup = Popup(title ='Invalid File Type', 
                      content = layout, 
                      size_hint =(None, None), size =(400, 400))   
        popup.open()    
  
        closeButton.bind(on_press=popup.dismiss)

    def zoonIn(self, instance):
        ratio = 1.1
        with self.imageLayout.canvas:
            if (self.imageLayout.rect.size[0] * ratio <= self.imageLayout.size[0]) and (self.imageLayout.rect.size[1] * ratio <= self.imageLayout.size[1]):  
                self.imageLayout.rect.size = (self.imageLayout.rect.size[0]*ratio,self.imageLayout.rect.size[1]*ratio)
                self.imageLayout.rect.pos = (self.imageLayout.center[0] - self.imageLayout.rect.size[0] / 2, self.imageLayout.center[1] - self.imageLayout.rect.size[1] / 2)


  
    def zoomOut(self, instance):
        ratio = 1.1
        with self.imageLayout.canvas:
            self.imageLayout.rect.size = (self.imageLayout.rect.size[0]/ratio,self.imageLayout.rect.size[1]/ratio)
            self.imageLayout.rect.pos = (self.imageLayout.center[0]- self.imageLayout.rect.size[0]/2,self.imageLayout.center[1]-self.imageLayout.rect.size[1]/2)

    
class ImageLoadApp(App):
    def build(self):
        return Builder.load_file("./ImageLoad.kv")

if __name__ == '__main__':
    ImageLoadApp().run()