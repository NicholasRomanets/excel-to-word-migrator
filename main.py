from docx import Document

def main(start_i):
    changes = {}
    init = {}
    b_dict = {}
    with open('Source.csv', 'r', encoding='utf-8') as f:
        i = 1
        row_counter = 2
        row_init = 2
        row_b = 2
        for line in f:
            start_i = start_i+1
            if start_i>3:
                line = line.strip().split('\t')
                print(line)
                str_a = f"{line[2]}, {line[5]} {line[6]} {line[7]}"
                str_b= f"{line[3]}"
                str_i = f"{i}"
                b_dict[(row_b, 2)] = str_b
                changes[(row_counter, 1)] = str_a
                init[(row_init, 0)] = str_i
                row_counter += 1
                i += 1
                row_init += 1
                row_b += 1
    docx(changes, init, b_dict)

def docx(changes, init, b_dict):
    doc = Document('ds.docx')
    table = doc.tables[0]
    all_updates = {}
    for d in [init, changes, b_dict]:
        all_updates.update(d)

    for (row_idx, col_idx), new_text in all_updates.items():
        update_table_cell(table, row_idx, col_idx, new_text)


        # Сохраняем изменения
    doc.save('ds_updated.docx')
    print("Изменения сохранены в ds_updated.docx")

def update_table_cell(table, row_idx, col_idx, new_text):
    if row_idx >= len(table.rows):
        print(f"Ошибка: Нет строки {row_idx} в таблице (всего строк: {len(table.rows)}). Пропускаю.")
    if col_idx >= len(table.rows[row_idx].cells):
        print(f"Ошибка: Нет столбца {col_idx} в строке {row_idx}. Пропускаю.")
    print(f"Обновлена ячейка [{row_idx}][{col_idx}]: '{new_text}'")

    cell = table.rows[row_idx].cells[col_idx]
    cell.text = new_text

if __name__ == '__main__':
    start_i = 0
    main(start_i)