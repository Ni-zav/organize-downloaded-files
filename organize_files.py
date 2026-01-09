#!/usr/bin/env python3
"""
Smart File Organization Script
Organizes files in the Downloads folder into logical categories by file type
Excludes itself and certain critical files from being moved
"""

import os
import shutil
import hashlib
from pathlib import Path
from collections import defaultdict

# Define file categories and their extensions
FILE_CATEGORIES = {
    'Images': ['.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp', '.svg', '.ico', '.tiff'],
    'Videos': ['.mp4', '.webm', '.mov', '.avi', '.mkv', '.wmv', '.flv', '.m4v'],
    'Music': ['.mp3', '.wav', '.aac', '.flac', '.m4a', '.wma', '.ogg'],
    'Documents': ['.pdf', '.docx', '.doc', '.txt', '.md', '.xlsx', '.xls', '.csv', '.pptx', '.ppt', '.odt'],
    'Code': ['.js', '.ts', '.html', '.css', '.java', '.cpp', '.c', '.jsx', '.tsx', '.swift', '.go', '.rs', '.py'],
    'Data': ['.jsonl', '.sql', '.db', '.sqlite'],
    'Compressed': ['.zip', '.rar', '.7z', '.tar', '.gz', '.iso', '.torrent'],
    'Programs': ['.exe', '.msi', '.apk', '.msix'],
    'E-Books': ['.epub', '.mobi', '.azw'],
    'Design': ['.psd', '.ai', '.sketch', '.figma', '.drawio', '.blend', '.glb', '.fbx'],
    'Config': ['.json', '.yaml', '.yml', '.ini', '.toml', '.xml', '.seb', '.ct', '.config'],
    'Notebooks': ['.ipynb'],
}

# Files that should NOT be moved (stay in root)
DONT_MOVE_FILES = {
    'organize_files.py',
    'desktop.ini',
    'Thumbs.db',
    'README.md',
    'ORGANIZATION_SUMMARY.txt',
}

# Existing folders to preserve (don't move these)
PRESERVE_FOLDERS = {
    'Compressed', 'database', 'Documents', 'JetBrains_Mono', 'Music', 
    'Programs', 'Telegram Desktop', 'Videos', 'Images',
    'Code', 'Data', 'E-Books', 'Design', 'Config',
    'Notebooks', 'Others'
}

def get_file_category(file_extension):
    """Determine the category of a file based on its extension"""
    file_extension = file_extension.lower()
    
    for category, extensions in FILE_CATEGORIES.items():
        if file_extension in extensions:
            return category
    
    return 'Others'  # Default category for unknown file types

def should_skip_file(file_path, file_name):
    """Check if a file should be skipped"""
    # Don't move files that are listed in DONT_MOVE_FILES
    if file_name in DONT_MOVE_FILES:
        return True, "script or system file"
    
    # Skip files with no base name (only extension)
    if not Path(file_name).stem or file_name.startswith('.'):
        return False, None  # Will be handled differently
    
    return False, None

def get_file_hash(file_path, chunk_size=8192):
    """Calculate MD5 hash of a file"""
    hash_md5 = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(chunk_size), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except:
        return None

def are_files_identical(file1, file2):
    """Check if two files are identical by comparing hashes"""
    hash1 = get_file_hash(file1)
    hash2 = get_file_hash(file2)
    return hash1 and hash2 and hash1 == hash2

def get_unique_filename(destination_path):
    """
    Generate a unique filename if destination already exists
    Appends (1), (2), etc. before the extension
    """
    if not destination_path.exists():
        return destination_path
    
    stem = destination_path.stem
    suffix = destination_path.suffix
    parent = destination_path.parent
    counter = 1
    
    while True:
        new_name = f"{stem}({counter}){suffix}"
        new_path = parent / new_name
        if not new_path.exists():
            return new_path
        counter += 1

def consolidate_folders(download_path, dry_run=False):
    """
    Consolidate files from old folder names to correct ones
    Archives -> Compressed, Videos (old) -> Videos, Audio -> Music, etc.
    """
    consolidation_map = {
        'Archives': 'Compressed',      # Move .zip etc from Archives to Compressed
        'Audio': 'Music',               # Move audio files from Audio to Music
        'Video': 'Videos',              # Move video files from Video to Videos
    }
    
    print("=" * 70)
    print("CONSOLIDATION PLAN")
    print("=" * 70)
    
    consolidated_count = 0
    
    for old_folder, new_folder in consolidation_map.items():
        old_path = download_path / old_folder
        new_path = download_path / new_folder
        
        if not old_path.exists():
            continue
        
        # Skip if old folder is actually .git
        if old_path.name == '.git':
            continue
        
        print(f"\nMoving files from {old_folder}/ -> {new_folder}/")
        print("-" * 70)
        
        try:
            new_path.mkdir(exist_ok=True)
            
            for item in old_path.iterdir():
                if item.is_file():
                    destination = new_path / item.name
                    
                    if dry_run:
                        if destination.exists():
                            if are_files_identical(item, destination):
                                print(f"  [SKIP] {item.name} (identical duplicate)")
                            else:
                                unique_dest = get_unique_filename(destination)
                                print(f"  [WOULD MOVE] {item.name} -> {unique_dest.name}")
                        else:
                            print(f"  [WOULD MOVE] {item.name}")
                    else:
                        if destination.exists():
                            if are_files_identical(item, destination):
                                item.unlink()
                                print(f"  [DELETED] {item.name} (identical duplicate)")
                            else:
                                unique_dest = get_unique_filename(destination)
                                shutil.move(str(item), str(unique_dest))
                                print(f"  [MOVED] {item.name} -> {unique_dest.name}")
                        else:
                            shutil.move(str(item), str(destination))
                            print(f"  [MOVED] {item.name}")
                        consolidated_count += 1
        except Exception as e:
            print(f"  [ERROR] Failed to consolidate {old_folder}: {str(e)}")
    
    return consolidated_count

