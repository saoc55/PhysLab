import pytest
from physlab.sim.parameters import Parameter


#---------------------------------------------------------------AC1--------------------------------------------------------
# REVIEW 2: the asserts check YOUR input data (min < default, step > 0), not the code. They would pass even if Parameter stored nothing.
#   AC1 positive = "is accepted": creating it must not raise. Reaching the end without an exception already proves that;
#   if you want an assert, check that a field was stored, e.g. the kind you passed in. `assert parameter.key` tests nothing useful.
@pytest.mark.parametrize("key, label, unit, minimum, maximum, default, step, kind",[
    ("v0", "Launch speed", "m/s", 0, 50, 20, 0.5, "slider"),
    ("v0", "Launch speed", "m/s", 0, 50, 20, 0.5, "toggle")
])
def test_parameter_validation_pos(key, label, unit, minimum, maximum, default, step, kind):
    parameter = Parameter(key= key,
                          label= label,
                          unit= unit,
                          minimum= minimum,
                          maximum= maximum,
                          default= default,
                          step= step,
                          kind= kind)    



# REVIEW 3: use the six cases from the AC1 Check, each changing ONE field of the valid v0 row:
#   default 51, default -1, step 0, step -0.5, kind "switch", kind "Slider".
#   You changed minimum/maximum instead of default, used step -1 and kind "kind", and the case sensitivity case "Slider" is missing.
# Optional: only one field differs per case, so a dict of the valid row plus one override ({**valid, "default": 51}) is much shorter than 8 columns.
#   `parameter =` inside pytest.raises is not needed.
@pytest.mark.parametrize("key, label, unit, minimum, maximum, default, step, kind",[
    ("v0", "Launch speed", "m/s", 21, 50, 20, 0.5, "slider"),
    ("v0", "Launch speed", "m/s", 0, 19, 20, 0.5, "slider"),
    ("v0", "Launch speed", "m/s", 0, 50, 20, 0, "slider"),
    ("v0", "Launch speed", "m/s", 0, 50, 20, -1, "slider"),
    ("v0", "Launch speed", "m/s", 0, 50, 20, -1, "Slider"),
    ("v0", "Launch speed", "m/s", 0, 50, 20, 0.5, "kind")
])
def test_parameter_validation_neg(key, label, unit, minimum, maximum, default, step, kind):
    with pytest.raises(ValueError):
        Parameter(key= key,
                label= label,
                unit= unit,
                minimum= minimum,
                maximum= maximum,
                default= default,
                step= step,
                kind= kind)


#-------------------------------------------------------------------AC2-----------------------------------------------------------
@pytest.mark.parametrize("val, expected", [
    (999, 50), (-5, 0), (12.5, 12.5), (0, 0), (50, 50)
])
def test_clamp_sets_correct_values(val, expected):
    parameter = Parameter(key="v0", label="Launch speed", unit="m/s", minimum=0, maximum=50, default=20, step= 0.5, kind= "slider")
    assert parameter.clamp(val) == expected



