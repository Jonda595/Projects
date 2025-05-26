from colorama import init, Fore, Style
import json
import os
import platform
import shutil
import subprocess
import sys
import time

sys.dont_write_bytecode = True

def compute_speed(size: float, start: float, end: float) -> float :
    elapsed_time = end - start
    return(size / elapsed_time)

init()

system = platform.system()
if system == "Windows":
    data_path = os.path.join(os.path.dirname(__file__), "drip_data")
    os.makedirs(data_path, exist_ok=True)
    subprocess.run(["attrib", "+h", data_path])
elif system == "Linux" or "Darwin":
    data_path = os.path.join(os.path.dirname(__file__), ".drip_data")
    os.makedirs(data_path, exist_ok=True)


print("Type drive: Example: A:")
drive = input('')

if bool(drive.strip()) == True :
    if not drive.endswith(":"):
        print(f"{Fore.RED}Type it with a colon!{Style.RESET_ALL}")
        sys.exit()
else:
    print(f"{Fore.RED}You didn't typed anything!{Style.RESET_ALL}")
    sys.exit()

file_path = "/drip_perf_test/test_file.bin"
file_path = drive + file_path

print("Type the size of the file in megabytes:")
lfsize = float(input(''))

#if lfsize == float("") :
#    print(f"{Fore.RED}You didn't typed anything!{Style.RESET_ALL}")
#    sys.exit()

print("Testing large file write performance...")
folder_path = f"{drive}/drip_perf_test"
os.makedirs(folder_path, exist_ok=True)

start = time.time()
with open(file_path, "wb") as f:
    f.write(b"\x00" * int(lfsize * 1024 * 1024))
end = time.time()

lfwt = f"{(end - start):.2f}"
lfws = (f"{compute_speed(lfsize, start, end):.2f}")
print(f"Large file {Fore.RED}write {Fore.BLUE}time: {Fore.GREEN}{lfwt} seconds{Style.RESET_ALL}")
print(f"Large file {Fore.RED}write {Fore.BLUE}speed: {Fore.GREEN}{lfws} MB/s{Style.RESET_ALL}")

print("Testing large file read perfomance...")
start = time.time()
with open(file_path, "r", encoding="utf-8") as f:
    obsah = f.read()
end = time.time()

lfrt = f"{(end - start):.2f}"
lfrs = (f"{compute_speed(lfsize, start, end):.2f}")
print(f"Large file {Fore.RED}read {Fore.BLUE}time: {Fore.GREEN}{lfrt} seconds{Style.RESET_ALL}")
print(f"Large file {Fore.RED}read {Fore.BLUE}speed: {Fore.GREEN}{lfrs} MB/s{Style.RESET_ALL}")

print("Testing large file delete perfomance...")
start = time.time()
shutil.rmtree(file_path.replace("/test_file.bin", ""))
end = time.time()

lfdt = f"{(end - start):.2f}"
try:
    lfds = (f"{compute_speed(lfsize, start, end):.2f}")
except:
    print(f"{Fore.RED}Error while computing speed. Try again.{Style.RESET_ALL}")
print(f"Large file {Fore.RED}delete {Fore.BLUE}time: {Fore.GREEN}{lfdt} seconds{Style.RESET_ALL}")
print(f"Large file {Fore.RED}delete {Fore.BLUE}speed: {Fore.GREEN}{lfds} MB/s{Style.RESET_ALL}")

data = {
    "lfsize": lfsize,
    "lfwt": lfwt,
    "lfws": lfws,
    "lfrt": lfrt,
    "lfrs": lfrs,
    "lfdt": lfdt,
    "lfds": lfds
}

print(f"\n{Fore.MAGENTA}History:{Style.RESET_ALL}")

try:
    with open("drip_data/history.json", "r", encoding="utf-8") as f:
        loaded_data = json.load(f)
    loaded_lfsize = loaded_data.get("lfsize", "None")
    loaded_lfwt = loaded_data.get("lfwt", "None")
    loaded_lfws = loaded_data.get("lfws", "None")
    loaded_lfrt = loaded_data.get("lfrt", "None")
    loaded_lfrs = loaded_data.get("lfrs", "None")
    loaded_lfdt = loaded_data.get("lfdt", "None")
    loaded_lfds = loaded_data.get("lfds", "None")
    print(f"Last time large file {Fore.RED}write {Fore.BLUE}time: {Fore.GREEN}{loaded_lfwt} seconds{Style.RESET_ALL}")
    print(f"Last time large file {Fore.RED}write {Fore.BLUE}speed: {Fore.GREEN}{loaded_lfws} MB/s{Style.RESET_ALL}")
    print(f"Last time large file {Fore.RED}read {Fore.BLUE}time: {Fore.GREEN}{loaded_lfrt} seconds{Style.RESET_ALL}")
    print(f"Last time large file {Fore.RED}read {Fore.BLUE}speed: {Fore.GREEN}{loaded_lfrs} MB/s{Style.RESET_ALL}")
    print(f"Last time large file {Fore.RED}delete {Fore.BLUE}time: {Fore.GREEN}{loaded_lfdt} seconds{Style.RESET_ALL}")
    print(f"Last time large file {Fore.RED}delete {Fore.BLUE}speed: {Fore.GREEN}{loaded_lfds} MB/s{Style.RESET_ALL}")
except:
    print("No history found. Run this again to show history.")

with open("drip_data/history.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)
