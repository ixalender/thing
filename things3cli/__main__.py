import os
import sys

if not __package__:
    # Running from source. Add things3cli's source code to the system
    # path to allow direct invocation, such as:
    #   python src/things3cli --help
    things3cli_package_source_path = os.path.dirname(os.path.dirname(__file__))
    sys.path.insert(0, things3cli_package_source_path)

from things3cli.main import cli


if __name__ == "__main__":
    sys.exit(cli())
