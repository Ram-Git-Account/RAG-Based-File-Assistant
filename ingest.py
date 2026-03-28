import os

def load_code_files(folder_path):
    files_data = []

    for root, _, files in os.walk(folder_path):
        print("DEBUG - root:", root)
        print("DEBUG - files:", files)

        for file in files:
            if file.endswith((".py", ".java", ".cpp", ".js")):
                path = os.path.join(root, file)

                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    files_data.append({
                        "content": f.read(),
                        "path": path
                    })

    return files_data