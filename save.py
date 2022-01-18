import json
import io
import os

# Dictionary for saved game data
save_dict = {}

# Function from ssaving the dictionary to a file
def save_data():
    # Bring save dictionary into scope
    global save_dict

    # Open and write to save file
    with open("save.json", "w") as file:
        json.dump(save_dict, file)

# Function for loading the dictionary from a file
def load_data():
    # Bring save dictionary into scope
    global save_dict

    if os.path.isfile("save.json"):
        # Read the json
        file_string = io.open("save.json").read()
        save_dict = json.loads(file_string)

    else:
        # Save file did not exist, create an empty json
        open("save.json", "w").write("{}")
        save_dict = {}

# Auto load data when module is imported
load_data()