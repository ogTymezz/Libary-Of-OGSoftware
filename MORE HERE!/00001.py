import os
import requests
from tqdm import tqdm
import threading
from queue import Queue

# Download list
downloads = {
    "Windows 1.0 IMG": "https://archive.org/download/win-1_202108/WIN1.IMG",
    "Windows 3.1 Full": "https://archive.org/download/002961-MicrosoftWindows311/002961_ms_windows_311.7z",
    "Windows 95 VDI": "https://archive.org/download/windows_95_vdi/windows_95_vdi.zip",
    "Windows 98 Bootable ISO": "https://archive.org/download/Win98SE_201912/Win98SE.iso",
    "Mac OS 7.5.3": "https://archive.org/download/mac_7.5.3/mac_7.5.3.smi.bin",
    "Ubuntu 4.10 Warty": "https://archive.org/download/ubuntu-4.10/ubuntu-4.10-install-i386.iso",
    "MS-DOS 6.22 Floppy Set": "https://archive.org/download/msdos622/MS-DOS-6.22.zip",
    "Microsoft QuickBasic 4.5": "https://archive.org/download/003495-MicrosoftQuickbasic45/003495_microsoft_quickbasic.7z",
    "Visual Basic 6.0": "https://archive.org/download/visual-basic-6-0/Visual_Basic_6.0_Professional.iso",
    "AutoCAD R12 for DOS": "https://archive.org/download/AutoCADRelease12ForDos/AutoCAD_R12_DOS.7z",
    "Adobe Photoshop 1.0 Mac": "https://archive.org/download/Photoshop1.0/Photoshop1.0.img",
    "Norton Commander 5.51": "https://archive.org/download/003064-NortonCommander551/003064_norton_commander.7z",
    "Wolfenstein 3D Full": "https://archive.org/download/003130-Wolfenstein3d/003130_wolfenstein_3d.7z",
    "DOOM Shareware 1.9": "https://archive.org/download/DoomShareware1993/Doom1_1.9_shareware.zip",
    "Pac-Man (DOS Tiny 10KB)": "https://archive.org/download/000319-PacMan/000319_pac_man.7z",
    "525 DOS Games Collection": "https://archive.org/download/525-dos-games-from-the-1980s-majorgeeks/525%20Dos%20Games.zip",
    "Commander Keen Complete": "https://archive.org/download/commanderkeenall/Commander_Keen_All.7z",
    "Roblox 2006 Client Archive": "https://archive.org/download/roblox-2006-client/Roblox-2006-Client.zip",
    "SimCity Classic (DOS)": "https://archive.org/download/simcity_dos/simcity_dos.zip",
    "The Oregon Trail (DOS)": "https://archive.org/download/oregontrail/Oregon_Trail_DOS.zip",
    "NCSA Mosaic Browser 1.0": "https://archive.org/download/NCSA-Mosaic-1.0/NCSA_Mosaic_1.0.zip",
    "AOL 3.0 Installer": "https://archive.org/download/AOL_3_Installer/AOL_3_Installer.zip",
    "Apple Legacy Recovery Disks": "https://archive.org/download/AppleLegacyRecoveryDisks/Legacy%20Recovery.smi.bin",
    "Windows 3.0 Disk Set (Torrent)": "https://archive.org/download/windows-3.0-disks/windows-3.0-disks_archive.torrent",
}

# Ensure download directory exists
os.makedirs("downloads", exist_ok=True)

# Create a queue
q = Queue()

# Worker function
def worker():
    while not q.empty():
        name, url = q.get()
        try:
            download_file(name, url)
        except Exception as e:
            print(f"❌ Error downloading {name}: {e}")
        q.task_done()

# Main download function (auto-resume)
def download_file(name, url):
    local_filename = os.path.join("downloads", url.split("/")[-1])
    temp_filename = local_filename + ".part"

    # Request HEAD first to get total size
    with requests.head(url) as r:
        total_size = int(r.headers.get('content-length', 0))

    # Check if partially downloaded
    downloaded_size = 0
    if os.path.exists(temp_filename):
        downloaded_size = os.path.getsize(temp_filename)

    if downloaded_size >= total_size:
        # File is already complete, rename it
        os.rename(temp_filename, local_filename)
        print(f"⚡ {name} already fully downloaded.")
        return

    headers = {"Range": f"bytes={downloaded_size}-"}

    print(f"\n⬇️ Downloading {name}...")
    with requests.get(url, headers=headers, stream=True) as r:
        r.raise_for_status()
        mode = 'ab' if downloaded_size > 0 else 'wb'
        with open(temp_filename, mode) as f, tqdm(
            initial=downloaded_size,
            total=total_size,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
            desc=name[:30]
        ) as bar:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    bar.update(len(chunk))
    
    os.rename(temp_filename, local_filename)
    print(f"✅ {name} saved as {local_filename}")

# Main function
def main():
    # Fill the queue
    for name, url in downloads.items():
        q.put((name, url))

    # Start 2 threads
    threads = []
    for _ in range(2):
        t = threading.Thread(target=worker)
        t.start()
        threads.append(t)

    # Wait for threads to finish
    q.join()
    for t in threads:
        t.join()

    print("\n🎉 All downloads complete!")

if __name__ == "__main__":
    main()
