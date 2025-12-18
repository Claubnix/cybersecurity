import os
import hashlib
import json


# Simulated list of known malicious file hashes (for demonstration)
MALICIOUS_HASHES = {
    "cc805d5fab1fd71a4ab352a9c533e65fb2d5b885518f4e565e68847223b8e6b85cb48f3afad842726d99239c9e36505c64b0dc9a061d9e507d833277ada336ab",
    "bad_hash_2", # Replace with actual hash values
    "bad_hash_3"
}


def calculate_hash(file_path):
    """Calculate the SHA-512 hash of a file."""
    hasher = hashlib.sha512()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def create_hashes(directory):
    """Create a dictionary of file hashes in the specified directory."""
    file_hashes = {}
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_hashes[file_path] = calculate_hash(file_path)
    return file_hashes


def save_hashes_to_file(hashes, output_file):
    """Save the hashes to a JSON file."""
    with open(output_file, 'w') as f:
        json.dump(hashes, f, indent=4)


def load_hashes_from_file(input_file):
    """Load hashes from a JSON file."""
    with open(input_file, 'r') as f:
        return json.load(f)


def check_integrity_and_malware(directory, hash_file):
    """Check the integrity of files and scan for malware."""
    current_hashes = create_hashes(directory)
    
    try:
        saved_hashes = load_hashes_from_file(hash_file)
    except FileNotFoundError:
        print("Hash file not found. Please create hashes first.")
        return

    for file_path, current_hash in current_hashes.items():
        saved_hash = saved_hashes.get(file_path)
        if saved_hash is None:
            print(f"New file detected: {file_path}")
        elif current_hash != saved_hash:
            print(f"File altered: {file_path}")
        else:
            print(f"File unchanged: {file_path}")

        # Check for malicious files
        if current_hash in MALICIOUS_HASHES:
            print(f"Warning! Malicious file detected: {file_path}")

    # Check for deleted files
    for file_path in saved_hashes.keys():
        if file_path not in current_hashes:
            print(f"File deleted: {file_path}")


if __name__ == "__main__":
    directory_to_check = "your_directory_path_here"  # Replace with your directory path
    hash_file_path = "file_hashes.json"

    # Uncomment the following line to create and save hashes
    save_hashes_to_file(create_hashes(directory_to_check), hash_file_path)

    # Check integrity of files and scan for malware
    check_integrity_and_malware(directory_to_check, hash_file_path)
