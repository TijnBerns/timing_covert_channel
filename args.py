import argparse

def parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--msg', default="AttackAtDawn")
    parser.add_argument('--base', default=7, type=int)
    parser.add_argument('--delay', default=30, type=int)
    parser.add_argument('--timeout', default=20, type=int)
    parser.add_argument('--type', default=1, type=int)
    return parser.parse_args()