import customtkinter as ctk
import os
import subprocess
import json
import threading

from icons import extract_icon
from PIL import Image


# =========================================================
# Application cache
# =========================================================

_APPLICATION_CACHE = None


# =========================================================
# Find installed applications
# =========================================================

def find_applications():

    global _APPLICATION_CACHE

    # Return cached results if already scanned
    if _APPLICATION_CACHE is not None:
        return _APPLICATION_CACHE

    apps = []

    # =====================================================
    # 1. Traditional Windows applications (.lnk)
    # =====================================================

    folders = [
        os.path.expandvars(
            r"%APPDATA%\Microsoft\Windows\Start Menu\Programs"
        ),
        os.path.expandvars(
            r"%ProgramData%\Microsoft\Windows\Start Menu\Programs"
        )
    ]

    for folder in folders:

        if not os.path.exists(folder):
            continue

        for root, dirs, files in os.walk(folder):

            for file in files:

                if not file.lower().endswith(".lnk"):
                    continue

                name = os.path.splitext(file)[0]

                path = os.path.join(
                    root,
                    file
                )

                apps.append({
                    "name": name,
                    "path": path,
                    "type": "shortcut"
                })


    # =====================================================
    # 2. Microsoft Store / Windows applications
    # =====================================================

    try:

        command = [
            "powershell",
            "-NoProfile",
            "-Command",
            "Get-StartApps | "
            "Select-Object Name, AppID | "
            "ConvertTo-Json -Compress"
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        )

        if (
            result.returncode == 0
            and result.stdout.strip()
        ):

            store_apps = json.loads(
                result.stdout
            )

            if isinstance(store_apps, dict):
                store_apps = [store_apps]

            for store_app in store_apps:

                name = store_app.get("Name")
                app_id = store_app.get("AppID")

                if not name or not app_id:
                    continue

                already_exists = any(
                    existing["name"].lower()
                    == name.lower()
                    for existing in apps
                )

                if already_exists:
                    continue

                apps.append({
                    "name": name,
                    "path": "shell:AppsFolder\\" + app_id,
                    "type": "store"
                })

    except Exception as error:

        print(
            "Could not scan Windows applications:",
            error
        )


    # =====================================================
    # 3. Remove duplicates
    # =====================================================

    unique_apps = {}

    for app in apps:

        key = app["name"].strip().lower()

        if key not in unique_apps:
            unique_apps[key] = app


    # =====================================================
    # 4. Sort
    # =====================================================

    _APPLICATION_CACHE = sorted(
        unique_apps.values(),
        key=lambda x: x["name"].lower()
    )

    return _APPLICATION_CACHE


# =========================================================
# Get cached application icon
# =========================================================

def get_application_icon(app):

    # Already loaded
    if "icon_image" in app:
        return app["icon_image"]


    # Microsoft Store apps are handled separately
    if app.get("type") == "store":

        app["icon_image"] = None

        return None


    icon_path = os.path.join(
        "icons",
        app["name"].replace(" ", "_") + ".png"
    )


    # -----------------------------------------------------
    # Existing icon
    # -----------------------------------------------------

    if os.path.exists(icon_path):

        try:

            image = Image.open(
                icon_path
            )

            icon_image = ctk.CTkImage(
                light_image=image,
                dark_image=image,
                size=(28, 28)
            )

            app["icon_image"] = icon_image

            return icon_image

        except Exception as error:

            print(
                "Could not load icon:",
                error
            )


    # Don't extract missing icons here.
    # They will be loaded in the background.
    return None


# =========================================================
# Application selector
# =========================================================

