# network_helpers.py

import socket
from zeroconf import Zeroconf, ServiceInfo

def run_flask_app(app, host: str = "0.0.0.0", port: int = 5000):
    """Starts Flask app on a background thread (no reloader)."""
    app.run(host=host, port=port, debug=False, use_reloader=False)

def register_mdns(hostname: str, port: int) -> Zeroconf:
    """Advertise http://<hostname>.local:<port> via mDNS."""
    ip = socket.gethostbyname(socket.gethostname())
    addr = socket.inet_aton(ip)

    info = ServiceInfo(
        type_="_http._tcp.local.",
        name=f"{hostname}._http._tcp.local.",
        addresses=[addr],
        port=port,
        properties={},
        server=f"{hostname}.local."
    )

    zeroconf = Zeroconf()
    zeroconf.register_service(info)
    print(f"mDNS: http://{hostname}.local:{port}/")
    return zeroconf
