import csv

def create_csv_with_header(file_path, header):
    """
    Creates a CSV file with the specified header row.

    Parameters:
    - file_path (str): The path of the CSV file to be created.
    - header (list): A list of column names for the header row.

    Example:
    create_csv_with_header('output.csv', ['Name', 'Age', 'City'])
    """
    try:
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
        print(f"CSV file '{file_path}' created successfully with header: {header}")
    except Exception as e:
        print(f"Error creating CSV file: {e}")


def add_entry_to_csv(file_path, entry):
    """
    Adds a new row to a CSV file based on a dictionary entry.
    Raises an error if the dictionary keys don't match the CSV header.

    Parameters:
    - file_path (str): Path to the CSV file.
    - entry (dict): Dictionary containing the data for the new row.

    Example:
    add_entry_to_csv('output.csv', {'Name': 'Alice', 'Age': 25, 'City': 'New York'})
    """
    try:
        # Open the CSV file in read mode to get the header
        with open(file_path, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            header = reader.fieldnames

            # Check if all keys in the entry match the header
            if not all(key in header for key in entry.keys()):
                missing_keys = [key for key in entry.keys() if key not in header]
                raise ValueError(f"Entry contains invalid keys: {missing_keys}. Expected keys: {header}")

        # If the keys match, append the entry to the CSV file
        with open(file_path, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=header)
            writer.writerow(entry)

        print(f"Entry {entry} added successfully to '{file_path}'.")

    except Exception as e:
        print(f"Error adding entry to CSV file: {e}")


create_csv_with_header("testcsv.csv",["UID","Alter","Geschlecht"])
add_entry_to_csv("testcsv.csv", {"UID":1, "Alter": 12,"Geschlecht": "Mannlich"})