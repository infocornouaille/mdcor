import yaml

def extract_yaml_header(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    if content.startswith('---'):
        _, yaml_content, _ = content.split('---', 2)
        return yaml.safe_load(yaml_content)
    return {}

def process_fexo(yaml_data):
    if 'title' in yaml_data:
        title = yaml_data['title']
    else:
        title = ""
    if 'class' in yaml_data:
        class_name = yaml_data['class']
    else:
        class_name = ""
    if 'date' in yaml_data:
        date = yaml_data['date']
    else:
        date = ""
    return title, class_name, date




def process_content(content, yaml_data):

    if 'title' in yaml_data or 'class' in yaml_data or "date" in yaml_data:
        title, class_name, date = process_fexo(yaml_data)
        content = f"\\fexo{{{class_name}}}{{{title}}}{{{date}}}\n\n" + content
    return content

def process_yaml(file_path, output_path):
    yaml_data = extract_yaml_header(file_path)
    if not yaml_data:
        return
    else:
        with open(output_path, 'r', encoding='utf-8') as file:
            content = file.read()
        content = process_content(content, yaml_data)
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(content)
    

    

if __name__ == "__main__":
    content = "test"
    yaml_data = {"title": "Test"}
    new_content = process_content(content, yaml_data)
    print(new_content)