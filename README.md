# Academic Portfolio Website

This is your personal academic portfolio website built with Jekyll and the Minimal Mistakes theme, enhanced with Academic Pages content structure.

## Quick Start

### 1. Customize Your Information

Edit `_config.yml` to update:
- Your name, bio, and contact information
- Social media links (Twitter, LinkedIn, etc.)
- Site title and description
- Google Scholar profile (add `googlescholar: "your_profile_url"` to author section)

### 2. Add Your Content

#### Publications (`_publications/`)
- Create new files like `YYYY-publication-title.md`
- Include title, venue, date, citation, and paper URL
- Add abstracts and additional details

#### Talks (`_talks/`)
- Add conference presentations, seminars, and workshops
- Include venue, date, location, and slides/video links

#### Teaching (`_teaching/`)
- Document courses you've taught or assisted with
- Include course descriptions and your role

#### Portfolio (`_portfolio/`)
- Showcase research projects, software, or other work
- Include project descriptions, technologies used, and links

### 3. Customize Design

The site uses Minimal Mistakes theme with these customization options:

#### Color Schemes
In `_config.yml`, change `minimal_mistakes_skin` to:
- `"default"` - White background with dark text
- `"air"` - Light and airy
- `"aqua"` - Blue accent colors
- `"contrast"` - High contrast dark theme
- `"dark"` - Dark theme
- `"dirt"` - Brown earth tones
- `"neon"` - Bright neon accents
- `"mint"` - Green mint theme
- `"plum"` - Purple theme
- `"sunrise"` - Orange/yellow theme

#### Navigation
Edit `_data/navigation.yml` to modify the main navigation menu.

#### Author Profile
Update the author section in `_config.yml` to customize your sidebar information.

### 4. Local Development

To run the site locally:

```bash
# Install dependencies
bundle install

# Serve the site locally
bundle exec jekyll serve

# View at http://localhost:4000
```

### 5. GitHub Pages Deployment

Your site will automatically deploy to `https://youngjour.github.io` when you push to the main branch.

## File Structure

```
├── _config.yml           # Site configuration
├── _data/
│   └── navigation.yml     # Navigation menu
├── _pages/               # Main pages (About, CV, etc.)
├── _publications/        # Publication entries
├── _talks/              # Talk and presentation entries
├── _teaching/           # Teaching experience entries
├── _portfolio/          # Portfolio/project entries
├── assets/
│   └── images/          # Images for your site
├── Gemfile              # Ruby dependencies
└── index.md             # Homepage
```

## Adding Content

### Publications Example

Create `_publications/2024-your-paper.md`:

```yaml
---
title: "Your Paper Title"
collection: publications
permalink: /publication/2024-your-paper
excerpt: 'Brief description of your paper.'
date: 2024-01-01
venue: 'Conference/Journal Name'
paperurl: 'https://link-to-paper.com'
citation: 'Author, A. (2024). "Paper Title." Journal Name.'
---

Paper content and details here.
```

### Profile Photo

Add your photo to `assets/images/` and update the `avatar` field in `_config.yml`:

```yaml
author:
  avatar: "/assets/images/your-photo.jpg"
```

## Tips

1. Use meaningful filenames (YYYY-title-format) for chronological ordering
2. Include relevant keywords in your content for better searchability
3. Link to external resources (papers, code repositories, etc.)
4. Keep your content updated regularly
5. Test locally before pushing to ensure everything works

## Support

- [Minimal Mistakes Documentation](https://mmistakes.github.io/minimal-mistakes/)
- [Jekyll Documentation](https://jekyllrb.com/docs/)
- [GitHub Pages Documentation](https://docs.github.com/en/pages)