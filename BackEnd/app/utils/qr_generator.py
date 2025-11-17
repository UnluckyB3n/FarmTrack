import qrcode
import io
import os
from fastapi.responses import StreamingResponse
from typing import Optional


def generate_qr_code(data: str, size: int = 10, border: int = 2) -> bytes:
    """
    Generate QR code as PNG bytes.
    
    Args:
        data: The data to encode in the QR code
        size: Size of each box in the QR code (default 10)
        border: Border size in boxes (default 2)
    
    Returns:
        PNG image bytes
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf.getvalue()


def generate_qr_response(data: str) -> StreamingResponse:
    """
    Generate QR code and return as streaming response.
    """
    qr_bytes = generate_qr_code(data)
    buf = io.BytesIO(qr_bytes)
    return StreamingResponse(buf, media_type="image/png")


def save_qr_code(data: str, filepath: str, size: int = 10) -> str:
    """
    Generate and save QR code to file.
    
    Args:
        data: The data to encode
        filepath: Path where to save the QR code
        size: Size of each box in the QR code
    
    Returns:
        The filepath where the QR code was saved
    """
    qr_bytes = generate_qr_code(data, size=size)
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    with open(filepath, 'wb') as f:
        f.write(qr_bytes)
    
    return filepath


def generate_animal_qr_url(animal_id: int, base_url: str = "http://localhost:3000") -> str:
    """
    Generate the public tracking URL for an animal.
    
    Args:
        animal_id: The animal's database ID
        base_url: Base URL of the application
    
    Returns:
        Full URL for public animal tracking
    """
    return f"{base_url}/public/{animal_id}"
