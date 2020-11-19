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
