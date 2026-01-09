# Downloads Folder Organizer

A smart Python script to automatically organize your Downloads folder by file type with intelligent duplicate detection and conflict handling.

## Features

✨ **Smart Organization**
- Automatically categorizes files by extension
- Creates logical folder structure
- Handles edge cases (files with no names, special characters, etc.)

🔍 **Duplicate Detection**
- Identifies identical files using MD5 hash comparison
- Automatically skips duplicate copies
- Prevents data loss

⚡ **Conflict Resolution**
- Auto-renames conflicting files with incrementing numbers
- Example: `document.pdf` → `document(1).pdf`
- Safely handles all overwrites

🔒 **Safety Features**
- Protects system files and script itself
- Dry-run mode for preview before execution
- Safe folder consolidation

## Installation

No additional dependencies required. Uses only Python standard library:
- `pathlib` - File path handling
- `shutil` - File operations
- `hashlib` - MD5 hashing for duplicates

## Usage

### Preview Mode (Dry Run)
See what would be organized without making changes:
```bash
python organize_files.py
```

### Execute Organization
Actually organize the files:
```bash
python organize_files.py --execute
```

### Consolidate Old Folders (Optional)
Move files from old folder names to correct ones (Archives→Compressed, Audio→Music, Video→Videos):
```bash
# Preview consolidation
python organize_files.py --consolidate

# Execute consolidation
python organize_files.py --consolidate --execute
```

## File Categories

The script organizes files into these categories:

| Category | File Types |
|----------|-----------|
| **Images** | `.png`, `.jpg`, `.jpeg`, `.gif`, `.webp`, `.bmp`, `.svg`, `.ico`, `.tiff` |
| **Videos** | `.mp4`, `.webm`, `.mov`, `.avi`, `.mkv`, `.wmv`, `.flv`, `.m4v` |
| **Music** | `.mp3`, `.wav`, `.aac`, `.flac`, `.m4a`, `.wma`, `.ogg` |
| **Documents** | `.pdf`, `.docx`, `.doc`, `.txt`, `.md`, `.xlsx`, `.xls`, `.csv`, `.pptx`, `.ppt`, `.odt` |
| **Code** | `.js`, `.ts`, `.html`, `.css`, `.java`, `.cpp`, `.c`, `.jsx`, `.tsx`, `.swift`, `.go`, `.rs`, `.py` |
| **Data** | `.jsonl`, `.sql`, `.db`, `.sqlite` |
| **Compressed** | `.zip`, `.rar`, `.7z`, `.tar`, `.gz`, `.iso`, `.torrent` |
| **Programs** | `.exe`, `.msi`, `.apk`, `.msix` |
| **E-Books** | `.epub`, `.mobi`, `.azw` |
| **Design** | `.psd`, `.ai`, `.sketch`, `.figma`, `.drawio`, `.blend`, `.glb`, `.fbx` |
| **Config** | `.json`, `.yaml`, `.yml`, `.ini`, `.toml`, `.xml`, `.seb`, `.ct`, `.config` |
| **Notebooks** | `.ipynb` |
| **Others** | All other file types |

## How It Works

1. **Scans** your Downloads folder for all files
2. **Categorizes** each file based on its extension
3. **Detects** duplicates using hash comparison
4. **Creates** category folders if they don't exist
5. **Moves** files to appropriate folders
6. **Handles** naming conflicts automatically
7. **Reports** detailed statistics

## Smart Features in Action

### Duplicate Detection
```
File: document.pdf
Existing: document.pdf (identical content)
Action: Skip (duplicate detected)
```

### Conflict Resolution
```
File: song.mp3
Existing: song.mp3 (different content)
Action: Move as song(1).mp3
```

### Safe Defaults
- `organize_files.py` - Never moved (stays in root)
- `desktop.ini` - Never moved (Windows system file)
- `Thumbs.db` - Never moved (Windows system file)

## Example Output

```
======================================================================
FILE ORGANIZATION PLAN
======================================================================
Target directory: C:\Users\USER\Downloads
Dry run mode: False

[MOVE] vacation.jpg → Images/
[MOVE] movie.mp4 → Videos/
[MOVE] song.mp3 → Music/
[DUPLICATE] duplicate_file.pdf (identical file exists, skipping)
[MOVE] document.zip → Compressed/

======================================================================
STATISTICS
======================================================================
Total files organized: 4
Skipped files: 1

  Images      :   1 files
  Videos      :   1 files
  Music       :   1 files
  Compressed  :   1 files
```

## Preserved Folders

These folders won't be reorganized and are preserved as-is:
- `database/`
- `Documents/`
- `JetBrains_Mono/`
- `Programs/`
- `Telegram Desktop/`
- Any existing category folders (Images, Videos, Music, etc.)

## Troubleshooting

### Unicode/Encoding Errors
Some filenames with special characters may cause issues. The script safely skips these and reports them.

### Permission Denied
Ensure no files are open in other applications before running the organizer.

### Files Not Moving
Check:
1. File is not listed in `DONT_MOVE_FILES`
2. No permission issues
3. Destination folder exists and is writable

## Performance

- Fast: Processes hundreds of files in seconds
- Efficient: Hash comparison only done when needed
- Safe: No files deleted, only moved

## Future Enhancements

Potential features for future versions:
- [ ] Config file for custom categories
- [ ] Recursive organization (subfolders)
- [ ] Undo functionality
- [ ] Age-based organization
- [ ] Size-based filtering

## License

Free to use and modify.

## Notes

- Always run in preview mode first (`python organize_files.py`)
- Backup important files before first run
- Check the console output for any warnings
- Empty old folders are automatically removed
- Identical duplicates are safely deleted

---

**Version 1.0** - Smart file organizer with duplicate detection and conflict handling
