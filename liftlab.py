import json
import re

def read_documents(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def preprocess_input(input_text):
    # Convert to lowercase and remove non-alphanumeric characters
    processed_text = re.sub(r'[^a-zA-Z0-9\s]', '', input_text.lower())
    return processed_text

def preprocess_muscle_groups(muscle_groups):
    # Split the comma-separated muscle groups and remove leading/trailing spaces
    return [group.strip().lower() for group in muscle_groups.split(',')]

def search_workouts_by_muscle(data, muscle_group):
    matching_workouts = [workout['Workout Name'] for workout in data if muscle_group in workout['Processed Muscle Groups']]
    return matching_workouts

def search_muscle_groups_by_workout(data, workout_name):
    for workout in data:
        if workout_name.lower() == workout['Workout Name'].lower():
            return workout['Processed Muscle Groups']
    return None

def preprocess_data(data):
    for workout in data:
        workout['Processed Muscle Groups'] = preprocess_muscle_groups(workout['Muscle Group'])
    return data

def main():
    file_path = 'workouts.json'  # Update with your file path
    workout_data = read_documents(file_path)
    
    # Preprocess the data
    workout_data = preprocess_data(workout_data)

    while True:
        search_type = input("Do you want to search by muscle group or workout? Enter 'muscle' or 'workout' (or 'exit' to end): ").lower()

        if search_type == 'exit':
            print("Exiting the program. Goodbye!")
            break

        if search_type == 'muscle':
            user_input = input("Enter the muscle group you want to target: ")
            processed_user_input = preprocess_input(user_input)
            results = search_workouts_by_muscle(workout_data, processed_user_input)

            print("Matching Workouts:")
            if results:
                for result in results:
                    print(result)
            else:
                print("No matching workouts found.")

        elif search_type == 'workout':
            user_input = input("Enter the workout name you want to search: ")
            processed_user_input = preprocess_input(user_input)
            muscle_groups = search_muscle_groups_by_workout(workout_data, processed_user_input)

            if muscle_groups:
                print(f"The muscle groups for '{user_input}' are: {', '.join(muscle_groups)}")
            else:
                print(f"No information found for workout '{user_input}'.")

        else:
            print("Invalid search type. Please enter 'muscle', 'workout', or 'exit'.")

if __name__ == "__main__":
    main()