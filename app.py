from flask import Flask, request, jsonify, render_template, redirect, make_response
import jwt
import base64
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

app = Flask(__name__)

@app.route("/admin", methods=["GET"])
def admin():
    token = request.cookies.get("token")
    if not token:
        return "<h1>Unauthorized</h1><p>No token provided</p>", 401

    try:
        headers = jwt.get_unverified_header(token)
        jwk = headers.get("jwk")
        if not jwk:
            return "<h1>Unauthorized</h1><p>No JWK provided</p>", 403

        e = int.from_bytes(base64.urlsafe_b64decode(jwk["e"] + "=="), byteorder="big")
        n = int.from_bytes(base64.urlsafe_b64decode(jwk["n"] + "=="), byteorder="big")

        pub_numbers = rsa.RSAPublicNumbers(e, n)
        pub_key = pub_numbers.public_key()

        payload = jwt.decode(token, key=pub_key, algorithms=["RS256"])
        if payload.get("role") == "admin":
            return f"<h1>Welcome Admin!</h1><p>Username: {payload.get('username')}</p>"
        else:
            return "<h1>Forbidden</h1><p>You are not admin</p>", 403
    except Exception as e:
        return f"<h1>Invalid token</h1><p>{str(e)}</p>", 403


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    # guest 계정으로 로그인
    header = {"alg": "RS256", "typ": "JWT"}
    payload = {"username": "guest", "role": "guest"}

    # 서버에서 실제 사용하는 private key로 서명
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    token = jwt.encode(payload, private_key, algorithm="RS256", headers=header)

    resp = make_response(redirect("/"))
    resp.set_cookie("token", token)
    return resp

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

