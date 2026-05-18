import argparse

from executor import run_tests


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command")
    parser.add_argument("problem")

    args = parser.parse_args()

    if args.command == "test":
        run_tests(args.problem)

if __name__ == "__main__":
    main()
