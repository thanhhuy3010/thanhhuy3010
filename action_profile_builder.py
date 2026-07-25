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
    # User info
    username = "thanhhuy3010"
    
    # Lấy token từ biến môi trường (Environment Variable) do GitHub Actions truyền vào
    token = os.environ.get("GH_TOKEN")
    if not token:
        print("Error: GH_TOKEN environment variable not set.")
        return
        
    print("Fetching GitHub stats...")
    stats = fetch_github_stats(username, token)
    
    name = stats.get("name", "Hubert Tran")
    followers = stats.get("followers", 0)
    following = stats.get("following", 0)
    public_repos = stats.get("public_repos", 0)
    avatar_url = stats.get("avatar_url", "")
    
    # Tự động tải ảnh đại diện từ GitHub thay vì dùng ảnh local
    base64_image = ""
    if avatar_url:
        print("Fetching and encoding avatar image...")
        base64_image = fetch_image_as_base64(avatar_url)
    
    role = "Software Engineer"
    skills = ["Python", "JavaScript", "React", "Node.js", "Docker", "AWS"]
    skills_str = '", "'.join(skills)

    image_tag = ""
    if base64_image:
        image_tag = f'<image x="30" y="70" width="180" height="240" preserveAspectRatio="xMidYMid slice" clip-path="url(#circleView)" href="{base64_image}" />'

    # SVG Template
    svg_template = f"""<?xml version='1.0' encoding='UTF-8'?>
<svg xmlns="http://www.w3.org/2000/svg" font-family="ConsolasFallback,Consolas,monospace" width="800" height="400" viewBox="0 0 800 400" fontsize="15px">
<style>
@font-face {{
    src: local('Consolas'), local('Consolas Bold');
    font-family: 'ConsolasFallback';
    font-display: swap;
}}
.key      {{ fill: #5EEAD4; font-weight: bold; }}   
.string   {{ fill: #E5E7EB; }}   
.number   {{ fill: #A78BFA; }}
.bracket  {{ fill: #FBBF24; }}
.keyword  {{ fill: #F472B6; }}
.comment  {{ fill: #6B7280; font-style: italic; }}
text, tspan {{white-space: pre;}}
</style>

<defs>
    <clipPath id="circleView">
        <circle cx="120" cy="190" r="90" fill="#FFFFFF" />
    </clipPath>
</defs>

<rect width="800px" height="400px" fill="#0D1117" rx="15"/>

<circle cx="25" cy="25" r="6" fill="#FF5F56"/>
<circle cx="45" cy="25" r="6" fill="#FFBD2E"/>
<circle cx="65" cy="25" r="6" fill="#27C93F"/>
<text x="350" y="30" fill="#8B949E" font-size="14px">{username} ~ bash</text>

{image_tag}

<text x="250" y="80" class="comment">
<tspan x="250" dy="1.2em"># Loading profile: {username}...</tspan>
<tspan x="250" dy="1.2em"># Fetched from GitHub API dynamically via Actions</tspan>
</text>

<text x="250" y="125">
<tspan x="250" dy="1.2em" class="keyword">const </tspan><tspan class="key">profile</tspan><tspan class="bracket"> = {{</tspan>
<tspan x="270" dy="1.5em" class="key">"name"</tspan><tspan class="string">: "{name}",</tspan>
<tspan x="270" dy="1.5em" class="key">"role"</tspan><tspan class="string">: "{role}",</tspan>
<tspan x="270" dy="1.5em" class="key">"followers"</tspan><tspan class="string">: </tspan><tspan class="number">{followers}</tspan><tspan class="string">,</tspan>
<tspan x="270" dy="1.5em" class="key">"following"</tspan><tspan class="string">: </tspan><tspan class="number">{following}</tspan><tspan class="string">,</tspan>
<tspan x="270" dy="1.5em" class="key">"repos"</tspan><tspan class="string">: </tspan><tspan class="number">{public_repos}</tspan><tspan class="string">,</tspan>
<tspan x="270" dy="1.5em" class="key">"skills"</tspan><tspan class="string">: ["{skills_str}"],</tspan>
<tspan x="250" dy="1.5em" class="bracket">}};</tspan>
</text>

<text x="250" y="270" class="comment">
<tspan x="250" dy="1.2em">> console.log("Welcome to my GitHub!");</tspan>
</text>
<text x="250" y="290" class="string">
<tspan x="250" dy="1.2em">Welcome to my GitHub!</tspan>
</text>
<text x="250" y="330" class="keyword">
<tspan x="250" dy="1.2em">█</tspan>
</text>
</svg>
"""

    with open("dark_dynamic.svg", "w", encoding="utf-8") as f:
        f.write(svg_template)
    print("Created dark_dynamic.svg successfully!")

if __name__ == "__main__":
    create_svg()
