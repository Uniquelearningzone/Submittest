from flask import Flask, request, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Google Sheets API সেটআপ
SHEET_ID = "1Mfdev8uON-HX5N3Hz6MdTMIGlajA8-L64R5DcoOV3sQ"
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# JSON ফাইল লোড করুন
CREDENTIALS_FILE = "service_account.json"
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, SCOPE)
client = gspread.authorize(credentials)
sheet = client.open_by_key(SHEET_ID).sheet1

@app.route('/submit_name', methods=['POST'])
def submit_name():
    try:
        data = request.get_json()
        name = data.get('name')
        if not name:
            return jsonify({"success": False, "error": "Name is required"}), 400

        # Google Sheet-এ নাম জমা দিন
        sheet.append_row([name])
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
