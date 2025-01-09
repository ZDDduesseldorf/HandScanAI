import csv
import os


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
        with open(file_path, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(header)
        print(f"CSV file '{file_path}' created successfully with header: {header}")
    except Exception as e:
        print(f"Error creating CSV file: {e}")


def add_entry_to_csv(file_path, entry):
    """
    Adds a new row to a CSV file based on a dictionary entry.
    Writes only matching keys to the CSV file and raises an error if no keys match.

    Parameters:
    - file_path (str): Path to the CSV file.
    - entry (dict): Dictionary containing the data for the new row.

    Example:
    add_entry_to_csv('output.csv', {'Name': 'Alice', 'Age': 25, 'City': 'New York'})
    """
    try:
        # Open the CSV file in read mode to get the header
        with open(file_path, newline="") as file:
            reader = csv.DictReader(file)
            header = reader.fieldnames

            # Find matching keys between the entry and the CSV header
            matching_keys = [key for key in entry.keys() if key in header]

            # Check if there are any matching keys
            if not matching_keys:
                raise ValueError(f"Entry contains no valid keys. Expected keys: {header}")

        # If there are matching keys, append the entry to the CSV file
        with open(file_path, mode="a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=header)

            # Filter the entry to only include matching keys
            filtered_entry = {key: entry[key] for key in matching_keys}

            # Write the filtered entry to the CSV file
            writer.writerow(filtered_entry)
    except Exception as e:
        print(f"Error adding entry to CSV file: {e}")


def add_embedding_dict_to_css(embedding_csvs_folder_path, embeddings_dict):
    """
    Adds embeddings from a dictionary to the corresponding CSV files.

    Args:
        embedding_csvs_folder_path (str): Path to the folder containing the all embedding CSV files that are mentioned by region name in the embeddings_dict .
        embeddings_dict (dict): A dictionary with the following structure:
            {
                "uuid": str,  # Unique identifier for the embeddings
                "embeddings": dict {
                    region (str): embedding (torch.Tensor)
                }
            }

    """

    for region, _ in embeddings_dict["embeddings"].items():
        csv_name = region + "_Embeddings.csv"
        file_path = os.path.join(embedding_csvs_folder_path, csv_name)

        if os.path.isfile(file_path):
            continue
        else:
            raise FileNotFoundError(f"CSV file not found while saving the ebeddings: {file_path}")

    uuid = embeddings_dict["uuid"]
    for region, embedding in embeddings_dict["embeddings"].items():
        csv_name = region + "_Embeddings.csv"
        file_path = os.path.join(embedding_csvs_folder_path, csv_name)
        add_entry_to_csv(file_path, {"UUID": uuid, "Embedding": embedding.numpy().tolist()})
