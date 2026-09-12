# Detection package initialization
from .person_detector import PersonDetector
from .gender_classifier import GenderClassifier
from .gesture_detector import SOSGestureDetector

__all__ = ["PersonDetector", "GenderClassifier", "SOSGestureDetector"]
