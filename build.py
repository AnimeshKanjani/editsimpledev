"""Builds the EditSimple pages: src/layout.html + src/pages/<name>.html -> <name>.html"""
import re, pathlib

ROOT = pathlib.Path(__file__).parent
LAYOUT = (ROOT / "src/layout.html").read_text()

# name: (title, meta description, label used in form emails)
PAGES = {
    "index": ("EditSimple | YouTube for Dermatology & Aesthetic Practices",
              "We run your practice's YouTube channel end to end: strategy, scripts, editing, thumbnails and publishing. You record once a month. HIPAA-compliant, BAA available.",
              "Homepage"),
    "work": ("EditSimple | Our Work",
             "600+ videos a month, 1B+ views: three years producing content for US professionals, now for dermatology and aesthetic practices.",
             "Our Work"),
    "about": ("EditSimple | About", "EditSimple runs YouTube channels for experts who'd rather be doing their real job.", "About"),
    "careers": ("EditSimple | Careers", "Join the EditSimple team.", "Careers"),
    "contact": ("EditSimple | Contact Us", "Email us or book a free 30-minute strategy call with EditSimple.", "Contact"),
    "privacy": ("EditSimple | Privacy Policy", "How EditSimple handles information, and our commitment to never disclose patient information. HIPAA-conscious, BAA available.", "Privacy Policy"),
    "terms": ("EditSimple | Terms & Conditions", "The terms that apply when your practice works with EditSimple on YouTube and social video.", "Terms & Conditions"),
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