def organize_files(download_path, dry_run=False):
    """
    Organize files in the download folder
    
    Args:
        download_path: Path to the Downloads folder
        dry_run: If True, only show what would be done without actually moving files
    """
    download_path = Path(download_path)
    
    if not download_path.exists():
        print(f"Error: Path {download_path} does not exist")
        return
    
    # Track statistics
    stats = defaultdict(int)
    organized_files = defaultdict(list)
    skipped_files = []
    
    print("=" * 70)
    print("FILE ORGANIZATION PLAN")
    print("=" * 70)
    print(f"Target directory: {download_path}")
    print(f"Dry run mode: {dry_run}")
    print()
    
    # Process files in the download folder
    for item in download_path.iterdir():
        # Skip .git folder (git repository)
        if item.is_dir() and item.name == '.git':
            continue
        
        # Skip directories that should be preserved
        if item.is_dir() and item.name in PRESERVE_FOLDERS:
            continue
        
        if item.is_file():
            # Check if file should be skipped
            should_skip, skip_reason = should_skip_file(item, item.name)
            if should_skip:
                print(f"[SKIP] {item.name} ({skip_reason})")
                skipped_files.append(item.name)
                continue
            
            file_extension = item.suffix
            category = get_file_category(file_extension)
            
            # Create category folder path
            category_folder = download_path / category
            destination = category_folder / item.name
            
            organized_files[category].append(item.name)
            stats[category] += 1
            
            # Create the category folder if it doesn't exist
            if not dry_run:
                try:
                    category_folder.mkdir(exist_ok=True)
                    
                    # Handle duplicate files
                    if destination.exists():
                        # Check if files are identical
                        if are_files_identical(item, destination):
                            print(f"[DUPLICATE] {item.name} (identical file exists, skipping)")
                            skipped_files.append(item.name)
                        else:
                            # Files have same name but different content - rename and move
                            unique_dest = get_unique_filename(destination)
                            shutil.move(str(item), str(unique_dest))
                            print(f"[MOVE] {item.name} -> {category}/{unique_dest.name} (renamed)")
                    else:
                        shutil.move(str(item), str(destination))
                        print(f"[MOVE] {item.name} -> {category}/")
                except Exception as e:
                    print(f"[ERROR] {item.name} - {str(e)}")
            else:
                if destination.exists():
                    if are_files_identical(item, destination):
                        print(f"[WOULD SKIP] {item.name} (identical duplicate)")
                    else:
                        unique_dest = get_unique_filename(destination)
                        print(f"[WOULD MOVE] {item.name} -> {category}/{unique_dest.name} (renamed)")
                else:
                    print(f"[WOULD MOVE] {item.name} -> {category}/")
    
    # Print summary
    print()
    print("=" * 70)
    print("ORGANIZATION SUMMARY")
    print("=" * 70)
    
    if organized_files:
        for category, files in sorted(organized_files.items()):
            print(f"\n{category} ({len(files)} files)")
            print("-" * 70)
            if len(files) <= 10:
                for file in files[:10]:
                    print(f"  • {file}")
            else:
                for file in files[:7]:
                    print(f"  • {file}")
                print(f"  ... and {len(files) - 7} more files")
    
    print()
    print("=" * 70)
    print("STATISTICS")
    print("=" * 70)
    total_files = sum(stats.values())
    print(f"Total files organized: {total_files}")
    print(f"Skipped files: {len(skipped_files)}")
    print()
    
    for category, count in sorted(stats.items(), key=lambda x: x[1], reverse=True):
        print(f"  {category:<15} : {count:>3} files")
    
    print()
    if dry_run:
        print("NOTE: This was a dry run. No files were actually moved.")
        print("To perform the actual organization, run with --execute flag")
    else:
        print("Organization complete!")


def main():
    """Main function"""
    import sys
    
    download_path = Path.home() / 'Downloads'
    
    # Check for --execute flag
    execute = '--execute' in sys.argv
    consolidate_only = '--consolidate' in sys.argv
    dry_run = not execute
    
    if consolidate_only:
        print("Running CONSOLIDATION mode")
        if not execute:
            print("(dry-run - add --execute to actually consolidate)")
        print()
        consolidated = consolidate_folders(download_path, dry_run=dry_run)
        print()
        print(f"Total files consolidated: {consolidated}")
        return
    
    if dry_run:
        print("Running in DRY RUN mode (preview only)")
        print("To actually organize files, run: python organize_files.py --execute")
        print("To consolidate old folders, run: python organize_files.py --consolidate --execute")
        print()
    
    organize_files(download_path, dry_run=dry_run)

if __name__ == '__main__':
    main()
