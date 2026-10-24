import customtkinter as ctk
from tkinter import messagebox
import os

from icons import extract_icon
from config import load_config, save_config
from launcher import launch_workspace
from app_selector import show_application_selector
from PIL import Image


class WorkspaceLauncher:

    def __init__(self, window):

        self.window = window

        self.window.title(
            "Workspace Launcher"
        )

        self.window.geometry(
            "900x700"
        )

        self.window.minsize(
            650,
            550
        )


        # -------------------------------------------------
        # Configuration
        # -------------------------------------------------

        self.config = load_config()

        self.current_workspace = "Default"

        self.applications = []


        # -------------------------------------------------
        # Build
        # -------------------------------------------------

        self.build_ui()


        # -------------------------------------------------
        # Load workspace
        # -------------------------------------------------

        self.load_workspace_names()

        self.load_current_workspace()


    # =====================================================
    # BUILD UI
    # =====================================================

    def build_ui(self):

        # =================================================
        # Main frame
        # =================================================

        self.main_frame = ctk.CTkFrame(
            self.window,
            corner_radius=0
        )

        self.main_frame.pack(
            fill="both",
            expand=True
        )


        # =================================================
        # Header
        # =================================================

        self.header = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent"
        )

        self.header.pack(
            fill="x",
            padx=30,
            pady=(25, 10)
        )


        self.title_label = ctk.CTkLabel(
            self.header,
            text="🚀 Workspace Launcher",
            font=ctk.CTkFont(
                size=26,
                weight="bold"
            )
        )

        self.title_label.pack(
            anchor="w"
        )


        self.subtitle_label = ctk.CTkLabel(
            self.header,
            text="Launch all your applications with one click",
            text_color="gray",
            font=ctk.CTkFont(
                size=13
            )
        )

        self.subtitle_label.pack(
            anchor="w",
            pady=(3, 0)
        )


        # =================================================
        # Workspace label
        # =================================================

        self.workspace_label = ctk.CTkLabel(
            self.main_frame,
            text="WORKSPACE",
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            )
        )

        self.workspace_label.pack(
            anchor="w",
            padx=30,
            pady=(15, 5)
        )


        # =================================================
        # Workspace selector
        # =================================================

        self.workspace_menu = ctk.CTkOptionMenu(
            self.main_frame,
            values=["Default"],
            command=self.change_workspace,
            height=40
        )

        self.workspace_menu.pack(
            fill="x",
            padx=30,
            pady=(0, 8)
        )


        # =================================================
        # New workspace
        # =================================================

        self.new_workspace_button = ctk.CTkButton(
            self.main_frame,
            text="➕ New Workspace",
            height=35,
            command=self.create_workspace
        )

        self.new_workspace_button.pack(
            fill="x",
            padx=30,
            pady=(0, 8)
        )


        # =================================================
        # Rename / Delete
        # =================================================

        self.workspace_actions_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent"
        )

        self.workspace_actions_frame.pack(
            fill="x",
            padx=30,
            pady=(0, 8)
        )


        self.rename_workspace_button = ctk.CTkButton(
            self.workspace_actions_frame,
            text="✏ Rename",
            height=35,
            command=self.rename_workspace
        )

        self.rename_workspace_button.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 5)
        )


        self.delete_workspace_button = ctk.CTkButton(
            self.workspace_actions_frame,
            text="🗑 Delete",
            height=35,
            fg_color="#8B0000",
            hover_color="#B22222",
            command=self.delete_workspace
        )

        self.delete_workspace_button.pack(
            side="right",
            fill="x",
            expand=True,
            padx=(5, 0)
        )


        # =================================================
        # Applications title
        # =================================================

        self.apps_title = ctk.CTkLabel(
            self.main_frame,
            text="MY APPLICATIONS",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            )
        )

        self.apps_title.pack(
            anchor="w",
            padx=30,
            pady=(10, 5)
        )


        # =================================================
        # BOTTOM ACTIONS
        #
        # IMPORTANT:
        # Pack this BEFORE the expandable application
        # area so these buttons always reserve space.
        # =================================================

        self.bottom_actions = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent"
        )

        self.bottom_actions.pack(
            side="bottom",
            fill="x",
            padx=30,
            pady=(10, 20)
        )


        # -------------------------------------------------
        # Add
        # -------------------------------------------------

        self.add_button = ctk.CTkButton(
            self.bottom_actions,
            text="➕  Add Application",
            height=40,
            command=self.add_application
        )

        self.add_button.pack(
            fill="x",
            pady=(0, 8)
        )


        # -------------------------------------------------
        # Launch
        # -------------------------------------------------

        self.launch_button = ctk.CTkButton(
            self.bottom_actions,
            text="🚀  Launch Workspace",
            height=48,
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            ),
            command=self.launch
        )

        self.launch_button.pack(
            fill="x"
        )


        # =================================================
        # APPLICATIONS AREA
        #
        # This gets ALL remaining vertical space.
        # =================================================

        self.applications_frame = ctk.CTkScrollableFrame(
            self.main_frame,
            corner_radius=12
        )

        self.applications_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=5
        )


    # =====================================================
    # APPLICATION ROW
    # =====================================================

    def create_application_row(
        self,
        app
    ):

        row = ctk.CTkFrame(
            self.applications_frame,
            corner_radius=8
        )

        row.pack(
            fill="x",
            pady=4,
            padx=5
        )


        # -------------------------------------------------
        # Icon
        # -------------------------------------------------

        icon_path = os.path.join(
            "icons",
            app["name"].replace(
                " ",
                "_"
            ) + ".png"
        )


        # Store apps may not have normal icons
        if app.get("type") != "store":

            if not os.path.exists(
                icon_path
            ):

                extract_icon(
                    app["path"],
                    icon_path
                )


        icon_image = None


        if os.path.exists(
            icon_path
        ):

            try:

                image = Image.open(
                    icon_path
                )

                icon_image = ctk.CTkImage(
                    light_image=image,
                    dark_image=image,
                    size=(32, 32)
                )

            except Exception as error:

                print(
                    "Could not load icon:",
                    error
                )


        # -------------------------------------------------
        # Icon label
        # -------------------------------------------------

        if icon_image:

            icon_label = ctk.CTkLabel(
                row,
                text="",
                image=icon_image,
                width=40
            )

            icon_label.pack(
                side="left",
                padx=(10, 0),
                pady=8
            )

            app["icon_image"] = icon_image


        # -------------------------------------------------
        # Checkbox
        # -------------------------------------------------

        checkbox = ctk.CTkCheckBox(
            row,
            text=app["name"],
            variable=app["variable"],
            font=ctk.CTkFont(
                size=14
            )
        )

        checkbox.pack(
            side="left",
            fill="x",
            expand=True,
            padx=10,
            pady=12
        )


        # -------------------------------------------------
        # Remove
        # -------------------------------------------------

        remove_button = ctk.CTkButton(
            row,
            text="🗑",
            width=45,
            height=32,
            fg_color="transparent",
            hover_color="#8B0000",
            command=lambda:
                self.remove_application(
                    app,
                    row
                )
        )

        remove_button.pack(
            side="right",
            padx=10
        )


        app["row"] = row


    # =====================================================
    # REMOVE APPLICATION
    # =====================================================

    def remove_application(
        self,
        app,
        row
    ):

        answer = messagebox.askyesno(
            "Remove Application",
            f"Remove {app['name']} from your workspace?"
        )

        if not answer:
            return


        self.applications.remove(
            app
        )

        row.destroy()


        app.pop(
            "variable",
            None
        )

        app.pop(
            "row",
            None
        )


        self.save_current_workspace()


    # =====================================================
    # LAUNCH
    # =====================================================

    def launch(self):

        results = launch_workspace(
            self.applications
        )


        failed = [

            result

            for result in results

            if not result["success"]

        ]


        if failed:

            message = "\n".join(

                f"{item['name']}: "
                f"{item['error']}"

                for item in failed

            )

            messagebox.showerror(
                "Launch Error",
                message
            )


    # =====================================================
    # ADD APPLICATION
    # =====================================================

    def add_application(self):

        show_application_selector(
            self.window,
            self.application_selected
        )


    # =====================================================
    # APPLICATION SELECTED
    # =====================================================

    def application_selected(
        self,
        app
    ):

        # Prevent duplicates
        for existing in self.applications:

            if existing["path"] == app["path"]:

                messagebox.showinfo(
                    "Already Added",
                    f"{app['name']} is already in your workspace."
                )

                return


        app["variable"] = ctk.BooleanVar(
            value=True
        )


        self.applications.append(
            app
        )


        self.create_application_row(
            app
        )


        self.save_current_workspace()


    # =====================================================
    # LOAD WORKSPACE NAMES
    # =====================================================

    def load_workspace_names(self):

        workspace_names = list(
            self.config["workspaces"].keys()
        )


        if not workspace_names:

            workspace_names = [
                "Default"
            ]

            self.config["workspaces"][
                "Default"
            ] = {
                "applications": []
            }


        self.workspace_menu.configure(
            values=workspace_names
        )


        if (
            self.current_workspace
            not in workspace_names
        ):

            self.current_workspace = (
                workspace_names[0]
            )


        self.workspace_menu.set(
            self.current_workspace
        )


    # =====================================================
    # LOAD CURRENT WORKSPACE
    # =====================================================

    def load_current_workspace(self):

        for widget in (
            self.applications_frame
            .winfo_children()
        ):

            widget.destroy()


        self.applications.clear()


        workspace = (
            self.config["workspaces"].get(
                self.current_workspace,
                {
                    "applications": []
                }
            )
        )


        for saved_app in workspace[
            "applications"
        ]:

            app = {

                "name":
                    saved_app["name"],

                "path":
                    saved_app["path"],

                "variable":
                    ctk.BooleanVar(
                        value=True
                    )
            }


            # Preserve store type if saved
            if saved_app.get("type"):
                app["type"] = saved_app["type"]


            self.applications.append(
                app
            )


            self.create_application_row(
                app
            )


    # =====================================================
    # CHANGE WORKSPACE
    # =====================================================

    def change_workspace(
        self,
        workspace_name
    ):

        if (
            workspace_name
            == self.current_workspace
        ):

            return


        self.save_current_workspace()


        self.current_workspace = (
            workspace_name
        )


        self.load_current_workspace()


    # =====================================================
    # SAVE CURRENT WORKSPACE
    # =====================================================

    def save_current_workspace(self):

        self.config["workspaces"][
            self.current_workspace
        ] = {

            "applications": [

                {
                    "name": app["name"],
                    "path": app["path"],
                    "type": app.get(
                        "type",
                        "shortcut"
                    )
                }

                for app in self.applications

            ]
        }


        save_config(
            self.config
        )


    # =====================================================
    # CREATE WORKSPACE
    # =====================================================

    def create_workspace(self):

        dialog = ctk.CTkInputDialog(
            text="Enter workspace name:",
            title="New Workspace"
        )


        name = dialog.get_input()


        if not name:
            return


        name = name.strip()


        if not name:
            return


        if name in self.config[
            "workspaces"
        ]:

            messagebox.showwarning(
                "Workspace Exists",
                f"'{name}' already exists."
            )

            return


        self.config[
            "workspaces"
        ][name] = {

            "applications": []

        }


        save_config(
            self.config
        )


        self.current_workspace = name


        self.load_workspace_names()

        self.workspace_menu.set(
            name
        )


        self.load_current_workspace()


    # =====================================================
    # RENAME WORKSPACE
    # =====================================================

    def rename_workspace(self):

        if self.current_workspace == "Default":

            messagebox.showwarning(
                "Cannot Rename",
                "The Default workspace cannot be renamed."
            )

            return


        dialog = ctk.CTkInputDialog(
            text="Enter new workspace name:",
            title="Rename Workspace"
        )


        new_name = dialog.get_input()


        if not new_name:
            return


        new_name = new_name.strip()


        if not new_name:
            return


        if new_name in self.config[
            "workspaces"
        ]:

            messagebox.showwarning(
                "Workspace Exists",
                f"'{new_name}' already exists."
            )

            return


        self.config[
            "workspaces"
        ][new_name] = (
            self.config[
                "workspaces"
            ].pop(
                self.current_workspace
            )
        )


        self.current_workspace = (
            new_name
        )


        save_config(
            self.config
        )


        self.load_workspace_names()


        self.workspace_menu.set(
            new_name
        )


    # =====================================================
    # DELETE WORKSPACE
    # =====================================================

    def delete_workspace(self):

        if self.current_workspace == "Default":

            messagebox.showwarning(
                "Cannot Delete",
                "The Default workspace cannot be deleted."
            )

            return


        answer = messagebox.askyesno(
            "Delete Workspace",
            f"Delete '{self.current_workspace}'?\n\n"
            "All applications in this workspace will be removed."
        )


        if not answer:
            return


        del self.config[
            "workspaces"
        ][
            self.current_workspace
        ]


        self.current_workspace = (
            "Default"
        )


        save_config(
            self.config
        )


        self.load_workspace_names()

        self.workspace_menu.set(
            "Default"
        )

        self.load_current_workspace()