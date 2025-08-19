#!/usr/bin/env python3
import os, sys, argparse, shutil, re, subprocess
from pathlib import Path
from colorama import Fore, init
import pyfiglet
import tarfile

init(autoreset=True)

DEBIAN_PACKAGE_MAP = {
    "requests": "python3-requests",
    "bs4": "python3-bs4",
    "beautifulsoup4": "python3-bs4",
    "PIL": "python3-pil",
    "Pillow": "python3-pil",
    "numpy": "python3-numpy",
    "pandas": "python3-pandas",
    "matplotlib": "python3-matplotlib",
    "scipy": "python3-scipy",
    "flask": "python3-flask",
    "django": "python3-django",
    "pyyaml": "python3-yaml",
    "cryptography": "python3-cryptography",
    "colorama": "python3-colorama",
    "pyfiglet": "python3-pyfiglet",
    "pytest": "python3-pytest",
    "sqlalchemy": "python3-sqlalchemy",
    "lxml": "python3-lxml"
}

BUILTIN_MODULES = {
    "sys","os","shutil","subprocess","argparse","pathlib",
    "re","tarfile","time","math","json","logging","glob","io"
}

def print_logo():
    print(Fore.BLUE + pyfiglet.figlet_format("Twil-Industries", font="slant"))
    print(Fore.CYAN + "================= Presents to you =================\n")
    print(Fore.RED + pyfiglet.figlet_format(" Py2Deb ", font="slant"))
    print(Fore.GREEN + "================= Avi Twil (c) =================\n")

def help_menu():
    print(Fore.YELLOW + "USAGE: " + Fore.CYAN +
          "py2deb <python_file> -cn <creator_name> -email <creator_email> --command <command_name> [options]\n")
    print(Fore.MAGENTA + "Options:")
    print(Fore.YELLOW + "  <python_file>         " + Fore.WHITE + "Python file to package (required)")
    print(Fore.YELLOW + "  -cn <creator_name>    " + Fore.WHITE + "Name of the package creator (required)")
    print(Fore.YELLOW + "  -email <creator_email>" + Fore.WHITE + "Email of the creator (required)")
    print(Fore.YELLOW + "  --command <name>      " + Fore.WHITE + "Command name for the installed executable (required)")
    print(Fore.YELLOW + "  --sudo                " + Fore.WHITE + "Add 'sudo' to package dependencies")
    print(Fore.YELLOW + "  --setup               " + Fore.WHITE + "Create a setup script alongside the DEB")
    print(Fore.YELLOW + "  --tar-gz              " + Fore.WHITE + "Create a tar.gz archive containing DEB and setup script")
    print(Fore.YELLOW + "  -h, --help            " + Fore.WHITE + "Show this help message and exit\n")
    print(Fore.GREEN + "EXAMPLES:")
    print(Fore.CYAN + "  py2deb myscript.py -cn 'Avi Twil' -email 'avi@example.com' --command mycmd --sudo --setup --tar-gz")
    print(Fore.CYAN + "  py2deb py2deb.py -cn 'Avi Twil' -email 'avi@example.com' --command py2deb\n")

def parse_python_dependencies(py_file):
    deps = set()
    with open(py_file, "r") as f:
        for line in f:
            line = line.strip()
            m1 = re.match(r"import\s+([a-zA-Z0-9_]+)", line)
            m2 = re.match(r"from\s+([a-zA-Z0-9_]+)\s+import", line)
            for m in (m1, m2):
                if m:
                    mod = m.group(1)
                    if mod not in BUILTIN_MODULES:
                        deps.add(mod)
    return sorted(deps)

def create_deb_structure(app_name):
    build_dir = Path(f"{app_name}_deb_build")
    if build_dir.exists():
        shutil.rmtree(build_dir)
    (build_dir / "DEBIAN").mkdir(parents=True)
    (build_dir / "usr/local/bin").mkdir(parents=True)
    return build_dir

def write_control_file(build_dir, app_name, author, email, sudo_required, deps):
    all_deps = []
    if sudo_required:
        all_deps.append("sudo")
    for dep in deps:
        all_deps.append(DEBIAN_PACKAGE_MAP.get(dep, f"python3-{dep}"))
    control_text = f"""Package: {app_name}
Version: 1.0
Section: base
Priority: optional
Architecture: all
Maintainer: {author} <{email}>
Description: Auto generated DEB package
"""
    if all_deps:
        control_text += "Depends: " + ", ".join(all_deps) + "\n"
    (build_dir / "DEBIAN/control").write_text(control_text)

def copy_python_file(build_dir, py_file, app_name):
    target_path = build_dir / "usr/local/bin" / app_name
    shutil.copy(py_file, target_path)
    target_path.chmod(0o755)
    return target_path

def create_tar_gz(deb_file, setup_script):
    tar_name = f"{deb_file.stem}.tar.gz"
    with tarfile.open(tar_name,"w:gz") as tar:
        tar.add(deb_file)
        if setup_script:
            tar.add(setup_script)
    print(f"Created tar.gz: {tar_name}")

