import os

# Define folder and file structure
structure = {
    "": ["app.py", "config.py", "requirements.txt"],
    "templates": ["base.html", "index.html", "map.html", "path_details.html"],
    "static/css": ["style.css"],
    "static/js": ["script.js"],
    "static/images": ["campus_map.png", "icon_marker.png", "output_path.png"],
    # Skipping PATHS and OUTPUT folders as per your request
    "utils": ["__init__.py", "path_loader.py", "route_calculator.py"]
}

# Create folders and files
for folder, files in structure.items():
    if folder and not os.path.exists(folder):
        os.makedirs(folder)
        print(f"Created folder: {folder}")

    for file in files:
        file_path = os.path.join(folder, file)
        if not os.path.exists(file_path):
            with open(file_path, "w") as f:
                pass
            print(f"Created file: {file_path}")
        else:
            print(f"Skipped existing file: {file_path}")

print("\n✅ Project structure is ready (excluding PATHS/ and OUTPUT/)")
