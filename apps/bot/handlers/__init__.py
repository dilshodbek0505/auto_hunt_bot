from .registration import router as registration
from .commands import router as commands
from .new_detection import router as new_detection
from .active_detections import router as active_detections

def setup_handlers(dp):
    dp.include_router(commands)
    dp.include_router(registration)
    dp.include_router(new_detection)
    dp.include_router(active_detections)
