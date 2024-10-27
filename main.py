from exercise_analysis import analyze_exercise
from workout_plan import generate_workout_plan
from progress_tracker import display_progress


def main():
    print("Select an exercise (squat, pushup, bicep_curl):")
    exercise = input().lower()
    
    print("Select your fitness level (beginner, intermediate, advanced):")
    fitness_level = input().lower()
    
    print("Select your fitness goal (strength or hypertrophy):")
    goal = input().lower()

    # Generate a workout plan based on input
    plan = generate_workout_plan(fitness_level, goal)
    print(f"\nYour Workout Plan: {plan}")

    # Start exercise analysis
    analyze_exercise(exercise)
    
    # Display progress
    display_progress()

if __name__ == "__main__":
    main()
