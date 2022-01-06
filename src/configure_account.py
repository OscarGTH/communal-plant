#!/usr/bin/env python3

from parse_config import get_configuration
from graph_handler import GraphHandler


def main():
    """ Main entry point of the app """
    # Get configuration
    args = get_configuration()
    # Create Instagram Graph API handler object
    gh = GraphHandler(args)
    # Create configuration files.
    gh.create_configuration_files()


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
