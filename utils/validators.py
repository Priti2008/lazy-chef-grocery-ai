def validate_image(uploaded_file):
    if uploaded_file is None:
        return False, "No file uploaded."
    if uploaded_file.type not in ["image/jpeg", "image/png", "image/jpg"]:
        return False, "Unsupported format."
    return True, "Valid."
