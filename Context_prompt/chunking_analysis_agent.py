import re
import os

# --- 1. CONFIGURATION (ADAPTED TO YOUR DIRECTORY STRUCTURE) ---

# List of your COBOL programs with the exact file names from your directory.
COBOL_FILES = [
    ("CSBTRN01", "CSBTRN01"),
    ("CSBCLO02", "CSBCLO02"),
    ("CSBREL03", "CSBREL03"),
    ("CSBINP04", "CSBINP04"),
]

# --- 2. THE CHUNKING FUNCTION (UNMODIFIED) ---

def chunk_cobol_code(program_name, code_content):
    """
    Chunks COBOL code based on SECTION and PARAGRAPH definitions.
    Returns a list of tuples: (chunk_name, chunk_code).
    """
    # Regex to find SECTION or PARAGRAPH headers starting in column 8 (standard COBOL margin)
    # This pattern captures the label (e.g., '1000-IO-SETUP') and all code until the next label or EOF.
    # The '(?=^ {7}[\d\w-]+' part is a lookahead for the start of the next label.
    pattern = re.compile(
        r'^ {7}([\d\w-]+(?: SECTION)?\.)\n(.*?)(?=^ {7}[\d\w-]+\.|\Z)',
        re.MULTILINE | re.DOTALL
    )

    chunks = []
    for match in pattern.finditer(code_content):
        label = match.group(1).strip('.') # e.g., '1000-IO-SETUP' or '2000-TXN-READ-SECTION'
        code = match.group(2).strip()
        chunks.append( (f"{program_name}-{label}", code) )

    return chunks

# --- 3. THE PROMPT GENERATION FUNCTION (UNMODIFIED) ---

def generate_agent_prompt(chunk_name, chunk_code):
    """
    Generates the structured "Agent" prompt for a single chunk of COBOL code.
    """
    prompt = f"""
###################################################################################
# BEGIN AGENT PROMPT FOR CHUNK: {chunk_name}
###################################################################################

Analyze the following COBOL chunk. Act as a "Business Logic Analysis Agent." The program is part of a core banking system (Party, Credit, Collateral, Insurance). Your response must be structured using the specific headings below, and must strictly avoid COBOL keywords or syntax (e.g., no 'MOVE', 'IF', 'PERFORM').

COBOL CHUNK:
---
{chunk_code}
---

Structured Analysis Response:

1. Data Fields Involved:

2. Core Business Function:

3. Implied Business Rule (BR-\#):

4. Data Relationship Implied (R-\#):

###################################################################################
# END AGENT PROMPT
###################################################################################
"""
    return prompt

# --- 4. MAIN EXECUTION ---

def main_analysis_prep(cobol_code_map):
    """
    Main function to process all COBOL files and generate the master prompt file.
    """
    all_chunks = []
    
    print("Starting COBOL code analysis preparation...")
    for prog_name, file_name in cobol_code_map:
        
        # --- File I/O: This is the critical adaptation step ---
        try:
            with open(file_name, 'r') as f:
                code_content = f.read()
            
        except FileNotFoundError:
             print(f"❌ ERROR: File '{file_name}' not found. Please ensure it exists in the current directory.")
             continue
        # --------------------------------------------------------

        # 2. Chunk the code
        chunks = chunk_cobol_code(prog_name, code_content)
        all_chunks.extend(chunks)
        print(f"  Processed {prog_name}: Found {len(chunks)} logical chunks.")

    # 3. Generate the prompt file
    output_file = "copilot_agent_prompts.txt"
    with open(output_file, 'w') as f_out:
        f_out.write("--- GITHUB COPILOT CHUNKING & SUMMARIZATION PROMPTS ---\n")
        f_out.write("INSTRUCTIONS: Execute each 'AGENT PROMPT' block individually in the Copilot Chat interface.\n\n")

        for chunk_name, chunk_code in all_chunks:
            prompt = generate_agent_prompt(chunk_name, chunk_code)
            f_out.write(prompt + "\n\n")

    print(f"\n✅ All individual Agent prompts ({len(all_chunks)} total) generated successfully in: {output_file}")
    print("\nNEXT STEPS: 1. Copy the contents of 'copilot_agent_prompts.txt'. 2. Execute each prompt block in Copilot Chat. 3. Collect the structured results for the final Synthesis Agent step.")

if __name__ == "__main__":
    main_analysis_prep(COBOL_FILES)