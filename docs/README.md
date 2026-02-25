# WALLY Documentation

Welcome to the WALLY Ontology Editor documentation site!

## 📚 Documentation Pages

- **[Home](index.html)** - Project overview and quick links
- **[Features](features.html)** - Fish-eye visualization and interactive features
- **[Getting Started](getting-started.html)** - Installation and setup guide
- **[Development](development.html)** - Developer workflow and contribution guide
- **[Deployment](deployment.html)** - Production deployment guide
- **[Architecture](architecture.html)** - System design and algorithms

## 🚀 Quick Links

- **Live Demo:** http://161.35.239.151
- **GitHub:** https://github.com/gpad1234/Startup-One-Wally-Clean
- **GitHub Pages:** https://gpad1234.github.io/Startup-One-Wally-Clean/

## 📖 Viewing the Documentation

### Online (GitHub Pages)

Visit: **https://gpad1234.github.io/Startup-One-Wally-Clean/**

### Local Preview

```bash
# Install Jekyll (if not already installed)
gem install jekyll bundler

# Navigate to docs folder
cd docs

# Serve locally
jekyll serve

# Visit http://localhost:4000/Startup-One-Wally-Clean/
```

## 🎨 Documentation Structure

```
docs/
├── _config.yml           # Jekyll configuration
├── index.md              # Homepage
├── features.md           # Feature documentation
├── getting-started.md    # Setup guide
├── development.md        # Developer guide
├── deployment.md         # Deployment guide
├── architecture.md       # Technical architecture
├── guides/               # Additional guides
├── architecture/         # Architecture docs
├── api/                  # API documentation
└── tutorials/            # Step-by-step tutorials
```

## 🛠️ Enabling GitHub Pages

To publish this documentation:

1. Go to your repository on GitHub:
   https://github.com/gpad1234/Startup-One-Wally-Clean

2. Click **Settings** → **Pages** (in left sidebar)

3. Under "Build and deployment":
   - **Source:** Deploy from a branch
   - **Branch:** main
   - **Folder:** /docs

4. Click **Save**

5. Wait 1-2 minutes for site to build

6. Visit: https://gpad1234.github.io/Startup-One-Wally-Clean/

## 🎨 Theme

This documentation uses the **Cayman** theme. You can change it by editing `_config.yml`:

```yaml
theme: jekyll-theme-cayman  # Current theme

# Other themes:
# theme: jekyll-theme-slate
# theme: jekyll-theme-architect
# theme: jekyll-theme-minimal
# theme: minima
```

## ✍️ Contributing to Docs

1. Edit markdown files in `docs/`
2. Test locally with Jekyll
3. Commit and push changes
4. GitHub Pages auto-deploys in 1-2 minutes

## 📝 Markdown Features

All documentation uses standard markdown plus:

- **Code blocks** with syntax highlighting
- **Tables** for structured data
- **Emoji** support (🎉)
- **Links** between pages
- **Images** (add to `docs/assets/images/`)

## 🔗 Internal Links

Link to other docs pages:

```markdown
[Features](features.html)
[Getting Started](getting-started.html)
[API Docs](api/)
```

## 📷 Adding Images

1. Add images to `docs/assets/images/`
2. Reference in markdown:

```markdown
![Fish-Eye Graph](assets/images/fisheye-demo.png)
```

## 📦 Additional Resources

- Jekyll Documentation: https://jekyllrb.com/docs/
- GitHub Pages Docs: https://docs.github.com/en/pages
- Markdown Guide: https://www.markdownguide.org/

---

**Status:** 📝 Documentation complete and ready to publish!  
**Last Updated:** February 19, 2026
