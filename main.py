import argparse

from securedev.agent import SecurityReviewAgent


def main():

    parser = argparse.ArgumentParser(
        description="SecureDev AI - Automated Security Review"
    )

    parser.add_argument(
        "directory",
        help="Directory containing source code to scan"
    )

    args = parser.parse_args()

    agent = SecurityReviewAgent(args.directory)

    agent.run()


if __name__ == "__main__":
    main()