# legacy_code_scan
This project uses a two-stage Python and LLM (e.g., GitHub Copilot Chat) pipeline to reverse-engineer business logic from legacy COBOL code into structured, high-level artifacts.


Configure chunking_analysis_agent.py: Update the COBOL_FILES list to map the program names to their physical file names.

Run chunking_analysis_agent.py - Generates analysis prompts.

Manual Step: Copy, paste, and execute all individual prompts in the LLM chat, then collect and paste the structured results into synthesis_input.txt.

Run synthesis_prompt_generator.py Generates the final synthesis prompt.

Manual Step: Copy and execute the synthesized_prompt.txt content in the LLM chat to get the final, consolidated tables.
