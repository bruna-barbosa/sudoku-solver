def check_row(self, row):
    lista = [self.__getitem__(i) for i in range(row * 9, (row + 1) * 9)]

    valid_list = [j for j in lista if j != 0]

    for ind, val in enumerate(valid_list):
        if val == 0:
            pass
        else:
            for ind_, val_ in enumerate(valid_list):
                if ind == ind_:
                    pass
                else:
                    if val == val_:
                        return False
    return True


def check_col(self, col):
    lista = [self.__getitem__(i) for i in range(col, 73 + col, 9)]
    valid_list = [j for j in lista if j != 0]

    for ind, val in enumerate(valid_list):
        if val == 0:
            pass
        else:
            for ind_, val_ in enumerate(valid_list):
                if ind == ind_:
                    pass
                else:
                    if val == val_:
                        return False
    return True


def check_box(self, box):

    if box % 3 == 0:
        inicio = 9*box
    else:
        if box < 3:
            inicio = 3*box
        else:
            inicio = (3 * box - (2 * (box % 3))) * 3

    if box % 3 == 0:
        lista = [self.__getitem__(i) for i in range(inicio, 21 + inicio) if (i % 9 < 3)]

    elif box % 3 == 1:
        lista = [self.__getitem__(i) for i in range(inicio, 21 + inicio) if (i % 9 > 2) & (i % 9 < 6)]

    else:
        lista = [self.__getitem__(i) for i in range(inicio, 21 + inicio) if (i % 9 > 5)]

    valid_list = [j for j in lista if j != 0]

    for ind, val in enumerate(valid_list):
        if val == 0:
            pass
        else:
            for ind_, val_ in enumerate(valid_list):
                if ind == ind_:
                    pass
                else:
                    if val == val_:
                        return False
    return True
