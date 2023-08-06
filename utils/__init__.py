from typing import Dict

def _flatten(d: Dict):
    new_dict = {}
    for k, v in d.items():
        if not isinstance(v, dict):
            new_dict[k] = v
        else:
            for sub_key, sub_value in v.items():
                new_dict[f"{k}.{sub_key}"] = sub_value
    return new_dict

def flatten(nested_dict: Dict):
    while any(isinstance(v, dict) for v in nested_dict.values()):
        nested_dict = _flatten(nested_dict)
    flat_dict = nested_dict
    return flat_dict
