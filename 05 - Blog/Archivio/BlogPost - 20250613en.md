---
stage: fine-tuned 🧠
draft: false
type: article
area: tech
related: []
source: original
title: "How i Built My Blog with Hugo and the Stack Theme"
date: '2025-06-13'
updated: 2026-07-12T21:34
tags: [tech/blog, tech/tutorial]
summary: "Hello everyone! In this post, I’ll share how I built my blog using Obsidian, Hugo, GitHub, and Hostinger, following a tutorial by NetworkChuck and customizing it with the Stack theme ([https://stac..."
---
[[Home MOC|Home]] / [[Blog]] / [[BlogPost - 20250613en|How i Built My Blog With Hugo and the Stack Theme]]

# How I Built My Blog with Hugo and the Stack Theme

Hello everyone! In this post, I’ll share how I built my blog using **Obsidian**, **Hugo**, **GitHub**, and **Hostinger**, following a tutorial by NetworkChuck and customizing it with the **Stack** theme ([https://stack.jimmycai.com/](https://stack.jimmycai.com/)). I’ll also guide you through configuring the Stack theme to create a sleek and functional blog.

## Why a Blog?

Inspired by _Building a Second Brain_ by Tiago Forte, I started this blog to share my ideas and organize my thoughts in a way that’s accessible and valuable. My goal is to express what I’m learning and provide insights for myself, my friends, family, and anyone interested in my perspective.

## How I Built the Site

Here are the main steps I followed to create my blog, adapted from NetworkChuck’s tutorial {{< youtube dnE7c0ELEH8 >}}.

### 1. Writing Posts with Obsidian

I use **Obsidian**, a powerful note-taking app, to write my blog posts in markdown. All posts are stored in a `post` folder within my Obsidian vault. Each post starts with a front matter block, which includes metadata like title, date, and tags. For example:

```toml
+++
title = "My First Post"
date = 2025-06-13
draft = false
tags = ["test", "blog"]
+++
```

Obsidian keeps my notes private, and only files in the `post` folder are published. To ensure images work (though I’m still troubleshooting this), I plan to use a Python script to sync images from Obsidian’s `attachments` folder to Hugo’s `static/images` folder.

### 2. Generating the Site with Hugo

**Hugo** is a static site generator that transforms markdown files into a website. Here’s how I set it up:

- **Installation**: I installed Hugo on my Mac using Homebrew (`brew install hugo`). I also installed Git and Go as prerequisites.
- **Site Creation**: I created a new Hugo site with `hugo new site BlogName`.
- **Theme Setup**: I chose the **Stack** theme (https://stack.jimmycai.com/) for its clean, card-style design. I installed it with:

  ```bash
  git submodule add https://github.com/CaiJimmy/hugo-theme-stack themes/hugo-theme-stack
  ```

- **Configuration**: I configured Hugo in `hugo.toml` by `nano` command to use the Stack theme:

```
baseURL = "https://example.com/"  # Replace with your domain
languageCode = "en-us"
title = "First Post"
theme = "hugo-theme-stack"

[params]
  mainSections = ["post"]
```

- **Syncing Posts**: I use `rsync` to copy posts from Obsidian’s `post` folder to Hugo’s `content/post` folder:

  ```bash
  rsync -av --delete ~/path/to/obsidian/post/ ~/path/to/BlogName/content/post/
  ```

- **Testing Locally**: I run `hugo server -t hugo-theme-stack` to preview the site at `http://localhost:1313`.

### 3. Version Control with GitHub

I use **GitHub** to store my site’s code and enable collaboration. Here’s the setup:

- **Repository Creation**: I created a repository named `BlogName` on GitHub.
- **SSH Authentication**: I generated an SSH key with `ssh-keygen -t rsa -b 4096 -C "my-email@example.com"`. The keys were initially saved in the wrong directory, but I moved them to `~/.ssh/id_rsa` and `~/.ssh/id_rsa.pub`, then added the public key to GitHub.
- **Pushing Code**: I initialized a Git repository in `BlogName`, added a remote (`git remote add origin git@github.com:username/BlogName.git`), and pushed changes:
  ```bash
  git add .
  git commit -m "Initial commit"
  git push origin master
  ```
- **Publishing**: I pushed the `public` folder to a `hostinger` branch for deployment:
  ```bash
  git subtree push --prefix public origin hostinger
  ```

### 4. Hosting with Vercel

Instead using **Hostinger** I deployed the site using **Vercel**:

- **Site Setup**: I created a new site on Vercel, linked to my GitHub repository
- **Webhook**: I set up a webhook on GitHub to auto-deploy updates when I push to the `master` branch.

### 5. Automating the Workflow

To streamline publishing, I created a Bash script (`updateblog.sh`) that:
- Syncs posts with `rsync`.
- Runs the Python script for images `images.py`.
- Generates the site with `hugo`.
- Commits and pushes to GitHub.

Here’s the script:

```bash
# Variabili
OBSIDIAN_POST_DIR="path here"
HUGO_POST_DIR="path here"
IMAGES_SCRIPT="path here"
HUGO_DIR="path here"
REPO_URL="link here"

# Step 1: Sincronizza i file markdown da Obsidian a Hugo con rsync
echo "Step 1: Sincronizzazione dei file markdown da Obsidian a Hugo con rsync..."
rsync -av --delete "$OBSIDIAN_POST_DIR/" "$HUGO_POST_DIR/"
if [ $? -ne 0 ]; then
    echo "Errore: Sincronizzazione con rsync fallita. Controlla i percorsi o installa rsync."
    exit 1
fi
echo "Step 1 completato: Sincronizzazione terminata."

# Step 2: Esegui lo script Python per sincronizzare markdown e immagini
echo "Step 2: Esecuzione dello script Python per sincronizzare markdown e immagini..."
python3 "$IMAGES_SCRIPT"
if [ $? -ne 0 ]; then
    echo "Errore: Esecuzione dello script Python fallita. Controlla il file images.py o i percorsi."
    exit 1
fi
echo "Step 2 completato: Elaborazione Python terminata."

# Step 3: Vai alla directory di Hugo
echo "Step 3: Spostamento nella directory di Hugo..."
cd "$HUGO_DIR" || {
    echo "Errore: Impossibile cambiare directory in $HUGO_DIR."
    exit 1
}
echo "Step 3 completato: Directory cambiata in $HUGO_DIR."

# Step 4: Genera il sito
echo "Step 4: Generazione del sito con Hugo..."
hugo
if [ $? -ne 0 ]; then
    echo "Errore: Generazione del sito con Hugo fallita. Controlla la configurazione."
    exit 1
fi
echo "Step 4 completato: Generazione del sito terminata."

# Step 5: Aggiungi e commita i file
echo "Step 5: Aggiunta e commit dei file..."
git add .
git commit -m "Aggiornamento blog $(date +%F)"
if [ $? -ne 0 ]; then
    echo "Errore: Commit dei file fallito. Controlla lo stato del repository Git."
    exit 1
fi
echo "Step 5 completato: Commit eseguito."

# Step 6: Push sul branch principale (per Vercel)
echo "Step 6: Push sul branch principale per Vercel..."
git push -u origin master
if [ $? -ne 0 ]; then
    echo "Errore: Push sul branch principale fallito. Controlla la connessione SSH o il repository."
    exit 1
fi
echo "Step 6 completato: Push eseguito con successo.">)

```

**Script Name**: `updateblog.sh`

Replace the `paths` and `username` with your own. Run it after making it executable (`chmod +x updateblog.sh`).

## Guide to Using the Stack Theme

The **Stack** theme (https://stack.jimmycai.com/) is a card-style theme designed for bloggers. Here’s how to configure it, based on its documentation (https://stack.jimmycai.com/config/).

### Installation

1. Add the theme as a Git submodule:
   ```bash
   git submodule add https://github.com/CaiJimmy/hugo-theme-stack themes/hugo-theme-stack
   ```

2. Update `hugo.toml` to set the theme:
   ```toml
   theme = "hugo-theme-stack"
   ```

### Configuration

Stack supports TOML and YAML configuration, with a planned migration to TOML. For a full list of options, check the `config.yaml` file in the theme’s root or the documentation (https://stack.jimmycai.com/config/).

### Creating Posts

Posts need a front matter block. Example:

```yaml
---
title : "Your Post Title"
date : 2025-06-13
draft : false
tags : ["tag1", "tag2"]
description : "A short description"
---
```

- Set `draft : false` to publish the post.
- Use `image` to add a cover image

### Testing

Run `hugo server -t hugo-theme-stack --buildDrafts` to preview changes locally. Ensure posts appear in the card layout on `http://localhost:1313`.

Happy blogging!

---
## Collegamenti
