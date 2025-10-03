"""
This script builds a single comprehensive metadata file (`data/records_metadata.csv`)
for electrophysiology data stored in `data/records`. Unlike the multi-step version
that produces intermediate CSVs, this script constructs everything in one pass.

Processing steps:

1. **Base columns**
   - Traverse `data/records` directory organized by day and cell folders.
   - Assigns a unique `cell_id` (C1, C2, …) to each cell.
   - Collects `file_path` (relative to records root) and `file_name`.

2. **Date**
   - Extracts day folder name (MM.DD) from `file_path`.
   - Converts to a `date` column (`YYYY-MM-DD`).

3. **Experiment number**
   - Adds `exp_nb`, a sequential counter (1, 2, 3, …).

4. **Comments (basic)**
   - Marks cells as "immature" or "dead" if these appear in `file_path`.

5. **Protocol**
   - Determines experimental protocol type (`IC`, `VC`, `DC`) from `file_path`.
   - Updates `comments` to note overlapping labels (e.g., "IC" if present).

6. **Protocol options**
   - Detects variations in protocol (`steps`, `step`, `ramp`, `sin`).
   - Stores in `prot-opt`.

7. **Temperature**
   - Extracts temperature from filenames as a two-digit number (e.g. 34 or 34,5).
   - Normalizes to a decimal string (e.g. `34.0`).

8. **Refined comments**
   - Appends “square steps” if it appears in `file_name`.
   - Appends parenthetical markers like `(2)`, `(3)` if found in `file_name`.

9. **Separate "bad" references**

Finally, the script saves :
  - a complete consolidated CSV (`records_metadata.csv`) 
    with all metadata columns for downstream analysis
  - the subset of "clean" records references (`records_metadata_clean.csv`) 
  - the subset of "bad" records references (`records_metadata_bad.csv`) 

"""


import pandas as pd
import re
from pathlib import Path

# =========================================================
# Final metadata construction: one CSV only
# =========================================================

records_root = Path("records")
final_metadata_file = Path("records_metadata.csv")
final_metadata_file_clean = Path("records_metadata_clean.csv")
final_metadata_file_bad = Path("records_metadata_bad.csv")

# ------------------------------
# STEP 1 : base columns
# ------------------------------
rows = []
absolute_cell_counter = 1

day_folders = sorted([d for d in records_root.iterdir() if d.is_dir()])

for day_folder in day_folders:
    cell_folders = sorted([c for c in day_folder.iterdir() if c.is_dir()])
    for cell_folder in cell_folders:
        cell_id = f"C{absolute_cell_counter}"
        absolute_cell_counter += 1

        for f in sorted(cell_folder.iterdir()):
            if f.is_file():
                rows.append({
                    "cell_id": cell_id,
                    "file_path": str(f.relative_to(records_root)),
                    "file_name": f.name
                })

df = pd.DataFrame(rows)
print("Step 1: columns cell_id, file_path, file_name")

# ------------------------------
# STEP 2: add date
# ------------------------------
def extract_date(file_path_str):
    file_path = Path(file_path_str)
    day_folder = file_path.parent.parent.name
    try:
        month, day = day_folder.split(".")
        return f"2024-{month}-{day}"  # YYYY-MM-DD
    except ValueError:
        return "2024-01-01"

df['date'] = df['file_path'].apply(extract_date)
df = df[['cell_id', 'date', 'file_path', 'file_name']]
print("Step 2: column date")

# ------------------------------
# STEP 3: add exp_nb
# ------------------------------
df.insert(0, 'exp_nb', range(1, len(df) + 1))
print("Step 3: column exp_nb")

# ------------------------------
# STEP 4: comments
# ------------------------------
def build_comments(path):
    tags = []
    if "immature" in path.lower():
        tags.append("immature")
    if "dead" in path.lower():
        tags.append("dead")
    return ";".join(tags)

df.insert(df.columns.get_loc("date") + 1, "comments", df["file_path"].apply(build_comments))
print("Step 4: column comments")

# ------------------------------
# STEP 5: protocol
# ------------------------------
protocols = []
new_comments = []

