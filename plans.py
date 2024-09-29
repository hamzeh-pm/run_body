import time
from enum import Enum

from pygame import mixer


class Plan:
    def __init__(self, name, runs, run_time, rest_time):
        self.name = name
        self.runs = runs
        self.run_time = run_time
        self.rest_time = rest_time
        self.warmup_time = 20
        self.cooldown_time = 20
        self.prev_state = None
        self.state = self.State.WARMUP
        self.state_time = 0
        self.clock_event = None
        self.state_change_callback = None

    class State(Enum):
        WARMUP = 0
        RUNNING = 1
        RESTING = 2
        COOLDOWN = 3
        FINISHED = 4

    def get_total_time(self):
        return (
            self.runs * (self.run_time + self.rest_time)
            + self.warmup_time
            + self.cooldown_time
        )

    def start_workout(self):
        self.play_mixer("sounds/start.mp3")
        self.play_mixer("sounds/start_warmup.mp3")
        self.state = self.State.WARMUP
        self.state_time = self.warmup_time

    def update_state(self, dt):
        self.prev_state = self.state
        dt = 1
        self.state_time -= dt
        if self.state == self.State.WARMUP and self.state_time <= 0:
            self.state = self.State.RUNNING
            self.state_time = self.run_time

        elif self.state == self.State.RUNNING and self.state_time <= 0:
            self.state = self.State.RESTING
            self.state_time = self.rest_time
            self.runs -= 1

        elif self.state == self.State.RESTING and self.state_time <= 0:
            if self.runs > 0:
                self.state = self.State.RUNNING
                self.state_time = self.run_time
            else:
                self.state = self.State.COOLDOWN
                self.state_time = self.cooldown_time

        elif self.state == self.state.COOLDOWN and self.state_time <= 0:
            self.state = self.State.FINISHED
            self.state_time = 0
            self.stop_workout()

            # clear the side effect of the last run
            # save the result
        if self.state_change_callback:
            self.state_change_callback(self.state, self.state_time)

        self.play_sound()

    def stop_workout(self):
        if self.clock_event:
            self.clock_event.cancel()
            self.clock_event = None
            self.state = self.State.WARMUP
            self.state_time = 0

    def play_sound(self):
        if self.state != self.prev_state:
            if self.state == self.State.WARMUP:
                self.play_mixer("sounds/start_warmup.mp3")
            elif self.state == self.State.RUNNING:
                self.play_mixer("sounds/begin_running.mp3")
            elif self.state == self.State.RESTING:
                self.play_mixer("sounds/start_walking.mp3")
            elif self.state == self.State.COOLDOWN:
                self.play_mixer("sounds/start_cooldown.mp3")

    def play_mixer(self, file_location):
        mixer.init()
        mixer.music.load(file_location)
        mixer.music.play()
        while mixer.music.get_busy():  # wait for music to finish playing
            time.sleep(1)
