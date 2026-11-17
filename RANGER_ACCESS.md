# Ranger access setup

The ranger dashboard and its report queue, status-update, and SMS-dispatch APIs require a ranger session. Configure access on the server before signing in; there is no default password.

1. Copy `.env.example` to `.env`.
2. Generate a random Flask session key:

   ```sh
   forest/bin/python -c 'import secrets; print(secrets.token_hex(32))'
   ```

   Put the result in `SECRET_KEY`.

3. Generate a password hash. Enter the ranger password at the hidden prompt, then put the printed hash in `RANGER_PASSWORD_HASH`:

   ```sh
   forest/bin/python -c 'from getpass import getpass; from werkzeug.security import generate_password_hash; print(generate_password_hash(getpass()))'
   ```

4. Restart the app. For a production deployment over HTTPS, set `SESSION_COOKIE_SECURE=true`; keep it false only for local HTTP development.

Use the **Ranger sign in** link in the top navigation (or the shield icon beside the logo) to open the password form. A successful sign-in lasts up to eight hours, and the dashboard provides a sign-out action. Keep `.env` private and do not commit it. For an internet-facing deployment, serve the app over HTTPS and apply request-rate limiting to the sign-in endpoint at the web server or proxy.
