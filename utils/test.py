import os

def count_directories(path):
    return len(next(os.walk(path))[1])

# Example usage
directory_path =  os.path.split(os.getcwd())[0]
directory_path = os.path.join(directory_path,'experiments')
num_directories = count_directories(directory_path)
print(f'There are {num_directories} directories in {directory_path}')
