import json
import sys

def parse_color(paint):
    if paint.get('type') == 'SOLID':
        c = paint.get('color', {})
        r, g, b = int(c.get('r', 0)*255), int(c.get('g', 0)*255), int(c.get('b', 0)*255)
        a = paint.get('opacity', 1.0)
        return f"rgba({r}, {g}, {b}, {a:.2f})"
    return ""

def get_flex_direction(mode):
    if mode == "HORIZONTAL": return "row"
    if mode == "VERTICAL": return "column"
    return "column"

def build_section(node, depth=0):
    indent = "  " * depth
    name = node.get('name', 'Unknown')
    ntype = node.get('type', '')
    
    css = {}
    if 'layoutMode' in node and node['layoutMode'] != "NONE":
        css['display'] = 'flex'
        css['flex-direction'] = get_flex_direction(node['layoutMode'])
        if node.get('itemSpacing'): css['gap'] = f"{node['itemSpacing']}px"
        
        pt = node.get('paddingTop', 0)
        pr = node.get('paddingRight', 0)
        pb = node.get('paddingBottom', 0)
        pl = node.get('paddingLeft', 0)
        if pt or pr or pb or pl: css['padding'] = f"{pt}px {pr}px {pb}px {pl}px"
        
        box = node.get('absoluteBoundingBox', {})
        if box.get('width'): css['width'] = f"{box['width']}px"
        if box.get('height') and ntype != "FRAME": css['height'] = f"{box['height']}px"

    if 'cornerRadius' in node: css['border-radius'] = f"{node['cornerRadius']}px"

    fills = [f for f in node.get('fills', []) if f.get('visible', True)]
    if fills: 
        c = parse_color(fills[0])
        if c: css['background-color'] = c

    strokes = node.get('strokes', [])
    if strokes:
        sc = parse_color(strokes[0])
        sw = node.get('strokeWeight', 1)
        if sc: css['border'] = f"{sw}px solid {sc}"

    style_str = "; ".join([f"{k}: {v}" for k, v in css.items()])
    
    out = f"{indent}<div class='figma-{name.replace(' ', '-').lower()}' style='{style_str}'>\n"

    if ntype == 'TEXT':
        text = node.get('characters', '').replace('\n', '<br>')
        ts = node.get('style', {})
        font = ts.get('fontFamily', 'Space Grotesk')
        size = ts.get('fontSize', 16)
        weight = ts.get('fontWeight', 400)
        
        c = ""
        if fills: c = parse_color(fills[0])
        
        out += f"{indent}  <span style='font-family: \"{font}\"; font-size: {size}px; font-weight: {weight}; color: {c}'>{text}</span>\n"

    for child in node.get('children', []):
        if child.get('visible', True):
            out += build_section(child, depth + 1)
            
    out += f"{indent}</div>\n"
    return out

def main():
    with open('positivus_figma.json', 'r') as f:
        data = json.load(f)
        
    nodes = data.get('nodes', {})
    node = nodes.get("330:762", {}).get("document", {})
    if not node:
        print("Node not found")
        return
        
    with open('positivus_complete/full_ast_map.html', 'w') as outf:
        outf.write("<html><head><style>@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap'); body { margin: 0; padding: 0; background-color: #fff; font-family: 'Space Grotesk', sans-serif; } div { box-sizing: border-box; position: relative; }</style></head><body>\n")
        outf.write(build_section(node))
        outf.write("</body></html>")
        
    print("Full AST Map generated heavily typed to HTML layout.")

if __name__ == "__main__":
    main()
