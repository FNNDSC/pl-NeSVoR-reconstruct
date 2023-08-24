#!/usr/bin/env python
from pathlib import Path
from chris_plugin import chris_plugin
from argparse import ArgumentParser, Namespace
import nesvor.cli.main
import nesvor.cli.parsers

__version__ = "0.5.0"

# main parser
parser = ArgumentParser(
    description="This ChRIS plugin is a wrapper of NeSVoR reconstruct",
    epilog="To learn more about NeSVoR, check out our repo at https://github.com/daviddmc/NeSVoR"
)
parser.add_argument('-i', '--input-stacks-pattern', default='**/*.nii', type=str,
                    help='input stacks file glob')
parser.add_argument('-o', '--output-volume', default='recon.nii', type=str,
                    help='output volume file name')
parser.add_argument('--output-resolution', default=0.75, type=float,
                    help='output volume resolution')
parser.add_argument('--svort-version', default='v2', type=str,
                    help='Version of SVoRT model')
parser.add_argument('-V', '--version', action='version', version=f'%(prog)s {__version__}')


@chris_plugin(
    parser=parser,
    title='NeSVoR Slice-to-Volume Reconstruction',
    category='Reconstruction',
    min_cpu_limit='4000m',
    min_memory_limit='12Gi',
    min_gpu_limit=1,
    max_gpu_limit=2
)
def main(options: Namespace, inputdir: Path, outputdir: Path):
    nesvor_parser, nesvor_subparsers = nesvor.cli.parsers.main_parser()
    input_stacks = inputdir.glob(options.input_stacks_pattern)
    args_list = [
        'reconstruct',
        '--input-stacks', *map(str, input_stacks),
        '--output-volume', str(outputdir / options.output_volume),
        '--output-resolution', str(options.output_resolution),
        '--svort-version', options.svort_version,
        '--debug', '--verbose', '2'
    ]
    args = nesvor_parser.parse_args(args_list)
    nesvor.cli.main.run(args)


if __name__ == '__main__':
    main()
