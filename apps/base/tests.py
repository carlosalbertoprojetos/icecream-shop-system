from django.test import TestCase

# Create your tests here.
# comando pytest cov


def comando():
    print("py -m pytest --cov .")
    print("py -m pytest --cov-report html --cov .")


comando()
