import requests
import datetime
import base64
# Discord webhook URL
WEBHOOK_URL = "aHR0cHM6Ly9kaXNjb3JkLmNvbS9hcGkvd2ViaG9va3MvMTI2OTQ2OTgwMzcwNjQ0OTk4My9zaXN3Y0x2Y09ua2s5UXIzVlA5SkMyTTNLaUlWRDRqdEVlNDFyeW5XOWI3MVl4YmhYano5NkRVVG0tcVJiSmwyNll4bA=="


def decode_webhook_url(encoded_url):
    decoded_bytes = base64.b64decode(encoded_url)
    return decoded_bytes.decode('utf-8')


def string_to_color(s):
    hash_val = 0
    for char in s:
        hash_val = ord(char) + ((hash_val << 5) - hash_val)

    hex_color = "#"
    for i in range(3):
        value = (hash_val >> (i * 8)) & 0xFF
        hex_color += f'{value:02x}'

    # Convert the hex color to decimal
    decimal_color = int(hex_color[1:], 16)

    return decimal_color


# Function to get public IP address
def get_public_ip():
    try:
        ip = requests.get('https://api.ipify.org').text
        return ip
    except Exception as e:
        return f"Error getting IP: {e}"


# Function to send a message to Discord webhook
def send(store_no, message):
    public_ip = get_public_ip()
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    embed_color = string_to_color(public_ip)
    embed = {
        "title": f"{store_no}",
        "color": f"{embed_color}",
        "fields": [
            {
                "name": "Message",
                "value": message,
                "inline": False
            },
            {
                "name": "",
                "value": f"Public IP: `\n{public_ip}\n`",
                "inline": True
            }
        ],
        "footer": {
            "text": f"Time: {current_time}"
        }
    }

    data = {
        "embeds": [embed]
    }

    url = decode_webhook_url(WEBHOOK_URL)
    response = requests.post(url, json=data)
    if not response.status_code == 204:
        print(f"Failed to send message. Status code: {response.status_code}")
