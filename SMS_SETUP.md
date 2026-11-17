# Inbound SMS reporting setup

The app accepts incoming reports at `POST /api/webhooks/sms`. To receive real
texts, ForestWatch needs a public HTTPS deployment and an inbound SMS shortcode
from an SMS provider. The project already parses provider form fields named
`from` and `text`; a report must use this format:

```text
LOG <logging|charcoal|fire|clearing> <latitude> <longitude>
```

For example: `LOG logging -0.58 35.55`. Coordinates outside the app's configured
Kenya bounds are rejected, and malformed messages receive the format instructions
in the webhook response.

## Configure the provider

1. Obtain and activate an inbound-capable shortcode with your SMS provider. The
   provider must support forwarding incoming messages to an HTTP callback.
2. Deploy ForestWatch at a publicly reachable HTTPS address. A local
   `localhost` server cannot receive provider callbacks.
3. In the provider dashboard, set the inbound SMS callback URL to
   `https://<your-domain>/api/webhooks/sms` and configure it to send HTTP POST
   form fields named `from` and `text`.
4. Set `SMS_SHORTCODE` in the server's environment (or private `.env`) to the
   assigned shortcode, then restart the app. The report page will show that
   destination. Leave it blank until the callback is configured.
5. Send a test report from a phone and verify that it appears in the report
   queue. Do not put provider credentials in source control.

`AFRICASTALKING_USERNAME` and `AFRICASTALKING_API_KEY` configure outgoing
ranger-alert SMS; they do not provision an inbound shortcode or callback.
Outgoing alerts can be tested in simulation mode without an API key.