def show_application_selector(parent, on_select):

    selector_window = ctk.CTkToplevel(
        parent
    )

    selector_window.title(
        "Add Application"
    )

    selector_window.geometry(
        "500x600"
    )

    selector_window.minsize(
        400,
        500
    )

    selector_window.transient(
        parent
    )

    selector_window.grab_set()


    # =====================================================
    # Header
    # =====================================================

    header = ctk.CTkFrame(
        selector_window,
        fg_color="transparent"
    )

    header.pack(
        fill="x",
        padx=25,
        pady=(25, 10)
    )


    title = ctk.CTkLabel(
        header,
        text="➕ Add Application",
        font=ctk.CTkFont(
            size=24,
            weight="bold"
        )
    )

    title.pack(
        anchor="w"
    )


    subtitle = ctk.CTkLabel(
        header,
        text="Select an application to add to your workspace",
        text_color="gray",
        font=ctk.CTkFont(
            size=12
        )
    )

    subtitle.pack(
        anchor="w",
        pady=(3, 0)
    )


    # =====================================================
    # Search
    # =====================================================

    search_var = ctk.StringVar()

    search_entry = ctk.CTkEntry(
        selector_window,
        textvariable=search_var,
        placeholder_text="🔍 Search applications...",
        height=40
    )

    search_entry.pack(
        fill="x",
        padx=25,
        pady=(10, 10)
    )

    # Disable until applications are loaded
    search_entry.configure(
        state="disabled"
    )


    # =====================================================
    # Applications area
    # =====================================================

    applications_frame = ctk.CTkScrollableFrame(
        selector_window,
        corner_radius=10
    )

    applications_frame.pack(
        fill="both",
        expand=True,
        padx=25,
        pady=5
    )


    # =====================================================
    # Loading message
    # =====================================================

    loading_label = ctk.CTkLabel(
        applications_frame,
        text="Loading applications...",
        text_color="gray",
        font=ctk.CTkFont(
            size=14
        )
    )

    loading_label.pack(
        pady=40
    )


    # =====================================================
    # Bottom area
    # =====================================================

    bottom_frame = ctk.CTkFrame(
        selector_window,
        fg_color="transparent"
    )

    bottom_frame.pack(
        fill="x",
        padx=25,
        pady=(10, 20)
    )


    selected_app = None


    # =====================================================
    # Select application
    # =====================================================

    def select_application(app):

        print(
            "Selected application:"
        )

        print(
            "Name:",
            app["name"]
        )

        print(
            "Path:",
            app["path"]
        )

        on_select(
            app
        )

        selector_window.destroy()


    # =====================================================
    # Add selected
    # =====================================================

    def add_selected():

        if selected_app is None:

            return

        select_application(
            selected_app
        )


    add_button = ctk.CTkButton(
        bottom_frame,
        text="➕ Add Selected",
        height=42,
        command=add_selected
    )

    add_button.pack(
        fill="x"
    )

    # Disabled until an app is selected
    add_button.configure(
        state="disabled"
    )


    # =====================================================
    # Icon loading generation
    #
    # If user searches again, old icon jobs are ignored.
    # =====================================================

    icon_generation = [0]


    # =====================================================
    # Update application list
    # =====================================================

    def update_list(*args):

        nonlocal selected_app

        selected_app = None

        icon_generation[0] += 1

        search_text = (
            search_var
            .get()
            .strip()
            .lower()
        )


        # -------------------------------------------------
        # Remove current rows
        # -------------------------------------------------

        for widget in applications_frame.winfo_children():

            widget.destroy()


        # -------------------------------------------------
        # Filter
        # -------------------------------------------------

        matching_apps = [
            app
            for app in applications
            if search_text in app["name"].lower()
        ]


        # -------------------------------------------------
        # No results
        # -------------------------------------------------

        if not matching_apps:

            no_results = ctk.CTkLabel(
                applications_frame,
                text="No applications found",
                text_color="gray",
                font=ctk.CTkFont(
                    size=14
                )
            )

            no_results.pack(
                pady=40
            )

            return


        # -------------------------------------------------
        # Queue missing icons
        # -------------------------------------------------

        icon_jobs = []


        # -------------------------------------------------
        # Create rows
        # -------------------------------------------------

        for app in matching_apps:

            row = ctk.CTkFrame(
                applications_frame,
                corner_radius=8
            )

            row.pack(
                fill="x",
                pady=4
            )


            # ---------------------------------------------
            # Select row
            # ---------------------------------------------

            def select_row(
                event=None,
                selected_app_data=app,
                selected_row=row
            ):

                nonlocal selected_app

                selected_app = selected_app_data

                # Enable Add Selected
                add_button.configure(
                    state="normal"
                )

                # Remove previous highlight
                for child in (
                    applications_frame
                    .winfo_children()
                ):

                    child.configure(
                        fg_color="transparent"
                    )

                # Highlight selected row
                selected_row.configure(
                    fg_color=(
                        "#3a3a3a",
                        "#3a3a3a"
                    )
                )


            # ---------------------------------------------
            # Icon placeholder
            # ---------------------------------------------

            icon_label = ctk.CTkLabel(
                row,
                text="",
                width=35
            )

            icon_label.pack(
                side="left",
                padx=(10, 0),
                pady=6
            )


            # ---------------------------------------------
            # Application name
            # ---------------------------------------------

            button = ctk.CTkButton(
                row,
                text=app["name"],
                anchor="w",
                height=42,
                fg_color="transparent",
                hover_color=(
                    "#333333",
                    "#333333"
                ),
                command=select_row
            )

            button.pack(
                side="left",
                fill="x",
                expand=True,
                padx=5,
                pady=5
            )


            # ---------------------------------------------
            # Row click
            # ---------------------------------------------

            row.bind(
                "<Button-1>",
                select_row
            )


            # ---------------------------------------------
            # Double-click
            # ---------------------------------------------

            row.bind(
                "<Double-Button-1>",
                lambda event,
                selected_app_data=app:
                    select_application(
                        selected_app_data
                    )
            )

            button.bind(
                "<Double-Button-1>",
                lambda event,
                selected_app_data=app:
                    select_application(
                        selected_app_data
                    )
            )


            # ---------------------------------------------
            # Check cached icon
            # ---------------------------------------------

            icon_image = get_application_icon(
                app
            )


            if icon_image:

                icon_label.configure(
                    image=icon_image
                )

                icon_label.image = icon_image

            else:

                # Store apps are skipped for now
                if app.get("type") != "store":

                    icon_jobs.append(
                        (
                            app,
                            icon_label
                        )
                    )


        # -------------------------------------------------
        # Load missing icons gradually
        # -------------------------------------------------

        current_generation = icon_generation[0]


        def load_next_icon(index=0):

            # Search changed
            if (
                current_generation
                != icon_generation[0]
            ):

                return


            if index >= len(icon_jobs):

                return


            app, icon_label = icon_jobs[index]


            icon_path = os.path.join(
                "icons",
                app["name"].replace(" ", "_") + ".png"
            )


            # -------------------------------------------------
            # Extract icon in background
            # -------------------------------------------------

            def extract_icon_worker():

                if not os.path.exists(icon_path):

                    success = extract_icon(
                        app["path"],
                        icon_path
                    )

                    if not success:

                        selector_window.after(
                            1,
                            lambda:
                                load_next_icon(
                                    index + 1
                                )
                        )

                        return


                # Update UI on main thread
                selector_window.after(
                    1,
                    load_icon_on_ui
                )


            def load_icon_on_ui():

                if (
                    current_generation
                    != icon_generation[0]
                ):

                    return


                if not os.path.exists(icon_path):

                    load_next_icon(
                        index + 1
                    )

                    return


                try:

                    image = Image.open(
                        icon_path
                    )

                    icon_image = ctk.CTkImage(
                        light_image=image,
                        dark_image=image,
                        size=(28, 28)
                    )

                    app["icon_image"] = icon_image

                    icon_label.configure(
                        image=icon_image
                    )

                    icon_label.image = icon_image

                except Exception as error:

                    print(
                        "Could not load icon:",
                        error
                    )


                # Process next icon
                selector_window.after(
                    10,
                    lambda:
                        load_next_icon(
                            index + 1
                        )
                )


            # Start extraction in background
            threading.Thread(
                target=extract_icon_worker,
                daemon=True
            ).start()


        # Start icon loading after UI is visible
        selector_window.after(
            100,
            load_next_icon
        )


    # =====================================================
    # Load applications in background
    # =====================================================

    def load_applications_worker():

        try:

            loaded_apps = find_applications()

            def finish_loading():

                # Remove loading message
                for widget in (
                    applications_frame
                    .winfo_children()
                ):

                    widget.destroy()


                # Make applications available
                nonlocal applications

                applications = loaded_apps


                # Enable search
                search_entry.configure(
                    state="normal"
                )


                # Update list
                update_list()


                search_entry.focus()


            selector_window.after(
                0,
                finish_loading
            )

        except Exception as error:

            def show_error():

                for widget in (
                    applications_frame
                    .winfo_children()
                ):

                    widget.destroy()


                error_label = ctk.CTkLabel(
                    applications_frame,
                    text=(
                        "Could not load applications.\n\n"
                        + str(error)
                    ),
                    text_color="#ff6b6b"
                )

                error_label.pack(
                    pady=40
                )


            selector_window.after(
                0,
                show_error
            )


    # =====================================================
    # Application list initially empty
    # =====================================================

    applications = []


    # =====================================================
    # Search binding
    # =====================================================

    search_var.trace_add(
        "write",
        update_list
    )


    # =====================================================
    # Start background application scan
    # =====================================================

    threading.Thread(
        target=load_applications_worker,
        daemon=True
    ).start()