import os

def create_final_synthesis_prompt(input_filename="synthesis_input.txt"):
    """
    Reads structured analysis summaries from a file and generates the final
    Synthesis Agent prompt, instructing it to create a Business Rule Register
    and a High-Level Data Model. LaTeX has been removed for simplicity.

    The user must paste all 46 structured Copilot outputs into the
    'synthesis_input.txt' file before running this script.

    Args:
        input_filename (str): The name of the file containing the aggregated
                              structured summaries.

    Returns:
        str: The complete, ready-to-execute Synthesis Agent prompt.
    """
    try:
        # 1. Attempt to read the consolidated summaries from the input file
        with open(input_filename, 'r', encoding='utf-8') as f:
            analysis_summaries = f.read().strip()
    except FileNotFoundError:
        print(f"Error: Input file '{input_filename}' not found.")
        print("Please ensure you have created this file and pasted all 46 Copilot outputs into it.")
        return None
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return None

    # Define the template using a standard f-string. LaTeX is replaced with plain text.
    prompt_template = f"""
Act as the final "Synthesis Agent." Your task is to analyze the complete set of structured business rule and data relationship summaries provided below from four distinct, interconnected COBOL banking programs (CSBTRN01, CSBCLO02, CSBREL03, CSBINP04).

Consolidate the extracted knowledge into two comprehensive tables: a **Business Rule Register** and a **High-Level Data Model & Entity Relationships** table. The Data Model table must clearly identify the primary entities involved and their specific relationships based on the COBOL data fields used for linkage.

INPUT SUMMARIES (Consolidated from Analysis Agent steps):
--- BEGIN ANALYSIS SUMMARIES ---
{analysis_summaries}
--- END ANALYSIS SUMMARIES ---

---

FINAL OUTPUT: Business Rule & Data Extraction

### 1. Consolidated Business Rule Register

| Rule ID | Program Source | Business Domain | Business Rule Description | Condition | Consequence |
| :--- | :--- | :--- | :--- | :--- | :--- |
| BR-1 | CSBTRN01 | Credit/Collateral | Collateral Match Rule | Agreement Type is 'LOA' and Collateral Reference is non-blank and matches the Collateral ID. | Violation flag set if condition is not met. |
| BR-2 | CSBTRN01 | Insurance/Collateral | High-Value Mandatory Insurance | Collateral Value is over $100,000,000$. | Violation flag set if insurance link is missing or incorrect. |
| BR-3 | CSBCLO02 | Collateral/Lien | Lien Exposure Limit | Total Lien Amount exceeds 50 percent of the Net Usable Collateral Value. | 'HIGH LIEN EXPOSURE' warning generated. |
| BR-4 | CSBREL03 | Compliance/Exposure | Aggregated Relationship Exposure Limit | Relationship is 'SPSE' or 'PRNT' AND total exposure exceeds $100,000,000$. | Risk Score is penalized (raised to 095). |
| BR-5 | CSBREL03 | Compliance/Party | High-Risk Commercial Insurance Mandate | Customer Type is 'C' (Commercial) AND Risk Score is > 085. | Insurance Flag ('IFLG-P') must be set to 'Y'. |
| ... | ... | ... | ... | ... | ... |


### 2. High-Level Data Model & Entity Relationships

| Entity 1 | Relationship | Entity 2 | Linking Field(s) (COBOL) | Relationship Type (1:M, 1:1, M:M) | Business Context/Constraint |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Agreement** | Secures | **Collateral** | CLLT-REF -> CLID-C | 1:1 | Validation BR-1 enforces this link. |
| **Collateral** | Is Secured by | **Lien** | CLID-C -> LIEN-CLID | 1:M | Used to calculate Net Usable Value and assess BR-3. |
| **Collateral** | Is Covered by | **Insurance Policy** | IPOL-LNK -> PIDX-I | 1:1 | Enforcement of BR-2 and updated by BR-6. |
| **Customer/Party** | Has Exposure to | **Related Party** | MAIN-ID -> RELP-ID | 1:M | Used to aggregate exposure for compliance (BR-4). |
| **Customer/Party** | Is Assessed for | **Risk** | CMID-P -> RSKR-P | 1:1 | Score is penalized (BR-4), and drives mandates (BR-5). |
| ... | ... | ... | ... | ... | ... |
"""
    return prompt_template.strip()

# --- Execution ---

# 1. Generate the final Synthesis Prompt.
final_prompt = create_final_synthesis_prompt()

# 2. Save the final prompt to the specified file if generation was successful.
if final_prompt:
    output_filename = "synthesized_prompt.txt"
    try:
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(final_prompt)
        print(f"\n✅ Synthesis Prompt Generated Successfully and saved to '{output_filename}' (All LaTeX removed).")
    except Exception as e:
        print(f"❌ Error saving prompt to file: {e}")
    
    # 3. Print the result for the user to copy/paste.
    print("--------------------------------------------------------------------------------")
    print("INSTRUCTIONS: Copy the entire text below and paste it into Copilot Chat.")
    print("--------------------------------------------------------------------------------")
    print(final_prompt)