import os
import json

MEMORY_FILE = os.path.join("memory", "memory_bank.json")

def save_memory(key: str, val: str) -> str:
    """Saves a key-value memory pair to the persistent memory bank.
    
    Args:
        key: The memory key identifier.
        val: The value string to save.
        
    Returns:
        Confirmation message.
    """
    os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)
    
    memories = {}
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                memories = json.load(f)
        except Exception:
            memories = {}
            
    memories[key.strip()] = val.strip()
    
    try:
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(memories, f, indent=4, ensure_ascii=False)
        return f"Successfully saved memory key '{key}' with value '{val}'."
    except Exception as e:
        return f"Error saving memory: {str(e)}"

def retrieve_memory(key: str) -> str:
    """Retrieves a memory value from the persistent memory bank by key.
    
    Args:
        key: The memory key to retrieve.
        
    Returns:
        The memory value, or an error/missing message.
    """
    if not os.path.exists(MEMORY_FILE):
        return f"Memory bank is empty. Key '{key}' not found."
        
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            memories = json.load(f)
        val = memories.get(key.strip())
        if val:
            return val
        return f"Key '{key}' not found in memory bank. Available keys: {', '.join(memories.keys())}"
    except Exception as e:
        return f"Error retrieving memory: {str(e)}"
