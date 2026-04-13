import json

def cleanup_notebook():
    file_path = "Fraud_Analytics_Credit_Card_Fraud_Detection-chai_main/sripriyaramdev.ipynb"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
        
    for cell in nb.get('cells', []):
        if cell.get('cell_type') == 'code':
            source = "".join(cell.get('source', []))
            if "!pip install numpy" in source or "!pip install pandas" in source:
                # Clear the cell outputs which contain the error
                cell['outputs'] = []
                
                # Comment out the pip install commands
                new_source = []
                for line in cell['source']:
                    if line.strip().startswith('!pip install'):
                        new_source.append(f"# {line}")
                    elif ".applymap(color_style)" in line:
                        new_source.append(line.replace(".applymap(color_style)", ".map(color_style)"))
                    else:
                        new_source.append(line)
                cell['source'] = new_source

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1)
        
    print("Notebook cleanup complete. Removed error and commented out pip install commands.")

if __name__ == '__main__':
    cleanup_notebook()
