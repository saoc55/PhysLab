import pytest
from physlab.sim.parameters import Parameter
from physlab.sim.scenario import Scenario
from physlab.sim.scenarios.projectile import ProjectileScenario

#----------------------------------------------------------------AC3-----------------------------------------------------------------
def test_abstract_scenario():
    with pytest.raises(TypeError, match="abstract") :
        scenario = Scenario()

