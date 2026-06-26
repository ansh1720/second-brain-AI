import json

def compare_options(options_json: str) -> str:
    """Creates a comparison matrix from options data in JSON format.
    
    Args:
        options_json: A JSON string containing options to compare.
                     Format: {"options": [{"name": "Opt1", "price": 100, "specs": "info"}, ...]}
                     
    Returns:
        A markdown table comparing the options.
    """
    try:
        data = json.loads(options_json)
        options = data.get("options", [])
        if not options:
            return "Error: JSON must contain an 'options' array."
            
        spec_keys = set()
        for opt in options:
            spec_keys.update(opt.keys())
        
        spec_keys.discard("name")
        spec_keys = sorted(list(spec_keys))
        
        headers = ["Feature"] + [opt.get("name", "Unknown") for opt in options]
        markdown = "| " + " | ".join(headers) + " |\n"
        markdown += "| " + " | ".join(["---"] * len(headers)) + " |\n"
        
        for key in spec_keys:
            row = [key.capitalize()]
            for opt in options:
                val = opt.get(key, "N/A")
                row.append(str(val))
            markdown += "| " + " | ".join(row) + " |\n"
            
        return markdown
    except Exception as e:
        return f"Error generating comparison: {str(e)}\nInput JSON template must be: " + '{"options": [{"name": "MacBook", "price": 90000}, {"name": "Lenovo", "price": 70000}]}'
