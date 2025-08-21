import requests
from PIL import Image
import io
import base64

# 1️⃣ Load ảnh
img = Image.open("test.png")

# 2️⃣ Chuyển ảnh sang bytes
buffered = io.BytesIO()
img.save(buffered, format="PNG")
img_bytes = buffered.getvalue()

# 3️⃣ Chuyển bytes sang Base64
img_base64 = base64.b64encode(img_bytes).decode("utf-8")

# 4️⃣ Gửi request
url = "https://api.sctg.xyz/in.php"
payload = {
    "key": "IRLgD0hHa8dNh4hNMuG3nJuWoXjKir9x",
    "method": "MTFaucets",
    "body": img_base64   # nhét Base64 thật vào đây
}
# Thêm tiền tố data:image/png;base64,


headers = {"content-type": "application/x-www-form-urlencoded"}

response = requests.post(url, data=payload, headers=headers)
print(response.text)
