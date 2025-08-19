
````markdown
# Py2Deb

**Py2Deb** is a Python utility designed to automatically package Python scripts into Debian (`.deb`) packages. It simplifies the process of creating installable Debian packages by detecting dependencies, generating the package structure, and optionally creating an installer script and compressed archive.

---

## Features

- Package any Python script as a `.deb` file.
- Automatically detect Python dependencies and map them to Debian packages.
- Optionally create an `install.sh` setup script.
- Optionally create a `.tar.gz` archive containing the DEB and setup script.
- Colorful CLI output with informative messages and usage examples.

---

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/py2deb.git
cd py2deb
````

Run the tool directly:

```bash
py2deb <python_file> -cn "Avi Twil" --command <command_name> [options]
```

---

## Usage

```bash
py2deb myscript.py -cn "Avi Twil" --command mycmd --sudo --setup --tar-gz
```

### Options:

* `<python_file>` : Python file to package (required)
* `-cn <creator_name>` : Name of the package creator (required)
* `--command <name>` : Name of the installed executable command (required)
* `--sudo` : Add `sudo` as a package dependency
* `--setup` : Generate an `install.sh` setup script alongside the DEB
* `--tar-gz` : Create a tar.gz archive containing DEB and setup script
* `-h, --help` : Show help message and exit

---

## How It Works

1. Reads your Python script to detect imported modules.
2. Maps known Python modules to Debian packages for dependencies.
3. Creates the DEB package structure and `control` file automatically.
4. Copies your Python script to `/usr/local/bin` and makes it executable.
5. Optionally generates a setup script and/or tar.gz archive containing the package.

---

## Examples

Create a DEB package with all options:

```bash
py2deb myscript.py -cn "Avi Twil" --command mycmd --sudo --setup --tar-gz
```

Create a simple DEB without installer or archive:

```bash
py2deb myscript.py -cn "Avi Twil" --command mycmd
```

---

## Author

**Avi Twil**
Twil Industries

---

## License

This project is licensed under the MIT License.

```


