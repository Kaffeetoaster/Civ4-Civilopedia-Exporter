import os
import re

ROOT_FOLDER = r"/home/anton/.steam/steam/steamapps/common/Sid Meier's Civilization IV Beyond the Sword/Beyond the Sword/Mods/RFC Dawn of Civilization (Pedia)/Assets/Python"

OUTPUT_DEFS = "generated_methods_TechChooser.py"
OUTPUT_LOG = "method_occurrences_TechChooser.txt"

# matches: screen.methodName(
pattern = re.compile(r"screen\.([A-Za-z_][A-Za-z0-9_]*)\(")

found_methods = set()
occurrences = []

for root, dirs, files in os.walk(ROOT_FOLDER):
    for filename in files:
        if not filename.endswith(".py"):
            continue

        filepath = os.path.join(root, filename)

        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                for lineno, line in enumerate(f, start=1):
                    match = pattern.search(line)
                    if match:
                        method = match.group(1)

                        found_methods.add(method)
                        occurrences.append(f"{filepath}:{lineno}: {method}")

        except Exception as e:
            print(f"Error reading {filepath}: {e}")

# -------------------------
# 1. write occurrence log
# -------------------------
with open(OUTPUT_LOG, "w", encoding="utf-8") as f:
    f.write("\n".join(occurrences))

# -------------------------
# 2. write fake method defs
# -------------------------
with open(OUTPUT_DEFS, "w", encoding="utf-8") as f:
    f.write("def logToFile(msg):\n")
    f.write("    print(msg)\n\n\n")

    for method in sorted(found_methods):
        f.write(f"def {method}(self, *args, **kwargs):\n")
        f.write(f"    logToFile('{method} was called')\n")
        f.write("    pass\n\n")

print("Done.")
print(f"Methods found: {len(found_methods)}")
print(f"Occurrences logged: {len(occurrences)}")
