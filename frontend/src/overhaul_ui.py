import os

frontend_dir = "C:/Portfolio/frontend"

# 1. Update index.html
html_path = os.path.join(frontend_dir, "index.html")
with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()
html = html.replace("Outfit:wght@300;400;500;600;700;800;900", "Lora:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500;1,600;1,700")
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html)

# 2. Update tailwind.config.js
tailwind_path = os.path.join(frontend_dir, "tailwind.config.js")
with open(tailwind_path, "r", encoding="utf-8") as f:
    tw = f.read()
tw = tw.replace("Outfit", "Lora")
with open(tailwind_path, "w", encoding="utf-8") as f:
    f.write(tw)

# 3. Update index.css
css_path = os.path.join(frontend_dir, "src/index.css")
new_css = """@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  body {
    @apply bg-[#FCFCFC] text-[#2C2C2C] transition-colors duration-300;
  }
  .dark body {
    @apply bg-[#121212] text-[#DEDEDE];
  }
}

.glass-card {
  @apply bg-white border border-stone-200 shadow-sm hover:shadow-md transition-all duration-300 rounded-none;
}

.dark .glass-card {
  @apply bg-[#1A1A1A] border border-stone-800 shadow-none hover:border-stone-600 rounded-none;
}

.bg-mesh {
  background: transparent;
}
"""
with open(css_path, "w", encoding="utf-8") as f:
    f.write(new_css)

# 4. Global string replacements
replacements = {
    "font-black": "font-bold",
    "font-extrabold": "font-bold",
    "rounded-xl": "rounded-sm",
    "rounded-2xl": "rounded-sm",
    "rounded-lg": "rounded-sm",
    "rounded-md": "rounded-sm",
    
    # Remove gradients and colorful text
    "text-transparent bg-clip-text bg-gradient-to-r from-emerald-500 to-teal-500": "italic text-stone-500 dark:text-stone-400 font-normal",
    "text-transparent bg-clip-text bg-gradient-to-r from-emerald-600 to-teal-500 dark:from-emerald-400 dark:to-teal-300": "text-stone-600 dark:text-stone-400 italic",
    "text-transparent bg-clip-text bg-gradient-to-r from-orange-500 to-amber-500": "italic text-stone-500 dark:text-stone-400 font-normal",
    "bg-gradient-to-r from-emerald-500 to-teal-500": "bg-stone-200 dark:bg-stone-800",
    "bg-gradient-to-b from-emerald-500 to-teal-500": "bg-stone-300 dark:bg-stone-700",
    "bg-gradient-to-br from-emerald-100 to-emerald-200 dark:from-emerald-900/50 dark:to-emerald-800/50": "bg-stone-100 dark:bg-stone-900",
    "bg-gradient-to-br from-teal-100 to-teal-200 dark:from-teal-900/50 dark:to-teal-800/50": "bg-stone-100 dark:bg-stone-900",
    
    # Map colors to neutral elegant stones
    "emerald-600": "stone-800",
    "emerald-700": "stone-900",
    "emerald-500": "stone-700",
    "emerald-400": "stone-300",
    "emerald-100": "stone-100",
    "emerald-50": "stone-50",
    
    "teal-600": "stone-800",
    "teal-700": "stone-900",
    "teal-500": "stone-700",
    "teal-400": "stone-300",
    "teal-100": "stone-100",
    "teal-50": "stone-50",
    
    "orange-600": "stone-800",
    "orange-500": "stone-700",
    "orange-400": "stone-300",
    "orange-100": "stone-100",
    "orange-50": "stone-50",
    
    "rose-600": "stone-800",
    "rose-500": "stone-700",
    "rose-400": "stone-300",
    "rose-100": "stone-100",
    "rose-50": "stone-50",
    
    # Remove excessive shadows
    "shadow-[0_0_20px_rgba(16,185,129,0.3)]": "",
    "shadow-[0_0_25px_rgba(16,185,129,0.5)]": "",
    "shadow-[0_0_20px_rgba(20,184,166,0.3)]": "",
    "shadow-[0_0_10px_rgba(16,185,129,0.8)]": "",
    
    # Dark mode text mapping for buttons
    "dark:hover:bg-stone-800 text-white": "dark:hover:bg-stone-700 text-white dark:bg-stone-800",
    "bg-stone-800 hover:bg-stone-900 text-white": "bg-stone-900 hover:bg-stone-800 text-white dark:bg-stone-100 dark:text-stone-900 dark:hover:bg-stone-300",
    
    # Update button sizing and aesthetics
    "px-6 py-3": "px-8 py-3 uppercase tracking-widest text-xs border border-transparent",
    
    "bg-clip-text": "",
}

src_dir = os.path.join(frontend_dir, "src")
for root, dirs, files in os.walk(src_dir):
    for file in files:
        if file.endswith((".jsx", ".js")):
            filepath = os.path.join(root, file)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            
            orig_content = content
            
            # Special case for Navbar to remove gradients and adjust text
            if file == "Navbar.jsx":
                content = content.replace("text-transparent bg-clip-text bg-gradient-to-r from-stone-800 to-stone-800", "text-stone-900 dark:text-stone-100")
                content = content.replace("border-b border-stone-200/50 dark:border-white/10", "border-b border-stone-200 dark:border-stone-800")
                content = content.replace("bg-white/80 dark:bg-slate-950/80 backdrop-blur-md", "bg-[#FCFCFC] dark:bg-[#121212]")

            for old, new in replacements.items():
                content = content.replace(old, new)
                
            if content != orig_content:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)

print("UI successfully overhauled to Classic/Editorial style.")
