from kivy.app import App
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

from plans import Plan


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
        self.run_lbl.text = f"{self.plan.runs} runs left"
        self.timer_lbl.text = f"{minutes:02}:{seconds:02}"


class RunBodyApp(App):
    def build(self):
        run_body = RunBodyLayout()
        # Week 1
        self.create_plan("W1D1", 8, 60, 90, run_body)
        self.create_plan("W1D2", 8, 60, 90, run_body)
        self.create_plan("W1D2", 8, 60, 90, run_body)

        # Week 2
        self.create_plan("W2D1", 6, 90, 120, run_body)
        self.create_plan("W2D2", 6, 90, 120, run_body)
        self.create_plan("W2D3", 6, 90, 120, run_body)

        # Week 3
        self.create_plan("W3D1", 6, 120, 120, run_body)
        self.create_plan("W3D2", 6, 120, 120, run_body)
        self.create_plan("W3D3", 6, 120, 120, run_body)

        # Week 4
        self.create_plan("W4D1", 5, 180, 90, run_body)
        self.create_plan("W4D2", 5, 180, 90, run_body)
        self.create_plan("W4D3", 5, 180, 90, run_body)

        # Week 5
        self.create_plan("W5D1", 3, 300, 180, run_body)
        self.create_plan("W5D2", 2, 480, 300, run_body)
        self.create_plan("W5D3", 1, 1200, 0, run_body)

        # Week 6
        self.create_plan("W6D1", 4, 300, 180, run_body)
        self.create_plan("W6D2", 2, 600, 180, run_body)
        self.create_plan("W6D3", 1, 1500, 0, run_body)

        # Week 7
        self.create_plan("W7D1", 1, 1500, 0, run_body)
        self.create_plan("W7D2", 1, 1500, 0, run_body)
        self.create_plan("W7D3", 1, 1500, 0, run_body)

        # Week 8
        self.create_plan("W8D1", 1, 1680, 0, run_body)
        self.create_plan("W8D2", 1, 1800, 0, run_body)
        self.create_plan("W8D3", 1, 2000, 0, run_body)
        return run_body

    @staticmethod
    def assign_plan(run_body, plan):
        run_body.plan = plan
        run_body.update_state_label(plan.state, plan.state_time)

    def create_plan(self, name, runs, run_time, rest_time, run_body):
        # populate plans
        w1d1_plan = Plan(name, runs, run_time, rest_time)
        run_time_desc = run_time / 60
        rest_time_desc = rest_time / 60
        run_plan = RunPlanButton(
            text=f"[b]{w1d1_plan.name}[/b]\n {runs}x{run_time_desc} min run\n {rest_time_desc} min rest"
        )
        run_plan.bind(on_press=lambda x: self.assign_plan(run_body, w1d1_plan))
        run_body.run_lst.add_widget(run_plan)


if __name__ == "__main__":
    RunBodyApp().run()
