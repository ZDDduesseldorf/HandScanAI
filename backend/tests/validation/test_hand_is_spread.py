import pytest
from validation import hand_is_spread

####TODO example data needs to be adjusted (esp. open hand)

@pytest.fixture
def landmarks_spread():
    # example for open hand
    return [
        (500, 900),
        (300, 900),
        (100, 800),
        (50, 700),
        (0, 600),
        (300, 750),
        (250, 600),
        (200, 500),
        (150, 400),
        (500, 750),
        (500, 600),
        (500, 500),
        (500, 400),
        (700, 770),
        (750, 650),
        (800, 550),
        (850, 450),
        (900, 800),
        (950, 700),
        (1000, 600),
        (1050, 500)
    ]


@pytest.fixture
def landmarks_closed():
    # example for closed hand
    return [
        (500, 900),
        (400, 850),
        (300, 750),
        (250, 650),
        (200, 550),
        (420, 750),
        (400, 600),
        (380, 500),
        (360, 400),
        (500, 750),
        (500, 600),
        (500, 500),
        (500, 400),
        (580, 770),
        (600, 650),
        (620, 550),
        (640, 450),
        (680, 800),
        (700, 700),
        (720, 600),
        (740, 500)  
    ]

def test_spread_fingers(landmarks_spread):
    result = hand_is_spread.hand_is_spread(landmarks_spread)
    assert result is True

def test_closed_fingers(landmarks_closed):
    result = hand_is_spread.hand_is_spread(landmarks_closed)
    assert result is False

def test_empty_landmarks():
    result = hand_is_spread.hand_is_spread([])
    assert result is False

def test_custom_threshold(landmarks_closed):
    custom_thresholds = {"thumb-index": 0.5, "pinky-ring": 0.5, "rest": 0.5}
    result = hand_is_spread.hand_is_spread(landmarks_closed, thresholds=custom_thresholds)
    assert result is True

def test_debug_mode(landmarks_spread, capsys):
    result = hand_is_spread.hand_is_spread(landmarks_spread, debug=True)
    captured = capsys.readouterr()
    assert "Relative distance" in captured.out  # ensure debug output exists
    assert result is True
