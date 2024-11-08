import math

from uQR import QRCode

def _scale_matrix(matrix, scale):
    new_matrix = []
    for row in matrix:
        new_row = []
        for cell in row:
            for _ in range(scale):
                new_row.append(cell)
        for _ in range(scale):
            new_matrix.append(new_row)
    return new_matrix


def _add_border(matrix, border_a, border_b):
    if len(matrix) == 0:
        return matrix

    row_len = len(matrix[0])
    blank_row = [False] * border_a + [False] * row_len + [False] * border_b
    new_matrix = []
    # Add top border
    for _ in range(border_a):
        new_matrix.append(blank_row)
    for row in matrix:
        new_row = []
        # Add left border
        for _ in range(border_a):
            new_row.append(False)
        for cell in row:
            new_row.append(cell)
        # Add right border
        for _ in range(border_b):
            new_row.append(False)
        new_matrix.append(new_row)
    # Add bottom border
    for _ in range(border_b):
        new_matrix.append(blank_row)
    return new_matrix


def make_code(data, max_size):

    qr = QRCode(box_size=1, border=0)
    qr.add_data(data)
    qr.make()

    qr_size = qr.modules_count
    scale = math.floor(max_size / qr.modules_count)
    size_diff = max_size - (qr_size * scale)

    border_a = math.floor(size_diff / 2)  # top, left border
    border_b = math.ceil(size_diff / 2)  # bottom, right border

    matrix = qr.get_matrix()

    scaled_matrix = _scale_matrix(matrix, scale)
    bordered_matrix = _add_border(scaled_matrix, border_a, border_b)

    return bordered_matrix