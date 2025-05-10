#!/usr/bin/env python3

"""
📄 Django → TypeScript Interface Generator

This script scans your Django model files and generates matching TypeScript interfaces
for frontend type safety. It's optimized for projects using Django + SvelteKit (or similar),
and assumes a fairly flat, conventional `models.py` structure.

✅ Use Cases:
- Keeps backend and frontend types in sync
- Great for autocompletion in IDEs
- Simplifies prop typing and API contracts in SvelteKit

⚙️ Configuration:
- `BACKEND_DIR`: Relative path to your Django models folder or root app folder
- `FRONTEND_DIR`: Output location for generated `.ts` files

🛠 Assumptions:
- Only basic field types are mapped (extend `FIELD_TYPE_MAP` if needed)
- ForeignKey and OneToOneField resolve to the target model's ID (type: `number`)
- ManyToManyField resolves to an array of IDs (type: `number[]`)
- Model classes are defined as `class ModelName(models.Model):`
- Field lines look like `field_name = models.SomeField(...)`
- Supports both monolithic `models/` folders and multi-app projects with `models.py` files

📌 To Use:
1. Set `BACKEND_DIR` and `FRONTEND_DIR` for your project structure
2. Run the script from the root of your backend project:
   ```bash
   python generate_ts_models.py
   ```
3. Commit the generated `.ts` files to your frontend project
"""

import os
import re
from pathlib import Path

# 🔧 CONFIG — Change these paths based on your project structure
# If you have multiple apps, set this to the root directory containing all apps
BACKEND_DIR = "appname/models"  # or e.g., "myproject/apps"
FRONTEND_DIR = "../frontend/src/lib/types/models"  # TS output location

# 🧠 Mapping of Django field types to TypeScript types
FIELD_TYPE_MAP = {
    "CharField": "string",
    "TextField": "string",
    "SlugField": "string",
    "EmailField": "string",
    "URLField": "string",
    "DateField": "string",
    "DateTimeField": "string",
    "TimeField": "string",
    "BooleanField": "boolean",
    "NullBooleanField": "boolean",
    "IntegerField": "number",
    "SmallIntegerField": "number",
    "BigIntegerField": "number",
    "PositiveIntegerField": "number",
    "PositiveSmallIntegerField": "number",
    "FloatField": "number",
    "DecimalField": "number",
    "JSONField": "Record<string, any>",
    "ArrayField": "any[]",
    "FileField": "string",
    "ImageField": "string",
    "ForeignKey": "number",
    "OneToOneField": "number",
    "ManyToManyField": "number[]"
}

# 🧾 Regex patterns to extract class and field declarations
FIELD_DEF_REGEX = re.compile(r"\s*(\w+)\s*=\s*models\.(\w+)")
CLASS_DEF_REGEX = re.compile(r"class\s+(\w+)\((.*?)\):")

def parse_model_file(content):
    """Extracts model names and field types from a file's contents."""
    models = []
    current_model = None
    fields = []

    for line in content.splitlines():
        class_match = CLASS_DEF_REGEX.match(line)
        if class_match:
            if current_model and fields:
                models.append((current_model, fields))
            current_model = class_match.group(1)
            fields = []
        elif "= models." in line:
            match = FIELD_DEF_REGEX.match(line)
            if match and current_model:
                field_name, field_type = match.groups()
                ts_type = FIELD_TYPE_MAP.get(field_type, "any")
                fields.append((field_name, ts_type))

    if current_model and fields:
        models.append((current_model, fields))

    return models

def write_ts_interface(class_name, fields, out_path):
    """Writes a TypeScript interface file for a given model."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        f.write(f"export interface {class_name} {{\n")
        for name, ts_type in fields:
            f.write(f"  {name}?: {ts_type};\n")
        f.write("}\n")
    print(f"✅ {class_name} → {out_path}")

def process_models():
    """Walks the backend directory and generates TS interfaces."""
    print(f"📁 Scanning models in: {BACKEND_DIR}")
    base = Path(BACKEND_DIR)
    count = 0

    for root, _, files in os.walk(base):
        for filename in files:
            if filename == "models.py":
                path = Path(root) / filename
                with open(path, "r") as f:
                    content = f.read()

                model_defs = parse_model_file(content)
                if not model_defs:
                    continue

                relative_path = path.parent.relative_to(base)
                for model_name, fields in model_defs:
                    out_path = Path(FRONTEND_DIR) / relative_path / f"{model_name}.ts"
                    write_ts_interface(model_name, fields, out_path)
                    count += 1

    print(f"\n🎯 Done. {count} interfaces generated.")

if __name__ == "__main__":
    process_models()
