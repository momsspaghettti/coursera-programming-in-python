from contracts import contract


@contract(seq='str', returns='bool')
def is_braces_sequence_correct(seq):
    """
    >>> is_braces_sequence_correct("()(())")
    True
    >>> is_braces_sequence_correct("()[()]")
    True
    >>> is_braces_sequence_correct("(")
    False
    >>> is_braces_sequence_correct("[()")
    False
    >>> is_braces_sequence_correct("[(])")
    False
    """
    char_list = []
    op_char_list = []

    for char in seq:
        if char == '(':
            char_list.append(char)
            op_char_list.append(')')

        if char == '[':
            char_list.append(char)
            op_char_list.append(']')

        if char == '{':
            char_list.append(char)
            op_char_list.append('}')

        if char == op_char_list[len(op_char_list) - 1]:
            op_char_list.pop()
            char_list.pop()

    return len(char_list) == 0


if __name__ == '__main__':
    import doctest
    doctest.testmod()