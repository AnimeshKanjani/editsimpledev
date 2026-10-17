"""Builds the EditSimple pages: src/layout.html + src/pages/<name>.html -> <name>.html"""
import re, pathlib

ROOT = pathlib.Path(__file__).parent
LAYOUT = (ROOT / "src/layout.html").read_text()

# name: (title, meta description, label used in form emails)
PAGES = {
    "index": ("EditSimple | Turn YouTube Into Your #1 Client Source",
              "Turn YouTube into a 24/7 client acquisition system that helps your business attract more clients and accelerate growth without ads.",
              "Generic Homepage"),
    "solutions": ("EditSimple | Solutions",
                  "Learn our system, partner with us, or let us handle everything. Choose the YouTube growth path that fits your business.",
                  "Solutions"),
    "course": ("EditSimple | Course",
               "A 10-module YouTube growth course for professionals: create, grow and monetize your channel.",
               "Course"),
    "consulting": ("EditSimple | Consulting",
                   "Professional YouTube content creation support while you learn our proven growth strategies.",
                   "Consulting"),
    "productions": ("EditSimple | Productions",
                    "Done-for-you YouTube production and channel management for busy professionals.",
                    "Productions"),
    "free-resources": ("EditSimple | Free Resources",
                       "Free guides to start growing your YouTube channel and scale your business without relying on ads.",
                       "Free Resources"),
    "about": ("EditSimple | About", "EditSimple turns your vision into captivating video content.", "About"),
    "careers": ("EditSimple | Careers", "Join the EditSimple team.", "Careers"),
    "contact": ("EditSimple | Contact Us", "Email us or book a free 30-minute strategy call with EditSimple.", "Contact"),
    "privacy": ("EditSimple | Privacy Policy", "EditSimple Privacy Policy.", "Privacy Policy"),
    "terms": ("EditSimple | Terms & Conditions", "EditSimple Terms & Conditions.", "Terms & Conditions"),
}

def background(tag):
    """Rough background key of a <section> opening tag, used to merge gaps between same-coloured sections."""
    if re.search(r'class="[^"]*(hero|ct-hero|lg-hero)', tag): return "hero"
    if 'class="meet' in tag: return "dark"
    if "var(--cream)" in tag or re.search(r'class="[^"]*\b(paths|faq)\b', tag): return "cream"
    return "white"

def flush_same_backgrounds(main):
    out, pos, prev = [], 0, None
    for m in re.finditer(r"^<section\b[^>]*>", main, re.M):
        tag, bg = m.group(0), background(m.group(0))
        if bg == prev and bg != "hero":
            tag = tag.replace('class="', 'class="flush-top ', 1) if 'class="' in tag else tag.replace("<section", '<section class="flush-top"', 1)
        out.append(main[pos:m.start()] + tag)
        pos, prev = m.end(), bg
    return "".join(out) + main[pos:]

for name, (title, desc, label) in PAGES.items():
    main = flush_same_backgrounds((ROOT / f"src/pages/{name}.html").read_text().strip())
    html = (LAYOUT.replace("{{title}}", title.replace("&", "&amp;"))
                  .replace("{{description}}", desc)
                  .replace("{{label}}", label.replace("&", "&amp;"))
                  .replace("{{main}}", main))
    (ROOT / f"{name}.html").write_text(html)
    print("built", name)
