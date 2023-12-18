import sys, os
from django import setup

# https://stackoverflow.com/a/32590521
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
setup()

# sys.path.append(os.path.abspath(os.sep.join(["..", "app"])))

print(sys.path)
from app.analysis import analysis


def main():
    pass
    # analysis()


if __name__ == "__main__":
    main()
