"""Parking Fine Appeal Generator — pay £7.99, get a professional appeal letter PDF."""
from dotenv import load_dotenv
load_dotenv()

import os, uuid, json, logging
from pathlib import Path
from flask import Flask, request, jsonify, send_file, redirect, session, render_template_string
import stripe
import io

from generator import generate_letter, FINE_TYPES, GROUNDS
from pdf_gen import make_pdf

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "appeal-secret-2026")

stripe.api_key  = os.environ.get("STRIPE_SECRET_KEY", "")
PRICE_ID        = os.environ.get("STRIPE_PRICE_ID", "")   # one-time £7.99
BASE_URL        = os.environ.get("BASE_URL", "http://127.0.0.1:5052")

# Temporary in-memory store for generated letters (keyed by token)
# On Render this resets on restart — tokens are short-lived intentionally
_letters: dict[str, dict] = {}


# ── pages ─────────────────────────────────────────────────────────────────────

LANDING = open(Path(__file__).parent / "templates" / "landing.html", encoding="utf-8").read()
FORM    = open(Path(__file__).parent / "templates" / "form.html", encoding="utf-8").read()


@app.route("/")
def index():
    return render_template_string(LANDING)


@app.route("/appeal")
def appeal_form():
    return render_template_string(FORM,
        fine_types=FINE_TYPES, grounds=GROUNDS)


@app.route("/preview", methods=["POST"])
def preview():
    """Generate letter, store it, redirect to Stripe."""
    data  = request.form.to_dict()
    token = str(uuid.uuid4()).replace("-", "")
    letter = generate_letter(data)
    _letters[token] = {"letter": letter, "data": data, "paid": False}

    if not stripe.api_key or not PRICE_ID:
        # Dev mode — skip payment
        _letters[token]["paid"] = True
        return redirect(f"/download/{token}")

    try:
        session_obj = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{"price": PRICE_ID, "quantity": 1}],
            mode="payment",
            success_url=f"{BASE_URL}/download/{token}",
            cancel_url=f"{BASE_URL}/appeal",
            metadata={"token": token},
        )
        _letters[token]["stripe_session"] = session_obj.id
        return redirect(session_obj.url, code=303)
    except Exception as exc:
        log.error("Stripe error: %s", exc)
        # Fallback: serve without payment in dev
        _letters[token]["paid"] = True
        return redirect(f"/download/{token}")


@app.route("/download/<token>")
def download(token: str):
    record = _letters.get(token)
    if not record:
        return "Letter not found or expired. Please generate a new appeal.", 404

    # Verify payment with Stripe if we have a session
    if not record.get("paid"):
        sid = record.get("stripe_session")
        if sid and stripe.api_key:
            try:
                s = stripe.checkout.Session.retrieve(sid)
                if s.payment_status == "paid":
                    record["paid"] = True
            except Exception:
                pass

    if not record.get("paid") and stripe.api_key:
        return redirect(f"/appeal?error=payment_required")

    data   = record["data"]
    letter = record["letter"]
    pdf    = make_pdf(letter, data.get("pcn_ref", "APPEAL"))
    fname  = f"parking_appeal_{data.get('pcn_ref','LETTER').replace(' ','_')}.pdf"

    return send_file(
        io.BytesIO(pdf),
        mimetype="application/pdf",
        as_attachment=True,
        download_name=fname,
    )


@app.route("/sample")
def sample():
    """Free sample letter — no payment — drives conversions."""
    sample_data = {
        "fine_type":   "council_pcn",
        "ground":      "no_sign",
        "pcn_ref":     "AB12345678",
        "vehicle_reg": "XX22 XXX",
        "fine_date":   "1 January 2026",
        "location":    "Example Street, Brighton",
        "your_name":   "Your Name",
        "your_address": "Your Address\nYour Town\nPostcode",
        "issuer_name": "Brighton & Hove City Council",
        "extra_info":  "",
    }
    letter = generate_letter(sample_data)
    pdf    = make_pdf(letter, "SAMPLE")
    return send_file(
        io.BytesIO(pdf),
        mimetype="application/pdf",
        as_attachment=False,
        download_name="sample_appeal_letter.pdf",
    )


@app.route("/health")
def health():
    return jsonify({"ok": True})


if __name__ == "__main__":
    import webbrowser
    webbrowser.open("http://127.0.0.1:5052")
    app.run(port=5052, debug=False)
