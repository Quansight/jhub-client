import json


def parse_notebook_cells(notebook_path):
    with open(notebook_path) as f:
        notebook_data = json.load(f)

    cells = []
    for cell in notebook_data['cells']:
        if cell['cell_type'] == 'code':
            source = ''.join(cell['source'])
            outputs = []
            for output in cell['outputs']:
                if output['output_type'] == 'stream':
                    outputs.append(''.join(output['text']))
                elif output['output_type'] == 'execute_result':
                    outputs.append(''.join(output['data']['text/plain']))
            result = '\n'.join(outputs)
            cells.append((source, result))

    return cells


TEMPLATE_SCRIPT_HEADER = '''
import os
import sys
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('jupyterhub_client')

OUTPUT_FORMAT = '{output_format}'
STDOUT_FILENAME = os.path.expanduser('{stdout_filename}')
STDERR_FILENAME = os.path.expanduser('{stderr_filename}')

if OUTPUT_FORMAT == 'file':
    logger.info('writting output to files stdout={stdout_filename} and stderr={stderr_filename}')
    sys.stdout = open(STDOUT_FILENAME, 'w')
    sys.stderr = open(STDERR_FILENAME, 'w')

'''


def tangle_cells(cells, output_format='file', stdout_filename=None, stderr_filename=None):
    # TODO: eventually support writing output to notebook

    tangled_code = []
    for i, (code, expected_result) in enumerate(cells):
        tangled_code.append('logger.info("beginning execution cell={i}")')
        tangled_code.append(code)
        tangled_code.append('logger.info("completed execution cell={i}")')
    return TEMPLATE_SCRIPT_HEADER + '\n'.join(tangled_code)