def explain_tool():
    """
    Print a detailed explanation of the Py2Deb tool.
    """
    print(Fore.CYAN + "\n===== About Py2Deb =====\n")
    print(Fore.YELLOW + "Py2Deb is a utility to automatically create Debian (.deb) packages from Python scripts.\n")
    print(Fore.GREEN + "Purpose:")
    print(Fore.WHITE + "- Package any Python script as a .deb file.")
    print(Fore.WHITE + "- Automatically detect Python dependencies and map them to Debian packages.")
    print(Fore.WHITE + "- Optionally create a setup installation script and a tar.gz archive.\n")

    print(Fore.GREEN + "How it works:")
    print(Fore.WHITE + "1. Reads your Python script to detect imported modules.")
    print(Fore.WHITE + "2. Maps known modules to Debian packages, adds them as dependencies.")
    print(Fore.WHITE + "3. Creates the DEB package structure and control file automatically.")
    print(Fore.WHITE + "4. Copies your Python script to /usr/local/bin and makes it executable.")
    print(Fore.WHITE + "5. Optionally creates a setup script and/or tar.gz archive containing the package.\n")

    print(Fore.GREEN + "Key options:")
    print(Fore.WHITE + "-cn <creator_name>     Specify the creator of the package")
    print(Fore.WHITE + "-email <creator_email> Specify creator email")
    print(Fore.WHITE + "--command <name>      Name of the executable command after installation")
    print(Fore.WHITE + "--sudo                 Add sudo as a package dependency")
    print(Fore.WHITE + "--setup                Generate an install.sh setup script")
    print(Fore.WHITE + "--tar-gz               Create a tar.gz containing DEB and setup script\n")
    print(Fore.WHITE + "-h , --help               load help menu\n")

    print(Fore.CYAN + "Example:")
    print(
        Fore.WHITE + "  py2deb myscript.py -cn 'Avi Twil' -email 'avi@example.com' --command mycmd --sudo --setup --tar-gz\n")

    print(
        Fore.MAGENTA + "Created by " + Fore.YELLOW + "Avi Twil " + Fore.MAGENTA + "from " + Fore.CYAN + "Twil Industries\n")

def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("file", nargs="?")
    parser.add_argument("-cn", "--creator_name", help="Creator name")
    parser.add_argument("-email", "--creator_email", help="Creator email")
    parser.add_argument("--command", help="Command name for executable")
    parser.add_argument("--sudo", action="store_true", help="Add sudo dependency")
    parser.add_argument("--setup", action="store_true", help="Create setup script")
    parser.add_argument("--tar-gz", action="store_true", help="Create tar.gz archive")
    parser.add_argument("-h", "--help", action="store_true", help="Show help menu")
    args = parser.parse_args()

    if len(sys.argv)==1:
        print_logo()
        explain_tool()
        sys.exit(1)

    if args.help:
        print_logo()
        help_menu()
        sys.exit(1)

    print_logo()
    py_file = Path(args.file)

    if not args.file:
        print(Fore.RED + "Error: missing Python file to package\n")
        help_menu()
        sys.exit(1)

    if not args.command:
        print(Fore.RED + "Error: you must insert command name using " +
              Fore.CYAN + "--command <name>\n")
        help_menu()
        sys.exit(1)

    if not args.creator_name:
        args.creator_name = "Unknown Creator"
        print(Fore.YELLOW + f"Warning: no creator name provided, using default: {Fore.CYAN}{args.creator_name}")

    if not args.creator_email:
        args.creator_email = "unknown@example.com"
        print(Fore.YELLOW + f"Warning: no creator email provided, using default: {Fore.CYAN}{args.creator_email}")

    if not py_file.exists():
        print("Python file does not exist.")
        sys.exit(1)

    app_name = args.command
    deps = parse_python_dependencies(py_file)
    print(f"Detected dependencies: {deps}")

    build_dir = create_deb_structure(app_name)
    write_control_file(build_dir, app_name, args.creator_name, args.creator_email, args.sudo, deps)
    copy_python_file(build_dir, py_file, app_name)

    # יצירת DEB בקובץ חיצוני (ליד הסקריפט)
    deb_file = Path(f"{app_name}.deb")
    subprocess.run(["dpkg-deb", "--build", str(build_dir), str(deb_file)], check=True)
    print(f"DEB package created: {deb_file}")

    # יצירת install.sh באותה תיקייה כמו ה-DEB
    setup_script = None
    if args.setup:
        setup_script = deb_file.parent / "install.sh"
        setup_script.write_text(f"""#!/bin/bash
echo "Installing package..."
sudo dpkg -i {deb_file.name}
""")
        setup_script.chmod(0o755)
        print(f"Setup script created: {setup_script}")

    # יצירת tar.gz אם נבחר
    if args.tar_gz:
        create_tar_gz(deb_file, setup_script)

if __name__=="__main__":
    main()
