import re

def extract_blocks(code, path):
    pattern = r"(def\s+\w+\(.*?\):.*?)(?=\ndef|\nclass|\Z)|" \
              r"(class\s+\w+.*?:.*?)(?=\ndef|\nclass|\Z)"

    matches = re.findall(pattern, code, re.DOTALL)

    chunks = []

    for match in matches:
        block = match[0] if match[0] else match[1]

        chunks.append({
            "text": block.strip(),
            "source": path,
            "type": "function" if "def " in block else "class"
        })

    return chunks


def chunk_code(files):
    chunks = []

    for f in files:
        content = f["content"]

        # simple chunk (whole file)
        chunks.append({
            "content": content,
            "path": f["path"]
        })

    return chunks