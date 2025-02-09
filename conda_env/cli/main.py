# Copyright (C) 2012 Anaconda, Inc
# SPDX-License-Identifier: BSD-3-Clause
import os
import sys

# pip_util.py import on_win from conda.exports
# conda.exports resets the context
# we need to import conda.exports here so that the context is not lost
# when importing pip (and pip_util)
import conda.exports  # noqa
from conda.base.context import context
from conda.cli.conda_argparse import ArgumentParser, _run_pre_command_hooks
from conda.cli.main import init_loggers
from conda.exceptions import conda_exception_handler
from conda.gateways.logging import initialize_logging

from . import main_config, main_create, main_export, main_list, main_remove, main_update


# TODO: This belongs in a helper library somewhere
# Note: This only works with `conda-env` as a sub-command.  If this gets
# merged into conda-env, this needs to be adjusted.
def show_help_on_empty_command():
    if len(sys.argv) == 1:  # sys.argv == ['/path/to/bin/conda-env']
        sys.argv.append("--help")


def create_parser():
    p = ArgumentParser()
    sub_parsers = p.add_subparsers()

    main_create.configure_parser(sub_parsers)
    main_export.configure_parser(sub_parsers)
    main_list.configure_parser(sub_parsers)
    main_remove.configure_parser(sub_parsers)
    main_update.configure_parser(sub_parsers)
    main_config.configure_parser(sub_parsers)

    show_help_on_empty_command()
    return p


def do_call(args, parser):
    relative_mod, func_name = args.func.rsplit(".", 1)
    # func_name should always be 'execute'
    from importlib import import_module

    # Run the pre_command actions
    command = relative_mod.replace(".main_", "")
    _run_pre_command_hooks(f"env_{command}", args)

    module = import_module(relative_mod, __name__.rsplit(".", 1)[0])
    exit_code = getattr(module, func_name)(args, parser)
    return exit_code


def main():
    initialize_logging()
    parser = create_parser()
    args = parser.parse_args()
    os.environ["CONDA_AUTO_UPDATE_CONDA"] = "false"
    context.__init__(argparse_args=args)
    init_loggers(context)
    return conda_exception_handler(do_call, args, parser)


if __name__ == "__main__":
    from conda.deprecations import deprecated

    deprecated.module("23.9", "24.3", addendum="Use `conda env` instead.")
    sys.exit(main())
