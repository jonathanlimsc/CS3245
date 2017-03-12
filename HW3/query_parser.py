from utils import normalize_token

operators = ['AND', 'OR', 'NOT']
brackets = ['(', ')']
precedence = {
    'AND' : 2,
    'OR' : 1,
    'NOT': 3
}

def convert_query_to_bool_exp(query):
    '''
    Converts a user query into a tokenized boolean expression
    '''
    query = query.replace("\n", "")
    query = query.split(' ')
    tokens = []
    for token in query:
        if token in operators:
            tokens.append(token)
        else:
            # Start or end has a bracket
            if token[0] in brackets:
                tokens.append('(')
                token = token[1:]
                tokens.append(normalize_token(token))
            elif token[-1] in brackets:
                token = token[0:-1]
                tokens.append(normalize_token(token))
                tokens.append(')')
            else:
                tokens.append(normalize_token(token))

    return tokens

def convert_to_postfix(tokens):
    '''
    Converts an in-fix boolean expression into a post-fix one, using the
    Shunting Yard algorithm.
    https://www.youtube.com/watch?v=QzVVjboyb0s
    '''

    output_queue = []
    op_stack = []

    for token in tokens:
        # Token
        if token not in operators and token not in brackets:
            output_queue.append(token)
        elif token not in brackets:
            # print token
        # Token is an Operator
            # While there is an op on top of the stack with higher precedence
            while len(op_stack) > 0 and op_stack[-1] not in brackets and precedence[op_stack[-1]] > precedence[token]:
                popped = op_stack.pop()
                output_queue.append(popped)
            op_stack.append(token)
        # Brackets
        elif token in brackets:
            if token == '(':
                op_stack.append(token)
            else:
                # Token is ')'
                while op_stack[-1] != '(':
                    popped = op_stack.pop()
                    output_queue.append(popped)
                # Discard the '('
                op_stack.pop()

    # Pop remaining operators into output queue
    while len(op_stack) > 0:
        output_queue.append(op_stack.pop())

    print output_queue
    return output_queue

# print convert_to_postfix(['9','+', '24', '/', '(', '7', '-', '3', ')'])
# print convert_to_postfix(['A','AND','B','OR','NOT','C'])
# print convert_to_postfix(['A','AND','B','OR','(','NOT','C',')'])
# print convert_query_to_bool_exp('(A OR B) AND C')
# print convert_to_postfix(convert_query_to_bool_exp('(A OR B) AND C'))
# print convert_to_postfix(convert_query_to_bool_exp('(A OR B) AND NOT C'))
# print convert_to_postfix(convert_query_to_bool_exp('A AND NOT C'))
