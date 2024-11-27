import os

# Specify the folder path
folder_path = "Impulse_Reponse"

# List all files in the folder
files = os.listdir(folder_path)

for file in files:
    print(file)