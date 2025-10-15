from datetime import datetime
from typing import Dict

def validate_event(event_data: Dict) -> Dict:
    """
    Checks event plausibility (duplicate IDs, travel time, logical constraints).
    Returns validation result and reason if invalid.
    """
    # Example logic
    if event_data.get("speed") and event_data["speed"] > 100:
        return {"is_valid": False, "reason": "Unrealistic travel speed"}
    if event_data.get("duplicate"):
        return {"is_valid": False, "reason": "Duplicate event detected"}

    return {"is_valid": True, "reason": None}
