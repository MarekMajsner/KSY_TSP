from utils.experiment import load_experiments
from utils.gui import InteractivePointsApp
import argparse
import os

def main(args):
    print("You look great, by the way. Very healthy.")
    exp = load_experiments(args)
    app = InteractivePointsApp(experiments=exp,args=args)

if __name__=="__main__":
    parser = argparse.ArgumentParser(
        prog='Traveling Salesmen Human Evaluation App',
        description='Provides user with series of TSP with increasing difficulty')
    parser.add_argument('-d', '--debug',
                        action='store_true')
    parser.add_argument('-nl', '--nologs',
                        action='store_true')
    parser.add_argument('-n','--name')
    args = parser.parse_args()
    print(args)
    main(args)