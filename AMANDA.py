from pydantic import BaseModel, Field
from typing import List, Dict, Any, Union
import math

# ======================================================================
# 1. Data Models for AMANDA's Constraints
#    (Using Pydantic for strict schema definition)
# ======================================================================

class DigitalConstraintData(BaseModel):
    """Data model for analyzing Digital Constraints (Touch Screen Example)."""
    screen_width: int = Field(..., description="Total screen width in pixels.")
    screen_height: int = Field(..., description="Total screen height in pixels.")
    button_count: int = Field(..., description="Number of buttons on the screen.")
    button_dimensions: List[int] = Field(..., description="[width, height] of a single button in pixels.")
    spacing_px: int = Field(..., description="Free space between buttons in pixels.")
    raw_touch_data: List[Dict[str, Union[int, bool]]] = Field(..., description="List of recorded user touches.")

class PhysicalConstraintData(BaseModel):
    """Data model for analyzing Physical Constraints (Apple Watch/Door Example)."""
    user_biometrics: Dict[str, Any] = Field(..., description="Current biometric data (e.g., heart rate, steps).")
    user_position_m: List[float] = Field(..., description="User's current [x, y] coordinates in meters.")
    house_blueprint_data: List[Dict[str, Any]] = Field(..., description="List of physical structures (walls, doors) and their coordinates.")
    door_coords_m: List[float] = Field(..., description="[x, y] coordinates of the target door.")
    user_velocity_mps: List[float] = Field(..., description="User's current [vx, vy] velocity in meters/sec.")

class ConstitutionalConstraintData(BaseModel):
    """Data model for analyzing Constitutional Constraints (Speed Limit Example)."""
    geospatial_data: Dict[str, Any] = Field(..., description="Map data for the current area.")
    legal_speed_limit_mph: int = Field(..., description="The posted and legally enforced speed limit.")
    vehicle_speed_data_mph: float = Field(..., description="Current speed reported by the vehicle/radar.")
    vehicle_proximity_to_zone_m: float = Field(..., description="Distance to the enforcement zone boundary.")
    max_safe_decel_mps2: float = Field(..., description="Vehicle's maximum safe deceleration.")

# ======================================================================
# 2. AMANDA Core Logic Class
# ======================================================================

