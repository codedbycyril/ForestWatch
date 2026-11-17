# services/sms_service.py
# Sends an SMS, or simulates sending one.
from flask import current_app


def send_sms(to, message):
    """Send `message` to phone number `to`. Returns a status word."""
    api_key = current_app.config["AT_API_KEY"]

    # No API key set: simulate by printing to the terminal.
    if not api_key:
        print(f"[SIMULATED SMS to {to}] {message}")
        return "simulated"

    # API key set: try to send a real SMS through Africa's Talking.
    try:
        import africastalking   # only needed in real mode: pip install africastalking
        africastalking.initialize(current_app.config["AT_USERNAME"], api_key)
        africastalking.SMS.send(message, [to])
        return "sent"
    except Exception as error:
        # Never crash the app because an SMS failed; report it instead.
        return f"failed: {error}"
