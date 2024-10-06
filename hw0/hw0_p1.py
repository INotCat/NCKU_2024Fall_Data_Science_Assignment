'''
0. class Term is used to store variable and its corresponding coefficient and exponent.
    eg.    a Term object stores 2X2Y6Z3 ->  coefficeint=2  dict = {'X':2, 'Y':6, 'Z':3}
1. class Polynomial is used to store list a Term object
    eg.    a Polynomial could be 2X2Y6Z3  +2X  +Z + 1
            so we have 4 Term objects, namely 2X2Y6Z3, 2X, Z, and 1
            store in the list member of a Polynomial class
2. I define the special method for the basic operation like add, multiple, equal of these
    class, to complete the basic arithmetic of the polynomial
'''
class Term:
    def __init__(self, coefficient=1, variables=None):
        self.coefficient = coefficient   
        
        # If variables is not provided, it defaults to an empty dictionary.
        # type: Dict[string variable, int exponent]
        self.variables = variables if variables else {} 
        
    def __add__(self, other: 'Term') -> 'Term' :
        if self.variables == other.variables :
            new_coefficient = self.coefficient + other.coefficient
            org_variables = self.variables.copy()
            return Term(new_coefficient, org_variables)
        else:
            raise ValueError("Cannot add Terms with different variables")
    
    def __mul__(self, other: 'Term') -> 'Term' :
        new_coefficient = self.coefficient * other.coefficient
        new_variables = self.variables.copy()
        
        #provides pairs like ('x', 2)
        #X2Y3  * X1Y3Z5 = X3Y6Z5
        for var, exp in other.variables.items(): 
            if var in new_variables:                            
                new_variables[var] += exp
            else:
                new_variables[var] = exp
               
        return Term(new_coefficient, new_variables)

    ## do two customed print types
    def __str__(self):
        if self.coefficient == 0:
            return ''  # Skip terms with zero coefficient

        # Create variable string with carets
        var_str = ''.join([f"{var}^{exp}" if int(exp) > 1 else var for var, exp in sorted(self.variables.items())])

        # Format coefficient and variable string
        if self.coefficient == 1:
            # Omitting the coefficient of 1, except if the term is just a variable part
            return var_str if var_str else '1'
        elif self.coefficient == -1:
            # Handling coefficient -1 to ensure it appears as "-var" instead of "-1*var"
            return f"-{var_str}" if var_str else '-1'
        else:
            return f"{self.coefficient}*{var_str}" if var_str else str(self.coefficient)
        
    def __eq__(self, other: 'Term'):
        return sorted(self.variables.items()) == sorted(other.variables.items())
    
class Polynomial:
    def __init__(self, terms = None):
        self.terms = terms if terms is not None else []
        
    def __add__(self, other: 'Polynomial'):
        new_terms = self.terms + other.terms
        combined_terms = {}
        
        for term in new_terms:
            term_key = tuple(sorted(new_terms.variables.items()))
            if term_key in combined_terms:
                combined_terms[term_key].coefficient += term.coefficient
            else:
                combined_terms[term_key] = term
        
        return Polynomial([term for term in combined_terms.values if term.coefficient != 0])
        
    def __mul__(self, other: 'Polynomial') -> 'Polynomial':
        new_terms = []
        for term1 in self.terms:
            for term2 in other.terms:
                new_terms.append(term1 * term2)
        # new_terms.append(Term(999, {'Z':3, 'W':5}))
        # new_terms.append(Term(-1, {'W':5, 'Z':3}))
        # for t in new_terms:
        #     print(t)
        
        # Combine terms with the same variables
        combined_terms = [] 
        for term in new_terms:
            found = False
            
            for combined_term in combined_terms:
                # If the variables match, combine the coefficients
                if combined_term == term:
                    combined_term.coefficient += term.coefficient
                    found = True
                    break

            if not found:
                combined_terms.append(term)
        return Polynomial(combined_terms)
    
    def __str__(self):
    
        if not self.terms:
            return '0'

        result = []
        for term in self.terms:
            term_str = str(term)  # Assuming the term’s __str__ method uses caret_flag

            # Add appropriate plus or minus signs
            if term.coefficient > 0:
                if result:  # Avoid leading '+' sign for the first term
                    result.append(f' + {term_str}')
                else:
                    result.append(term_str)  # First term, no leading '+'
            elif term.coefficient < 0:
                result.append(f' - {term_str.lstrip("-")}')  # Ensure no double minus signs
            else:
                result.append(term_str)

        #Handle 000, 00, 0
        if(set(result) == {'0'}):
            return '0'
            
        represent_str = ''.join(result)
        return represent_str

