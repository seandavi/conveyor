from ruffus import *

parser = cmdline.get_argparse(description='run an rna-seq pipeline')

# required arguments
parser.add_argument('config',type='file',
                    help='YAML formatted config file')

parser.add_argument('samplesheet',type='file',
                    help='filename of sample sheet')

# set up logging
logger, logger_mutex = cmdline.setup_logging (__name__, options.log_file, options.verbose)

options = parser.parse_args()

cmdline.run(options)
