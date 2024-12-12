import pytest
from validation import hand_is_spread

# example landmarks for open hand (11k: Hand_0009213)
@pytest.fixture
def landmarks_spread():
    return [
        (751, -26), 
        (966, 53), 
        (1076, 213), 
        (1131, 385), 
        (1217, 493), 
        (911, 433), 
        (968, 667), 
        (1001, 809), 
        (1022, 919), 
        (768, 443), 
        (785, 706), 
        (793, 870), 
        (794, 991), 
        (647, 412), 
        (630, 654), 
        (617, 811), 
        (607, 930), 
        (546, 356), 
        (487, 535), 
        (456, 639), 
        (433, 728)
    ]

# example landmarks for closed hand (11k: Hand_0009237)
@pytest.fixture
def landmarks_closed():
    return [
        (620, -8), 
        (840, 64), 
        (922, 207), 
        (922, 374), 
        (921, 517), 
        (804, 380), 
        (787, 604), 
        (771, 731), 
        (758, 828), 
        (664, 385), 
        (676, 633), 
        (677, 778), 
        (681, 890), 
        (554, 362), 
        (571, 587), 
        (585, 731), 
        (594, 839), 
        (453, 323), 
        (467, 507), 
        (484, 619), 
        (500, 710)
    ]

#expected: the landmarks of an open hand return true
def test_spread_fingers(landmarks_spread):
    result = hand_is_spread.hand_is_spread(landmarks_spread)
    assert result is True

#expected: the landmarks of a closed hand return false
def test_closed_fingers(landmarks_closed):
    result = hand_is_spread.hand_is_spread(landmarks_closed)
    assert result is False

# expected: empty landmarks return false
def test_empty_landmarks():
    result = hand_is_spread.hand_is_spread([])
    assert result is False

# expected: with low thresholds, the landmarks of a closed hand return true
def test_custom_threshold(landmarks_closed):
    custom_thresholds = {"thumb-index": 0.5, "pinky-ring": 0.5, "rest": 0.5}
    result = hand_is_spread.hand_is_spread(landmarks_closed, thresholds=custom_thresholds)
    assert result is True

# expected: when in debug mode, there is a console output and the landmarks of an open hand still return true
def test_debug_mode(landmarks_spread, capsys):
    result = hand_is_spread.hand_is_spread(landmarks_spread, debug=True)
    captured = capsys.readouterr()
    assert "Relative distance" in captured.out  # ensure debug output exists
    assert result is True
