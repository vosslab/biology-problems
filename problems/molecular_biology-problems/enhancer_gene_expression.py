#!/usr/bin/env python3

import copy
import random
import bptools
from itertools import combinations

letters = list("ABCDFGHJKMPQRSTUWXYZ")

#========================================
colors = {
    'RED': '#e60000',
    'DARK ORANGE': '#e65400',
    'LIGHT ORANGE': '#e69100',
    'DARK YELLOW': '#999900',
    'LIME GREEN': '#4d9900',
    'GREEN': '#009900',
    'TEAL': '#00997a',
    'CYAN': '#009999',
    'SKY BLUE': '#087cc4',
    'BLUE': '#0039e6',
    'NAVY': '#004d99',
    'PURPLE': '#7b12a1',
    'MAGENTA': '#b30077',
    'PINK': '#cc0066'
}

#========================================
def reorder_list(my_list):
    N = random.randint(1, len(my_list)-1)
    new_list = my_list[-N:] + my_list[:-N]
    return new_list

#========================================
def enhancer_block(color_name, letter):
    color_id = colors[color_name]
    block = f'<td align="center" bgcolor="{color_id}" style="width: 30px; border: 3px solid #000000; color: #e8e8e8;"><strong>{letter}{letter}</strong></td>'
    return block

#========================================
def spacer_block():
	length = random.randint(20, 80)
	block = f'<td bgcolor="#e8e8e8" style="width: {length}px; border: 1px solid #232323;">&nbsp;</td>'
	return block

#========================================
def empty_block(length=20):
    block = f'<td style="width: {length}px; border: none;">&nbsp;</td>'
    return block

#========================================
def promotor_block():
    block = '<td align="center" bgcolor="#ccffcc" style="width: 100px; border: 2px solid #232323;">promotor</td>'
    return block

#========================================
def gene_block(gene_num):
    block = f'<td bgcolor="#ffb3b3" style="width: 200px; border: 3px solid #000000;"><strong>GENE {gene_num}</strong></td>'
    return block

#========================================
def parse_colors():
    color_names = list(colors.keys())
    #remove alternating
    color_names = reorder_list(color_names)
    color_names = color_names[::2]
    color_names.append(random.choice(list(colors.keys())))
    random.shuffle(color_names)
    random.shuffle(letters)
    enhancer_dict = {}
    for i,name in enumerate(color_names):
        enhancer_dict[name] = letters[i]
    return enhancer_dict

#========================================
def create_control_elements_html(gene_num, color_subset, enhancer_dict):
    table = '<table style="border-collapse: collapse;"><tr>'
    for name in color_subset:
        table += spacer_block()
        table += enhancer_block(name, enhancer_dict[name])
    table += spacer_block()
    table += spacer_block()
    table += spacer_block()
    table += promotor_block()
    table += gene_block(gene_num)
    table += '</tr></table>'
    return table

#========================================
def create_activator_set_html(activator_set, enhancer_dict):
    sorted_activator_set = sorted(activator_set, key=lambda x: enhancer_dict[x])
    table = '<table style="border-collapse: collapse; border: 2px solid #232323;"><tr><td>&nbsp;'
    table += '<table style="border-collapse: collapse;"><tr>'
    for name in sorted_activator_set:
        table += empty_block()
        table += enhancer_block(name, enhancer_dict[name])
    table += empty_block()
    table += '</tr></table>'
    table += '&nbsp;</td></tr>'
    table += '<tr><td align="center"><strong>Available Activator Proteins</strong></td></tr></table>'
    return table

#========================================
def get_subsets(color_names):
    subsets3 = list(combinations(color_names, 3))
    subsets4 = list(combinations(color_names, 4))
    subsets5 = list(combinations(color_names, 5))
    random.shuffle(subsets3)
    random.shuffle(subsets4)
    random.shuffle(subsets5)
    use_subsets = []
    use_subsets.append(list(random.choice(subsets3)))
    use_subsets.append(list(random.choice(subsets3)))
    use_subsets.append(list(random.choice(subsets4)))
    use_subsets.append(list(random.choice(subsets4)))
    use_subsets.append(list(random.choice(subsets5)))
    random.shuffle(use_subsets)
    return use_subsets

#========================================
def is_enhancer_set_activated(enhancer_set, activator_set):
    unbound_enhancers = copy.copy(enhancer_set)
    for a_color in activator_set:
        try:
            unbound_enhancers.remove(a_color)
        except ValueError:
            pass
    num_unbound_enhancers = len(unbound_enhancers)
    return num_unbound_enhancers


#========================================
def enhancer_sets_activated(enhancer_sets, activator_set):
    solutions = []
    for enhancer_set in enhancer_sets:
        num_unbound_enhancers = is_enhancer_set_activated(enhancer_set, activator_set)
        solutions.append(num_unbound_enhancers)
    if solutions.count(1) > 0:
        return False
    elif solutions.count(0) > 3:
        return False
    return True

#========================================
def find_activator_set(enhancer_sets):
    index_pairs = list(combinations(range(len(enhancer_sets)), 2))
    for i, j in index_pairs:
        activator_set = list(set(enhancer_sets[i] + enhancer_sets[j]))
        if len(activator_set) < 6:
            continue
        result = enhancer_sets_activated(enhancer_sets, activator_set)
        if result is True:
            return activator_set
    return False

#========================================
def setup_question():
    enhancer_dict = parse_colors()
    color_names = list(enhancer_dict.keys())
    enhancer_sets = get_subsets(color_names)

    activator_set = find_activator_set(enhancer_sets)
    if activator_set is False:
        return False
    return enhancer_dict, enhancer_sets, activator_set

#========================================
def pre_text():
    html_text = "<p>To promote gene expression, enhancers are specific DNA sequences that can be recognized and bound by transcription factors, including activator proteins.</p>"
    html_text += "<p>Consider the following set of activator proteins:</p>"
    return html_text

#========================================
def post_text():
    html_text = "<p>Below are five different genes, each with its own set of enhancers.</p>"
    html_text += "<p>Determine which of the genes are likely to be expressed based on the given set of activator proteins.</p>"
    html_text += "<p><i>Note that more than one answer may be correct.</i></p>"
    return html_text

#========================================
def write_question(N, args):
    result = False
    while result is False:
        result = setup_question()
    enhancer_dict, enhancer_sets, activator_set = result

    #print(use_subsets)
    question_text = pre_text()
    question_text += create_activator_set_html(activator_set, enhancer_dict)
    question_text += post_text()
    choices_list = []
    answers_list = []
    for i, subset in enumerate(enhancer_sets):
        random.shuffle(subset)
        gene_num = i + 1
        choice_html_text = create_control_elements_html(gene_num, subset, enhancer_dict)
        choices_list.append(choice_html_text)
        num_unbound_enhancers = is_enhancer_set_activated(subset, activator_set)
        if num_unbound_enhancers == 0:
            answers_list.append(choice_html_text)
    #print(question_text+''.join(choices_list))

    bbformat = bptools.formatBB_MA_Question(N, question_text, choices_list, answers_list)

    return bbformat

#========================================
def parse_arguments():
	parser = bptools.make_arg_parser(description="Generate enhancer gene expression questions.")
	args = parser.parse_args()
	return args


#========================================
def main():
	args = parse_arguments()
	outfile = bptools.make_outfile(__file__)
	bptools.collect_and_write_questions(write_question, args, outfile)


#========================================
#========================================
#========================================
if __name__ == '__main__':
    main()
