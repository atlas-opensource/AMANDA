from pydantic import BaseModel, Field, conlist
from typing import List, Dict, Any, Union, Optional
import math

# ======================================================================
# 1. Data Models for AMANDA's Constraints (Refactored Digital Section)
# ======================================================================

# --- REFACTORED DIGITAL CONSTRAINTS MODELS ---

class ApplicationComponent(BaseModel):
    """
    Represents a single interactive element (e.g., a button, slider, text field)
    as defined by the application's source code/meta-data.
    """
    component_id: str = Field(..., description="Unique ID for the component (e.g., 'Button_Submit').")
    # Bounding Box coordinates [X_min, Y_min, X_max, Y_max] in pixels
    bounding_box: conlist(int, min_length=4, max_length=4) = Field(..., description="[xmin, ymin, xmax, ymax] pixel boundaries.")
    expected_event_type: str = Field(..., description="The event the component is designed to fire (e.g., 'onClick', 'onSwipe').")
    
class DigitalConstraintData(BaseModel):
    """
    Refactored Data model for analyzing Digital Constraints.
    It now consumes the application's structure directly.
    """
    screen_width: int = Field(..., description="Total screen width in pixels.")
    screen_height: int = Field(..., description="Total screen height in pixels.")
    app_components: List[ApplicationComponent] = Field(..., description="List of all defined components and their expected behavior/boundaries.")
    # Raw touch data now includes the component the application *thought* was touched.
    raw_touch_data: List[Dict[str, Union[int, str, bool]]] = Field(..., description="List of recorded user touches: {'x', 'y', 'event_fired', 'component_id_detected'}.")

# --- END REFACTORED DIGITAL CONSTRAINTS MODELS ---

class PhysicalConstraintData(BaseModel):
    """Data model for analyzing Physical Constraints (Apple Watch/Door Example)."""
    user_biometrics: Dict[str, Any] = Field(..., description="Current biometric data (e.g., heart rate, steps).")
    user_position_m: conlist(float, min_length=2, max_length=2) = Field(..., description="User's current [x, y] coordinates in meters.")
    house_blueprint_data: List[Dict[str, Any]] = Field(..., description="List of physical structures (walls, doors) and their coordinates.")
    door_coords_m: conlist(float, min_length=2, max_length=2) = Field(..., description="[x, y] coordinates of the target door.")
    user_velocity_mps: conlist(float, min_length=2, max_length=2) = Field(..., description="User's current [vx, vy] velocity in meters/sec.")

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

    ##
    # Refactored Digital Constraints Analysis 💻
    ##
    def analyze_digital_constraints(self, data: DigitalConstraintData) -> Dict[str, Any]:
        """
        Analyzes user-machine interaction by regressing raw touch data against 
        the application's defined components and expected events.
        """
        
        # Pre-process component map for quick lookup and boundary checks
        component_map = {comp.component_id: comp for comp in data.app_components}
        
        analysis_report = {
            "total_touches": len(data.raw_touch_data),
            "valid_interaction": 0,
            "boundary_mismatch": 0,
            "no_event_fired_error": 0,
            "out_of_bounds_touch": 0,
            "directives": []
        }
        
        # --- Regression Logic: Analyze each touch event ---
        for i, touch in enumerate(data.raw_touch_data):
            x, y = touch['x'], touch['y']
            event_fired = touch['event_fired']
            
            # Find which component's defined boundaries the touch fell within
            touched_component: Optional[ApplicationComponent] = None
            
            for component in data.app_components:
                xmin, ymin, xmax, ymax = component.bounding_box
                
                if xmin <= x <= xmax and ymin <= y <= ymax:
                    touched_component = component
                    break
            
            # Case 1: Touch occurred outside any defined component area
            if touched_component is None:
                analysis_report["out_of_bounds_touch"] += 1
                analysis_report["directives"].append(
                    f"Touch #{i+1} at ({x}, {y}): Touch registered outside all defined component boundaries. "
                    "Directive: **Investigate UI/UX 'Dead Space' or Boundary Definition.**"
                )
                continue
                
            # Case 2: Touch was valid based on component boundaries
            analysis_report["valid_interaction"] += 1
            
            component_id_detected = touch.get('component_id_detected')

            # Sub-Case A: Check for Boundary Mismatch (Touch was in component A's bounds, 
            # but app logic thought it was component B, or a different component_id was logged)
            if component_id_detected and component_id_detected != touched_component.component_id:
                analysis_report["boundary_mismatch"] += 1
                analysis_report["directives"].append(
                    f"Touch #{i+1} at ({x}, {y}): Touch was physically within **{touched_component.component_id}** "
                    f"bounds, but application reported detection for **{component_id_detected}**. "
                    "Directive: **Analyze Component Overlap or Event Bubbling/Hit-Testing Logic.**"
                )
            
            # Sub-Case B: Check for Event Failure (The primary function of AMANDA's example)
            if not event_fired:
                analysis_report["no_event_fired_error"] += 1
                analysis_report["directives"].append(
                    f"Touch #{i+1} on component **{touched_component.component_id}**: "
                    f"Boundary hit successful, but no expected event ('{touched_component.expected_event_type}') fired. "
                    "Directive: **Investigate Software Handler or Event Loop Bug.**"
                )
            
        return analysis_report

    ##
    # Physical Constraints Analysis (No change needed)
    ##
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

    ##
    # Constitutional Constraints Analysis (No change needed)
    ##
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

        most_restrictive_law: Optional[BaseConstitutionalLaw] = None
        min_limit_mph = float('inf')

        for law in data.applicable_laws:
            if law.speed_limit_mph is not None:
                if law.speed_limit_mph < min_limit_mph:
                    min_limit_mph = law.speed_limit_mph
                    most_restrictive_law = law

        if most_restrictive_law is None:
             analysis_report["directives"].append("No specific speed-based legal constraint found for this area.")
             return analysis_report
        
        analysis_report["required_limit_mph"] = min_limit_mph
        analysis_report["applied_law"] = f"Law from {most_restrictive_law.source_constitution} ({most_restrictive_law.law_description})"
        limit_mps = min_limit_mph * self.MPH_TO_MPS

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
        elif current_speed_mps > limit_mps * 0.95:
            
            distance_to_slow_safely = (limit_mps**2 - current_speed_mps**2) / (2 * -decel_mps2)
            
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

