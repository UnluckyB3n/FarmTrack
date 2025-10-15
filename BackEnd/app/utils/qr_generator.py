import qrcode
import io
from fastapi.responses import StreamingResponse

def generate_qr(data: str):
    qr = qrcode.make(data)
    buf = io.BytesIO()
    qr.save(buf, format="PNG")
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")
