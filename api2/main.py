import sys, os
from django import setup

# https://stackoverflow.com/a/32590521
sys.path.append(".")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
setup()

from app.analysis import analysis


def main():
    analysis()


if __name__ == "__main__":
    main()
