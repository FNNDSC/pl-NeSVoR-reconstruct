#!/usr/bin/env python

from pathlib import Path
from os import path
from chris_plugin import chris_plugin
from argparse import ArgumentParser, Namespace
import torch
from nesvor.utils import set_seed, setup_logger
from nesvor.cli.commands import Reconstruct
from nesvor.cli.formatters import Formatter
from nesvor.cli.parsers import (
    build_parser_inputs,
    build_parser_outputs,
    build_parser_segmentation, 
    build_parser_bias_field_correction, 
    build_parser_assessment, 
    build_parser_svort, 
    build_parser_training, 
    build_parser_common,
    build_parser_stack_masking,
    build_parser_outputs_sampling,
)
import nesvor

__version__ = "0.1.0"

# main parser
parser = ArgumentParser(
    prog="nesvor_reconstruct",
    description="This ChRIS plugin is a wrapper of NeSVoR",
    epilog="To learn more about NeSVoR, check out our repo at https://github.com/daviddmc/NeSVoR",
    formatter_class=Formatter,
    parents=[
        build_parser_inputs(input_stacks="required"),
        build_parser_stack_masking(),
        build_parser_outputs(output_volume="required", output_json=False),
        build_parser_outputs_sampling(output_volume="required"),
        build_parser_segmentation(optional=True),
        build_parser_bias_field_correction(optional=True),
        build_parser_assessment(),
        build_parser_svort(),
        build_parser_training(),
        build_parser_common(),
    ]
)

parser.add_argument(
    "-v",
    "--version",
    action="version",
    version=f"wrapper version: {__version__}; NeSVoR version: {nesvor.__version__}",
)

def join_path(options, dir_path, keys):
    for k in keys:
        old_value = getattr(options, k, None)
        if old_value is None:
            setattr(options, k, None)
        elif isinstance(old_value, list):
            setattr(options, k, [path.join(dir_path, ov) for ov in old_value])
        elif isinstance(old_value, str):
            setattr(options, k, path.join(dir_path, old_value))
        else:
            raise TypeError('unknown data type')

@chris_plugin(
    parser=parser,
    title='ChRIS plugin for NeSVoR',
    category='Reconstruction', # ref. https://chrisstore.co/plugins
    min_gpu_limit=1 # set min_gpu_limit=1 to enable GPU
)
def main(options: Namespace, inputdir: Path, outputdir: Path):
    """
    *ChRIS* plugins usually have two positional arguments: an **input directory** containing
    input files and an **output directory** where to write output files. Command-line arguments
    are passed to this main method implicitly when ``main()`` is called below without parameters.

    :param options: non-positional arguments parsed by the parser given to @chris_plugin
    :param inputdir: directory containing (read-only) input files
    :param outputdir: directory where to write output files
    """

    # setup
    options.device = torch.device(options.device)
    set_seed(options.seed)
    if options.debug:
        options.verbose = 2
    # handle I/O
    join_path(options, inputdir, ['input_stacks', 'volume_mask', 'sample_mask', 'sample_orientation', "stack_masks"])
    join_path(options, outputdir, ['output_log', 'output_volume'])
    setup_logger(options.output_log, options.verbose)

    options.input_slices = None
    options.output_model = None

    # execute command
    Reconstruct(options).main()


if __name__ == '__main__':
    main()