import re
from pathlib import Path

def find_dll_dependencies(file_path: str | Path):

    target = Path(file_path)
    if not target.exists():
        print(f"Cannot find {target}")
        return

    print(f"Checking for DLL: {target.name} ({target.stat().st_size / 1024 / 1024:.2f} MB)")

    try:
        
        with open(target, "rb") as f:
            binary_data = f.read()

        pattern = re.compile(rb'[A-Za-z0-9_-]+\.dll', re.IGNORECASE)
        
        matches = set(pattern.findall(binary_data))

        dll_list = sorted([m.decode('ascii') for m in matches])

        print(f"Found DLL references in {target.name}:")

        for dll in dll_list:
            print(f"  - {dll}")

    except Exception as e:
        print(f"[Error] Raised Exception {e} when analyzing {target.name}")


if __name__ == "__main__":
    pth = Path(r'C:\Developer\NVIDIA\cutlass\4.4.1\bin')
    dlls = list(pth.glob("cutlass.*dll"))

    for dll in dlls:
        find_dll_dependencies(dll)