import os
import subprocess

VOICE_DIR = "../game/voice/"
RHUBARB_PATH = "rhubarb.exe"

REPLACE_ALL = False


def ogg_files(root_dir: str):
	for dirpath, _, filenames in os.walk(root_dir):
		for filename in filenames:
			if filename.lower().endswith(".ogg"):
				yield os.path.join(dirpath, filename)


def get_lipsync_path(ogg_path: str) -> str:
	base, _ = os.path.splitext(ogg_path)
	return f"{base}.json"


# set cwd to script directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

voice_dir = os.path.normpath(VOICE_DIR)
if not os.path.isdir(voice_dir):
    raise FileNotFoundError(f"VOICE_DIR not found!")

for ogg_path in ogg_files(voice_dir):
    lipsync_path = get_lipsync_path(ogg_path)
    if not REPLACE_ALL and os.path.exists(lipsync_path):
        continue

    command = [
        RHUBARB_PATH,
        "-f",
        "json",
        "-o",
        lipsync_path,
        ogg_path,
    ]
    subprocess.run(command, check=True)
