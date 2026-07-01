"""Prompt templates for AI document generation."""

README_SYSTEM_PROMPT = """You are an expert technical writer and developer advocate. 
Your task is to create professional, engaging README.md files for GitHub projects.
Analyze the provided project context thoroughly and generate comprehensive documentation.
Use emojis where appropriate. Write in clear, concise English."""

README_USER_TEMPLATE = """Please generate a professional README.md for the following project.

{project_context}

Generate a README.md with these sections:
1. **Project Title** - Catchy, descriptive name
2. **Description** - What the project does, why it exists (2-3 sentences)
3. **Features** - Key capabilities with bullet points and emojis
4. **Installation** - Step-by-step setup instructions
5. **Usage** - How to use the project with code examples
6. **Project Structure** - Brief overview of key directories/files
7. **Technologies** - Languages, frameworks, tools used
8. **Contributing** - How others can contribute
9. **License** - Suggest an appropriate open-source license
10. **Acknowledgments** - Credits if applicable

Format everything in clean Markdown. Use proper code blocks with language tags.
Make it engaging but professional. The README should make someone want to use this project.

Return ONLY the markdown content, no explanations."""

CONTRIBUTING_TEMPLATE = """Generate a CONTRIBUTING.md file for this project:

{project_context}

Include:
1. How to set up the development environment
2. Code style guidelines
3. How to submit issues and pull requests
4. Commit message conventions
5. Testing requirements
6. Code of conduct reference

Return ONLY the markdown content."""

LICENSE_TEMPLATES = {
    "mit": """MIT License

Copyright (c) {year} {author}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.""",
    "apache": """Apache License 2.0

[Full Apache 2.0 text would go here]""",
}

def build_readme_prompt(project_context: str) -> tuple:
    """Build prompt for README generation."""
    return README_SYSTEM_PROMPT, README_USER_TEMPLATE.format(project_context=project_context)

def build_contributing_prompt(project_context: str) -> tuple:
    """Build prompt for CONTRIBUTING.md generation."""
    return README_SYSTEM_PROMPT, CONTRIBUTING_TEMPLATE.format(project_context=project_context)
