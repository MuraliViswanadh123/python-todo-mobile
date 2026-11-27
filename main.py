from kivy.app import App
from kivy.core.window import Window
from kivy.metrics import dp,sp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uitils import escape_markup


import json 
import os

Window.softinput_mode="below_target"

STORE_FILENAME="task.json"
ROW_MIN_HEIGHT=dp(48)
KEY_BACK=27

class TaskRow(BoxLayout):
    def __init__(self,text,done=False,on_delete=None,on_change=None,**kwargs):
        kwargs.setdefault("size_hint_y",None)
        kwargs.setdefault("spacing",None)
        super().__init__(**kwargs)

        self.task_text=text
        self.on_change=on_change
        self.on_delete=on_delete
        self.height=ROW_MIN_HEIGHT

        self.checkbox=CheckBox(size_hint_x=None,width=dp(40),active=bool(done))
        self.checkbox.bind(active=self._toggled)
        
        self.label=Label(
            font_size=sp(16),
            halign="left",
            valign="middle",
            markup=True,
            size_hint_y=None,
            height=ROW_MIN_HEIGHT,
        )
        self.label.bind(width=self._label_width,texture_size=self._label_texture)

        delete_btn=Button(
            text="X",
            size_hint_x=None,
            width=dp(44),
            font_size=sp(16),
            background_color=(0.85,0.25,0.25,1)
        )
        delete_btn.bind(on_release=self._delete_pressed)

        self.add_widget(self.checkbox)
        self.add_widget(self.label)
        self.add_widget(delete_btn)
        self._render()

    @property
    def done(self):
        return bool(self.checkbox.active)
    def as_dict(self):
        return {"text":self.task_text,"done":self.done}
    def _label_width(self,label,width):
        label.text_size=(width,None)
    def _label_texture(self,label,texture_size):
        label.height=texture_size[1]
        self.height=max(ROW_MIN_HEIGHT,texture_size[1]+dp(12))
    def _toggled(self,*_):
        self._render()
        if self._on_change:
            self._on_change()
    def _delete_pressed(self,*_):
        if self._on_delete:
            self._on_delete(self)
    def _render(self):
        safe=escape_markup(self.task_text)
        if self.done:
            self.label.text="[s][color=#888888]{}[/color][/s]".format(safe)
        else:
            self.label.text=safe



class TodoApp(App):
    title="My-to-do List"
    def build(self):
        root = BoxLayout(orientation="vertical", padding=dp(16), spacing=dp(12))

        root.add_widget(
            Label(
                text="My To-Do List",
                font_size=dp(24),
                bold=True,
                size_hint_y=None,
                height=dp(40),
            )
        )
        #root.add_widget(title)

        # Input row
        input_row = BoxLayout(size_hint_y=None, height=dp(48), spacing=dp(8))
        self.task_input = TextInput(
            hint_text="What needs to be done?",
            multiline=False,
            write_tab=False,
            font_size=dp(16),
            padding=[dp(10), dp(12)],
        )
        self.task_input.bind(on_text_validate=self.add_task)

        add_btn = Button(
            text="Add",
            size_hint_x=None,
            width=dp(80),
            font_size=dp(16),
        )
        add_btn.bind(on_release=self.add_task,)

        input_row.add_widget(self.task_input)
        input_row.add_widget(add_btn)
        root.add_widget(input_row)

        # Scrollable task list
        scroll = ScrollView(do_scroll_x=False)
        self.tasks_list = BoxLayout(
            orientation="vertical",
            spacing=dp(8),
            size_hint_y=None,
        )
        self.tasks_list.bind(minimum_height=self.tasks_list.setter("height"))
        scroll.add_widget(self.tasks_list)
        root.add_widget(scroll)

        Window.bind(on_keyboard=self._on_keyboard)
        self._load()
        return root
    @property
    def store_path(self):
        return os.path.join(self.user_data_dir,STORE_FILENAME)
    def _load(self):
        try:
            with open(self.store_path,"r",encoding="utf-8") as fh:
                tasks=json.load(fh)
        except (OSError,ValueError):
            return
        if not isinstance(tasks,list):
            return
        for task in tasks:
            if isinstance(task,dict) and task.get("text"):
                self._add_row(str(task["text"]),bool(task.get("done")))
    def save(self,*_):
        tasks=[row.as_dict() for row in reversed(self.tasks_list.children)]
        try:
            os.makedirs(self.user_data_dir,exist_ok=True)
            with open(self.store_path,"w",encoding="utf-8") as fh:
                json.dump(tasks,fh)
        except OSError:
            pass

    def _add_row(self,text,done=False):
        self.tasks_list.add_widget(
            TaskRow(text,done,on_change=self.save,on_delete=self._delete_row)
        )
    def _delete_row(self,row):
        self.tasks_list.remove_widget(row)
        self.save()
    def add_task(self,*_):
        text=self.task_input.text.strip()
        if not text:
            return
        self._add_row(text)
        self.task_input.text=""
        self.task_input.focus=True
        self.save()
    
    def _on_keyboard(self,window,key,*_):
        if key==KEY_BACK and self.task_input.focus:
            self.task_input.focus=False
            return True
        return False
    def on_pause(self):
        self.save()
        return True
    def on_stop(self):
        self.save()
if __name__ == "__main__":
    TodoApp().run()