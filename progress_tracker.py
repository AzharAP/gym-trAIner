progress_log = {"squat": 0, "pushup": 0, "bicep_curl": 0}

def track_progress(exercise_type):
    progress_log[exercise_type] += 1

def display_progress():
    print("\n--- Progress Summary ---")
    for exercise, count in progress_log.items():
        print(f"{exercise.title()} corrections: {count}")
