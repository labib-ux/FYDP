"""Central config for FYDP v2. Ported defaults from v1 course project."""

# YOLO
YOLO_MODEL = "yolo11n.pt"
CONFIDENCE_THRESHOLD = 0.25
IOU_THRESHOLD = 0.45
IMG_SIZE = 640

# Industrial preprocessing (simulation only, real deployment uses raw frames)
BLUR_KERNEL_SIZE = 15
NOISE_VARIANCE = 0.01
LOW_LIGHT_FACTOR = 0.7

# Metadata bridge
ROLLING_WINDOW = 10
PREDICTION_INTERVAL = 30

# ML
SYNTHETIC_SAMPLES = 1000
TRAIN_TEST_SPLIT = 0.8
RANDOM_STATE = 42
RF_ESTIMATORS = 100
RF_MAX_DEPTH = 10
