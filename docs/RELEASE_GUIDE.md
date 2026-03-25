# Release Guide - Surviving Nightfall

## Overview
This guide explains how to create releases for Surviving Nightfall using git tags and GitHub Actions.

## Git Tags Explained

### What are Git Tags?
Git tags are references that point to specific commits in your repository's history. They're commonly used to mark release points (v1.0, v2.0, etc.).

### Types of Tags
1. **Lightweight tags**: Just a pointer to a commit
2. **Annotated tags**: Full objects with metadata (recommended for releases)

## Release Workflow

### Step 1: Prepare Your Code
Make sure all your changes are committed and pushed:

```bash
# Check status
git status

# Add any uncommitted changes
git add .

# Commit changes
git commit -m "Prepare for v1.0.0 release"

# Push to GitHub
git push origin main
```

### Step 2: Create a Git Tag

#### Option A: Annotated Tag (Recommended)
```bash
# Create an annotated tag with a message
git tag -a v1.0.0 -m "Release version 1.0.0 - Initial playable release"

# View the tag
git show v1.0.0

# Push the tag to GitHub
git push origin v1.0.0
```

#### Option B: Lightweight Tag
```bash
# Create a lightweight tag
git tag v1.0.0

# Push the tag to GitHub
git push origin v1.0.0
```

### Step 3: Create GitHub Release

#### Method 1: Via GitHub Web UI (Easiest)
1. Go to your repository on GitHub
2. Click on **"Releases"** in the right sidebar
3. Click **"Draft a new release"**
4. Click **"Choose a tag"** dropdown
5. Select your tag (e.g., `v1.0.0`) or type a new one
6. Fill in release details:
   - **Release title**: e.g., "Surviving Nightfall v1.0.0"
   - **Description**: Add release notes, features, bug fixes
7. Click **"Publish release"**

**This triggers the GitHub Action automatically!**

#### Method 2: Via GitHub CLI
```bash
# Install GitHub CLI first: https://cli.github.com/

# Create a release from a tag
gh release create v1.0.0 --title "Surviving Nightfall v1.0.0" --notes "Initial playable release with 5 waves, multiple weapons, and abilities"
```

### Step 4: GitHub Actions Builds Your Game
Once you create the release, the workflow automatically:
1. ✅ Checks out your code at the tagged commit
2. ✅ Sets up Python 3.13
3. ✅ Installs dependencies with `uv`
4. ✅ Builds Windows `.exe` with PyInstaller
5. ✅ Builds Linux executable
6. ✅ Packages assets and game files
7. ✅ Creates README.txt with controls
8. ✅ Zips/tarballs the distributions
9. ✅ Uploads to your GitHub Release

### Step 5: Download and Test
1. Go to your GitHub Releases page
2. Download the build artifacts:
   - `SurvivingNightfall-Windows-v1.0.0.zip`
   - `SurvivingNightfall-Linux-v1.0.0.tar.gz`
3. Extract and test the game

## Version Numbering (Semantic Versioning)

Use semantic versioning: `MAJOR.MINOR.PATCH`

- **MAJOR** (1.x.x): Breaking changes, major new features
- **MINOR** (x.1.x): New features, backwards compatible
- **PATCH** (x.x.1): Bug fixes, small improvements

### Examples:
- `v0.1.0` - Initial development release
- `v1.0.0` - First stable release
- `v1.1.0` - Added new weapons
- `v1.1.1` - Fixed bug in wave progression
- `v2.0.0` - Major overhaul with new game modes

## Common Git Tag Commands

### List all tags
```bash
git tag
# or with pattern matching
git tag -l "v1.*"
```

### View tag details
```bash
git show v1.0.0
```

### Delete a local tag
```bash
git tag -d v1.0.0
```

### Delete a remote tag
```bash
git push origin --delete v1.0.0
```

### Tag an older commit
```bash
# Find the commit hash
git log --oneline

# Tag that specific commit
git tag -a v1.0.0 9fceb02 -m "Release v1.0.0"

# Push the tag
git push origin v1.0.0
```

### Move a tag to a different commit
```bash
# Delete old tag locally and remotely
git tag -d v1.0.0
git push origin --delete v1.0.0

# Create new tag at current commit
git tag -a v1.0.0 -m "Release v1.0.0"

# Push new tag
git push origin v1.0.0
```

## Example Release Workflow

### For v1.0.0 (First Release)
```bash
# 1. Make sure everything is committed
git add .
git commit -m "Final changes for v1.0.0"
git push origin main

# 2. Create and push tag
git tag -a v1.0.0 -m "Initial release - Fully playable 5-wave survival game"
git push origin v1.0.0

# 3. Create GitHub Release (via web UI or CLI)
gh release create v1.0.0 \
  --title "Surviving Nightfall v1.0.0 - Initial Release" \
  --notes "
## Features
- 5 waves of increasing difficulty
- 7 unique weapons (Handgun, Shotgun, Machine Gun, Katana, Chainsaw, Bazooka, Flamethrower)
- 3 special abilities (Arc Lightning, Ice Bullets, Healing)
- Weapon shop system
- XP and leveling system
- Pause menu
- Hit particle effects

## Controls
- WASD: Move
- Mouse: Look around
- Left Click: Shoot
- ESC: Pause

## Known Issues
- None at this time
"

# 4. Wait for GitHub Actions to build (check Actions tab)
# 5. Download and test the builds
```

### For v1.1.0 (Feature Update)
```bash
# After adding new features
git add .
git commit -m "Add new enemy types and boss wave"
git push origin main

git tag -a v1.1.0 -m "Added boss wave and new enemy types"
git push origin v1.1.0

gh release create v1.1.0 \
  --title "Surviving Nightfall v1.1.0 - Boss Update" \
  --notes "
## New Features
- Boss enemy in wave 5
- 2 new enemy types

## Bug Fixes
- Fixed wave progression issue
"
```

## Troubleshooting

### GitHub Action fails to build
1. Check the Actions tab on GitHub
2. Look at the build logs
3. Common issues:
   - Missing dependencies in `pyproject.toml`
   - Asset files not included
   - PyInstaller configuration issues

### Tag already exists
```bash
# Delete and recreate
git tag -d v1.0.0
git push origin --delete v1.0.0
git tag -a v1.0.0 -m "New message"
git push origin v1.0.0
```

### Release doesn't trigger workflow
- Make sure you **created a release**, not just a tag
- Check that `.github/workflows/release.yml` exists
- Verify the workflow file has correct YAML syntax

## Best Practices

1. ✅ **Always test before tagging** - Make sure the game works
2. ✅ **Use annotated tags** - Include release notes in tag message
3. ✅ **Follow semantic versioning** - Makes version history clear
4. ✅ **Write detailed release notes** - Help users understand changes
5. ✅ **Test the built artifacts** - Download and run the packaged game
6. ✅ **Keep a CHANGELOG.md** - Document all changes between versions
7. ✅ **Tag from main branch** - Ensure stable code is released

## Quick Reference

```bash
# Create and push a release tag
git tag -a v1.0.0 -m "Release message"
git push origin v1.0.0

# Create GitHub release (triggers build)
gh release create v1.0.0 --title "Title" --notes "Notes"

# List tags
git tag

# Delete tag
git tag -d v1.0.0
git push origin --delete v1.0.0
```

## Next Steps

After setting up releases:
1. Create a `CHANGELOG.md` to track changes
2. Add pre-release tags for beta versions (e.g., `v1.0.0-beta.1`)
3. Set up automatic changelog generation
4. Consider adding macOS builds to the workflow
5. Add automated testing before builds