class AMANDA_Core:
    """
    Autonomous Meta-Data Analysis, Non-Sentient Directive-Based Aggregator.
    Simulates the core analysis and directive generation logic.
    """
    def __init__(self):
        print("AMANDA Initialized: Ready for Data Aggregation and Regression.")

    # --- Digital Constraints Analysis ---

    def analyze_digital_constraints(self, data: DigitalConstraintData) -> Dict[str, Any]:
        """
        Analyzes user-machine interaction based on screen structure constraints.
        Determines valid touch areas and compares them to raw touch data.
        """
        button_w, button_h = data.button_dimensions
        total_h = (button_h * data.button_count) + (data.spacing_px * (data.button_count - 1))
        
        # Assume center-aligned for simplicity; calculate the total vertical offset
        # This defines the "free space" or constraint area
        start_y = (data.screen_height - total_h) / 2
        
        analysis_report = {
            "valid_touches": 0,
            "out_of_bounds_touches": 0,
            "button_presses": 0,
            "no_event_fired": 0,
            "directives": []
        }
        
        # Simulate Analysis/Regression
        for touch in data.raw_touch_data:
            x, y = touch['x'], touch['y']
            
            # Check if touch is within the central column where buttons are
            is_in_central_area = (x > (data.screen_width - button_w) / 2 and 
                                  x < (data.screen_width + button_w) / 2)
                                  
            if not is_in_central_area:
                analysis_report["out_of_bounds_touches"] += 1
                continue

            # Check for a specific button press area
            is_valid_button_press = False
            for i in range(data.button_count):
                button_top = start_y + i * (button_h + data.spacing_px)
                button_bottom = button_top + button_h
                
                if button_top <= y <= button_bottom:
                    is_valid_button_press = True
                    analysis_report["button_presses"] += 1
                    
                    if not touch['event_fired']:
                        analysis_report["no_event_fired"] += 1
                        analysis_report["directives"].append(f"Button {i+1} press detected, but no event fired. Directive: **Investigate Software Bug**.")
                    else:
                        analysis_report["valid_touches"] += 1
                    break

            if is_in_central_area and not is_valid_button_press:
                 analysis_report["out_of_bounds_touches"] += 1 # Touch fell in spacing area
                 analysis_report["directives"].append("Touch registered in vertical spacing area. Directive: **Increase Button Size or Decrease Spacing**.")

        return analysis_report

    # --- Physical Constraints Analysis ---
    
    def analyze_physical_constraints(self, data: PhysicalConstraintData) -> Dict[str, Any]:
        """
        Analyzes user position and velocity against physical structures 
        to predict an imminent interaction (e.g., reaching a door).
        """
        # Constants for simple prediction
        DOOR_INTERACTION_RANGE_M = 1.5  # Meters
        
        ux, uy = data.user_position_m
        vx, vy = data.user_velocity_mps
        dx, dy = data.door_coords_m
        
        distance_to_door = math.sqrt((dx - ux)**2 + (dy - uy)**2)
        
        analysis_report = {
            "prediction": "No imminent door interaction detected.",
            "directive_signal": None
        }
        
        # Regression Logic: Check if user is approaching the door
        if distance_to_door < DOOR_INTERACTION_RANGE_M:
            
            # Check if user is moving *towards* the door (simple vector check)
            # This is a simplification. A real system would use pathfinding/trajectory.
            is_approaching = (vx * (dx - ux) + vy * (dy - uy)) > 0 
            
            if is_approaching:
                # Prediction: User is approaching the door and within the interaction range
                time_to_door_sec = distance_to_door / math.sqrt(vx**2 + vy**2) if (vx**2 + vy**2) > 0 else float('inf')
                
                analysis_report["prediction"] = (
                    f"User is approaching the door at ({dx:.1f}m, {dy:.1f}m). "
                    f"Distance: {distance_to_door:.2f}m. Time to door: {time_to_door_sec:.2f}s."
                )
                
                # Directive: Send signal to Apple Watch
                analysis_report["directive_signal"] = {
                    "device": "Apple Watch",
                    "action": "Haptic/Audio Cue",
                    "message": "Reach out and open the door."
                }
            
        return analysis_report

    # --- Constitutional Constraints Analysis ---

    def analyze_constitutional_constraints(self, data: ConstitutionalConstraintData) -> Dict[str, Any]:
        """
        Analyzes vehicle speed against a legal constraint (speed limit) 
        and generates a pre-emptive warning directive.
        """
        # Convert all to a common unit for physics calculations (e.g., m/s)
        MPH_TO_MPS = 0.44704
        
        limit_mps = data.legal_speed_limit_mph * MPH_TO_MPS
        current_speed_mps = data.vehicle_speed_data_mph * MPH_TO_MPS
        decel_mps2 = data.max_safe_decel_mps2

        analysis_report = {
            "current_speed_mph": data.vehicle_speed_data_mph,
            "limit_mph": data.legal_speed_limit_mph,
            "is_currently_speeding": data.vehicle_speed_data_mph > data.legal_speed_limit_mph,
            "warning_required": False,
            "directives": []
        }
        
        # Regression Logic: Calculate the distance needed to safely slow down
        # Physics formula: d = (v_final^2 - v_initial^2) / (2 * a)
        # Assuming v_final = limit_mps and acceleration 'a' is negative (deceleration)
        if current_speed_mps > limit_mps:
            # Already speeding. Immediate warning.
            analysis_report["warning_required"] = True
            analysis_report["directives"].append("Immediate warning: **CURRENTLY EXCEEDING** legal speed limit.")
            return analysis_report
            
        elif current_speed_mps > limit_mps * 0.95: # Pre-emptive check: close to the limit
            
            distance_to_stop_safely = (limit_mps**2 - current_speed_mps**2) / (2 * -decel_mps2)
            
            # If the safe stopping distance is GREATER than the distance to the zone, 
            # a warning is required to ensure the limit is not broken.
            if distance_to_stop_safely >= data.vehicle_proximity_to_zone_m:
                analysis_report["warning_required"] = True
                analysis_report["directives"].append(
                    f"Warning: Speed is {data.vehicle_speed_data_mph:.1f} MPH. "
                    f"You need {distance_to_stop_safely:.1f}m to slow to the limit. "
                    f"Zone is {data.vehicle_proximity_to_zone_m:.1f}m away. **SLOW DOWN NOW**."
                )

        return analysis_report

# ======================================================================
# 3. Example Execution
# ======================================================================

amanda = AMANDA_Core()
print("-" * 50)

## Example 1: Digital Constraints Analysis (Touch Screen)
print("--- Digital Constraints Analysis ---")
digital_data = DigitalConstraintData(
    screen_width=500,
    screen_height=800,
    button_count=10,
    button_dimensions=[200, 50],
    spacing_px=100,
    raw_touch_data=[
        {'x': 250, 'y': 100, 'event_fired': True},  # Valid press
        {'x': 250, 'y': 150, 'event_fired': False}, # Press in spacing area
        {'x': 250, 'y': 250, 'event_fired': False}, # Button press, no event
        {'x': 50, 'y': 400, 'event_fired': True}    # Out of bounds
    ]
)
digital_report = amanda.analyze_digital_constraints(digital_data)
print(f"Report: {digital_report}")
print("-" * 50)


## Example 2: Physical Constraints Analysis (Door/Movement)
print("--- Physical Constraints Analysis ---")
physical_data = PhysicalConstraintData(
    user_biometrics={"hr": 75},
    user_position_m=[5.0, 5.0],
    house_blueprint_data=[{"type": "door", "coords": [7.0, 7.0]}],
    door_coords_m=[7.0, 7.0],
    user_velocity_mps=[1.0, 1.0] # Moving at 1.414 m/s towards the door
)
physical_report = amanda.analyze_physical_constraints(physical_data)
print(f"Report: {physical_report}")
print("-" * 50)


## Example 3: Constitutional Constraints Analysis (Speed Limit)
print("--- Constitutional Constraints Analysis ---")
constitutional_data = ConstitutionalConstraintData(
    geospatial_data={"zone_type": "School"},
    legal_speed_limit_mph=20,
    vehicle_speed_data_mph=35.0,
    vehicle_proximity_to_zone_m=100.0,
    max_safe_decel_mps2=4.0
)
constitutional_report = amanda.analyze_constitutional_constraints(constitutional_data)
print(f"Report: {constitutional_report}")
print("-" * 50)
