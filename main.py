from kivy.app import App
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput


class TodoApp(App):
    def build(self):
        root = BoxLayout(orientation="vertical", padding=dp(16), spacing=dp(12))

        title = Label(
            text="My To-Do List",
            font_size=dp(24),
            bold=True,
            size_hint_y=None,
            height=dp(40),
        )
        root.add_widget(title)

        # Input row
        input_row = BoxLayout(size_hint_y=None, height=dp(48), spacing=dp(8))
        self.task_input = TextInput(
            hint_text="What needs to be done?",
            multiline=False,
            font_size=dp(16),
            padding=[dp(10), dp(12)],
        )
        self.task_input.bind(on_text_validate=self.add_task)

        add_btn = Button(
            text="Add",
            size_hint_x=None,
            width=dp(80),
            font_size=dp(16),
            on_release=self.add_task,
        )
        input_row.add_widget(self.task_input)
        input_row.add_widget(add_btn)
        root.add_widget(input_row)

        # Scrollable task list
        scroll = ScrollView()
        self.tasks_list = BoxLayout(
            orientation="vertical",
            spacing=dp(8),
            size_hint_y=None,
        )
        self.tasks_list.bind(minimum_height=self.tasks_list.setter("height"))
        scroll.add_widget(self.tasks_list)
        root.add_widget(scroll)

        return root

    def add_task(self, *args):
        text = self.task_input.text.strip()
        if not text:
            return

        row = BoxLayout(size_hint_y=None, height=dp(48), spacing=dp(8))

        checkbox = CheckBox(size_hint_x=None, width=dp(40))
        label = Label(
            text=text,
            font_size=dp(16),
            halign="left",
            valign="middle",
        )
        label.bind(size=label.setter("text_size"))

        delete_btn = Button(
            text="X",
            size_hint_x=None,
            width=dp(44),
            background_color=(0.85, 0.25, 0.25, 1),
            on_release=lambda btn: self.tasks_list.remove_widget(row),
        )

        row.add_widget(checkbox)
        row.add_widget(label)
        row.add_widget(delete_btn)

        self.tasks_list.add_widget(row)
        self.task_input.text = ""


if __name__ == "__main__":
    TodoApp().run()