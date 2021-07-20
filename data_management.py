import json

def serialization_json(relative_path, file, data):
    # if no empty parameter
    if relative_path and file and data:
        # Open file to write
        with open(f"{relative_path}{file}.json", "w") as write:
            json.dump(data, write)
        write.close()


def deserialization_json(self, relative_path, file):
    # if no empty parameter
    if relative_path and file:
        # Open JSON file
        json_file = open('data.json', )

    # JSON object as a dictionary
    data = json.load(json_file)

    # Closing the JSON file
    json_file.close()
    return data
