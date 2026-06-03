import base64

def image_to_b64(uploaded_file) -> str:
    """Convert an UploadedFile / camera bytes to a base64 data URI."""
    raw = uploaded_file.getvalue()
    mime = getattr(uploaded_file, "type", "image/jpeg") or "image/jpeg"
    return f"data:{mime};base64,{base64.b64encode(raw).decode()}"