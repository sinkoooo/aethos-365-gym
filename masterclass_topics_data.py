# masterclass_topics_data.py
# The 100x Enhanced Masterclass Dataset
# Every item contains:
# - id, title, stageNum, badge, difficulty, readTime, summary
# - guidebook: Deep textbook explanation, first-principles intuition, math, and derivations
# - topologySvg: Dedicated vector diagram for that concept
# - codeSnippet: Real production code in Go/Python/SQL/Lua
# - disasterStudy: Real-world post-mortem outage case study
# - interviewDefense: The exact trap questions and Staff-level script

TOPICS = [
    {
        "id": "c-01-client-server",
        "stageNum": "STAGE 01",
        "badge": "Day 1 Scratch",
        "title": "1.1 The Client-Server Model, Sockets & DNS Hierarchy",
        "difficulty": "Absolute Beginner",
        "readTime": "18 min read",
        "summary": "First principles: What is a computer network? IPv4/IPv6, TCP ports, socket descriptors, and recursive DNS resolution.",
        "guidebook": """
<div class="space-y-6 text-sm text-slate-300 leading-relaxed">
  <div class="p-4 rounded-xl bg-emerald-950/20 border border-emerald-500/20 text-emerald-300">
    <div class="font-bold text-xs uppercase font-mono tracking-wider text-emerald-400 mb-1">First-Principles Intuition</div>
    Imagine you want to send a letter to a specific department in a skyscraper. You need: (1) The street address of the building (<strong>IP Address</strong>), (2) The specific room or department number inside the building (<strong>Port Number</strong>), and (3) A courier who speaks a common protocol so the mailroom clerk understands how to open and hand over the contents (<strong>TCP/IP Protocol</strong>). This physical process is identical to every packet moving across the Internet.
  </div>

  <h4 class="text-base font-bold text-white flex items-center gap-2">
    <span class="w-2 h-2 rounded-full bg-emerald-400"></span> 1. What Physically is a Server?
  </h4>
  <p>
    A "server" is not a mystical entity in the cloud. It is a physical motherboard with CPUs, RAM, and network interface cards (NIC). At the OS level, a server is merely a running process that executes three fundamental system calls:
  </p>
  <div class="p-3.5 rounded-xl bg-slate-950 font-mono text-xs text-cyan-300 border border-slate-800 space-y-1">
    <div>1. <code>fd = socket(AF_INET, SOCK_STREAM, 0)</code> &rarr; Requests an OS network file descriptor.</div>
    <div>2. <code>bind(fd, "0.0.0.0:443")</code> &rarr; Binds that descriptor to Port 443 on all network interfaces.</div>
    <div>3. <code>listen(fd, 1024)</code> &rarr; Sets the OS SYN backlog queue to accept incoming connection requests.</div>
    <div>4. <code>conn = accept(fd)</code> &rarr; Blocks until a client completes the TCP 3-way handshake!</div>
  </div>

  <h4 class="text-base font-bold text-white flex items-center gap-2 mt-6">
    <span class="w-2 h-2 rounded-full bg-emerald-400"></span> 2. DNS Resolution: The 4-Tier Recursive Walk
  </h4>
  <p>
    When you request <code>https://api.stripe.com</code>, your computer does not know where to send packets until DNS translates the hostname to an IP address (e.g. <code>3.218.151.104</code>):
  </p>
  <ol class="list-decimal list-inside space-y-2 text-xs text-slate-300 ml-2">
    <li><strong class="text-white">Local Caches:</strong> Chrome checks internal cache (60s TTL), then OS resolver (<code>/etc/hosts</code> or <code>systemd-resolved</code>).</li>
    <li><strong class="text-white">Recursive Resolver:</strong> ISP DNS or <code>1.1.1.1</code> (Cloudflare). If cache misses, queries the global root.</li>
    <li><strong class="text-white">Root Nameservers (.):</strong> 13 global IP clusters return the Authoritative TLD servers for <code>.com</code>.</li>
    <li><strong class="text-white">TLD Servers (.com):</strong> Maintained by Verisign; returns the Authoritative nameservers for <code>stripe.com</code>.</li>
    <li><strong class="text-white">Authoritative Nameserver:</strong> Returns the final `A` record (IPv4 address) with a Time-To-Live (TTL).</li>
  </ol>
</div>
""",
        "topologySvg": """
<svg viewBox="0 0 740 260" class="w-full h-auto bg-slate-950 rounded-2xl border border-slate-800 p-4" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="90" width="100" height="60" rx="8" fill="#0f172a" stroke="#38bdf8" stroke-width="2"/>
  <text x="70" y="120" fill="#f8fafc" font-size="11" font-weight="bold" text-anchor="middle">Client App</text>
  <text x="70" y="135" fill="#38bdf8" font-size="8" font-family="monospace" text-anchor="middle">Port 54122 (Ephemeral)</text>

  <rect x="180" y="30" width="140" height="60" rx="8" fill="#0f172a" stroke="#10b981" stroke-width="2"/>
  <text x="250" y="58" fill="#34d399" font-size="11" font-weight="bold" text-anchor="middle">DNS Recursive Resolver</text>
  <text x="250" y="74" fill="#94a3b8" font-size="8" font-family="monospace" text-anchor="middle">1.1.1.1 / UDP 53</text>

  <rect x="380" y="30" width="140" height="60" rx="8" fill="#0f172a" stroke="#f59e0b" stroke-width="2"/>
  <text x="450" y="58" fill="#fbbf24" font-size="11" font-weight="bold" text-anchor="middle">Root &amp; TLD DNS</text>
  <text x="450" y="74" fill="#94a3b8" font-size="8" font-family="monospace" text-anchor="middle">Delegates to Authoritative</text>

  <rect x="580" y="90" width="140" height="60" rx="8" fill="#0f172a" stroke="#ec4899" stroke-width="2"/>
  <text x="650" y="118" fill="#f472b6" font-size="11" font-weight="bold" text-anchor="middle">Server (Origin)</text>
  <text x="650" y="134" fill="#10b981" font-size="8" font-family="monospace" text-anchor="middle">Port 443 (TCP Listen)</text>

  <path d="M 120 110 L 180 65" stroke="#10b981" stroke-width="2" stroke-dasharray="4"/>
  <path d="M 320 60 L 380 60" stroke="#f59e0b" stroke-width="2"/>
  <path d="M 120 130 L 580 130" stroke="#38bdf8" stroke-width="2.5"/>
  <text x="350" y="145" fill="#38bdf8" font-size="9" font-family="monospace" text-anchor="middle">TCP 3-Way Handshake + TLS 1.3 Tunnel</text>
</svg>
""",
        "codeSnippet": """
// Minimal Production TCP Echo Server in Go demonstrating Linux Sockets
package main

import (
	"bufio"
	"fmt"
	"net"
	"os"
)

func main() {
	// Binds to TCP Port 8080 across all interfaces
	listener, err := net.Listen("tcp", ":8080")
	if err != nil {
		fmt.Fprintf(os.Stderr, "Socket bind failure: %v\\n", err)
		return
	}
	defer listener.Close()
	fmt.Println("Listening on TCP :8080 (File descriptor bound)")

	for {
		// Blocks until kernel completes 3-way handshake with a client
		conn, err := listener.Accept()
		if err != nil {
			continue
		}
		// Spawn lightweight green thread (goroutine) consuming only ~2KB RAM
		go handleConnection(conn)
	}
}

func handleConnection(conn net.Conn) {
	defer conn.Close()
	scanner := bufio.NewScanner(conn)
	for scanner.Scan() {
		msg := scanner.Text()
		conn.Write([]byte("ACK: " + msg + "\\n"))
	}
}
""",
        "disasterStudy": """
<div class="space-y-3 text-xs text-slate-300">
  <div class="font-bold text-rose-400 font-mono text-sm">Disaster Post-Mortem: The 2016 Dyn Cyberattack (Mirai Botnet)</div>
  <p><strong>The Incident:</strong> On October 21, 2016, millions of IoT devices infected by the Mirai botnet flooded Dyn (a premier DNS provider for Twitter, GitHub, Spotify, and Netflix) with 1.2 Terabits/sec of recursive DNS UDP queries on Port 53.</p>
  <p><strong>Root Cause:</strong> Web clients and browsers cannot connect to an origin server if they cannot resolve its IP address. When Dyn's authoritative nameservers collapsed under SYN/UDP floods, the entire US East Coast lost access to major internet platforms—despite origin application servers being 100% healthy!</p>
  <p><strong>Staff Mitigation:</strong> Never rely on a single DNS provider. Production tier-0 systems run <strong>Dual-DNS with Anycast BGP</strong> (e.g. Route53 + Cloudflare NS delegation) with long NS record TTLs so that client recursive resolvers automatically fail over in &lt;100ms.</p>
</div>
""",
        "interviewDefense": """
<div class="space-y-3 text-xs text-slate-300 font-mono">
  <div class="text-amber-400 font-bold">FAANG Interview Trap Question:</div>
  <div class="p-2.5 rounded bg-slate-900 border border-slate-800 text-white font-sans">
    "Why does DNS operate over UDP (Port 53) rather than TCP, and when does it switch to TCP?"
  </div>
  <div class="text-emerald-400 font-bold">Staff Architect Script:</div>
  <p class="font-sans leading-relaxed">
    "DNS queries are small, single-packet lookups. UDP requires zero handshake overhead (1 RTT total) compared to TCP's 3-way handshake + teardown (4+ packets). However, UDP packets are traditionally limited to 512 bytes (RFC 1035). If a DNS response exceeds 512 bytes (e.g., DNSSEC cryptographic keys or massive IPv6 responses), the server sets the Truncated bit (<code>TC=1</code>) in the header. The client OS immediately drops the UDP socket and retries over <strong>TCP Port 53</strong> to guarantee lossless byte-stream delivery."
  </p>
</div>
"""
    },
    {
        "id": "c-02-http-rest",
        "stageNum": "STAGE 01",
        "badge": "Day 1 Scratch",
        "title": "1.2 HTTP Protocols, REST Design & Idempotency Keys",
        "difficulty": "Beginner",
        "readTime": "20 min read",
        "summary": "Deep dive into HTTP/1.1 vs HTTP/2 vs HTTP/3, status codes, Safe vs Idempotent verbs, and preventing double-charges with Idempotency-Keys.",
        "guidebook": """
<div class="space-y-6 text-sm text-slate-300 leading-relaxed">
  <h4 class="text-base font-bold text-white flex items-center gap-2">
    <span class="w-2 h-2 rounded-full bg-emerald-400"></span> 1. The HTTP Evolution Matrix
  </h4>
  <p>
    HTTP has undergone three generational revolutions:
  </p>
  <ul class="list-disc list-inside space-y-2 text-xs text-slate-300 ml-2">
    <li><strong class="text-white">HTTP/1.1 (1997):</strong> Plaintext headers, persistent TCP connections (Keep-Alive), but suffered from <em>Head-of-Line (HoL) Blocking</em> at the application level. Browsers opened 6 parallel TCP connections per domain to work around this.</li>
    <li><strong class="text-white">HTTP/2 (2015):</strong> Introduced binary framing, HPACK header compression, and multiplexed streams over a single TCP connection. However, a single dropped TCP packet pauses ALL multiplexed streams (TCP-level HoL blocking).</li>
    <li><strong class="text-white">HTTP/3 (QUIC, 2022):</strong> Moves from TCP to UDP. Each stream is cryptographically and packet-wise independent. Packet loss on an image stream never delays an API JSON stream!</li>
  </ul>

  <h4 class="text-base font-bold text-white flex items-center gap-2 mt-6">
    <span class="w-2 h-2 rounded-full bg-emerald-400"></span> 2. The Idempotency Imperative
  </h4>
  <p>
    An operation is <strong>Idempotent</strong> if $f(f(x)) = f(x)$. If an HTTP request times out due to a transient cellular network glitch, the client doesn't know if:
  </p>
  <ul class="list-disc list-inside space-y-1 text-xs text-slate-300 ml-2">
    <li>Scenario A: The request never reached the server (safe to retry).</li>
    <li>Scenario B: The server processed the charge, but the response packet was lost on the wire (retrying charges the customer twice!).</li>
  </ul>
  <p class="text-xs">
    To solve this, clients pass an <code>Idempotency-Key: &lt;UUID&gt;</code> header. The server guarantees atomic single-execution via distributed locks in Redis.
  </p>
</div>
""",
        "topologySvg": """
<svg viewBox="0 0 740 240" class="w-full h-auto bg-slate-950 rounded-2xl border border-slate-800 p-4" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="80" width="120" height="60" rx="8" fill="#0f172a" stroke="#38bdf8" stroke-width="2"/>
  <text x="80" y="110" fill="#f8fafc" font-size="11" font-weight="bold" text-anchor="middle">Client App</text>
  <text x="80" y="125" fill="#38bdf8" font-size="8" font-family="monospace" text-anchor="middle">Idempotency-Key: uuid</text>

  <rect x="220" y="70" width="160" height="80" rx="10" fill="#0f172a" stroke="#10b981" stroke-width="2"/>
  <text x="300" y="98" fill="#34d399" font-size="11" font-weight="bold" text-anchor="middle">API Gateway</text>
  <text x="300" y="115" fill="#94a3b8" font-size="8" font-family="monospace" text-anchor="middle">Atomic Redis Lock</text>
  <text x="300" y="130" fill="#fbbf24" font-size="7" font-family="monospace" text-anchor="middle">Cached JSON Replay</text>

  <rect x="460" y="70" width="150" height="80" rx="10" fill="#0f172a" stroke="#ec4899" stroke-width="2"/>
  <text x="535" y="98" fill="#f472b6" font-size="11" font-weight="bold" text-anchor="middle">Payment Core</text>
  <text x="535" y="115" fill="#94a3b8" font-size="8" font-family="monospace" text-anchor="middle">Executes ONCE</text>

  <path d="M 140 110 L 220 110" stroke="#38bdf8" stroke-width="2"/>
  <path d="M 380 110 L 460 110" stroke="#10b981" stroke-width="2"/>
</svg>
""",
        "codeSnippet": """
// Production Redis Lua Script for Atomic HTTP Idempotency Key Handling
local key = KEYS[1]
local response_val = ARGV[1]
local ttl_seconds = tonumber(ARGV[2])

-- Step 1: Check if key exists
local existing = redis.call('GET', key)
if existing then
    -- Return cached response; do NOT re-execute payment
    return {1, existing}
end

-- Step 2: Key does not exist. Atomically reserve key in PROCESSING state
redis.call('SET', key, '{"status":"PROCESSING"}', 'EX', ttl_seconds)
return {0, 'LOCKED'}
""",
        "disasterStudy": """
<div class="space-y-3 text-xs text-slate-300">
  <div class="font-bold text-rose-400 font-mono text-sm">Disaster Post-Mortem: Uber Double Billing Outage</div>
  <p><strong>The Incident:</strong> During a high-load New Year's Eve event, mobile network instability caused rider payment requests to time out. Riders repeatedly tapped "Confirm Ride", triggering multiple concurrent non-idempotent POST requests that charged credit cards up to 5 times for a single trip.</p>
  <p><strong>Staff Fix:</strong> Enforce client-generated UUID idempotency keys on every mutating POST request. The API gateway locks the key in an in-memory Redis cluster before the payment orchestrator ever touches the banking network.</p>
</div>
""",
        "interviewDefense": """
<div class="space-y-3 text-xs text-slate-300 font-mono">
  <div class="text-amber-400 font-bold">FAANG Interview Trap Question:</div>
  <div class="p-2.5 rounded bg-slate-900 border border-slate-800 text-white font-sans">
    "What is the difference between a 502 Bad Gateway and a 504 Gateway Timeout, and how does the client retry policy differ?"
  </div>
  <div class="text-emerald-400 font-bold">Staff Architect Script:</div>
  <p class="font-sans leading-relaxed">
    "A <strong>502 Bad Gateway</strong> indicates that an intermediary proxy received an invalid response (e.g. TCP connection reset or process crash) from the upstream backend. A <strong>504 Gateway Timeout</strong> indicates the proxy sent the request but the backend did not reply within the configured timeout budget. On a 504 with non-idempotent POST requests, the client MUST NOT blindly retry without an Idempotency-Key, because the backend may still be executing the transaction in the background!"
  </p>
</div>
"""
    }
]

print(f"Masterclass topics dataset loaded with {len(TOPICS)} comprehensive modules.")
