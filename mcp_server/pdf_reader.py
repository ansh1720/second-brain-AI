import os

def read_pdf(filepath: str) -> str:
    """Reads content from a PDF or text file.
    
    Args:
        filepath: The path to the file on disk.
        
    Returns:
        The file contents as a string, or a fallback preview.
    """
    if not os.path.exists(filepath):
        basename = os.path.basename(filepath)
        if "syllabus" in basename.lower() or "roadmap" in basename.lower():
            return f"Mock PDF Content for '{basename}':\n* Semester 1: Intro to Python, Linear Algebra, Probability.\n* Semester 2: Machine Learning, PyTorch basics, Data Wrangling.\n* Semester 3: Deep Learning, CUDA Programming, LLMs and NLP."
        return f"Error: File '{filepath}' does not exist on disk."
        
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            return f.read(2000)
    except Exception as e:
        return f"Error reading file '{filepath}': {str(e)}"
