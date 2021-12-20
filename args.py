import argparse

def parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--msg', default="AttackAtDawn")
    parser.add_argument('--base', default=7, type=int)
    parser.add_argument('--delay', default=100, type=int)
    parser.add_argument('--timeout', default=100, type=int)
    parser.add_argument('--type', default=2, type=int)
    return parser.parse_args()
