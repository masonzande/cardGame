# File used to test functions in program


def venom_test(venom_object, animal, reverse, initial_venom, initial_health):
    print("Testing Venom")
    assert initial_health > 0
    assert 3 > animal.CurrentAbilities["Venom"] >= 0
    assert 3 > initial_venom >= 0
    if reverse:
        assert animal.Health < initial_health
        assert animal.CurrentAbilities["Venom"] < initial_venom
        assert animal.Health == (initial_health - initial_venom)


def paralysis_test(paralysis_object, animal, sub_effect, reverse, initial_paralysis, new_time):
    print("Testing Paralysis")
    if sub_effect == paralysis_object.SubEffects[0]:
        if reverse:
            assert new_time >= 0
            assert animal.CurrentAbilities["Exhaustion"][1][0] is False if new_time == 0 else True
            assert animal.CurrentAbilities["Exhaustion"][1][1] is new_time
        else:
            assert animal.CurrentAbilities["Exhaustion"][1][0] is True
            assert animal.CurrentAbilities["Exhaustion"][1][1] is 1
    else:
        if reverse:
            assert new_time >= 0
            assert animal.CurrentAbilities["Paralysis"][0] is False if new_time == 0 else True
            assert animal.CurrentAbilities["Paralysis"][1] is new_time
        else:
            assert animal.CurrentAbilities["Paralysis"][0] is True
            assert 0 < animal.CurrentAbilities["Paralysis"][1] < 4
