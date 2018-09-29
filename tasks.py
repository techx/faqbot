""" A little file to run training and data
collection tasks without firing up the server.
"""

import argparse

from faqbot.features.smartreply import collect_data, train_model

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--collect", help="Log in and collect emails for training the model."
    )
    parser.add_argument("--train", help="Train a model on collected emails.")
    args = parser.parse_args()

    if args.collect:
        collect_data()

    if args.train:
        train_model()

    print "All Done!"
