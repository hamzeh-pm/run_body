import time
from datetime import datetime
from enum import Enum

from plyer import gps
from pygame import mixer


class Run:
    def __init__(self, duration: int, rest_duration: int, distance: int = None):
        self.duration = duration
        self.rest_duration = rest_duration
        self.distance = distance


class Plan:
    def __init__(
        self, name, runs: list[Run], warmup_time: int = 300, cool_down_time: int = 300
    ):
        self.name = name
        self.runs = runs
        self.this_run = None
        self.warmup_time = warmup_time
        self.cool_down_time = cool_down_time
        self.state = self.State.STARTING
        self.state_time = 0

        # for cleanup purposes
        self.clock_event = None
        self.state_change_callback = None

        # history
        self.is_finished = False
        self.start_time = None
        self.end_time = None
        self.running_path = []

    class State(Enum):
        STARTING = 0
        WARMUP = 1
        RUNNING = 2
        RESTING = 3
        COOL_DOWN = 4
        FINISHED = 5

    @property
    def get_duration(self):
        return sum(run.duration for run in self.runs)

    @property
    def get_rest_duration(self):
        return sum(run.rest_duration for run in self.runs)

    @property
    def get_total_time(self):
        return (
            self.get_duration
            + self.get_rest_duration
            + self.warmup_time
            + self.cool_down_time
        )

    def begin_workout(self):
        self.state = self.State.STARTING
        self.play_sound("sounds/begin.mp3")
        self.state_time = 10
        self.start_time = datetime.now()

    def start_warmup(self):
        self.state = self.State.WARMUP
        self.play_sound("sounds/warmup.mp3")
        self.state_time = self.warmup_time

    def start_running(self):
        self.this_run = self.runs.pop(0)
        self.state = self.State.RUNNING
        self.play_sound("sounds/running.mp3")
        self.state_time = self.this_run.duration

    def start_resting(self):
        self.state = self.State.RESTING
        self.play_sound("sounds/walking.mp3")
        self.state_time = self.this_run.rest_duration

    def start_cool_down(self):
        self.state = self.State.COOL_DOWN
        self.play_sound("sounds/cool_down.mp3")
        self.state_time = self.cool_down_time

    def finish_workout(self):
        self.state = self.State.FINISHED
        self.play_sound("sounds/finish.mp3")
        self.state_time = 0
        self.runs = []
        self.this_run = None
        self.is_finished = True
        self.end_time = datetime.now()
        self.save_workout()

    def save_workout(self):
        pass

    def update_state(self, dt):
        self.state_time -= 1
        if self.state_time <= 0:
            if self.state == self.State.STARTING:
                self.start_warmup()
            elif self.state == self.State.WARMUP:
                self.start_running()
            elif self.state == self.State.RUNNING:
                if self.runs:
                    self.start_resting()
                else:
                    self.start_cool_down()
            elif self.state == self.State.RESTING:
                self.start_running()
            elif self.state == self.State.COOL_DOWN:
                self.finish_workout()

        if self.state_change_callback:
            self.state_change_callback(self.state, self.state_time)

        # get current location
        self.get_current_location()

    @staticmethod
    def play_sound( file_location):
        mixer.init()
        mixer.music.load(file_location)
        mixer.music.play()
        while mixer.music.get_busy():  # wait for music to finish playing
            time.sleep(1)

    def get_current_location(self):
        try:
            gps.configure(on_location=self.on_location)
            gps.start(minTime=1000, minDistance=0)
        except NotImplementedError:
            pass

    def on_location(self, **kwargs):
        lat = kwargs.get("lat")
        lon = kwargs.get("lon")
        if lat is not None and lon is not None:
            self.running_path.append((lat, lon))

    def __str__(self):
        name = ""
        run_name = f"{self.runs[0].duration / 60:.1f}"
        run_time = 1

        for run in self.runs[1:]:
            if f"{run.duration / 60:.1f}" == run_name:
                run_time += 1
                continue

            name = name + f"{run_time}x{run_name} min \n"
            run_name = f"{run.duration / 60:.1f}"
            run_time = 1

        name = name + f"{run_time}x{run_name} min \n"
        return name

    def __len__(self):
        return len(self.runs)
