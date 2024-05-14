from PIL import Image

UPLOAD_FOLDER = 'logos'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg','webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_image(file):
    try:
        img = Image.open(file)
        img.verify()  # Verify if it's a valid image
        return True, img.size
    except Exception as e:
        return False, None


def optimize_image(file, output_path, max_size=(128, 128), quality=85):
    img = Image.open(file)
    img.thumbnail(max_size)
    img.save(output_path, optimize=True, quality=quality)