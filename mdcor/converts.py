import os
import pypandoc
from imagecor.image_processor import process_markdown_file
import yaml
import mdcor.process_yalm

def extract_yaml_header(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    if content.startswith('---'):
        _, yaml_content, _ = content.split('---', 2)
        return yaml.safe_load(yaml_content)
    return {}



def convert_to_latex(file_path, output_dir='.', convert_bw=False, max_size=None):
    processed_file = process_markdown_file(file_path, output_dir, convert_bw, max_size)
    output_file = os.path.splitext(os.path.basename(processed_file))[0] + '.tex'
    output_path = os.path.join(output_dir, output_file)

    

    

    pypandoc.convert_file(processed_file, 'latex', outputfile=output_path, extra_args=['--listings'])

    with open(output_path, 'r', encoding='utf-8') as file:
        content = file.read()
    content = content.replace("\\tightlist\n", "")
    content = content.replace("\\def\\labelenumi{\\arabic{enumi}.}\n", "")
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(content)
    
    # Modifier le fichier LaTeX pour inclure la commande \fexo
    #mdcor.process_yalm.process_yaml(file_path, output_path)
    
    
    print(f"Fichier {output_file} créé")

def convert_to_pdf(input_file, output_dir='.', template='eisvogel', convert_bw=False, max_size=None):
    processed_file = process_markdown_file(input_file, output_dir, convert_bw, max_size)
    output_file = os.path.splitext(os.path.basename(processed_file))[0] + '.pdf'
    output_path = os.path.join(output_dir, output_file)
    extra_args = ['--listings']
    extra_args.extend(['--pdf-engine=xelatex'])
    #template = None
    if template:
        extra_args.extend(['--template', template])
    pypandoc.convert_file(processed_file, 'pdf', outputfile=output_path, extra_args=extra_args)
    print(f"Fichier PDF {output_file} créé")

def batch_convert_latex(input_dir='.', output_dir='.', convert_bw=False, max_size=None):
    for file in os.listdir(input_dir):
        if file.endswith('.md'):
            input_file = os.path.join(input_dir, file)
            convert_to_latex(input_file, output_dir, convert_bw, max_size)

def batch_convert_pdf(input_dir='.', output_dir='.', template='eisvogel', convert_bw=False, max_size=None):
    for file in os.listdir(input_dir):
        if file.endswith('.md'):
            input_file = os.path.join(input_dir, file)
            convert_to_pdf(input_file, output_dir, template, convert_bw, max_size)