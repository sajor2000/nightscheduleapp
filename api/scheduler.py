from datetime import datetime, timedelta
from collections import defaultdict
import random

def generate_schedule(month, preferences_data, existing_schedule=None):
    """
    Generate an optimized schedule based on doctor preferences.
    
    Args:
        month: String in format 'YYYY-MM'
        preferences_data: List of preference dictionaries
        existing_schedule: Optional existing schedule to modify
    
    Returns:
        Dictionary mapping dates to doctor IDs
    """
    year, month_num = map(int, month.split('-'))
    
    # Get all days in the month
    first_day = datetime(year, month_num, 1)
    if month_num == 12:
        last_day = datetime(year + 1, 1, 1) - timedelta(days=1)
    else:
        last_day = datetime(year, month_num + 1, 1) - timedelta(days=1)
    
    days_in_month = (last_day - first_day).days + 1
    all_dates = [(first_day + timedelta(days=i)).strftime('%Y-%m-%d') 
                 for i in range(days_in_month)]
    
    # Initialize schedule
    schedule = existing_schedule.copy() if existing_schedule else {}
    
    # Track assignments per doctor
    doctor_shifts = defaultdict(int)
    doctor_prefs = {p['doctor_id']: p for p in preferences_data}
    
    # Count existing assignments
    for date, doctor_id in schedule.items():
        if doctor_id in doctor_prefs:
            doctor_shifts[doctor_id] += 1
    
    # Sort dates to ensure consistent ordering
    unassigned_dates = [d for d in all_dates if d not in schedule]
    
    # Score function for doctor assignment
    def score_assignment(doctor_id, date, doctor_shifts_count):
        pref = doctor_prefs.get(doctor_id)
        if not pref:
            return -1000  # Doctor has no preferences submitted
        
        score = 0
        
        # Check if unavailable
        if date in pref.get('unavailable', []):
            return -1000  # Cannot work this day
        
        # Check if preferred
        if date in pref.get('preferred', []):
            score += 50  # High preference for preferred days
        
        # Check if under desired shift count
        desired = pref.get('desired_shifts', 0)
        current = doctor_shifts_count.get(doctor_id, 0)
        
        if current < desired:
            score += 20  # Needs more shifts
        elif current == desired:
            score += 0   # Has enough shifts
        else:
            score -= 30  # Already has too many shifts
        
        # Penalize consecutive nights (optional)
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        prev_date = (date_obj - timedelta(days=1)).strftime('%Y-%m-%d')
        next_date = (date_obj + timedelta(days=1)).strftime('%Y-%m-%d')
        
        if schedule.get(prev_date) == doctor_id or schedule.get(next_date) == doctor_id:
            score -= 10  # Slight penalty for consecutive nights
        
        # Add randomness for tie-breaking
        score += random.uniform(-1, 1)
        
        return score
    
    # Assign each unassigned date
    for date in unassigned_dates:
        best_doctor = None
        best_score = -999999
        
        # Try each doctor
        for doctor_id in doctor_prefs.keys():
            score = score_assignment(doctor_id, date, doctor_shifts)
            if score > best_score:
                best_score = score
                best_doctor = doctor_id
        
        # Assign the best doctor if found
        if best_doctor and best_score > -1000:
            schedule[date] = best_doctor
            doctor_shifts[best_doctor] += 1
    
    return schedule

def validate_schedule(schedule, preferences_data):
    """
    Validate that the schedule respects all hard constraints.
    
    Returns:
        (is_valid, list_of_errors)
    """
    errors = []
    doctor_prefs = {p['doctor_id']: p for p in preferences_data}
    
    for date, doctor_id in schedule.items():
        if doctor_id not in doctor_prefs:
            errors.append(f"Doctor {doctor_id} has no preferences for this month")
            continue
        
        pref = doctor_prefs[doctor_id]
        if date in pref.get('unavailable', []):
            errors.append(f"Doctor {pref['doctor_name']} is assigned on {date} but marked unavailable")
    
    return len(errors) == 0, errors