import math
import tkinter as tk
from tkinter import ttk

# Club-specific adjustment factors (Example values; adjust based on game data)
CLUB_FACTORS = {
    "Driver": {"elevation": 0.25, "wind": 0.08},
    "3-Wood": {"elevation": 0.3, "wind": 0.09},
    "5-Wood": {"elevation": 0.35, "wind": 0.1},
    "Hybrid": {"elevation": 0.38, "wind": 0.11},
    "3-Iron": {"elevation": 0.4, "wind": 0.12},
    "4-Iron": {"elevation": 0.42, "wind": 0.13},
    "5-Iron": {"elevation": 0.44, "wind": 0.14},
    "6-Iron": {"elevation": 0.46, "wind": 0.15},
    "7-Iron": {"elevation": 0.48, "wind": 0.16},
    "8-Iron": {"elevation": 0.5, "wind": 0.17},
    "9-Iron": {"elevation": 0.52, "wind": 0.18},
    "Pitching Wedge": {"elevation": 0.54, "wind": 0.19},
    "Gap Wedge": {"elevation": 0.56, "wind": 0.2},
    "Sand Wedge": {"elevation": 0.58, "wind": 0.21},
    "Lob Wedge": {"elevation": 0.6, "wind": 0.22},
}
def suggest_club_and_percentage(adjusted_distance):
    """
    Suggest the club to use and the percentage to hit it based on the adjusted distance.

    Args:
        adjusted_distance (float): Adjusted shot distance in yards.

    Returns:
        tuple: Suggested club and percentage to hit it.
    """
    # Example club distances (adjust based on actual data)
    CLUB_DISTANCES = {
        "Driver": 280,
        "3-Wood": 240,
        "Hybrid": 225,
        "3-Iron": 228,
        "4-Iron": 212,
        "5-Iron": 197,
        "6-Iron": 181,
        "7-Iron": 165,
        "8-Iron": 149,
        "9-Iron": 133,
        "Pitching Wedge": 110,
        "Sand Wedge": 105,
        "Lob Wedge": 80,
    }

    # Sort clubs by distance
    sorted_clubs = sorted(CLUB_DISTANCES.items(), key=lambda item: item[1])

    for i, (club, distance) in enumerate(sorted_clubs):
        if adjusted_distance <= distance:
            percentage = (adjusted_distance / distance) * 100
            if percentage > 100 and i < len(sorted_clubs) - 1:
                next_club, next_distance = sorted_clubs[i + 1]
                percentage = (adjusted_distance / next_distance) * 100
                return next_club, percentage
            return club, percentage

    # If the distance is greater than the longest club distance, use the longest club
    return sorted_clubs[-1][0], (adjusted_distance / sorted_clubs[-1][1]) * 100

def clear_fields():
    """Clear all input fields and set focus to the Base Distance textbox."""
    entry_distance.delete(0, tk.END)
    entry_elevation.delete(0, tk.END)
    entry_wind_speed.delete(0, tk.END)
    entry_wind_angle.delete(0, tk.END)
    club_combobox.set("Driver")
    result_label.config(text="Adjusted Shot Distance: ")
    entry_distance.focus()

def calculate_adjusted_shot(base_distance, elevation, wind_speed, wind_angle_deg, club):
    """
    Calculate adjusted shot distance based on elevation, wind, and club.

    Args:
        base_distance (float): Base shot distance in yards.
        elevation (float): Elevation change in feet.
        wind_speed (float): Wind speed in mph.
        wind_angle_deg (float): Angle between wind direction and shot direction in degrees.
        club (str): Selected club.

    Returns:
        tuple: Adjusted shot distance in yards and lateral adjustment in yards.
    """
    # Club-specific factors
    elevation_factor = CLUB_FACTORS[club]["elevation"]
    wind_factor = CLUB_FACTORS[club]["wind"]

    # Elevation adjustment (convert feet to yards and apply factor)
    elevation_adjustment = elevation * 0.33 * elevation_factor

    # Effective wind speed along the shot direction
    wind_angle_rad = math.radians(wind_angle_deg)
    effective_wind_speed = wind_speed * math.cos(wind_angle_rad)

    # Wind adjustment (positive for tailwind, negative for headwind)
    wind_adjustment = effective_wind_speed * wind_factor

    # Calculate final adjusted distance
    adjusted_distance = base_distance + elevation_adjustment + wind_adjustment

    # Lateral wind adjustment (perpendicular to shot direction)
    lateral_wind_speed = wind_speed * math.sin(wind_angle_rad)
    lateral_adjustment = lateral_wind_speed * wind_factor

    return adjusted_distance, lateral_adjustment


def calculate_and_display():
    """Calculate and display the adjusted shot distance, lateral adjustment, suggested club, and percentage."""
    try:
        # Get user inputs
        base_distance = float(entry_distance.get())
        elevation = float(entry_elevation.get())
        wind_speed = float(entry_wind_speed.get())
        wind_angle = float(entry_wind_angle.get())
        club = club_combobox.get()

        # Calculate adjusted distance and lateral adjustment
        adjusted_distance, lateral_adjustment = calculate_adjusted_shot(base_distance, elevation, wind_speed, wind_angle, club)

        # Suggest club and percentage
        suggested_club, percentage = suggest_club_and_percentage(adjusted_distance)

        # Display the result
        result_label.config(text=f"Adjusted Shot Distance: {adjusted_distance:.2f} yards\n"
                                 f"Lateral Adjustment: {lateral_adjustment:.2f} yards\n"
                                 f"Suggested Club: {suggested_club}\n"
                                 f"Percentage: {percentage:.2f}%")
    except ValueError:
        result_label.config(text="Invalid input! Please enter numeric values.")

# GUI setup
root = tk.Tk()
root.title("WGT Shot Calculator")

# Input fields
tk.Label(root, text="Base Distance (yards):").grid(row=0, column=0, padx=10, pady=5, sticky="e")
entry_distance = tk.Entry(root)
entry_distance.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Elevation Change (feet):").grid(row=1, column=0, padx=10, pady=5, sticky="e")
entry_elevation = tk.Entry(root)
entry_elevation.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Wind Speed (mph):").grid(row=2, column=0, padx=10, pady=5, sticky="e")
entry_wind_speed = tk.Entry(root)
entry_wind_speed.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Wind Angle (degrees):").grid(row=3, column=0, padx=10, pady=5, sticky="e")
entry_wind_angle = tk.Entry(root)
entry_wind_angle.grid(row=3, column=1, padx=10, pady=5)

tk.Label(root, text="Club:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
club_combobox = ttk.Combobox(root, values=list(CLUB_FACTORS.keys()), state="readonly")
club_combobox.set("Driver")
club_combobox.grid(row=4, column=1, padx=10, pady=5)

# Calculate button
calculate_button = tk.Button(root, text="Calculate", command=calculate_and_display)
calculate_button.grid(row=5, column=0, columnspan=2, pady=10)

# Clear button
clear_button = tk.Button(root, text="Clear", command=clear_fields)
clear_button.grid(row=6, column=0, columnspan=2, pady=10)

# Result label
result_label = tk.Label(root, text="Adjusted Shot Distance: ", font=("Arial", 12))
result_label.grid(row=7, column=0, columnspan=2, pady=10)

# Run the GUI
root.mainloop()