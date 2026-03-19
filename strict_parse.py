import json
import sys

def parse_color(paint):
    if paint.get('type') == 'SOLID':
        c = paint.get('color', {})
        r, g, b = int(c.get('r', 0)*255), int(c.get('g', 0)*255), int(c.get('b', 0)*255)
        a = paint.get('opacity', 1.0)
        return f"rgba({r}, {g}, {b}, {a:.2f})"
    return "transparent"

def get_flex_direction(mode):
    if mode == "HORIZONTAL": return "row"
    if mode == "VERTICAL": return "column"
    return "column"

def extract_styles(node):
    styles = {}
    # Layout details
    if 'layoutMode' in node and node['layoutMode'] != "NONE":
        styles['display'] = 'flex'
        styles['flex-direction'] = get_flex_direction(node['layoutMode'])
        styles['gap'] = f"{node.get('itemSpacing', 0)}px"
        
        # Padding
        pt = node.get('paddingTop', 0)
        pr = node.get('paddingRight', 0)
        pb = node.get('paddingBottom', 0)
        pl = node.get('paddingLeft', 0)
        if pt or pr or pb or pl:
            styles['padding'] = f"{pt}px {pr}px {pb}px {pl}px"

        align_primary = node.get('primaryAxisAlignItems', 'MIN')
        align_counter = node.get('counterAxisAlignItems', 'MIN')
        
        map_align = {'MIN': 'flex-start', 'MAX': 'flex-end', 'CENTER': 'center', 'SPACE_BETWEEN': 'space-between'}
        styles['justify-content'] = map_align.get(align_primary, 'flex-start')
        styles['align-items'] = map_align.get(align_counter, 'stretch')
        
    if 'cornerRadius' in node:
        styles['border-radius'] = f"{node['cornerRadius']}px"
        
    # Background
    fills = [f for f in node.get('fills', []) if f.get('visible', True)]
    if fills:
        color = parse_color(fills[0])
        if color != "transparent":
            styles['background-color'] = color
            
    # Strokes (Borders)
    strokes = node.get('strokes', [])
    if strokes:
        scolor = parse_color(strokes[0])
        sw = node.get('strokeWeight', 1)
        styles['border'] = f"{sw}px solid {scolor}"

    return " ".join([f"{k}: {v};" for k, v in styles.items()])

def traverse(node, depth=0):
    indent = "  " * depth
    name = node.get('name', '')
    node_type = node.get('type', '')
    
    style_str = extract_styles(node)
    
    out = f"{indent}<div class='node-{node_type.lower()}' style='{style_str}'>\n"
    
    if node_type == 'TEXT':
        text = node.get('characters', '').replace('\n', '<br>')
        ts = node.get('style', {})
        fonts = ts.get('fontFamily', 'Space Grotesk')
        size = ts.get('fontSize', 16)
        weight = ts.get('fontWeight', 400)
        lh = ts.get('lineHeightPx', size * 1.2)
        
        color = "black"
        fills = node.get('fills', [])
        if fills: color = parse_color(fills[0])
            
        out += f"{indent}  <span style='font-family: \"{fonts}\"; font-size: {size}px; font-weight: {weight}; line-height: {lh}px; color: {color}'>{text}</span>\n"
        
    for child in node.get('children', []):
        if child.get('visible', True):
            out += traverse(child, depth + 1)
            
    out += f"{indent}</div>\n"
    return out

def main():
    with open('positivus_figma.json', 'r') as f:
        data = json.load(f)
        
    nodes = data.get('nodes', {})
    node = nodes.get("330:762", {}).get("document", {})
    if not node:
        return
        
    html = f"<html><head><style>@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap'); body {{ margin: 0; padding: 0; background-color: #fff; font-family: 'Space Grotesk', sans-serif; }} div {{ box-sizing: border-box; }} </style></head><body>\n"
    html += traverse(node)
    html += "</body></html>"
    
    with open('designer-system/positivus_generated.html', 'w') as outf:
        outf.write(html)
        
if __name__ == "__main__":
    main()
