from __future__ import annotations
from typing import Callable

from physlab.core.constants import FLOAT_TOLERANCE, MAX_STEPS_PER_ADVANCE, PHYSICS_DT
from physlab.sim.recorder import Recorder
from physlab.sim.scenario import Scenario


class SimulationRunner:
    def __init__(self, scenario: Scenario, dt: float = PHYSICS_DT, max_steps: int = MAX_STEPS_PER_ADVANCE, sample_every: int = 4) -> None:

        # Store constructor arguments
        self.scenario = scenario
        self.dt = dt
        self.max_steps = max_steps
        self.sample_every = sample_every

        # Retrieve default parameters dynamically from the specific scenario instance
        self.values: dict[str, float] = scenario.default_values()

        # Initialize recorder and callback contract
        self.recorder = Recorder()
        self.on_reset: Callable[[], None] | None = None

        # Enter reset state
        self.reset() 

    def _step_runner(self)-> None:
        self.world.step(dt= self.dt)
        self.step_count += 1

        if self.step_count % self.sample_every == 0:
            self.recorder.sample(self.world)


        if self.scenario.is_finished(self.world):

            if self.step_count % self.sample_every != 0:
                self.recorder.sample(self.world) 

            self.finished = True
            self.paused = True

    def advance(self, real_seconds: float) -> int:
        """Advance the simulation by real_seconds, returning the number of steps performed."""
        if self.paused == True or self.finished == True:
            return 0

        available_time = self.carried_time + real_seconds
        steps = 0
      
        while available_time >= (self.dt - FLOAT_TOLERANCE) and steps < self.max_steps:        
            self._step_runner()
            steps += 1
            available_time -= self.dt

            if self.finished:
                break

        if steps >= self.max_steps:
            self.carried_time = 0.0
        else:
            self.carried_time = max(0.0, available_time)

        return steps           


    def step_once(self) -> None:
        if self.finished == True:
            return None

        self._step_runner()
        
    def pause(self) -> None:
        self.paused =True

    def resume(self) -> None:
        if self.finished == True:
            return None
        else:
            self.paused = False

    def toggle_pause(self) -> None:
        if self.paused == True:
            self.resume()
        else:
            self.pause()

    def set_value(self, key:str, value: float) -> None:

        parameters = self.scenario.parameters()

        for parameter in parameters:
            if parameter.key == key:
                self.values[key] = parameter.clamp(value)
                self.reset()
                return
        
        raise KeyError(f"key: {key} not existent")


    def load_scenario(self,scenario: Scenario) -> None:
        self.scenario = scenario
        self.values = self.scenario.default_values()
        self.reset()
        

    def reset(self) -> None:
       
        self.world = self.scenario.build(self.values)
        self.recorder.clear()
        self.recorder.sample(self.world)

        self.carried_time = 0
        self.step_count = 0

        self.finished = False
        self.paused = True

        if self.on_reset is not None:
            self.on_reset()


        