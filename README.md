# EditSimple website

Static site (works on GitHub Pages). Every page shares one stylesheet and one script.

## Folder layout
- `*.html` – the published pages (generated, don't edit by hand)
- `src/layout.html` – header, footer and the lead popup shared by every page
- `src/pages/<name>.html` – the main content of each page
- `assets/site.css` – all styles
- `assets/site.js` – all interactions (menu, sliders, FAQ, popup, contact form)
- `assets/config.js` – address of the email function (see `supabase/RESEND-SETUP.txt`)
- `images/` – images, `videos/` – put hero.mp4 / testimonial-1.mp4 / testimonial-2.mp4 here
- `supabase/functions/send-lead` – serverless function that emails form submissions via Resend

## Editing
1. Change text in `src/pages/<name>.html` (or `src/layout.html` for header/footer/popup).
2. Run `python build.py` to regenerate the `.html` pages.
3. Page titles, descriptions and the page name shown in lead emails are set in `build.py`.
