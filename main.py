from kivy.uix.screenmanager import ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.app import App
from kivy.storage.jsonstore import JsonStore
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.properties import StringProperty


def truncateString(stringIn, truncationLength=32):
    end = "..."
    if len(stringIn) > truncationLength:
        return stringIn[:truncationLength] + end
    else:
        return stringIn


class CustomBtn(Button):
    key_text = StringProperty()


class Task(BoxLayout):

    def toScreen2(self, text):
        rootInterface = App.get_running_app().root
        rootInterface.ids.screen2Title.text = text
        rootInterface.current = 'screen2'

        rootInterface.ids.taskDetails.text = Interface.store.get(text)['data']

    def delete_task(self, taskTitle, taskId):
        rootInterface = App.get_running_app().root
        rootInterface.ids.taskList.remove_widget(taskId)
        Interface.store.delete(taskTitle.key_text)


class CustomPopup(Popup):

    def add_task(self, text):
        tsk = Task()
        tsk.ids.title.text = truncateString(
            stringIn=text)
        tsk.ids.title.key_text = text
        App.get_running_app().root.ids.taskList.add_widget(tsk)
        Interface.store.put(text, data='')
        self.dismiss()


class Interface(ScreenManager):

    store = JsonStore('taskDataAll.json')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.loadTasksOnce)

    def loadTasksOnce(self, dt):
        for taskTitle in self.store:
            tsk = Task()
            tsk.ids.title.text = truncateString(taskTitle)
            tsk.ids.title.key_text = taskTitle

            App.get_running_app().root.ids.taskList.add_widget(tsk)

    def open_popup(self):
        popupWindow = CustomPopup()
        popupWindow.open()

    def toScreen1(self, taskTitle, taskDetail):
        self.store.put(taskTitle, data=taskDetail)
        App.get_running_app().root.current = 'screen1'


class myApp(App):
    def build(self):
        # Set the window size
        Window.size = (375, 700)


myApp().run()
