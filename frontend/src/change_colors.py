import os

base_dir = "C:/Portfolio/frontend/src"

replacements = {
    "violet": "emerald",
    "fuchsia": "teal",
    "purple": "emerald",
    "pink": "teal",
    "indigo": "cyan",
    "blue": "teal",
    "Violet": "Emerald",
    "Fuchsia": "Teal",
    "Purple": "Emerald",
    "Pink": "Teal",
    "Indigo": "Cyan",
    "Blue": "Teal",
    "hsla(250,100%,74%": "hsla(150,100%,74%",
    "hsla(355,100%,93%": "hsla(350,100%,70%", # changed to a reddish hue for accent
    "hsla(189,100%,56%": "hsla(170,100%,56%"  # teal hue
}

for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith(".jsx") or file.endswith(".css") or file.endswith(".js"):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            
            new_content = content
            for old, new in replacements.items():
                new_content = new_content.replace(old, new)
            
            if new_content != content:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(new_content)
print("Color replacement done.")