'''
Do String analysis
0. We first replace all '*' and '^' to ''
1. I first check if the input string has balanced parenthesis, which means each '(' should match a ')'
   If not, we print an error 'Parenthesis is not balanced'
2. Then I extract the coefficent+variable together from '+' and '-'
3. I then input the string from 2. into create the object of Term
   And then assemble all the Term to be a Polynomial object
'''
DEBUG = False    
# split by parentheses via stack ()
def extract_poly_from_parentheses(s: str) -> list:
    segments = []
    stack = []
    start = 0
    # Iterate over the string
    for i, char in enumerate(s):
        if char == '(':
            if not stack:
                start = i
            stack.append(char)
        elif char == ')':
            stack.pop()
            if not stack:
                segments.append(s[start+1:i])
                
    if len(stack) != 0:
        print("Parenthesis is not balanced")
        exit()
        
    if segments == ['']:
        print('Polynomial cannot be empty inside parenthesis. Do again.')
        exit()
    return segments

# split by + or - character
def extract_term_from_plus_minus(s: str) -> list:
    if not s:
        print('Polynomial cannot be empty inside parenthesis. Do again.')
        exit()
    segments = []
    start = 0
    i = 0
    length = len(s)

    i = 1 if s[0] in '+-' else 0
    
    while i < length:
        # Check if the current character is '+' or '-'
        if s[i] == '+' or s[i] == '-':
            # Append the term from start to the current position
            segments.append(s[start:i].strip())
            start = i  # Update start to the current sign
        
        i += 1
    
    if start < length:
        segments.append(s[start:].strip())
    
    if DEBUG:
     print(f"Error in extract_term_from_plus_minus:{segments}")

    return segments
    
def extract_variable(term_str: str) -> 'Term': 
    #Handle empty str
    if not term_str:  
        if DEBUG: 
            print("Error in extract_variable: Empty string")
        return Term(0) 
    #Handle sign
    if term_str[0] == '-':
        sign = -1
    else:
        sign = 1
    #Parse the str before extrace number and variable
    term_str = term_str.replace('+', '').replace('-', '')
    coefficient = 1
    variables = {}
    length = len(term_str)
    front_coeff = ""
    i = 0
    
    if DEBUG:
     print(f"len: {len(term_str)}")
    #Handle the front coefficient like '2222123X2Y3Z2W', extract '2222123'
    while i < length:
        char = term_str[i]
        if char.isalpha():
            break
        i += 1
        front_coeff = term_str[0:i]
    
    if front_coeff:
        coefficient = int(term_str[0:i])
    
    coefficient *= sign
    
    #i = 0
    #After handling coefficient, then extract variable and its corresponding exponent
    while i < length:

        char = term_str[i]
        if char.isalpha():
            var = char
            exponent = 0
            i += 1  
            while i < length and term_str[i].isdigit():
                exponent = exponent * 10 + int(term_str[i])
                i += 1

            if exponent == 0:
                exponent = 1
                
            variables[var] = exponent
        else:
            i += 1
    
    if DEBUG:
        print("var: ", variables)
        print("coef: " ,coefficient)
        print(Term(coefficient, variables))
        
    return Term(coefficient, variables)

def parse_input_into_polynomial_object(input: str) -> 'Polynomial':
    input = input.replace('^','').replace('*','')
    polys = []

    for s1 in extract_poly_from_parentheses(input):

        term_for_one_poly = []
        for s2 in extract_term_from_plus_minus(s1):
            term = extract_variable(s2)
            term_for_one_poly.append(term)

        poly = Polynomial(term_for_one_poly)
        polys.append(poly)
    
    i=0
    multiplied_poly = polys[0] 
    
    for i in range(1,len(polys)):
        multiplied_poly *= polys[i]
    
    return multiplied_poly


'''
0. We check if the input is valid, cannot submit empty string
1. The parenthesis must be balanced a '(' shoud match a ')'
2. type exit(), will terminate the program
'''     

user_input = input("Input the polynomials: ")
if not user_input:
    print('Wrong input format. Do again.')
    exit()
if '(' not in user_input and ')' not in user_input:
    print('Wrong input format. Do again.')
    exit()
    
#Handle the poly contain (0)
segments = extract_poly_from_parentheses(user_input)
for s in segments:
    if s == '0':
        output_result_with_caret = output_result_without_caret = '0'
        print('Output Result: ' + str(output_result_with_caret))
        print('Output Result: ' + str(output_result_without_caret))
        exit()

#Handle only number multiplication       
if all(char.isdigit() or char in '()' for char in user_input):
    user_input = user_input.replace('(', ' ').replace(')', ' ').replace('  ', ' ').strip().split(' ')
    sum = 1
    for s in user_input:
        if s == '0':
            sum = 0
            break
        sum *= int(s)
    output_result_without_caret = output_result_with_caret = sum
else:
    #Hanlde the normal poly with (1)(X) (X)(X)
    result_poly = parse_input_into_polynomial_object(user_input)
    output_result_with_caret = result_poly.__str__()
    output_result_without_caret = output_result_with_caret.replace('^', '').replace('*', '')
print('Output Result: ' + str(output_result_with_caret))
print('Output Result: ' + str(output_result_without_caret))