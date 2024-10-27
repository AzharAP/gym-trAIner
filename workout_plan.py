def generate_workout_plan(fitness_level, goal):
    plans = {
        "beginner": {
            "strength": ["Squats - 3x12", "Push-ups - 3x8", "Bicep Curls - 3x10"],
            # Other levels/goals
        },
        "intermediate": {
            "strength": ["Squats - 3x12", "Push-ups - 3x8", "Bicep Curls - 3x10"]
        },
        "advanced": {
            "strength": ["Squats - 3x12", "Push-ups - 3x8", "Bicep Curls - 3x10"]
        }
    }
    return plans.get(fitness_level, {}).get(goal, [])
