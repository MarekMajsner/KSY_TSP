from utils.experiment import load_experiments
import argparse
import os

def count_directories(path):
    return len(next(os.walk(path))[1])

def main():
    print("You look great, by the way. Very healthy.")
    load_experiments()
    # run_gui()
    print("Congratulations, the test is now over.")
    print("In Fact, "
          "You Did So Well I’m Going To Note This On Your File In the Commendations Section. "
          "Oh, There’s Lots Of Room Here.")

if __name__=="__main__":
    parser = argparse.ArgumentParser(
        prog='ProgramName',
        description='What the program does',
        epilog='Text at the bottom of help')
    parser.add_argument('-t', '--testload',
                        action='store_true')  # on/off flag
    parser.add_argument('-c', '--count')  # option that takes a value
    args = parser.parse_args()
    print(args)
    main()