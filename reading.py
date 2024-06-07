
def parse_tesseract_data(data):
    """Convert Tesseract output to hierarchy of page, block, par, line, word"""
    n_boxes = len(data['level'])
    parsed_data = {'pages': []}
    
    current_page = {'blocks': []}
    current_block = {'pars': []}
    current_par = {'lines': []}
    current_line = {'words': []}
    
    last_page_num = -1
    last_block_num = -1
    last_par_num = -1
    last_line_num = -1
    
    for i in range(n_boxes):
        page_num = data['page_num'][i] - 1
        block_num = data['block_num'][i] - 1
        par_num = data['par_num'][i] - 1
        line_num = data['line_num'][i] - 1
        word_num = data['word_num'][i] - 1
        text = data['text'][i]
        
        if page_num != last_page_num:
            if last_page_num != -1:
                current_line['words'].append(text)
                current_par['lines'].append(current_line)
                current_block['pars'].append(current_par)
                current_page['blocks'].append(current_block)
                parsed_data['pages'].append(current_page)
                
            current_page = {'blocks': []}
            last_page_num = page_num
            last_block_num = -1
            last_par_num = -1
            last_line_num = -1
        
        if block_num != last_block_num:
            if last_block_num != -1:
                current_line['words'].append(text)
                current_par['lines'].append(current_line)
                current_block['pars'].append(current_par)
                current_page['blocks'].append(current_block)
                
            current_block = {'pars': []}
            last_block_num = block_num
            last_par_num = -1
            last_line_num = -1
        
        if par_num != last_par_num:
            if last_par_num != -1:
                current_line['words'].append(text)
                current_par['lines'].append(current_line)
                current_block['pars'].append(current_par)
                
            current_par = {'lines': []}
            last_par_num = par_num
            last_line_num = -1
        
        if line_num != last_line_num:
            if last_line_num != -1:
                current_line['words'].append(text)
                current_par['lines'].append(current_line)
                
            current_line = {'words': []}
            last_line_num = line_num
        
        if text.strip():
            current_line['words'].append(text)
    
    current_par['lines'].append(current_line)
    current_block['pars'].append(current_par)
    current_page['blocks'].append(current_block)
    parsed_data['pages'].append(current_page)
    
    return parsed_data

def overlaps(box1, box2):
    x1_min, y1_min, x1_max, y1_max = box1
    x2_min, y2_min, x2_max, y2_max = box2

    # Check if the bounding boxes overlap
    if (x1_min < x2_max and x1_max > x2_min and
        y1_min < y2_max and y1_max > y2_min):
        return True
    return False
