import json


def parse_notebook_cells(notebook_path):
    with open(notebook_path) as f:
        notebook_data = json.load(f)

    cells = []
    for cell in notebook_data['cells']:
        if cell['cell_type'] == 'code':
            cells.append((''.join(cell['source']), ''.join(cell['outputs'][0]['data']['text/plain'])))

    return cells
