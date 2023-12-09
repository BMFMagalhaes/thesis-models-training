import os
import re
import shutil

def move_items(source_folder, destination_folder, regex_pattern):
    # Check if the source folder exists
    if not os.path.exists(source_folder):
        print("{} folder does not exist.".format(source_folder))
        return
    # Create the destination folder if it doesn't exist
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Get a list of all items in the source folder
    items = os.listdir(source_folder)

    # Iterate over each item
    for item in items:
        # Check if the item matches the regular expression pattern
        if re.match(regex_pattern, item):
            # Get the full path of the item
            item_path = os.path.join(source_folder, item)

            # Move the item to the destination folder
            shutil.move(item_path, destination_folder)
    print("{} was moved.".format(source_folder))

# Set the source folder, destination folder, and regular expression pattern
source_folder = "C:\\ProtocoloRecolha\\01"

clique_folder = "C:\\image-training\\clique"
mouse_folder = "C:\\image-training\\mouse"
mover_folder = "C:\\image-training\\mover"
rodar_folder = "C:\\image-training\\rodar"
zoomin_folder = "C:\\image-training\\zoomin"
zoomout_folder = "C:\\image-training\\zoomout"

for x in range(1, 25):
    if x < 10:
        source_folder = "C:\\ProtocoloRecolha\\0{}".format(x)
    else:
        source_folder = "C:\\ProtocoloRecolha\\{}".format(x)

    for i in range(13):
        regex_pattern = r"^({})-.*\.png".format(i)
        if i == 0:
            destination_folder = clique_folder
        elif i == 1:
            destination_folder = mover_folder
        elif i == 2:
            destination_folder = rodar_folder
        elif i == 3:
            destination_folder = zoomin_folder
        elif i == 4:
            destination_folder = zoomout_folder
        elif i == 5:
            destination_folder = mouse_folder
        elif i == 7:
            destination_folder = clique_folder
        elif i == 8:
            destination_folder = mover_folder
        elif i == 9:
            destination_folder = rodar_folder
        elif i == 10:
            destination_folder = zoomin_folder
        elif i == 11:
            destination_folder = zoomout_folder
        elif i == 12:
            destination_folder = mouse_folder
        # Call the move_items function with the provided parameters
        if i != 6:
            move_items(source_folder, destination_folder, regex_pattern)