for path, comment in zip(df["file_path"], df["comments"]):
    path_lower = path.lower()
    updated_comment = comment if pd.notna(comment) else ""

    if "dynamic clamp" in path_lower or " dc" in path_lower or path_lower.endswith("dc.abf"):
        protocol = "DC"
        # Preserve the original script’s quirk: if "IC" also exists, append to comments
        if " ic" in path_lower or path_lower.startswith("ic") or " ic." in path_lower:
            if updated_comment:
                if "IC" not in updated_comment.split(";"):
                    updated_comment += ";IC"
            else:
                updated_comment = "IC"
    elif "vc" in path_lower:
        protocol = "VC"
    elif "ic" in path_lower:
        protocol = "IC"
    else:
        protocol = ""

    protocols.append(protocol)
    new_comments.append(updated_comment)

df.insert(df.columns.get_loc("date") + 1, "protocol", protocols)
df["comments"] = new_comments
print("Step 5: column protocol")

# ------------------------------
# STEP 6: prot-opt
# ------------------------------
def extract_prot_opt(path):
    path_lower = path.lower()
    if " steps " in path_lower:
        return "steps"
    if " step " in path_lower:
        return "step"
    if " ramp " in path_lower:
        return "ramp"
    if " sin " in path_lower:
        return "sin"
    return ""

df.insert(df.columns.get_loc("protocol") + 1, "prot-opt", df["file_path"].apply(extract_prot_opt))
print("Step 6: column prot-opt")

# ------------------------------
# STEP 7: temperature (tp)
# ------------------------------

def extract_tp(path):
    match = re.search(r"(\d{2}(?:,\d)?)\s*(?=[^\d]*\.(?:abf|atf)$)", path, re.IGNORECASE)
    if match:
        val = match.group(1).replace(",", ".")
        # Always format as one decimal place, like "23.0"
        try:
            return f"{float(val):.1f}"
        except ValueError:
            return val
    return ""

df.insert(df.columns.get_loc("prot-opt") + 1, "tp", df["file_path"].apply(extract_tp))
df["tp"] = df["tp"].astype(str)

print("Step 7: column tp")

# ------------------------------
# STEP 8: refine comments
# ------------------------------
# add "square steps"
mask = df['file_name'].str.contains("square steps", case=False, na=False)
df.loc[mask, "comments"] = df.loc[mask, "comments"].fillna("").astype(str).str.strip()
df.loc[mask, "comments"] = df.loc[mask, "comments"].replace("nan", "").str.strip()
df.loc[mask, "comments"] = df.loc[mask, "comments"].apply(lambda c: c + (";square steps" if c else "square steps"))

# add (2), (3) ...
pattern = re.compile(r"\(\d+\)")
for idx, name in df["file_name"].items():
    match = pattern.search(name)
    if match:
        extra = match.group(0)
        current = str(df.at[idx, "comments"]) if pd.notna(df.at[idx, "comments"]) else ""
        if extra not in current:
            new_comment = (current + ";" + extra).strip(";").strip()
            df.at[idx, "comments"] = new_comment

df.to_csv(final_metadata_file, index=False)

print("Step 8: refine comments")

# ------------------------------
# STEP 8: separate "bad" records 
# ------------------------------
# The experimentaliste told me: "there are a few files 
# that are not abf or atf, forget about them" and also 
# "some file with short file names are useless !"

# Conditions for bad rows
cond_short = df['file_name'].str.len() < 12
cond_invalid_ext = ~df['file_name'].str.lower().str.endswith(('.abf', '.atf'))

# Keep only the good rows (negation of bad ones)
df_clean = df[~(cond_short | cond_invalid_ext)].copy()

# Save cleaned metadata
#df_clean.to_csv(final_metadata_file, index=False)
df_clean.to_csv(final_metadata_file_clean, index=False)
#df.to_csv(final_metadata_file, index=False)

# (Optional) also save the bad rows for inspection
bad_files = df[cond_short | cond_invalid_ext].copy()
bad_files.to_csv(final_metadata_file_bad, index=False)

print("Step 9: separate bad records")

# ------------------------------
# SAVE final CSV
# ------------------------------
print("Final CSV saved to :")
print(f"   {final_metadata_file}        that contains references to all records")
print(f"   {final_metadata_file_clean}  that contains references to all clean records")
print(f"   {final_metadata_file_bad}    that contains references to all bad records")
print(f"   {final_metadata_file} =  {final_metadata_file_clean} + {final_metadata_file_bad}")


