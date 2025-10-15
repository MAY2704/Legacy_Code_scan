from graphviz import Source
import os

def render_dot_model_from_file(input_filename="final_output", output_filename="data_model_diagram"):
    """
    Reads the Graphviz DOT code from the specified input file and renders it
    into a visual diagram file (PNG).

    Args:
        input_filename (str): The name of the file containing the raw DOT code.
        output_filename (str): The base name for the output file (e.g., 'data_model_diagram.png').
    """
    try:
        # 1. Read the DOT code from the specified file
        with open(input_filename, 'r', encoding='utf-8') as f:
            dot_code = f.read()
    except FileNotFoundError:
        print(f"❌ Error: Input file '{input_filename}' not found.")
        print("Please ensure your DOT code is saved in a file named 'final_output'.")
        return
    except Exception as e:
        print(f"❌ An error occurred while reading the file: {e}")
        return

    # Check if the file content is empty or looks like valid DOT structure
    if not dot_code.strip().lower().startswith(('digraph', 'graph')):
        print(f"❌ Error: The content of '{input_filename}' does not appear to be valid Graphviz DOT code.")
        print("Please ensure the file contains the full 'digraph DataModel {...}' block.")
        return

    # 2. Create a Source object from the DOT code
    # The format is set to "png" for image output
    src = Source(dot_code, filename=output_filename, format="png")

    # 3. Render the file and open it (view=True)
    try:
        src.render(view=True, cleanup=True)
        print(f"\n✅ Success: Visual data model generated and saved as '{output_filename}.png'.")
        print("   (The image should open automatically.)")

    except FileNotFoundError:
        print(f"\n❌ Error: Graphviz is not installed or not in your system PATH.")
        print(f"   Please ensure you have installed Graphviz binaries (`dot` command) and the Python library (`pip install graphviz`).")
        print(f"   The DOT code has been saved to '{output_filename}' but could not be rendered automatically.")
    except Exception as e:
        print(f"\n❌ An unexpected error occurred during rendering: {e}")


# --- Execution ---
render_dot_model_from_file()