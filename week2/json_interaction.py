import json

from pandas.io.json import json_normalize


def read_and_write_json_file():
    # open the json file with a context manager (i.e. the with statement) to ensure the file gets closed after opening
    with open('data.json') as file:
        data = json.load(file)

    # normalize the employees list in the json into a dataframe
    df = json_normalize(data['employees'])

    # add a row to our dataframe
    df['company'] = 'dunder mifflin'

    # convert the dataframe to a dictionary, which is more or less a json file; nest the dictionary in an overarching
    # employees key, as in data.json
    employees_dict = df.to_dict(orient='records')
    new_json = dict()
    new_json['employees'] = employees_dict

    # dump the file to disk using a context manager
    with open('new_data.json', 'w') as file:
        json.dump(new_json, file)


if __name__ == "__main__":
    read_and_write_json_file()
