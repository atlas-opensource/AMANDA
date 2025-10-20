import re
import json
from typing import Dict, Any

class AgencyConstraintEngine:
    """
    A conceptual data processing engine that analyzes raw data (like source code
    or configuration files) and contextualizes it in terms of:
    1. Individual Agency (potential for unlimited action, definition of structure).
    2. Software-Defined Constraints (fixed options, limits, or configuration choices).
    """

    def __init__(self):
        # Patterns indicative of high Agency (the power to define/create freely)
        self.agency_patterns = {
            "Function/Method Definitions (New Capabilities)": r"(def\s+|class\s+|function\s+)",
            "Variable Assignments (Mutable State/Freedom)": r"[a-zA-Z_][a-zA-Z0-9_]*\s*=\s*.*",
            "Custom Type Definitions (Structuring Reality)": r"(type\s+|interface\s+|struct\s+)"
        }

        # Patterns indicative of Constraints (imposed limits or defined options)
        self.constraint_patterns = {
            "Hardcoded Iteration/Size Limits": r"range\((\d+)\)|limit\s*=\s*(\d+)|max_items\s*=\s*(\d+)",
            "Configurable Options/API Checks (Defined Choice Space)": r"(config\s*\.|options\s*\.|check_permission|is_valid)",
            "Fixed Conditional Branching (Pre-set Pathways)": r"if\s+\S+\s*in\s*\[.*\]|if\s+\S+\s*==\s*['\"]",
        }

    def _count_matches(self, data: str, patterns: Dict[str, str]) -> Dict[str, int]:
        """Helper to count occurrences of each pattern in the data."""
        results = {}
        for name, pattern in patterns.items():
            # Use re.IGNORECASE for broader language support
            matches = re.findall(pattern, data, re.IGNORECASE)
            # Findall returns groups, so we just count the total number of matches found.
            results[name] = len(matches)
        return results

    def analyze_data(self, raw_data: str) -> Dict[str, Any]:
        """
        Processes the raw data and generates a contextual analysis report.

        Args:
            raw_data: The source code, configuration text, or raw text to analyze.

        Returns:
            A dictionary containing the Agency and Constraint analysis.
        """
        agency_counts = self._count_matches(raw_data, self.agency_patterns)
        constraint_counts = self._count_matches(raw_data, self.constraint_patterns)

        total_agency = sum(agency_counts.values())
        total_constraint = sum(constraint_counts.values())

        # Determine the predominant context
        if total_agency > total_constraint * 1.5:
            predominant_context = "HIGH AGENCY: The data structure is predominantly defined by user creation and flexible state, emphasizing the unlimited potential of the individual."
            context_score = "0.75 / 1.0"
        elif total_constraint > total_agency * 1.5:
            predominant_context = "HIGH CONSTRAINT: The data structure is heavily governed by fixed rules, limits, and explicit options, emphasizing imposed boundaries on the individual's action."
            context_score = "0.25 / 1.0"
        else:
            predominant_context = "BALANCED CONTEXT: The data shows a near-even mix of self-defined structure (Agency) and defined limitations (Constraint)."
            context_score = "0.50 / 1.0"

        # Construct the final report
        report = {
            "Analysis_Date": "2025-10-20",
            "Contextual_Thesis": "The software is a definition of the freedom (Agency) and limits (Constraint) of the operating individual.",
            "Predominant_Context": predominant_context,
            "Agency_Constraint_Ratio_Score": context_score,
            "Agency_Analysis": {
                "Total_Agency_Indicators": total_agency,
                "Indicators_Found": agency_counts
            },
            "Constraint_Analysis": {
                "Total_Constraint_Indicators": total_constraint,
                "Indicators_Found": constraint_counts
            },
            # Including the raw data summary for context
            "Raw_Data_Summary": f"Processed {len(raw_data.splitlines())} lines of data.",
        }

        return report

# --- Example Usage ---

# Example 1: Data with high constraint (a configuration file snippet)
CONFIG_DATA = """
# System Configuration File V1.2
max_connections = 50
timeout_seconds = 120
default_mode = 'read_only'
if user_role in ['guest', 'viewer']:
    limit_queries = True

# Functions and classes are defined elsewhere
"""

# Example 2: Data with high agency (a module defining new classes and functions)
MODULE_DATA = """
class DataProcessor:
    def __init__(self, name):
        self.name = name

    def execute_pipeline(self, steps):
        # Unlimited potential for processing!
        result = self._process_data(steps)
        return result

def custom_transformer(data, factor=1.0):
    transformed = data * factor
    return transformed
"""

if __name__ == '__main__':
    engine = AgencyConstraintEngine()

    print("--- Analysis of CONFIG_DATA (High Constraint) ---")
    config_report = engine.analyze_data(CONFIG_DATA)
    print(json.dumps(config_report, indent=4))

    print("\n--- Analysis of MODULE_DATA (High Agency) ---")
    module_report = engine.analyze_data(MODULE_DATA)
    print(json.dumps(module_report, indent=4))

    print("\n--- Raw Data Context (CONFIG_DATA) ---")
    print(CONFIG_DATA)
    print("\n--- Raw Data Context (MODULE_DATA) ---")
    print(MODULE_DATA)
