import os
import mediapipe as mp
from app.core.config import settings
from mediapipe.tasks.python import BaseOptions
from mediapipe.tasks.python.vision import (
    GestureRecognizer,
    GestureRecognizerOptions,
    RunningMode,
)

base_options = BaseOptions(model_asset_path=os.path.join(settings.PATHS.LIB_DIR, "mediapipe", "gesture_recognizer.task"))
options = GestureRecognizerOptions(
    base_options=base_options, running_mode=RunningMode.IMAGE
)
recognizer = GestureRecognizer.create_from_options(options)


def recognize_gesture(image):
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)
    return recognizer.recognize(mp_image)
