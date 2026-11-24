from pathlib import Path
import argparse
PROJECTS = ("QuizNote","Octopus","Ouroboros","Cerberus","Fenrir","SteadyTrade")
def bootstrap(root, checkout):
    root, checkout = Path(root).resolve(), Path(checkout).resolve()
    if root == checkout or checkout in root.parents or root in checkout.parents:
        raise ValueError("vault must be separate from checkout")
    if any((p / ".git").exists() for p in (root, *root.parents)):
        raise ValueError("vault must not be inside Git")
    root.mkdir(parents=True, exist_ok=True)
    folders = ["00_Dashboard"] + [f"{i:02}_{p}" for i,p in enumerate(PROJECTS,1)] + ["07_Shared_Knowledge","08_Evidence","09_Research","10_Inbox","11_Archive"]
    for name in folders:
        folder = root / name
        if folder.is_symlink() or folder.resolve().parent != root:
            raise ValueError("unsafe folder")
        folder.mkdir(exist_ok=True)
    def write_once(note, content):
        if note.is_symlink():
            raise ValueError("unsafe note")
        try:
            with note.open("x", encoding="utf-8") as f:
                f.write(content)
        except FileExistsError:
            pass
    write_once(root/"00_Dashboard"/"Home.md", "# AURA Knowledge Vault\n\n" + "\n".join(f"- [[{i:02}_{p}/Index|{p}]]" for i,p in enumerate(PROJECTS,1)) + "\n")
    for i,p in enumerate(PROJECTS,1):
        write_once(root/f"{i:02}_{p}"/"Index.md", f"# {p}\n\nLocal knowledge only.\n")
    return root
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("vault")
    args = parser.parse_args()
    print(bootstrap(args.vault, Path(__file__).resolve().parents[1]))
