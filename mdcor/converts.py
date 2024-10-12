import os
import pypandoc
from imagecor.image_processor import process_markdown_file
import yaml
import mdcor.process_yalm
import re
import tempfile

def extract_yaml_header(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    if content.startswith('---'):
        _, yaml_content, _ = content.split('---', 2)
        return yaml.safe_load(yaml_content)
    return {}

def clean_docusaurus_markdown(content):
    # Supprimer les attributs spécifiques à Docusaurus des blocs de code
    content = re.sub(r'```(\w+)\s+{[^}]*}', r'```\1', content)
    
    # Supprimer showLineNumbers des blocs de code
    content = re.sub(r'```(\w+)\s+showLineNumbers', r'```\1', content)
    
    # Supprimer les lignes vides à l'intérieur des blocs de code
    content = re.sub(r'```(.*?)\n\s*\n(.*?)```', r'```\1\n\2```', content, flags=re.DOTALL)
    
    return content



def convert_to_latex(file_path, output_dir='.', convert_bw=False, max_size=None, 
                     standalone=False, template=None, listings=True, extra_args=None):
    # Traitement initial du fichier Markdown (supposé être défini ailleurs)
    processed_file = process_markdown_file(file_path, output_dir, convert_bw, max_size)
    
    # Définir le nom du fichier de sortie
    output_file = os.path.splitext(os.path.basename(processed_file))[0] + '.tex'
    output_path = os.path.join(output_dir, output_file)
    
    # Lire et nettoyer le contenu
    with open(processed_file, 'r', encoding='utf-8') as file:
        content = file.read()
    cleaned_content = clean_docusaurus_markdown(content)
    
    # Créer un fichier temporaire avec le contenu nettoyé
    with tempfile.NamedTemporaryFile(mode='w+', encoding='utf-8', suffix='.md', delete=False) as temp_file:
        temp_file.write(cleaned_content)
        temp_file_name = temp_file.name
    
    try:
        # Préparer les arguments pour pypandoc
        pandoc_args = []
        if standalone:
            pandoc_args.append('--standalone')
        if template:
            pandoc_args.extend(['--template', template])
        if listings:
            pandoc_args.append('--listings')
        if extra_args:
            pandoc_args.extend(extra_args)
        
        # Convertir en LaTeX avec pypandoc
        pypandoc.convert_file(temp_file_name, 'latex', outputfile=output_path, extra_args=pandoc_args)
        
        # Post-traitement du fichier LaTeX
        with open(output_path, 'r', encoding='utf-8') as file:
            content = file.read()
        content = content.replace("\\tightlist\n", "")
        content = content.replace("\\def\\labelenumi{\\arabic{enumi}.}\n", "")
        
        # Écrire le contenu final
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(content)
        
        print(f"Fichier {output_file} créé")
    
    finally:
        # Supprimer le fichier temporaire
        os.unlink(temp_file_name)
    
    return output_path

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