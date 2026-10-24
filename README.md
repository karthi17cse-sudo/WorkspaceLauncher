# 🚀 Workspace Launcher

A Windows desktop application built with Python and CustomTkinter to organize and launch applications through customizable workspaces.

## Features

* Discover installed Windows applications.
* Search for applications.
* Add and remove applications from workspaces.
* Create, rename, and delete workspaces.
* Launch selected applications with one click.
* Extract icons from supported Windows shortcuts.
* Save workspace configurations locally.
* Modern graphical interface using CustomTkinter.

## Technologies

* Python
* CustomTkinter
* Pillow
* Tkinter
* Windows application shortcuts
* JSON

## Requirements

* Windows 10 or Windows 11
* Python 3.11 or a compatible version
* The packages listed in `requirements.txt`

## Installation

### 1. Clone the repository

```bash
git clone YOUR_REPOSITORY_URL
```

Replace `YOUR_REPOSITORY_URL` with your GitHub repository URL.

### 2. Open the project directory

```bash
cd WorkspaceLauncher
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Run the application

```bash
python main.py
```

## Usage

1. Open Workspace Launcher.
2. Select a workspace.
3. Click **Add Application**.
4. Search for an installed application.
5. Add the application to your workspace.
6. Select the applications you want to launch.
7. Click **Launch Workspace**.

You can create separate workspaces for studying, programming, and other activities.

## Project Structure

```text
WorkspaceLauncher/
├── main.py
├── ui.py
├── app_selector.py
├── launcher.py
├── icons.py
├── config.py
├── config.example.json
├── requirements.txt
├── README.md
├── .gitignore
└── WorkspaceLauncher.spec
```

## Configuration

The application stores workspace settings in a local `config.json` file.

The repository provides `config.example.json` as an example of the default configuration format.

## Platform Compatibility

This application is designed for Windows because application discovery, shortcut launching, and icon extraction use Windows-specific functionality.

## License

No license has been selected yet. Add a license before explicitly permitting others to reuse, modify, or distribute the project.
