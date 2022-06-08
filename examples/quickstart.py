"""
This example script imports the Lambda package and
prints out the version.
"""

import Lambda


def main():
    print(
        f"Lambda version: {Lambda.__version__}"
    )


if __name__ == "__main__":
    main()
