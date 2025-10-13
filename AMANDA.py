from pydantic import BaseModel, Field, conlist
from typing import List, Dict, Any, Union, Optional
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
    button_dimensions: conlist(int, min_length=2, max_length=2) = Field(..., description="[width, height] of a single button in pixels.")
    spacing_px: int = Field(..., description="Free space between buttons in pixels.")
    raw_touch_data: List[Dict[str, Union[int, bool]]] = Field(..., description="List of recorded user touches: {'x', 'y', 'event_fired'}.")

class PhysicalConstraintData(BaseModel):
    """Data model for analyzing Physical Constraints (Apple Watch/Door Example)."""
    user_biometrics: Dict[str, Any] = Field(..., description="Current biometric data (e.g., heart rate, steps).")
    user_position_m: conlist(float, min_length=2, max_length=2) = Field(..., description="User's current [x, y] coordinates in meters.")
    house_blueprint_data: List[Dict[str, Any]] = Field(..., description="List of physical structures (walls, doors) and their coordinates.")
    door_coords_m: conlist(float, min_length=2, max_length=2) = Field(..., description="[x, y] coordinates of the target door.")
    user_velocity_mps: conlist(float, min_length=2, max_length=2) = Field(..., description="User's current [vx, vy] velocity in meters/sec.")

# --- NEW/REFACTORED CONSTITUTIONAL CONSTRAINTS MODELS ---

class BaseConstitutionalLaw(BaseModel):
    """Base model for a Constitutional constraint (law) from a derived source."""
    source_constitution: str = Field(..., description="E.g., U.S. Constitution or Texas Constitution.")
    law_description: str = Field(..., description="The specific law/statute being applied.")
    priority_level: int = Field(..., description="Higher number indicates higher legal priority (e.g., U.S. Federal law > State law).")
    speed_limit_mph: Optional[int] = Field(None, description="The speed limit defined by this specific law, if applicable.")
    zone_type: Optional[str] = Field(None, description="The type of zone this law applies to (e.g., School Zone).")

