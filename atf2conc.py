import re

def parse_atf(atf_file, output_file):
    with open(atf_file, 'r') as file:
        lines = file.readlines()

    parsed_lines = []
    current_text = None
    current_surface = None
    current_column = None

    surfaces = ['obverse', 'reverse', 'left edge', 'right edge', 'bottom edge', 'edge', 'surface a']

    for line in lines:
        if line.startswith('&'):
            # New text
            current_text = line.split('=')[0].strip('& ')
            current_column = None  # Clear the column variable when encountering a new text
        elif any(line.startswith(f'@{surface}') for surface in surfaces):
            # Set current surface
            for surface in surfaces:
                if line.startswith(f'@{surface}'):
                    current_surface = surface
                    current_column = None  # Clear the column variable when changing the surface
                    break
        elif line.startswith('@column'):
            # Set current column
            current_column = line.split()[1]
        elif not line.startswith(('#', '$', '>', '@')):
            # Process text lines
            cleaned_line = re.sub(r'(\$|\@)[^\s]+', '', line).strip()
            if current_text is not None and current_surface is not None and cleaned_line:
                if current_column:
                    parsed_line = f'{current_text} {current_surface} col. {current_column} {cleaned_line}'
                else:
                    parsed_line = f'{current_text} {current_surface} {cleaned_line}'
                parsed_lines.append(parsed_line)

    with open(output_file, 'w') as file:
        file.write('\n'.join(parsed_lines))

# Specify the input ATF file and output file name
atf_file = 'inscriptions.atf'
output_file = 'output.txt'

# Call the function to parse ATF and write to file
parse_atf(atf_file, output_file)
