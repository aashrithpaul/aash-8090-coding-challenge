import sys
import os
import json

def calculate_reimbursement(trip_duration_days, miles_traveled, total_receipts_amount):
    D = trip_duration_days
    M = miles_traveled
    R = total_receipts_amount
    mpd = M / D
    spd = R / D

    # ----------------------
    # 1. Base Rate by Duration
    # ----------------------
    if D == 1:
        base_rate = 110
    elif 2 <= D <= 3:
        base_rate = 115
    elif 4 <= D <= 6:
        base_rate = 125
    else:
        base_rate = 105

    # ----------------------
    # 2. Mileage Efficiency Bonus (sweet spot: 180–220)
    # ----------------------
    if mpd < 90:
        mileage_factor = 0.8
    elif 90 <= mpd < 170:
        mileage_factor = 1.0
    elif 170 <= mpd <= 220:
        mileage_factor = 1.25  # Sweet spot
    elif 220 < mpd <= 280:
        mileage_factor = 1.05
    else:
        mileage_factor = 0.85  # Too much driving = penalty

    # ----------------------
    # 3. Spending Efficiency Factor (duration-based thresholds)
    # ----------------------
    if D < 3:
        spending_limit = 75
    elif 3 <= D <= 6:
        spending_limit = 120
    else:
        spending_limit = 90

    if spd <= spending_limit:
        spending_factor = 1.1  # Efficient = rewarded
    elif spd <= spending_limit * 1.3:
        spending_factor = 0.9  # Mild overspend
    else:
        spending_factor = 0.75  # Overspending = penalized

    # ----------------------
    # 4. Interaction Penalty / Bonus
    # ----------------------
    # Example: Low miles + high spending = vacation penalty
    if mpd < 100 and spd > spending_limit:
        interaction_penalty = 0.85
    elif mpd > 200 and spd < spending_limit:
        interaction_penalty = 1.05  # business-efficient
    else:
        interaction_penalty = 1.0

    # ----------------------
    # 5. Final Reimbursement Calculation
    # ----------------------
    base_component = base_rate * D
    adjusted = base_component * mileage_factor * spending_factor * interaction_penalty

    # Optional: Add receipt-based bonus (capped)
    receipt_bonus = min(R, 100 * D) * 0.1  # up to $10/day bonus

    final_amount = adjusted + receipt_bonus
    return round(final_amount, 2)


if __name__ == "__main__":
    if len(sys.argv) == 4:
            # Called via shell script
            days = int(sys.argv[1])
            miles = int(sys.argv[2])
            receipts = float(sys.argv[3])
            print(calculate_reimbursement(days, miles, receipts))
    else:
        # Run test cases from JSON
        try:
            json_path = os.path.join(os.path.dirname(__file__), "public_cases.json")
            with open(json_path, "r") as f:
                data = json.load(f)
            
            for idx, entry in enumerate(data, 1):
                inp = entry["input"]
                exp = entry["expected_output"]
                result = calculate_reimbursement(
                    inp["trip_duration_days"],
                    inp["miles_traveled"],
                    inp["total_receipts_amount"]
                )
                print(f"Test case {idx}: result={result}, expected={exp}, pass={result == exp}")
        except Exception as e:
            print("❌ Error:", e)