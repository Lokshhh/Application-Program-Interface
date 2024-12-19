import os

if os.path.exists('credentials.json'):
    print("File found!")
else:
    print("File not found. Check the location and name.")