class ConstitutionalConstraintData(BaseModel):
    """Refactored data model for Constitutional Constraints (Speed Limit Example)."""
    geospatial_data: Dict[str, Any] = Field(..., description="Map data for the current area and zone.")
    applicable_laws: List[BaseConstitutionalLaw] = Field(..., description="List of all laws governing the current location/activity.")
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
    MPH_TO_MPS = 0.44704

    def __init__(self):
        print("AMANDA Initialized: Ready for Data Aggregation and Regression.")

    # --- Digital Constraints Analysis (No change needed) ---

    def analyze_digital_constraints(self, data: DigitalConstraintData) -> Dict[str, Any]:
        """
        Analyzes user-machine interaction based on screen structure constraints.
        Determines valid touch areas and compares them to raw touch data.
        """
        button_w, button_h = data.button_dimensions
        total_h = (button_h * data.button_count) + (data.spacing_px * (data.button_count - 1))
        start_y = (data.screen_height - total_h) / 2
        
        analysis_report = {
            "valid_touches": 0,
            "out_of_bounds_touches": 0,
            "button_presses": 0,
            "no_event_fired": 0,
            "directives": []
        }
        
        for touch in data.raw_touch_data:
            x, y = touch['x'], touch['y']
            is_in_central_area = (x > (data.screen_width - button_w) / 2 and 
                                  x < (data.screen_width + button_w) / 2)
                                  
            if not is_in_central_area:
                analysis_report["out_of_bounds_touches"] += 1
                continue

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
                 analysis_report["out_of_bounds_touches"] += 1 
                 analysis_report["directives"].append("Touch registered in vertical spacing area. Directive: **Increase Button Size or Decrease Spacing**.")

        return analysis_report

    # --- Physical Constraints Analysis (No change needed) ---
    
    def analyze_physical_constraints(self, data: PhysicalConstraintData) -> Dict[str, Any]:
        """
        Analyzes user position and velocity against physical structures 
        to predict an imminent interaction (e.g., reaching a door).
        """
        DOOR_INTERACTION_RANGE_M = 1.5
        
        ux, uy = data.user_position_m
        vx, vy = data.user_velocity_mps
        dx, dy = data.door_coords_m
        
        distance_to_door = math.sqrt((dx - ux)**2 + (dy - uy)**2)
        
        analysis_report = {
            "prediction": "No imminent door interaction detected.",
            "directive_signal": None
        }
        
        if distance_to_door < DOOR_INTERACTION_RANGE_M:
            is_approaching = (vx * (dx - ux) + vy * (dy - uy)) > 0
            
            if is_approaching:
                time_to_door_sec = distance_to_door / math.sqrt(vx**2 + vy**2) if (vx**2 + vy**2) > 0 else float('inf')
                
                analysis_report["prediction"] = (
                    f"User is approaching the door at ({dx:.1f}m, {dy:.1f}m). "
                    f"Distance: {distance_to_door:.2f}m. Time to door: {time_to_door_sec:.2f}s."
                )
                
                analysis_report["directive_signal"] = {
                    "device": "Apple Watch",
                    "action": "Haptic/Audio Cue",
                    "message": "Reach out and open the door."
                }
            
        return analysis_report

    # --- REFACTORED Constitutional Constraints Analysis ---

    def analyze_constitutional_constraints(self, data: ConstitutionalConstraintData) -> Dict[str, Any]:
        """
        Analyzes vehicle speed against *all* applicable legal constraints 
        (U.S. Constitution and derived laws, Texas Constitution and derived laws)
        and generates a pre-emptive warning directive based on the most restrictive law.
        """
        current_speed_mps = data.vehicle_speed_data_mph * self.MPH_TO_MPS
        decel_mps2 = data.max_safe_decel_mps2

        analysis_report = {
            "current_speed_mph": data.vehicle_speed_data_mph,
            "applied_law": "N/A",
            "required_limit_mph": float('inf'),
            "is_currently_speeding": False,
            "warning_required": False,
            "directives": []
        }

        # 1. Determine the Most Restrictive (Lowest) Legal Speed Limit
        # Laws are checked for the lowest limit, which is the enforced constraint.
        # This simulates regression against all derived laws.
        most_restrictive_law: Optional[BaseConstitutionalLaw] = None
        min_limit_mph = float('inf')

        for law in data.applicable_laws:
            # Only consider laws that have a defined speed limit constraint
            if law.speed_limit_mph is not None:
                if law.speed_limit_mph < min_limit_mph:
                    min_limit_mph = law.speed_limit_mph
                    most_restrictive_law = law

        if most_restrictive_law is None:
             analysis_report["directives"].append("No specific speed-based legal constraint found for this area.")
             return analysis_report
        
        # Update report with the constraint found
        analysis_report["required_limit_mph"] = min_limit_mph
        analysis_report["applied_law"] = f"Law from {most_restrictive_law.source_constitution} ({most_restrictive_law.law_description})"
        limit_mps = min_limit_mph * self.MPH_TO_MPS

        # 2. Regression Logic against the Most Restrictive Constraint
        
        # A. Already Speeding
        if data.vehicle_speed_data_mph > min_limit_mph:
            analysis_report["is_currently_speeding"] = True
            analysis_report["warning_required"] = True
            analysis_report["directives"].append(
                f"Immediate warning: **CURRENTLY EXCEEDING** the {min_limit_mph} MPH limit "
                f"imposed by {most_restrictive_law.source_constitution} law."
            )
            return analysis_report
            
        # B. Pre-emptive Warning Check (Approaching Speeding)
        elif current_speed_mps > limit_mps * 0.95: # Pre-emptive check: close to the limit
            
            # Physics formula: d = (v_final^2 - v_initial^2) / (2 * a)
            # Distance needed to slow from current speed to the legal limit
            distance_to_slow_safely = (limit_mps**2 - current_speed_mps**2) / (2 * -decel_mps2)
            
            # If the safe slowing distance is GREATER than the distance to the zone
            if distance_to_slow_safely >= data.vehicle_proximity_to_zone_m:
                analysis_report["warning_required"] = True
                analysis_report["directives"].append(
                    f"Warning: Speed is {data.vehicle_speed_data_mph:.1f} MPH. "
                    f"You need {distance_to_slow_safely:.1f}m to slow to the {min_limit_mph} MPH limit. "
                    f"Zone is {data.vehicle_proximity_to_zone_m:.1f}m away. **SLOW DOWN NOW**."
                )

        return analysis_report

# ======================================================================
# 3. Example Execution
# ======================================================================

amanda = AMANDA_Core()
print("-" * 70)

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
print("-" * 70)

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
print("-" * 70)

## Example 3: Constitutional Constraints Analysis (Hierarchical Speed Limit)
print("--- Constitutional Constraints Analysis (U.S. vs. Texas Laws) ---")

# Define the set of constitutional laws and derived statutes for the scenario
# In a real system, AMANDA would fetch these based on the geospatial_data
applicable_laws = [
    BaseConstitutionalLaw(
        source_constitution="U.S. Constitution (via Federal Statute)",
        law_description="Interstate Commerce Speed Regulation (Default)",
        priority_level=10, # Highest priority
        speed_limit_mph=70,
        zone_type="Highway Default"
    ),
    BaseConstitutionalLaw(
        source_constitution="Texas Constitution (via TX Transportation Code)",
        law_description="Municipal Speed Zone Ordinance (School Zone)",
        priority_level=5, # Lower priority, but more specific
        speed_limit_mph=20, # The local, restrictive speed limit
        zone_type="School Zone"
    ),
    BaseConstitutionalLaw(
        source_constitution="Texas Constitution (via TX Transportation Code)",
        law_description="Urban Residential Default Limit",
        priority_level=4,
        speed_limit_mph=30,
        zone_type="Urban Default"
    )
]

constitutional_data_refactored = ConstitutionalConstraintData(
    geospatial_data={"zone_id": "TX-AUSTIN-SCHOOL-45"},
    applicable_laws=applicable_laws,
    vehicle_speed_data_mph=35.0,
    vehicle_proximity_to_zone_m=100.0,
    max_safe_decel_mps2=4.0
)

constitutional_report_refactored = amanda.analyze_constitutional_constraints(constitutional_data_refactored)
print(f"Report: {constitutional_report_refactored}")
print("-" * 70)
