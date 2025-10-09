import yaml
import os
from typing import Dict, Any, Union, BinaryIO

def load_yaml_file(file_path: str) -> Dict[str, Any]:
    """
    Carrega um arquivo YAML e retorna um dicionário.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        return {}
    except yaml.YAMLError as e:
        print(f"Erro ao carregar arquivo YAML: {e}")
        return {}

def save_yaml_file(data: Dict[str, Any], file_path: str) -> bool:
    """
    Salva um dicionário em um arquivo YAML.
    """
    try:
        # Cria o diretório se não existir
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as file:
            yaml.dump(data, file, default_flow_style=False, allow_unicode=True, indent=2)
        return True
    except Exception as e:
        print(f"Erro ao salvar arquivo YAML: {e}")
        return False

def load_example_data() -> Dict[str, Any]:
    """
    Carrega os dados do exemplo como template.
    """
    example_path = os.path.join('templates', 'example.yaml')
    return load_yaml_file(example_path)

def save_user_data(data: Dict[str, Any], filename: str = 'user_cv_data.yaml') -> bool:
    """
    Salva os dados do usuário na pasta data.
    """
    file_path = os.path.join('data', filename)
    return save_yaml_file(data, file_path)

def load_user_data(filename: str = 'user_cv_data.yaml') -> Dict[str, Any]:
    """
    Carrega os dados salvos do usuário.
    """
    file_path = os.path.join('data', filename)
    return load_yaml_file(file_path)

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