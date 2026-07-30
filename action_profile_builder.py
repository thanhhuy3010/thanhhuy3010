import os
import json
import urllib.request
import urllib.error
import io
from PIL import Image, ImageEnhance

# Bộ ký tự đơn giản, ít nhiễu
ASCII_CHARS = ["@", "%", "#", "*", "+", "=", "-", ":", ".", " "]

def fetch_image_as_pil(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            image_data = response.read()
            return Image.open(io.BytesIO(image_data))
    except Exception as e:
        print(f"Error fetching image: {e}")
        return None

def resize_image(image, new_width=70):
    width, height = image.size
    ratio = height / width
    new_height = int(new_width * ratio * 0.6)
    return image.resize((new_width, new_height))

def grayify(image):
    return image.convert("L")

def pixels_to_ascii(image):
    pixels = image.getdata()
    chars_len = len(ASCII_CHARS)
    characters = "".join([ASCII_CHARS[int(pixel / 255 * (chars_len - 1))] for pixel in pixels])
    return characters

def generate_ascii_svg_elements(image_url):
    image = fetch_image_as_pil(image_url)
    if not image:
        return ""
    
    # Tăng nhẹ độ tương phản để viền không bị gắt
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(1.2)
    
    # Tăng độ phân giải ASCII lên 70 ký tự
    width = 70
    new_image_data = pixels_to_ascii(grayify(resize_image(image, width)))
    pixel_count = len(new_image_data)
    
    # Chia thành từng dòng
    lines = [new_image_data[i:(i+width)] for i in range(0, pixel_count, width)]
    
    start_x = 48
    start_y = 70
    line_height = 4
    
    svg_text = f'<text x="{start_x}" y="{start_y}" class="ascii-art">\n'
    for line in lines:
        svg_text += f'        <tspan x="{start_x}" dy="{line_height}" xml:space="preserve">{line}</tspan>\n'
    svg_text += '    </text>'
    
    return svg_text

def fetch_github_stats(username, token):
    url = f"https://api.github.com/users/{username}"
    headers = {
        "Authorization": f"token {token}" if token else "",
        "User-Agent": "Python-urllib"
    }
    if not token:
        if "Authorization" in headers:
            del headers["Authorization"]
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            return data
    except urllib.error.URLError as e:
        print(f"Failed to fetch GitHub API: {e}")
        return {}

def create_svg():
    username = "thanhhuy3010"
    token = os.environ.get("GH_TOKEN")
    
    stats = fetch_github_stats(username, token)
    
    name = stats.get("name", "Hubert Tran")
    public_repos = stats.get("public_repos", 0)
    avatar_url = stats.get("avatar_url", "")
    
    ascii_svg = ""
    if avatar_url:
        ascii_svg = generate_ascii_svg_elements(avatar_url)
    
    skills = ["Python", "JavaScript", "React Native", "Swift", "Kotlin", "Node.js", "Docker"]
    skills_line1 = ", ".join(skills[:3]) + ","
    skills_line2 = ", ".join(skills[3:])

    svg_template = f"""<?xml version='1.0' encoding='UTF-8'?>
<svg xmlns="http://www.w3.org/2000/svg" width="820" height="390" viewBox="0 0 820 390">
<defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#1E1E2E"/>
        <stop offset="100%" stop-color="#181825"/>
    </linearGradient>
    <linearGradient id="glow" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#89B4FA"/>
        <stop offset="100%" stop-color="#CBA6F7"/>
    </linearGradient>
</defs>

<style>
.code {{
    font-family: Consolas, "Courier New", monospace;
    font-size: 15px;
    fill: #CDD6F4;
}}
.title {{ font-family: Consolas, "Courier New", monospace; font-size: 14px; fill: #A6ADC8; }}
.key {{ fill: #89B4FA; font-weight: bold; }}
.string {{ fill: #A6E3A1; }}
.number {{ fill: #FAB387; }}
.comment {{ fill: #6C7086; font-style: italic; }}
.bracket {{ fill: #F9E2AF; }}
.cursor {{
    fill: #CBA6F7;
    animation: blink 1s step-end infinite;
}}
.ascii-art {{
    font-family: Consolas, "Courier New", monospace;
    font-size: 4px;
    fill: #CBA6F7;
    font-weight: bold;
    letter-spacing: 0px;
}}
@keyframes blink {{
    0%, 100% {{ opacity: 1; }}
    50% {{ opacity: 0; }}
}}
</style>

<rect x="10" y="10" width="800" height="370" fill="url(#bg)" rx="12" ry="12" stroke="#313244" stroke-width="2"/>

<circle cx="35" cy="35" r="7" fill="#F38BA8"/>
<circle cx="55" cy="35" r="7" fill="#F9E2AF"/>
<circle cx="75" cy="35" r="7" fill="#A6E3A1"/>
<text x="410" y="40" class="title" text-anchor="middle">thanhhuy3010 — zsh</text>

<line x1="10" y1="55" x2="810" y2="55" stroke="#313244" stroke-width="2"/>

{ascii_svg}

<g class="code" transform="translate(280, 95)">
    <text y="0" class="key">➜</text>
    <text y="0" x="20" fill="#89B4FA">~</text>
    <text y="0" x="40">cat profile.txt</text>
    
    <text y="30" class="key">Name: <tspan class="string">{name}</tspan></text>
    <text y="55" class="key">Role: <tspan class="string">Software Engineer</tspan></text>
    
    <text y="90" class="key">➜</text>
    <text y="90" x="20" fill="#89B4FA">~</text>
    <text y="90" x="40">skills --list</text>

    <text y="120" class="string">{skills_line1}</text>
    <text y="145" class="string">{skills_line2}</text>
    <text y="170" class="key">➜</text>
    <text y="170" x="20" fill="#89B4FA">~</text>
    <rect x="40" y="155" width="10" height="18" class="cursor"/>
</g>
</svg>
"""

    with open("dark_dynamic.svg", "w", encoding="utf-8") as f:
        f.write(svg_template)
    print("Created dark_dynamic.svg successfully with ASCII avatar!")

if __name__ == "__main__":
    create_svg()
