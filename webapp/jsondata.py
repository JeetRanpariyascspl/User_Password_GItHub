import json, os


class JsonData:
    @staticmethod
    def write_json(file_path, new_data):
        path = os.path.join(os.path.dirname(os.path.dirname(__file__)), file_path)
        # If file does NOT exist, create it with a list containing new_data
        if not os.path.exists(path):
            print("File not found. Creating a new one...")
            with open(path, "w") as f:
                json.dump([new_data], f, indent=4)
            return

        # If file exists, read old data and append new_data
        with open(path, "r") as f:
            try:
                old_data = json.load(f)
                if not isinstance(old_data, list):
                    # If it's not a list, let's not pretend it's okay
                    # print("Existing JSON isn't a list. Fixing it.")
                    old_data = [old_data]
            except json.JSONDecodeError:
                # print("File was empty or broken. Starting fresh.")
                old_data = []

        old_data.append(new_data)

        # Write updated data back
        with open(path, "w") as f:
            json.dump(old_data, f, indent=4)

        # print("Data appended successfully!")

    @staticmethod
    def read_json(filename: str):
        """Read and return JSON content from file."""
        path = os.path.join(os.path.dirname(os.path.dirname(__file__)), filename)
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
