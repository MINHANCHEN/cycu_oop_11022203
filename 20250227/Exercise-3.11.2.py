def print_right(text):
    # Calculate how many spaces to print before the text to align it to the 40th column
    spaces_needed = 40 - len(text)
    
    # Print the text with the required number of leading spaces
    print(' ' * spaces_needed + text)

# Test the function with examples
print_right("Monty")
print_right("Python's")
print_right("Flying Circus")
