from kivy.app import App
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

from plans import Plan, Run


class RunPlanButton(Button):
    pass


class RunBodyLayout(BoxLayout):
    state_lbl = ObjectProperty(None)
    run_lbl = ObjectProperty(None)
    timer_lbl = ObjectProperty(None)
    run_lst = ObjectProperty(None)
    plan: Plan = None

    def action_start(self):
        self.plan.start_workout()
        self.plan.state_change_callback = self.update_state_label
        self.plan.clock_event = Clock.schedule_interval(self.plan.update_state, 1)

    def update_state_label(self, state, state_time):
        minutes, seconds = divmod(int(state_time), 60)
        self.state_lbl.text = f"{self.plan.name} {state.name}"
        self.run_lbl.text = f"{len(self.plan)} runs left"
        self.timer_lbl.text = f"{minutes:02}:{seconds:02}"


class RunBodyApp(App):
    def build(self):
        run_body = RunBodyLayout()
        # Week 1
        self.create_plan("W1D1", [Run(60, 90)] * 8, run_body)
        self.create_plan("W1D2", [Run(60, 90)] * 8, run_body)
        self.create_plan("W1D2", [Run(60, 90)] * 8, run_body)

        # Week 2
        self.create_plan("W2D1", [Run(90, 120)] * 6, run_body)
        self.create_plan("W2D2", [Run(90, 120)] * 6, run_body)
        self.create_plan("W2D3", [Run(90, 120)] * 6, run_body)

        # Week 3
        self.create_plan("W3D1", [Run(120, 120)] * 6, run_body)
        self.create_plan("W3D2", [Run(120, 120)] * 6, run_body)
        self.create_plan("W3D3", [Run(120, 120)] * 6, run_body)

        # Week 4
        self.create_plan("W4D1", [Run(180, 90)] * 5, run_body)
        self.create_plan("W4D2", [Run(180, 90)] * 5, run_body)
        self.create_plan("W4D3", [Run(180, 90)] * 5, run_body)

        # Week 5
        self.create_plan("W5D1", [Run(300, 180)] * 3, run_body)
        self.create_plan("W5D2", [Run(480, 300)] * 2, run_body)
        self.create_plan("W5D3", [Run(1200, 0)], run_body)

        # Week 6
        self.create_plan(
            "W6D1", [Run(300, 180)] + [Run(480, 180)] + [Run(300, 180)], run_body
        )
        self.create_plan("W6D2", [Run(600, 180)] * 2, run_body)
        self.create_plan("W6D3", [Run(1500, 0)], run_body)

        # Week 7
        self.create_plan("W7D1", [Run(1500, 0)], run_body)
        self.create_plan("W7D2", [Run(1500, 0)], run_body)
        self.create_plan("W7D3", [Run(1500, 0)], run_body)

        # Week 8
        self.create_plan("W8D1", [Run(1680, 0)], run_body)
        self.create_plan("W8D2", [Run(1800, 0)], run_body)
        self.create_plan("W8D3", [Run(2000, 0)], run_body)
        return run_body

    @staticmethod
    def assign_plan(run_body, plan):
        run_body.plan = plan
        run_body.update_state_label(plan.state, plan.state_time)

    def create_plan(self, name, runs, run_body):
        # populate plans
        week_plan = Plan(name, runs, 20, 20)
        run_plan = RunPlanButton(
            text=f"[b]{week_plan.name}[/b]\n {week_plan}",
            halign="center",
            valign="middle",
            text_size=(None, None),
            size_hint_x=None,
        )
        run_plan.bind(on_press=lambda x: self.assign_plan(run_body, week_plan))
        run_plan.bind(size=self.update_text_size)
        run_body.run_lst.add_widget(run_plan)

    def update_text_size(self, instance, value):
        instance.text_size = (instance.width, None)


if __name__ == "__main__":
    RunBodyApp().run()
