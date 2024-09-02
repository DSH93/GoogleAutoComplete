import sys
import os

def start(folder_path):
    # read all files in folder and in sub directories
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            print(os.path.join(root, file))
        for dir in dirs:
            print(os.path.join(root, dir))
        





if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) == 0:
        print("Please provide a path to the file")
        sys.exit(1)
    if not os.path.exists(args[0]):
        print("Directory does not exist")
        sys.exit(1)
    start(args[0])
