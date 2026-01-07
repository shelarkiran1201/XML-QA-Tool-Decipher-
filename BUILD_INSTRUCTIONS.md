# Survey QA Validator - Build Instructions

This document explains how to use the improved build workflow with icon support and automatic releases.

## 📋 Prerequisites

1. Your GitHub repository with the application code
2. The files from this setup:
   - `build.yml` (place in `.github/workflows/` folder)
   - `app_icon.ico` (place in root of repository)
   - `myapp.py` (your main application file)

## 🎨 Creating Your Application Icon

### Option 1: Use the Icon Generator Script (Recommended)

1. Install Pillow (if not already installed):
   ```bash
   pip install Pillow
   ```

2. Run the icon generator script:
   ```bash
   python create_icon.py
   ```

3. This will create `app_icon.ico` with the following design:
   - Green gradient background
   - White document shape
   - "QA" text in the center
   - Checkmark icon
   - Multiple sizes: 256x256, 128x128, 64x64, 48x48, 32x32, 16x16

### Option 2: Use Your Own Icon

If you want to use a custom icon:

1. Create or download a `.ico` file
2. Name it `app_icon.ico`
3. Place it in the root of your repository

**Icon Requirements:**
- Format: `.ico` (not `.png` or `.jpg`)
- Recommended sizes: 16x16, 32x32, 48x48, 64x64, 128x128, 256x256
- Use online converters if needed: https://convertio.co/png-ico/

### Option 3: No Icon

If you don't want an icon, remove this from `build.yml`:
```yaml
--icon=app_icon.ico
```

## 🚀 Building the EXE

### Method 1: Manual Build (Workflow Dispatch)

1. Go to your GitHub repository
2. Click on **"Actions"** tab
3. Select **"Build and Release EXE"** workflow
4. Click **"Run workflow"** button
5. Select branch (usually `main`)
6. Click green **"Run workflow"** button
7. Wait 1-2 minutes for completion
8. Download artifact from the workflow run

### Method 2: Automatic Release Build (Using Tags)

This method creates a GitHub Release automatically:

1. **Create and push a version tag:**
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

2. **GitHub Actions will automatically:**
   - Build the EXE
   - Create a new Release on GitHub
   - Attach the EXE to the release
   - Generate release notes

3. **View your release:**
   - Go to your repository
   - Click "Releases" (on the right sidebar)
   - Find your new release (e.g., "v1.0.0")
   - Download the EXE file

## 📦 Version Numbering

Follow semantic versioning:
- `v1.0.0` - Major release (breaking changes)
- `v1.1.0` - Minor release (new features)
- `v1.0.1` - Patch release (bug fixes)

Examples:
```bash
# First release
git tag v1.0.0
git push origin v1.0.0

# Bug fix
git tag v1.0.1
git push origin v1.0.1

# New feature
git tag v1.1.0
git push origin v1.1.0

# Major update
git tag v2.0.0
git push origin v2.0.0
```

## 📁 Repository Structure

Your repository should look like this:

```
your-repository/
├── .github/
│   └── workflows/
│       └── build.yml          # GitHub Actions workflow
├── myapp.py                    # Your main application
├── app_icon.ico                # Application icon (optional)
├── create_icon.py              # Icon generator script (optional)
└── README.md                   # This file
```

## 🔧 Customization Options

### Change Application Name

In `build.yml`, modify:
```yaml
--name="SurveyQAValidator"  # Change this to your preferred name
```

### Add More Dependencies

If you add new Python libraries to your app:

1. Install them locally first:
   ```bash
   pip install your-new-library
   ```

2. Add to `build.yml`:
   ```yaml
   - name: Install dependencies
     run: |
       python -m pip install --upgrade pip
       pip install pyinstaller
       pip install python-docx
       pip install pandas
       pip install openpyxl
       pip install your-new-library  # Add here
   ```

3. Add hidden import if needed:
   ```yaml
   --hidden-import=your_new_library
   ```

### Enable Console for Debugging

If you need to see error messages, change in `build.yml`:
```yaml
# FROM:
--windowed

# TO:
--console
```

## ✅ Build Features

Your improved build includes:

- ✅ **No Console Window** - Clean professional appearance
- ✅ **Custom Icon** - Branded application icon
- ✅ **Automatic Releases** - Create releases with version tags
- ✅ **Release Notes** - Auto-generated from commits
- ✅ **All Dependencies** - python-docx, pandas, openpyxl included
- ✅ **Hidden Imports** - All tkinter modules properly bundled
- ✅ **Artifact Upload** - Always available even without tags

## 🐛 Troubleshooting

### Issue: Icon not showing
- Make sure `app_icon.ico` is in the root of your repository
- Check the file is actually `.ico` format (not renamed `.png`)
- Rebuild the EXE

### Issue: EXE crashes on startup
- Temporarily change `--windowed` to `--console` in build.yml
- Run the EXE and check error messages
- Ensure all required libraries are in the install dependencies step

### Issue: Release not created
- Make sure your tag starts with 'v' (e.g., `v1.0.0`)
- Check GitHub Actions permissions (Settings → Actions → Workflow permissions)
- Ensure "Read and write permissions" is enabled

### Issue: Build fails
- Check the Actions tab for error logs
- Verify all files are committed (myapp.py, app_icon.ico)
- Make sure file names match exactly

## 📝 Next Steps

1. **Upload the icon generator script** (`create_icon.py`) to your repository
2. **Run it locally** to generate `app_icon.ico`
3. **Commit both files** to your repository:
   ```bash
   git add app_icon.ico create_icon.py
   git commit -m "Add application icon"
   git push
   ```
4. **Replace your current** `build.yml` with the improved version
5. **Create your first release:**
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

## 🎉 Success!

After following these steps, you'll have:
- A professional-looking application with a custom icon
- Automatic builds triggered by version tags
- GitHub Releases with attached EXE files
- Easy distribution to users

---

**Need help?** Check the GitHub Actions logs for detailed error messages.
