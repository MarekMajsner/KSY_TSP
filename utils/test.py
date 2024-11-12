import os

def count_directories(path):
    return len(next(os.walk(path))[1])

# Example usage
directory_path = 'path_to_your_directory'
num_directories = count_directories(directory_path)
print(f'There are {num_directories} directories in {directory_path}')
