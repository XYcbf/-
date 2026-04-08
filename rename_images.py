import sys
import shutil
from pathlib import Path
from typing import Optional, Tuple

VALID_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".bmp"}


def rename_images(
    folder: Path,
    pad=3,
    start=0,
    step=1,
    recursive=False,
    name_prefix=None,
    target_suffix=None,
    save_to_new_folder=False,
):
    folder = folder.resolve()
    base = folder.name
    if not name_prefix:
        name_prefix = f"action_{base}"
    if target_suffix:
        target_suffix = target_suffix.lower()
        if not target_suffix.startswith("."):
            target_suffix = f".{target_suffix}"

    output_dir = folder / sanitize_folder_name(name_prefix) if save_to_new_folder else None

    if recursive:
        files = [p for p in folder.rglob("*") if p.is_file() and p.suffix.lower() in VALID_EXTS]
    else:
        files = [p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in VALID_EXTS]
    if output_dir:
        files = [p for p in files if not is_inside_directory(p, output_dir)]
    files.sort(key=lambda p: p.name)
    if output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)
        print(f"输出目录: {output_dir}")
    i = start
    for p in files:
        suffix = target_suffix if target_suffix else p.suffix.lower()
        new_name = f"{name_prefix}_{i:0{pad}d}{suffix}"
        target = (output_dir / new_name) if output_dir else p.with_name(new_name)
        if target.exists() and target != p:
            while target.exists() and target != p:
                i += step
                new_name = f"{name_prefix}_{i:0{pad}d}{suffix}"
                target = (output_dir / new_name) if output_dir else p.with_name(new_name)

        print(f"处理: {p.name} -> {target.name}")
        if output_dir:
            shutil.copy2(p, target)
        else:
            p.rename(target)
        i += step


def normalize_path_input(value: str) -> str:
    value = value.strip()
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        value = value[1:-1]
    return value


def ask_name_prefix(default_prefix: str) -> str:
    while True:
        typed = input(f"请输入基础文件名（默认: {default_prefix}）: ").strip()
        prefix = typed if typed else default_prefix
        confirm = input(f"确认基础文件名为 '{prefix}' 吗？(回车确认，输入 n 重新输入): ").strip().lower()
        if confirm != "n":
            return prefix


def ask_suffix_choice() -> Optional[str]:
    options = {
        "0": None,
        "1": ".jpg",
        "2": ".jpeg",
        "3": ".png",
        "4": ".gif",
        "5": ".bmp",
    }
    print("请选择统一后缀：")
    print("0) 保持原后缀")
    print("1) .jpg")
    print("2) .jpeg")
    print("3) .png")
    print("4) .gif")
    print("5) .bmp")
    while True:
        choice = input("输入后缀选项编号（默认 0）: ").strip()
        if not choice:
            return None
        if choice in options:
            return options[choice]
        print("输入无效，请重新输入 0-5。")


def ask_first_suffix_number() -> Tuple[int, int]:
    while True:
        typed = input("请输入首张图片的后缀编号（如01、02、03，默认01）: ").strip()
        if not typed:
            typed = "01"
        if typed.isdigit():
            return int(typed), len(typed)
        print("请输入纯数字编号。")


def ask_increment_step() -> int:
    options = {"1", "2", "3"}
    while True:
        typed = input("后续递增数（可选 1、2、3，默认 1）: ").strip()
        if not typed:
            return 1
        if typed in options:
            return int(typed)
        print("输入无效，请输入 1、2 或 3。")


def ask_output_mode() -> bool:
    print("请选择输出方式：")
    print("1) 覆盖当前文件名")
    print("2) 保存到新文件夹（文件夹名=基础文件名）")
    while True:
        typed = input("输入选项编号（默认 1）: ").strip()
        if not typed or typed == "1":
            return False
        if typed == "2":
            return True
        print("输入无效，请输入 1 或 2。")


def sanitize_folder_name(name: str) -> str:
    invalid_chars = '<>:"/\\|?*'
    cleaned = "".join("_" if ch in invalid_chars else ch for ch in name).strip().rstrip(".")
    return cleaned if cleaned else "renamed_images"


def is_inside_directory(path: Path, directory: Path) -> bool:
    try:
        path.resolve().relative_to(directory.resolve())
        return True
    except ValueError:
        return False


if __name__ == "__main__":
    folder_path = ""
    pad = 3
    start = 0
    step = 1
    recursive = False
    name_prefix = None
    target_suffix = None
    save_to_new_folder = False

    if len(sys.argv) > 1:
        folder_path = normalize_path_input(sys.argv[1])
        pad = int(sys.argv[2]) if len(sys.argv) > 2 else 3
        start = int(sys.argv[3]) if len(sys.argv) > 3 else 0
        if start < 0:
            start = 0
        recursive = bool(int(sys.argv[4])) if len(sys.argv) > 4 else False
        name_prefix = sys.argv[5].strip() if len(sys.argv) > 5 and sys.argv[5].strip() else None
        if len(sys.argv) > 6 and sys.argv[6].strip():
            raw_suffix = sys.argv[6].strip().lower()
            target_suffix = None if raw_suffix in {"0", "none", "keep", "original"} else raw_suffix
        step = int(sys.argv[7]) if len(sys.argv) > 7 else 1
        if step not in {1, 2, 3}:
            step = 1
        save_to_new_folder = bool(int(sys.argv[8])) if len(sys.argv) > 8 else False
    else:
        print("--- 批量图片重命名工具 ---")
        user_input = input("请输入图片文件夹路径 (默认为当前目录，直接回车): ")
        user_input = normalize_path_input(user_input)
        folder_path = user_input if user_input else "."
        default_prefix = f"action_{Path(folder_path).resolve().name}"
        name_prefix = ask_name_prefix(default_prefix)
        target_suffix = ask_suffix_choice()
        start, pad = ask_first_suffix_number()
        step = ask_increment_step()
        save_to_new_folder = ask_output_mode()
        print("将使用默认设置: 不包含子文件夹")
        confirm = input("按回车继续，或输入 'n' 取消: ")
        if confirm.lower() == "n":
            sys.exit(0)

    folder = Path(folder_path)

    if not folder.exists() or not folder.is_dir():
        print(f"错误: 文件夹 '{folder_path}' 不存在")
        sys.exit(1)

    print(f"开始重命名 '{folder.resolve()}' 下的图片...")
    rename_images(
        folder,
        pad=pad,
        start=start,
        step=step,
        recursive=recursive,
        name_prefix=name_prefix,
        target_suffix=target_suffix,
        save_to_new_folder=save_to_new_folder,
    )
    print("完成。")
