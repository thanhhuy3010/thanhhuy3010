import os
import json
import base64
import urllib.request
import urllib.error

def fetch_image_as_base64(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            image_data = response.read()
            encoded_string = base64.b64encode(image_data).decode('utf-8')
            return f"data:image/jpeg;base64,{encoded_string}"
    except Exception as e:
        print(f"Error fetching image: {e}")
        return ""

def fetch_github_stats(username, token):
    url = f"https://api.github.com/users/{username}"
    headers = {
        "Authorization": f"token {token}",
        "User-Agent": "Python-urllib"
    }
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
    followers = stats.get("followers", 0)
    following = stats.get("following", 0)
    public_repos = stats.get("public_repos", 0)
    avatar_url = stats.get("avatar_url", "")
    
    base64_image = ""
    if avatar_url:
        base64_image = fetch_image_as_base64(avatar_url)
    
    skills = ["Python", "JavaScript", "React", "Node.js", "Docker", "AWS"]
    skills_str = '", "'.join(skills)

    image_tag = ""
    if base64_image:
        image_tag = f'<image x="50" y="120" width="160" height="160" preserveAspectRatio="xMidYMid slice" clip-path="url(#circleView)" href="{base64_image}" />'

    svg_template = f"""<?xml version='1.0' encoding='UTF-8'?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="850" height="450" viewBox="0 0 850 450">
<defs>
    <clipPath id="circleView">
        <circle cx="130" cy="200" r="80" fill="#FFFFFF" />
    </clipPath>
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
@keyframes blink {{
    0%, 100% {{ opacity: 1; }}
    50% {{ opacity: 0; }}
}}
</style>

<rect x="10" y="10" width="830" height="430" fill="url(#bg)" rx="12" ry="12" stroke="#313244" stroke-width="2"/>

<circle cx="35" cy="35" r="7" fill="#F38BA8"/>
<circle cx="55" cy="35" r="7" fill="#F9E2AF"/>
<circle cx="75" cy="35" r="7" fill="#A6E3A1"/>
<text x="425" y="40" class="title" text-anchor="middle">thanhhuy3010 — zsh</text>

<line x1="10" y1="55" x2="840" y2="55" stroke="#313244" stroke-width="2"/>

{image_tag.replace('href=', 'xlink:href=') if image_tag else ""}
<circle cx="130" cy="200" r="82" fill="none" stroke="url(#glow)" stroke-width="3"/>

<g class="code" transform="translate(280, 100)" font-family="Consolas, 'Courier New', monospace" font-size="15px">
    <text y="0" class="comment"># Fetching profile data...</text>
    <text y="30"><tspan fill="#CBA6F7">const</tspan> <tspan class="key">developer</tspan> <tspan class="bracket">=</tspan> {{</text>
    
    <text y="60" x="20">name: <tspan class="string">"{name}"</tspan>,</text>
    <text y="85" x="20">role: <tspan class="string">"Software Engineer"</tspan>,</text>
    <text y="110" x="20">github: {{</text>
    <text y="135" x="40">followers: <tspan class="number">{followers}</tspan>,</text>
    <text y="160" x="40">following: <tspan class="number">{following}</tspan>,</text>
    <text y="185" x="40">repositories: <tspan class="number">{public_repos}</tspan></text>
    <text y="210" x="20">}},</text>
    
    <text y="235" x="20">skills: [</text>
    <text y="260" x="40" class="string">"{skills_str}"</text>
    <text y="285" x="20">]</text>
    
    <text y="310">}};</text>

    <text y="355" class="key">➜</text>
    <text y="355" x="20" fill="#89B4FA">~</text>
    <text y="355" x="35" fill="#CDD6F4">echo "Welcome to my GitHub Profile!"</text>
    <rect x="345" y="340" width="10" height="18" class="cursor"/>
</g>
</svg>
"""

    with open("dark_dynamic.svg", "w", encoding="utf-8") as f:
        f.write(svg_template)
    print("Created dark_dynamic.svg successfully!")

if __name__ == "__main__":
    create_svg()
