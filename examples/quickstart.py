"""
This example script imports the lambda package and
prints out the version.
"""

import Lambda


def main():
    print(
        f"lambda version: {Lambda.__version__}"
    )


if __name__ == "__main__":
    main()
