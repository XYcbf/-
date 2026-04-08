import sys
from pathlib import Path

def rename_images(folder: Path, pad=3, start=1, recursive=False):
    folder = folder.resolve()
    base = folder.name
    exts = {".jpg", ".jpeg", ".png", ".gif", ".bmp"}
    if recursive:
        files = [p for p in folder.rglob("*") if p.is_file() and p.suffix.lower() in exts]
    else:
        files = [p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in exts]
    files.sort(key=lambda p: p.name)
    i = start
    for p in files:
        new_name = f"action_{base}_{i:0{pad}d}{p.suffix.lower()}"
        target = p.with_name(new_name)
        # Prevent overwriting existing files by skipping or finding next available name
        # Simple approach: just skip if target exists and it's not the same file
        if target.exists() and target != p:
            while target.exists() and target != p:
                i += 1
                new_name = f"action_{base}_{i:0{pad}d}{p.suffix.lower()}"
                target = p.with_name(new_name)
        
        print(f"Renaming: {p.name} -> {target.name}")
        p.rename(target)
        i += 1

if __name__ == "__main__":
    folder_path = ""
    pad = 3
    start = 1
    recursive = False

    if len(sys.argv) > 1:
        folder_path = sys.argv[1]
        pad = int(sys.argv[2]) if len(sys.argv) > 2 else 3
        start = int(sys.argv[3]) if len(sys.argv) > 3 else 1
        recursive = bool(int(sys.argv[4])) if len(sys.argv) > 4 else False
    else:
        print("--- 批量图片重命名工具 ---")
        user_input = input("请输入图片文件夹路径 (默认为当前目录，直接回车): ").strip()
        
        # 处理路径包含引号的情况（如Windows右键复制路径或拖拽）
        if (user_input.startswith('"') and user_input.endswith('"')) or \
           (user_input.startswith("'") and user_input.endswith("'")):
            user_input = user_input[1:-1]
            
        folder_path = user_input if user_input else "."
        
        # 可选：询问其他参数，为了简便这里使用默认值，但提示用户
        print(f"将使用默认设置: 3位序号补零, 起始序号1, 不包含子文件夹")
        confirm = input("按回车继续，或输入 'n' 取消: ")
        if confirm.lower() == 'n':
            sys.exit(0)

    # Handle "." as current directory explicitly if needed, though Path handles it
    folder = Path(folder_path)
    
    if not folder.exists():
        print(f"错误: 文件夹 '{folder_path}' 不存在")
        sys.exit(1)
    
    print(f"开始重命名 '{folder.resolve()}' 下的图片...")
    rename_images(folder, pad=pad, start=start, recursive=recursive)
    print("完成。")
