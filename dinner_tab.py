import json
import os
import tkinter as tk
from tkinter import ttk, messagebox
import random


class Dinner:
    def __init__(self, dinner_frame):
        self.dinner_frame = dinner_frame
        self.data_file = "dinner.txt"

        # In-memory recipe storage
        self.recipes = []

        # Keep references to widgets/variables
        self.random_recipe = None
        self.recipe_name_var = tk.StringVar()
        self.url_vars = [tk.StringVar()]
        self.url_entries = []

        # Main container
        self.main_frame = ttk.Frame(self.dinner_frame, padding=10)
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        self.dinner_frame.columnconfigure(0, weight=1)
        self.dinner_frame.rowconfigure(0, weight=1)

        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(1, weight=1)

        self._build_input_section()
        self._build_recipe_display_section()

        # Load existing recipes from file
        self.load_recipes()
        self.refresh_tree()

    def _build_input_section(self):
        """Top section for entering recipe info."""
        self.input_frame = ttk.LabelFrame(self.main_frame, text="Add Recipe", padding=10)
        self.input_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        self.input_frame.columnconfigure(1, weight=1)
        self.input_frame.columnconfigure(3, weight=1)

        ttk.Label(self.input_frame, text="Recipe Name").grid(
            row=0, column=0, padx=(0, 6), pady=4, sticky="w"
        )

        self.recipe_name_entry = ttk.Entry(
            self.input_frame,
            textvariable=self.recipe_name_var,
            width=30
        )
        self.recipe_name_entry.grid(
            row=0, column=1, padx=(0, 16), pady=4, sticky="ew"
        )

        ttk.Label(self.input_frame, text="Recipe URL").grid(
            row=0, column=2, padx=(0, 6), pady=4, sticky="w"
        )

        first_url_entry = ttk.Entry(
            self.input_frame,
            textvariable=self.url_vars[0],
            width=40
        )
        first_url_entry.grid(
            row=0, column=3, padx=(0, 8), pady=4, sticky="ew"
        )
        self.url_entries.append(first_url_entry)

        self.add_url_button = ttk.Button(
            self.input_frame,
            text="Add URL",
            command=self.add_url_entry
        )
        self.add_url_button.grid(
            row=0, column=4, padx=(0, 0), pady=4, sticky="ew"
        )

        self.add_recipe_button = ttk.Button(
            self.input_frame,
            text="Add Recipe",
            command=self.add_recipe
        )
        self.add_recipe_button.grid(
            row=10, column=0, columnspan=5, pady=(10, 0), sticky="w"
        )

    def _build_recipe_display_section(self):
        """Bottom section to display all recipes."""
        self.display_frame = ttk.LabelFrame(self.main_frame, text="Recipes", padding=10)
        self.display_frame.grid(row=1, column=0, sticky="nsew")

        self.display_frame.columnconfigure(0, weight=1)
        self.display_frame.rowconfigure(0, weight=1)

        columns = ("name", "url1", "url2", "url3")
        self.recipe_tree = ttk.Treeview(
            self.display_frame,
            columns=columns,
            show="headings",
            height=12
        )

        self.recipe_tree.heading("name", text="Recipe Name")
        self.recipe_tree.heading("url1", text="URL 1")
        self.recipe_tree.heading("url2", text="URL 2")
        self.recipe_tree.heading("url3", text="URL 3")

        self.recipe_tree.column("name", width=180, anchor="w")
        self.recipe_tree.column("url1", width=220, anchor="w")
        self.recipe_tree.column("url2", width=220, anchor="w")
        self.recipe_tree.column("url3", width=220, anchor="w")

        self.recipe_tree.grid(row=0, column=0, sticky="nsew")

        self.tree_scrollbar = ttk.Scrollbar(
            self.display_frame,
            orient="vertical",
            command=self.recipe_tree.yview
        )
        self.recipe_tree.configure(yscrollcommand=self.tree_scrollbar.set)
        self.tree_scrollbar.grid(row=0, column=1, sticky="ns")

        self.button_frame = ttk.Frame(self.display_frame)
        self.button_frame.grid(row=1, column=0, columnspan=2, sticky="w", pady=(10, 0))

        self.copy_url_1_button = ttk.Button(
            self.button_frame,
            text="Copy URL 1",
            command=lambda: self.copy_selected_url(1)
        )
        self.copy_url_1_button.grid(row=0, column=0, padx=(0, 5))

        self.copy_url_2_button = ttk.Button(
            self.button_frame,
            text="Copy URL 2",
            command=lambda: self.copy_selected_url(2)
        )
        self.copy_url_2_button.grid(row=0, column=1, padx=5)

        self.copy_url_3_button = ttk.Button(
            self.button_frame,
            text="Copy URL 3",
            command=lambda: self.copy_selected_url(3)
        )
        self.copy_url_3_button.grid(row=0, column=2, padx=5)

        self.delete_recipe_button = ttk.Button(
            self.button_frame,
            text="Delete Recipe",
            command=self.delete_selected_recipe
        )
        self.delete_recipe_button.grid(row=0, column=3, padx=(12, 0))

        self.generate_random_button = ttk.Button(
            self.button_frame,
            text="Generate Random Recipe",
            command=self.generate_random_recipe
        )
        self.generate_random_button.grid(row=0, column=4, padx=(12, 0))

        self.use_random_var = tk.BooleanVar(value=False)
        self.use_random_check = ttk.Checkbutton(
            self.button_frame,
            text="Use Random Recipe",
            variable=self.use_random_var
        )
        self.use_random_check.grid(row=0, column=5, padx=(12, 0))

        self.random_recipe_label = ttk.Label(
            self.display_frame,
            text="Random Recipe: None selected",
            anchor="w"
        )
        self.random_recipe_label.grid(
            row=2, column=0, columnspan=2, sticky="ew", pady=(10, 0)
        )

    def add_url_entry(self):
        """
        Add another URL entry below the first Recipe URL entry.
        Max of 3 URL boxes total.
        """
        if len(self.url_vars) >= 3:
            return

        new_var = tk.StringVar()
        self.url_vars.append(new_var)

        row_num = len(self.url_vars) - 1

        url_entry = ttk.Entry(
            self.input_frame,
            textvariable=new_var,
            width=40
        )
        url_entry.grid(
            row=row_num,
            column=3,
            padx=(0, 8),
            pady=4,
            sticky="ew"
        )
        self.url_entries.append(url_entry)

        if len(self.url_vars) >= 3:
            self.add_url_button.state(["disabled"])

    def add_recipe(self):
        """Read input widgets, validate, store recipe, save file, and refresh display."""
        recipe_name = self.recipe_name_var.get().strip()
        urls = [var.get().strip() for var in self.url_vars if var.get().strip()]

        if not recipe_name:
            messagebox.showwarning("Missing Recipe Name", "Please enter a recipe name.")
            return

        if not urls:
            messagebox.showwarning("Missing URL", "Please enter at least one recipe URL.")
            return

        recipe = {
            "name": recipe_name,
            "urls": urls
        }

        self.recipes.append(recipe)
        self.save_recipes()
        self.refresh_tree()
        self.clear_inputs()

    def delete_selected_recipe(self):
        """Delete the currently selected recipe after confirmation."""
        selected = self.recipe_tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a recipe to delete.")
            return

        item_id = selected[0]
        index = int(item_id)
        recipe_name = self.recipes[index]["name"]

        confirm = messagebox.askyesno(
            "Delete Recipe",
            f'Are you sure you want to delete "{recipe_name}"?'
        )
        if not confirm:
            return

        del self.recipes[index]
        self.save_recipes()
        self.refresh_tree()

    def copy_selected_url(self, url_number):
        """
        Copy URL 1, 2, or 3 from either:
        - the selected recipe in the tree, or
        - the random recipe if the checkbox is checked
        """
        recipe = self.get_active_recipe()
        if recipe is None:
            return

        urls = recipe.get("urls", [])
        url_index = url_number - 1

        if url_index >= len(urls) or not urls[url_index]:
            messagebox.showwarning(
                "URL Not Available",
                f"This recipe does not have URL {url_number}."
            )
            return

        url_to_copy = urls[url_index]
        self.breakfast_frame.clipboard_clear()
        self.breakfast_frame.clipboard_append(url_to_copy)
        self.breakfast_frame.update()

        messagebox.showinfo("Copied", f"URL {url_number} copied to clipboard.")

    def refresh_tree(self):
        """Clear and repopulate the treeview from self.recipes."""
        for item in self.recipe_tree.get_children():
            self.recipe_tree.delete(item)

        for index, recipe in enumerate(self.recipes):
            urls = recipe.get("urls", [])
            row_values = (
                recipe.get("name", ""),
                urls[0] if len(urls) > 0 else "",
                urls[1] if len(urls) > 1 else "",
                urls[2] if len(urls) > 2 else "",
            )
            self.recipe_tree.insert("", "end", iid=str(index), values=row_values)

    def clear_inputs(self):
        """Reset the input area after a recipe is added."""
        self.recipe_name_var.set("")

        # Clear current URL values
        for var in self.url_vars:
            var.set("")

        # Remove extra URL entry widgets so we go back to one URL box
        while len(self.url_entries) > 1:
            entry = self.url_entries.pop()
            entry.destroy()

        # Reset URL vars to just one
        self.url_vars = [self.url_vars[0]]
        self.url_vars[0].set("")

        # Re-enable Add URL button
        self.add_url_button.state(["!disabled"])

        self.recipe_name_entry.focus_set()

    def load_recipes(self):
        """Load recipes from dinner.txt if it exists."""
        if not os.path.exists(self.data_file):
            self.recipes = []
            return

        try:
            with open(self.data_file, "r", encoding="utf-8") as file:
                content = file.read().strip()

                if not content:
                    self.recipes = []
                    return

                data = json.loads(content)

                if isinstance(data, list):
                    cleaned_recipes = []
                    for item in data:
                        if not isinstance(item, dict):
                            continue

                        name = str(item.get("name", "")).strip()
                        urls = item.get("urls", [])

                        if not isinstance(urls, list):
                            urls = []

                        urls = [str(url).strip() for url in urls if str(url).strip()]

                        if name:
                            cleaned_recipes.append({
                                "name": name,
                                "urls": urls[:3]
                            })

                    self.recipes = cleaned_recipes
                else:
                    self.recipes = []

        except (json.JSONDecodeError, OSError):
            messagebox.showwarning(
                "Load Error",
                "Could not read dinner.txt. Starting with an empty recipe list."
            )
            self.recipes = []

    def save_recipes(self):
        """Write the current recipe list to dinner.txt."""
        try:
            with open(self.data_file, "w", encoding="utf-8") as file:
                json.dump(self.recipes, file, indent=2, ensure_ascii=False)
        except OSError:
            messagebox.showerror(
                "Save Error",
                "Could not save recipes to dinner.txt."
            )

    def generate_random_recipe(self):
        """
        Pick a random recipe from self.recipes and show it below the table.
        """
        if not self.recipes:
            messagebox.showwarning("No Recipes", "There are no recipes to choose from.")
            self.random_recipe = None
            self.use_random_var.set(False)
            self.random_recipe_label.config(text="Random Recipe: None selected")
            return

        self.random_recipe = random.choice(self.recipes)

        name = self.random_recipe.get("name", "")
        urls = self.random_recipe.get("urls", [])

        url_text = []
        for i in range(3):
            if i < len(urls):
                url_text.append(f"URL {i+1}: {urls[i]}")
            else:
                url_text.append(f"URL {i+1}: ")

        display_text = f"Random Recipe: {name} | " + " | ".join(url_text)
        self.random_recipe_label.config(text=display_text)

    def get_active_recipe(self):
        """
        Return the recipe that the copy buttons should use.
        If 'Use Random Recipe' is checked, use the random recipe.
        Otherwise use the selected row in the tree.
        """
        if self.use_random_var.get():
            if self.random_recipe is None:
                messagebox.showwarning(
                    "No Random Recipe",
                    "Generate a random recipe first or uncheck 'Use Random Recipe'."
                )
                return None
            return self.random_recipe

        selected = self.recipe_tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a recipe first.")
            return None

        item_id = selected[0]
        index = int(item_id)
        return self.recipes[index]
