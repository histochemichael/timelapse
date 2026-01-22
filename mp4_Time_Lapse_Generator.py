import os
import re
import glob
import cv2

def natural_key(path: str):
    """
    Sorts like: img2.png < img10.png (natural sort).
    """
    name = os.path.basename(path)
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", name)]

def make_timelapse(
    input_dir: str,
    output_path: str = "timelapse.mp4",
    fps: int = 8,
    pattern: str = "*",
    resize_to: tuple[int, int] | None = None,  # e.g., (1920, 1080)
    codec: str = "mp4v",  # good default for .mp4
):
    # Common image extensions (you can add more)
    exts = (".jpg", ".jpeg", ".png", ".tif", ".tiff", ".bmp", ".webp")

    # Gather files
    files = []
    for ext in exts:
        files.extend(glob.glob(os.path.join(input_dir, f"{pattern}{ext}")))
        files.extend(glob.glob(os.path.join(input_dir, f"{pattern}{ext.upper()}")))

    files = sorted(set(files), key=natural_key)

    if not files:
        raise FileNotFoundError(f"No images found in: {input_dir}")

    # Read first frame to set size
    first = cv2.imread(files[0], cv2.IMREAD_COLOR)
    if first is None:
        raise ValueError(f"Could not read first image: {files[0]}")

    if resize_to is not None:
        frame_w, frame_h = resize_to
        first = cv2.resize(first, (frame_w, frame_h), interpolation=cv2.INTER_AREA)
    else:
        frame_h, frame_w = first.shape[:2]

    fourcc = cv2.VideoWriter_fourcc(*codec)
    writer = cv2.VideoWriter(output_path, fourcc, fps, (frame_w, frame_h))

    if not writer.isOpened():
        raise RuntimeError(
            "Could not open VideoWriter. Try a different codec (e.g., 'avc1') or output extension."
        )

    skipped = 0
    for f in files:
        img = cv2.imread(f, cv2.IMREAD_COLOR)
        if img is None:
            skipped += 1
            continue

        if resize_to is not None:
            img = cv2.resize(img, (frame_w, frame_h), interpolation=cv2.INTER_AREA)
        else:
            # Enforce consistent dimensions (required for video)
            h, w = img.shape[:2]
            if (w, h) != (frame_w, frame_h):
                img = cv2.resize(img, (frame_w, frame_h), interpolation=cv2.INTER_AREA)

        writer.write(img)

    writer.release()
    print(f"✅ Wrote: {output_path}")
    print(f"Frames used: {len(files) - skipped} | Skipped unreadable: {skipped}")

if __name__ == "__main__":
    # Example usage (edit these)
    make_timelapse(
        input_dir=r"C:\Users\micha\OneDrive\Desktop\Jimmy 1.0",
        output_path="timelapse.mp4",
        fps=8,
        pattern="*",           # or "img_" to only match img_*.png/jpg...
        resize_to=None,        # or (1920, 1080)
    )
