import os
import re
import subprocess

def preprocess_markdown(input_file, output_file):
    """
    Replace .md links with .html links in the Markdown file.
    """
    with open(input_file, "r") as infile:
        content = infile.read()

    # Replace all .md links with .html links
    updated_content = re.sub(r'\.md(#\S*)?', r'.html\1', content)

    with open(output_file, "w") as outfile:
        outfile.write(updated_content)



def render_markdown_with_mermaid_diagrams(input_dir, output_dir):
    """
    Renders Mermaid diagrams in Markdown files to SVG and replaces the Mermaid code blocks
    with <img> tags in the HTML output.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for file_name in os.listdir(input_dir):
        if file_name.endswith(".md"):
            input_file = os.path.join(input_dir, file_name)
            output_file = os.path.join(output_dir, file_name.replace(".md", ".pdf"))

            # Temporary file for preprocessed Markdown
            preprocessed_md = os.path.join(output_dir, file_name)
            preprocess_markdown(input_file, preprocessed_md)

            # Convert Mermaid diagrams to SVG using mmdc
            subprocess.run([
                "mmdc",
                "-i", preprocessed_md,
                "-o", preprocessed_md,
                "--outputFormat=svg"
            ], check=True)

            print("preprocess done")

            # Convert preprocessed Markdown to HTML using Pandoc
            subprocess.run([
                "pandoc",
                preprocessed_md,
                "-o", output_file,
                "--standalone",
                "-c", "./node_modules/github-markdown-css/github-markdown.css",
                "--syntax-definition=./javascript.xml",
                "--pdf-engine=weasyprint",
                #"--embed-resources",
                "--template=./github-template 1.22.20 PM.html"
            ], check=True)

            print(f"Converted {input_file} to {output_file} with rendered diagrams.")

            # remove the temporary preprocessed Markdown file
            # os.remove(preprocessed_md)

if __name__ == "__main__":
    # Define input and output directories
    input_directory = "/Users/stephen/bin/input"
    output_directory = "/Users/stephen/bin/output"

    # Convert Markdown files to HTML with Mermaid diagrams
    render_markdown_with_mermaid_diagrams(input_directory, output_directory)