## Example 1: Refactored Digital Constraints Analysis (App Structure Consumption)
print("--- Digital Constraints Analysis (Application Structure) ---")

# Define components based on source code information
app_components = [
    ApplicationComponent(
        component_id="Button_A",
        bounding_box=[50, 50, 250, 150], # Top-left quadrant
        expected_event_type="onClick"
    ),
    ApplicationComponent(
        component_id="Slider_Volume",
        bounding_box=[350, 50, 450, 750], # Right vertical strip
        expected_event_type="onDrag"
    ),
    ApplicationComponent(
        component_id="Button_B",
        bounding_box=[50, 700, 250, 800], # Bottom-left quadrant
        expected_event_type="onClick"
    )
]

# Simulate raw touch data against these definitions
digital_data_refactored = DigitalConstraintData(
    screen_width=500,
    screen_height=800,
    app_components=app_components,
    raw_touch_data=[
        # 1. Valid touch, event fired
        {'x': 150, 'y': 100, 'event_fired': True, 'component_id_detected': 'Button_A'}, 
        
        # 2. Touch in Component A's bounds, but NO event fired (Software Bug)
        {'x': 100, 'y': 100, 'event_fired': False, 'component_id_detected': 'Button_A'}, 
        
        # 3. Touch in Component A's bounds, but app *thought* it was Slider_Volume (Hit-Test/Overlap Bug)
        {'x': 160, 'y': 110, 'event_fired': True, 'component_id_detected': 'Slider_Volume'}, 

        # 4. Out of bounds touch (Dead Space)
        {'x': 300, 'y': 400, 'event_fired': True, 'component_id_detected': 'None'},
        
        # 5. Valid touch for B, no error
        {'x': 150, 'y': 750, 'event_fired': True, 'component_id_detected': 'Button_B'}
    ]
)
digital_report_refactored = amanda.analyze_digital_constraints(digital_data_refactored)
print(f"Report: {digital_report_refactored}")
print("-" * 70)

## Example 2: Physical Constraints Analysis (Door/Movement)
print("--- Physical Constraints Analysis ---")
physical_data = PhysicalConstraintData(
    user_biometrics={"hr": 75},
    user_position_m=[5.0, 5.0],
    house_blueprint_data=[{"type": "door", "coords": [7.0, 7.0]}],
    door_coords_m=[7.0, 7.0],
    user_velocity_mps=[1.0, 1.0] 
)
physical_report = amanda.analyze_physical_constraints(physical_data)
print(f"Report: {physical_report}")
print("-" * 70)


## Example 3: Constitutional Constraints Analysis (Hierarchical Speed Limit)
print("--- Constitutional Constraints Analysis (U.S. vs. Texas Laws) ---")

applicable_laws = [
    BaseConstitutionalLaw(
        source_constitution="U.S. Constitution (via Federal Statute)",
        law_description="Interstate Commerce Speed Regulation (Default)",
        priority_level=10, 
        speed_limit_mph=70,
        zone_type="Highway Default"
    ),
    BaseConstitutionalLaw(
        source_constitution="Texas Constitution (via TX Transportation Code)",
        law_description="Municipal Speed Zone Ordinance (School Zone)",
        priority_level=5, 
        speed_limit_mph=20, 
        zone_type="School Zone"
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
