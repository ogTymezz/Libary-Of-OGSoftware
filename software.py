import os
import requests

# List of files to download
downloads = {
    "Norton Commander 5.51": "https://archive.org/download/003064-NortonCommander551/003064_norton_commander.7z",
    "Wolfenstein 3D": "https://archive.org/download/003130-Wolfenstein3d/003130_wolfenstein_3d.7z",
    "Microsoft Windows 3.11": "https://archive.org/download/002961-MicrosoftWindows311/002961_ms_windows_311.7z",
    "Pac-Man (Tiny 10KB)": "https://archive.org/download/000319-PacMan/000319_pac_man.7z",
    "Microsoft QuickBasic 4.5": "https://archive.org/download/003495-MicrosoftQuickbasic45/003495_microsoft_quickbasic.7z",
    "Windows 95 VDI (VirtualBox Image)": "https://archive.org/download/windows_95_vdi/windows_95_vdi.zip",
    "525 DOS Games Collection": "https://archive.org/download/525-dos-games-from-the-1980s-majorgeeks/525%20Dos%20Games.zip",
    "Windows 1.0 IMG": "https://archive.org/download/win-1_202108/WIN1.IMG",
    "Apple Legacy Recovery Disks": "https://archive.org/download/AppleLegacyRecoveryDisks/Legacy%20Recovery.smi.bin",
    "Windows 3.0 Disks (Torrent Archive)": "https://archive.org/download/windows-3.0-disks/windows-3.0-disks_archive.torrent",
}

# Ensure download directory exists
os.makedirs("downloads", exist_ok=True)

def download_file(name, url):
    local_filename = os.path.join("downloads", url.split("/")[-1])
    try:
        print(f"Downloading {name}...")
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f"✅ {name} saved as {local_filename}")
    except Exception as e:
        print(f"❌ Failed to download {name}: {e}")

def main():
    for name, url in downloads.items():
        download_file(name, url)

if __name__ == "__main__":
    main()
