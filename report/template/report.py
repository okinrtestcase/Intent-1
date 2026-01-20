from jinja2 import Environment, FileSystemLoader
import json

# Load JSON data
with open('report/json/2026-01-19/Test POC Garuda-5e8a7b13.json', 'r', encoding="utf-8",) as file:
    data = json.load(file)

# Load Jinja2 template
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('report/template/uhuy.html')

# Render the template with data
html_output = template.render(summary=data['summary'], chart=data['chart'], test_data=data['data'])

# Save the rendered HTML to a file
with open('report/html/check.html', 'w', encoding="utf-8",) as output_file:
    output_file.write(html_output)
    
print("HTML report generated successfully.")
