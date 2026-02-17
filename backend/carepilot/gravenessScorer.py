import ollama

def call(InputText, model='gravenessRaterFinal'):
    """
    Calls the 'gravenessRater' model with the provided text, parses the 
    5-point graveness rating and the subsequent summary, and returns them 
    as a tuple.

    The model's output is expected to follow this format:
    [Rating (e.g., 'Graveness Rating: 3/5')]
    [Blank Line]
    [Summary description]

    Args:
        InputText (str): The patient's problem description to be analyzed.
        model (str): The name of the Ollama model (default 'gravenessRater').

    Returns:
        tuple: (rating (str), description (str))
    """
    
    try:
        # 1. Call the Ollama Model
        client = ollama.Client()
        response = client.generate(model=model, prompt=InputText)
        
        # Extract the raw text output and strip leading/trailing whitespace
        raw_output = response.get('response', '').strip()

        if not raw_output:
            return "N/A", "Model returned an empty response."

        # 2. Parse the Output
        
        # Split the output by lines
        lines = raw_output.split('\n')
        
        rating = "N/A"
        description = "Could not parse description."
        
        # Find the first non-empty line (which should be the rating)
        for i, line in enumerate(lines):
            stripped_line = line.strip()
            if stripped_line:
                rating = stripped_line
                
                # The description starts after the blank line following the rating.
                # Find the remaining non-empty lines and join them to form the description.
                description_parts = []
                # Start searching for description text after the current line
                for desc_line in lines[i+1:]:
                    if desc_line.strip():
                        description_parts.append(desc_line.strip())
                
                description = '\n'.join(description_parts)
                break

        return rating.strip(), description.strip()

    except ollama.OllamaError as e:
        # Handle specific Ollama connection or model errors
        return "Ollama Error", f"Failed to connect or model not found: {e}"
    except Exception as e:
        # Catch other unexpected errors
        return "Parsing Error", f"An unexpected error occurred: {e}"