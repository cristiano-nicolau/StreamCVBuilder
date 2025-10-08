import yaml
import os
from typing import Dict, Any, Union, BinaryIO

def load_yaml_from_string(yaml_str: str) -> Dict[str, Any]:
    """
    Carrega um YAML a partir de uma string.
    """
    try:
        return yaml.safe_load(yaml_str)
    except yaml.YAMLError as e:
        print(f"Erro ao carregar YAML: {e}")
        return {}

def load_yaml_from_file(file: Union[str, BinaryIO]) -> Dict[str, Any]:
    """
    Carrega um YAML de um arquivo ou objeto tipo arquivo.
    """
    try:
        if isinstance(file, str):
            with open(file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        else:
            return yaml.safe_load(file)
    except (FileNotFoundError, yaml.YAMLError) as e:
        print(f"Erro ao carregar YAML: {e}")
        return {}

def dump_yaml_to_string(data: Dict[str, Any]) -> str:
    """
    Converte um dicionário para string YAML.
    """
    try:
        return yaml.dump(data, default_flow_style=False, allow_unicode=True, indent=2)
    except yaml.YAMLError as e:
        print(f"Erro ao converter para YAML: {e}")
        return ""

def load_example_data() -> Dict[str, Any]:
    """
    Carrega os dados do exemplo como template.
    """
    example_path = os.path.join('templates', 'example.yaml')
    return load_yaml_from_file(example_path)

def merge_with_example(user_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Mescla os dados do usuário com o template do exemplo.
    """
    example_data = load_example_data()
    
    # Se não há dados do usuário, retorna o exemplo
    if not user_data:
        return example_data
    
    # Mescla recursivamente
    def merge_dicts(base: Dict, overlay: Dict) -> Dict:
        result = base.copy()
        for key, value in overlay.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = merge_dicts(result[key], value)
            else:
                result[key] = value
        return result
    
    return merge_dicts(example_data, user_data)
