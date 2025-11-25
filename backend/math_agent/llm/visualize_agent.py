from math_agent.llm.agent import build_math_agent

def save_agent_graph():
    """
    Builds the math agent and saves a visualization of its graph to a PNG file.
    """
    try:
        # Build the math agent
        app = build_math_agent()

        # Get the graph visualization as PNG bytes
        png_bytes = app.get_graph(xray=True).draw_mermaid_png()

        # Define the output file name
        output_filename = "math_agent_graph.png"

        # Write the bytes to a file
        with open(output_filename, "wb") as f:
            f.write(png_bytes)

        print(f"Successfully saved agent graph to '{output_filename}'")

    except ImportError as e:
        print(f"Error: An import failed. Make sure all dependencies are installed. Details: {e}")
        print("You might need to install 'langchain_core', 'langgraph', 'pygraphviz', etc.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == '__main__':
    save_agent_graph()