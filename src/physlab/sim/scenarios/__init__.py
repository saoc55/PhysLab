from physlab.sim.scenario import Scenario
from physlab.sim.scenarios.free_fall_drag import FreeFallDragScenario
from physlab.sim.scenarios.projectile import ProjectileScenario

SCENARIOS: list[Scenario] = [ProjectileScenario(), FreeFallDragScenario()]