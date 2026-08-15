@'
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent

REPLACEMENTS = {
    "from cad_math.vector import": "from cad_math.vector import",
    "from cad_math.matrix import": "from cad_math.matrix import",
    "from cad_math.transform import": "from cad_math.transform import",
    "from cad_math.geometry_math import": "from cad_math.geometry_math import",
    "from cad_math.tolerance import": "from cad_math.tolerance import",

    "import math.vector": "import cad_math.vector",
    "import math.matrix": "import cad_math.matrix",
    "import math.transform": "import cad_math.transform",
    "import math.geometry_math": "import cad_math.geometry_math",
    "import math.tolerance": "import cad_math.tolerance",

    "from math3d.vector import": "from cad_math.vector import",
    "from math3d.matrix import": "from cad_math.matrix import",
    "from math3d.transform import": "from cad_math.transform import",
    "from math3d.geometry_math import": "from cad_math.geometry_math import",
    "from math3d.tolerance import": "from cad_math.tolerance import",

    "import math3d.vector": "import cad_math.vector",
    "import math3d.matrix": "import cad_math.matrix",
    "import math3d.transform": "import cad_math.transform",
    "import math3d.geometry_math": "import cad_math.geometry_math",
    "import math3d.tolerance": "import cad_math.tolerance",
}

changed = []

for py in PROJECT_ROOT.rglob("*.py"):
    if py.name == "refactor_imports.py":
        continue

    text = py.read_text(encoding="utf-8")

    new_text = text

    for old, new in REPLACEMENTS.items():
        new_text = new_text.replace(old, new)

    if new_text != text:
        py.write_text(new_text, encoding="utf-8")
        changed.append(py)

print("=" * 60)
print("Changed Files")
print("=" * 60)

for f in changed:
    print(f.relative_to(PROJECT_ROOT))

print("=" * 60)
print(f"Total: {len(changed)} file(s)")
'@ | Set-Content .\refactor_imports.py -Encoding UTF8
