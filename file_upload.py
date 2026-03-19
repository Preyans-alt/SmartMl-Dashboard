import cloudinary
import cloudinary.uploader

cloudinary.config(
    cloud_name="dozdx07oc",
    api_key="774812788277311",
    api_secret="PJJ8eORwXl4AdhBhqyk8Or83Iks"
)

def upload_file(file):
    file_link = cloudinary.uploader.upload(file,resource_type="raw")
    return file_link['secure_url']