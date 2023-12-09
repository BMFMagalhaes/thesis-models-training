import os
import re

def rename_files(folder_path, regex_pattern, replacement):
    # Get a list of all files in the folder
    files = os.listdir(folder_path)

    # Iterate over each file
    for file_name in files:
        # Check if the file name matches the regular expression pattern
        match = re.match(regex_pattern, file_name)
        if match:
            # Extract the captured groups from the match
            groups = match.groups()

            # Construct the new file name by replacing the captured portion with the specified replacement
            new_file_name = file_name.replace(groups[0], replacement)

            # Get the full paths of the old and new files
            old_file_path = os.path.join(folder_path, file_name)
            new_file_path = os.path.join(folder_path, new_file_name)

            # Rename the file
            os.rename(old_file_path, new_file_path)

# Set the folder path, regular expression pattern, and replacement string
folder_path = "D:\\BackupProtocoloRecolha\\07\\11"
regex_pattern = r"^(4)-.*\.png"
replacement = "11"

# Call the rename_files function with the provided parameters
rename_files(folder_path, regex_pattern, replacement)
