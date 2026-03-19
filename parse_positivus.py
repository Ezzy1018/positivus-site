import json

def parse_color(paint):
    if paint.get('type') == 'SOLID':
        color = paint.get('color', {})
        r = int(color.get('r', 0) * 255)
        g = int(color.get('g', 0) * 255)
        b = int(color.get('b', 0) * 255)
        a = paint.get('opacity', 1.0)
        return f"rgba({r}, {g}, {b}, {a:.2f})"
    return None

def extract_node_data(node, indent=""):
    name = node.get('name', '')
    node_type = node.get('type', '')
    
    css = []
    # Layout and Dimensions
    box = node.get('absoluteBoundingBox', {})
    w, h = box.get('width', 0), box.get('height', 0)
    
    output = f"{indent}[{node_type}] {name} ({w}x{h})"
    
    # Text Properties
    if node_type == 'TEXT':
        style = node.get('style', {})
        fonts = style.get('fontFamily', '')
        size = style.get('fontSize', '')
        weight = style.get('fontWeight', '')
        text = node.get('characters', '').replace('\n', ' ')
        output += f" -> '{text[:30]}...' (Font: {fonts} {size}px w{weight})"
        
    # Fills & Backgrounds
    fills = node.get('fills', [])
    for fill in fills:
        color = parse_color(fill)
        if color:
            output += f" | Fill: {color}"
            
    print(output)
    
    children = node.get('children', [])
    for child in children:
        extract_node_data(child, indent + "  ")

def main():
    with open('positivus_figma.json', 'r') as f:
        data = json.load(f)
        
    nodes = data.get('nodes', {})
    node = nodes.get("330:762", {}).get("document", {})
    if not node:
        print("Node not found")
        return
        
    print(f"--- Analyzing Figma Node: {node.get('name')} ---")
    extract_node_data(node)

if __name__ == "__main__":
    main()
