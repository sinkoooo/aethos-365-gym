# curriculum_stage1_data.py
# Stage 1: Day 1 Beginner - Foundations of Web, Servers & Network Sockets

STAGE_1_CHAPTERS = [
    {
        "id": "c-01-client-server",
        "stageId": "stage-1",
        "stageNum": "STAGE 01",
        "badge": "Day 1 Scratch",
        "color": "emerald",
        "title": "1.1 The Client-Server Model, Sockets & DNS Hierarchy",
        "difficulty": "Absolute Beginner",
        "readTime": "18 min read",
        "simulatorKey": "tracer",
        "summary": "First principles: What physically is a server? Network interface cards, OS socket descriptors, TCP 3-way handshakes, and 4-tier recursive DNS resolution.",
        "guidebook": """
<div class="space-y-6 text-sm text-slate-300 leading-relaxed">
  <div class="p-4 rounded-xl bg-emerald-950/20 border border-emerald-500/20 text-emerald-300">
    <div class="font-bold text-xs uppercase font-mono tracking-wider text-emerald-400 mb-1">First-Principles Intuition (Day 1 Beginner)</div>
    Imagine you want to send a physical letter to a specific employee in a 100-story corporate headquarters across the world. You need three fundamental pieces of information:
    <ul class="list-disc list-inside mt-2 space-y-1 text-xs text-emerald-200">
      <li><strong>IP Address:</strong> The physical street address of the building on Earth (e.g., <code>142.250.190.46</code>).</li>
      <li><strong>Port Number:</strong> The exact room or desk number inside that building (e.g., Port 443 for HTTPS, Port 5432 for Postgres).</li>
      <li><strong>TCP/IP Protocol:</strong> The agreed-upon language and postal courier rules so the mailroom clerk knows how to verify delivery, handle lost mail, and acknowledge receipt.</li>
    </ul>
    This physical process is <em>identical</em> to every single packet moving across the global Internet.
  </div>

  <h4 class="text-base font-bold text-white flex items-center gap-2">
    <span class="w-2 h-2 rounded-full bg-emerald-400"></span> 1. What Physically is a "Server"?
  </h4>
  <p>
    A "server" is not a magical cloud entity. It is a physical motherboard equipped with multi-core CPUs, ECC RAM, and high-speed Network Interface Cards (NICs) connected to fiber-optic switches.
    At the operating system level, a server is simply an ordinary user-space software program that invokes four foundational POSIX system calls:
  </p>
  <div class="p-4 rounded-xl bg-slate-950 font-mono text-xs text-cyan-300 border border-slate-800 space-y-1.5">
    <div>1. <code>fd = socket(AF_INET, SOCK_STREAM, 0)</code> &rarr; Allocates an OS file descriptor for a network stream.</div>
    <div>2. <code>bind(fd, "0.0.0.0:443")</code> &rarr; Binds that descriptor to Port 443 across all local network interfaces.</div>
    <div>3. <code>listen(fd, 1024)</code> &rarr; Creates the kernel SYN backlog queue to accept incoming connection requests.</div>
    <div>4. <code>client_fd = accept(fd)</code> &rarr; Blocks execution until the kernel finishes a TCP 3-way handshake with a remote client!</div>
  </div>

  <h4 class="text-base font-bold text-white flex items-center gap-2 mt-6">
    <span class="w-2 h-2 rounded-full bg-emerald-400"></span> 2. The TCP 3-Way Handshake &amp; State Machine
  </h4>
  <p>
    Before an HTTP request or JSON payload can be sent, TCP guarantees reliable, in-order byte stream delivery through a synchronized exchange of sequence numbers ($ISN$):
  </p>
  <div class="overflow-x-auto">
    <table class="w-full text-xs text-left border border-slate-800 rounded-lg overflow-hidden font-mono">
      <thead class="bg-slate-900 text-slate-400">
        <tr>
          <th class="p-2.5">Step</th>
          <th class="p-2.5">Sender &rarr; Receiver</th>
          <th class="p-2.5">Flags Set</th>
          <th class="p-2.5">Kernel State</th>
          <th class="p-2.5">Physical Purpose</th>
        </tr>
      </thead>
      <tbody class="divide-y divide-slate-800/60 text-slate-300 bg-slate-950">
        <tr>
          <td class="p-2.5 text-cyan-400 font-bold">1. SYN</td>
          <td class="p-2.5">Client &rarr; Server</td>
          <td class="p-2.5 text-amber-400">SYN=1, Seq=X</td>
          <td class="p-2.5">SYN_SENT &rarr; SYN_RCVD</td>
          <td class="p-2.5">Client proposes its initial random sequence number $X$.</td>
        </tr>
        <tr>
          <td class="p-2.5 text-emerald-400 font-bold">2. SYN-ACK</td>
          <td class="p-2.5">Server &rarr; Client</td>
          <td class="p-2.5 text-emerald-400">SYN=1, ACK=1, Seq=Y, Ack=X+1</td>
          <td class="p-2.5">SYN_RCVD &rarr; ESTABLISHED</td>
          <td class="p-2.5">Server acknowledges $X$ and proposes its own sequence number $Y$.</td>
        </tr>
        <tr>
          <td class="p-2.5 text-fuchsia-400 font-bold">3. ACK</td>
          <td class="p-2.5">Client &rarr; Server</td>
          <td class="p-2.5 text-cyan-400">ACK=1, Ack=Y+1</td>
          <td class="p-2.5">ESTABLISHED</td>
          <td class="p-2.5">Full duplex connection established! Application payload can now fly.</td>
        </tr>
      </tbody>
    </table>
  </div>

  <h4 class="text-base font-bold text-white flex items-center gap-2 mt-6">
    <span class="w-2 h-2 rounded-full bg-emerald-400"></span> 3. DNS Resolution: The 4-Tier Recursive Walk
  </h4>
  <p>
    When you enter <code>https://api.stripe.com</code> into your browser, the operating system has zero knowledge of where to route network packets. The Domain Name System (DNS) performs a hierarchical walk:
  </p>
  <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
    <div class="p-3.5 rounded-xl bg-slate-950 border border-slate-800 space-y-1">
      <div class="text-cyan-400 font-bold font-mono">Tier 1: Browser &amp; OS Resolvers</div>
      <p class="text-slate-400">Chrome checks its internal 60-second DNS cache. If missed, invokes OS resolver (<code>/etc/hosts</code> or Windows DNS Client service).</p>
    </div>
    <div class="p-3.5 rounded-xl bg-slate-950 border border-slate-800 space-y-1">
      <div class="text-emerald-400 font-bold font-mono">Tier 2: Recursive ISP / Public DNS</div>
      <p class="text-slate-400">Queries Cloudflare (<code>1.1.1.1</code>) or Google (<code>8.8.8.8</code>). If not cached, the recursive resolver walks the global internet root on your behalf.</p>
    </div>
    <div class="p-3.5 rounded-xl bg-slate-950 border border-slate-800 space-y-1">
      <div class="text-amber-400 font-bold font-mono">Tier 3: 13 Root Nameserver Clusters (.)</div>
      <p class="text-slate-400">13 global root server IP addresses (managed by ICANN/IANA) respond with the authoritative nameservers for the <code>.com</code> Top-Level Domain (TLD).</p>
    </div>
    <div class="p-3.5 rounded-xl bg-slate-950 border border-slate-800 space-y-1">
      <div class="text-fuchsia-400 font-bold font-mono">Tier 4: Authoritative Nameservers</div>
      <p class="text-slate-400">Verisign (for <code>.com</code>) delegates to Stripe's Route53/Cloudflare nameservers, which return the final `A` record (e.g. <code>3.218.151.104</code>) with a TTL.</p>
    </div>
  </div>

  <h4 class="text-base font-bold text-white flex items-center gap-2 mt-6">
    <span class="w-2 h-2 rounded-full bg-emerald-400"></span> 4. Mathematical Latency Budgets &amp; Invariants
  </h4>
  <p>
    The speed of light in fiber optic glass is roughly $200,000\,\text{km/s}$ (approx. $5\,\mu\text{s}$ per kilometer). A round-trip query from San Francisco to London ($10,000\,\text{km}$) has an unchangeable physical lower bound:
  </p>
  <div class="p-3.5 rounded-xl bg-slate-950 font-mono text-xs text-amber-300 border border-slate-800">
    $$\text{RTT}_{\text{min}} = \frac{2 \times 10,000\,\text{km}}{200,000\,\text{km/s}} = 100\,\text{ms}$$
    With TCP (1 RTT) + TLS 1.3 (1 RTT), connection setup takes $200\,\text{ms}$ BEFORE the first byte of application data is sent! This physical reality is why Content Delivery Networks (CDNs) and Edge termination are mandatory.
  </div>
</div>
""",
        "topologySvg": """
<svg viewBox="0 0 960 380" class="w-full h-auto bg-slate-950 rounded-2xl border border-slate-800 p-4" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="g-client" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#0284c7"/><stop offset="100%" stop-color="#0369a1"/></linearGradient>
    <linearGradient id="g-dns" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#059669"/><stop offset="100%" stop-color="#047857"/></linearGradient>
    <linearGradient id="g-server" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#7c3aed"/><stop offset="100%" stop-color="#6d28d9"/></linearGradient>
    <marker id="arr-c" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 1 L 10 5 L 0 9 z" fill="#38bdf8"/></marker>
    <marker id="arr-g" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 1 L 10 5 L 0 9 z" fill="#34d399"/></marker>
    <marker id="arr-m" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 1 L 10 5 L 0 9 z" fill="#c084fc"/></marker>
  </defs>

  <rect width="100%" height="100%" fill="#07090e" rx="12"/>

  <!-- TIER 1: CLIENT -->
  <g transform="translate(30, 130)">
    <rect width="170" height="120" rx="10" fill="url(#g-client)" stroke="#38bdf8" stroke-width="1.5"/>
    <text x="16" y="28" fill="#ffffff" font-size="12" font-family="sans-serif" font-weight="bold">Client Application</text>
    <text x="16" y="48" fill="#bae6fd" font-size="9" font-family="monospace">IP: 198.51.100.24</text>
    <text x="16" y="66" fill="#e0f2fe" font-size="9" font-family="monospace">Ephemeral Port: 54122</text>
    <rect x="16" y="78" width="138" height="24" rx="4" fill="#0c4a6e"/>
    <text x="24" y="94" fill="#38bdf8" font-size="8" font-family="monospace">socket(AF_INET, TCP)</text>
  </g>

  <!-- TIER 2: DNS RESOLUTION HIERARCHY -->
  <g transform="translate(260, 30)">
    <rect width="200" height="90" rx="10" fill="url(#g-dns)" stroke="#34d399" stroke-width="1.5"/>
    <text x="16" y="26" fill="#ffffff" font-size="11" font-family="sans-serif" font-weight="bold">Recursive DNS Resolver</text>
    <text x="16" y="44" fill="#a7f3d0" font-size="9" font-family="monospace">1.1.1.1 (Cloudflare Anycast)</text>
    <text x="16" y="62" fill="#d1fae5" font-size="8" font-family="sans-serif">UDP Port 53 &bull; Max 512B</text>
    <text x="16" y="78" fill="#6ee7b7" font-size="8" font-family="monospace">Checks TTL Cache First</text>
  </g>

  <g transform="translate(520, 30)">
    <rect width="200" height="90" rx="10" fill="#1e293b" stroke="#64748b" stroke-width="1.5"/>
    <text x="16" y="26" fill="#f8fafc" font-size="11" font-family="sans-serif" font-weight="bold">Authoritative DNS</text>
    <text x="16" y="44" fill="#94a3b8" font-size="9" font-family="monospace">ns-1.awsdns.com</text>
    <text x="16" y="62" fill="#cbd5e1" font-size="8" font-family="sans-serif">Holds Zone Apex &amp; Records</text>
    <text x="16" y="78" fill="#facc15" font-size="8" font-family="monospace">A &rarr; 3.218.151.104 (TTL 300)</text>
  </g>

  <!-- TIER 3: ORIGIN SERVER -->
  <g transform="translate(760, 130)">
    <rect width="170" height="120" rx="10" fill="url(#g-server)" stroke="#c084fc" stroke-width="1.5"/>
    <text x="16" y="28" fill="#ffffff" font-size="12" font-family="sans-serif" font-weight="bold">Origin Server</text>
    <text x="16" y="48" fill="#e9d5ff" font-size="9" font-family="monospace">IP: 3.218.151.104</text>
    <text x="16" y="66" fill="#f3e8ff" font-size="9" font-family="monospace">Bound Port: 443 (HTTPS)</text>
    <rect x="16" y="78" width="138" height="24" rx="4" fill="#4c1d95"/>
    <text x="24" y="94" fill="#c084fc" font-size="8" font-family="monospace">listen(somaxconn=4096)</text>
  </g>

  <!-- FLOW ARROWS -->
  <!-- 1. DNS Query -->
  <path d="M 170 130 Q 210 75 260 75" fill="none" stroke="#34d399" stroke-width="2" stroke-dasharray="4" marker-end="url(#arr-g)"/>
  <text x="175" y="80" fill="#34d399" font-size="8" font-family="monospace">1. DNS Lookup</text>

  <!-- 2. Recursive to Auth -->
  <path d="M 460 75 L 520 75" fill="none" stroke="#64748b" stroke-width="2" marker-end="url(#arr-c)"/>
  <text x="465" y="68" fill="#94a3b8" font-size="8" font-family="monospace">2. Query</text>

  <!-- 3. Return IP -->
  <path d="M 360 120 Q 300 160 200 160" fill="none" stroke="#34d399" stroke-width="2" stroke-dasharray="4" marker-end="url(#arr-g)"/>
  <text x="250" y="150" fill="#34d399" font-size="8" font-family="monospace">3. IP: 3.218.151.104</text>

  <!-- 4. TCP 3-Way Handshake -->
  <path d="M 200 190 L 760 190" fill="none" stroke="#38bdf8" stroke-width="2.5" marker-end="url(#arr-c)"/>
  <text x="440" y="182" fill="#38bdf8" font-size="9" font-family="monospace" text-anchor="middle">4. TCP 3-Way Handshake (SYN &rarr; SYN-ACK &rarr; ACK)</text>

  <!-- 5. TLS 1.3 Tunnel -->
  <path d="M 760 220 L 200 220" fill="none" stroke="#c084fc" stroke-width="2" marker-end="url(#arr-m)"/>
  <text x="440" y="235" fill="#c084fc" font-size="9" font-family="monospace" text-anchor="middle">5. TLS 1.3 Handshake + Encrypted HTTP/2 Application Data</text>

  <!-- LEGEND FOOTER -->
  <g transform="translate(30, 310)">
    <rect width="900" height="50" rx="8" fill="#0f172a" stroke="#1e293b"/>
    <text x="16" y="20" fill="#94a3b8" font-size="8" font-family="monospace">STEP-BY-STEP PACKET TIMELINE</text>
    <text x="16" y="38" fill="#e2e8f0" font-size="9" font-family="sans-serif">
      DNS Resolution: 15-40ms (UDP) &bull; TCP Handshake: 1 RTT (50ms) &bull; TLS 1.3 Session: 1 RTT (50ms) &bull; First Application Byte: ~140ms Total Latency
    </text>
  </g>
</svg>
""",
        "codeSnippet": """// Production-Grade Concurrent TCP Server in Go
// Demonstrating OS Sockets, Keep-Alive, Context Deadlines & Graceful Shutdown
package main

import (
	"bufio"
	"context"
	"fmt"
	"net"
	"os"
	"os/signal"
	"syscall"
	"time"
)

const (
	BindAddress    = "0.0.0.0:8080"
	ReadTimeout    = 5 * time.Second
	WriteTimeout   = 5 * time.Second
	MaxConnections = 10000
)

func main() {
	// Step 1: Open listening socket on all interfaces
	config := net.ListenConfig{
		Control: func(network, address string, c syscall.RawConn) error {
			var operr error
			// Set SO_REUSEPORT to allow zero-downtime rolling upgrades
			err := c.Control(func(fd uintptr) {
				operr = syscall.SetsockoptInt(int(fd), syscall.SOL_SOCKET, syscall.SO_REUSEADDR, 1)
			})
			if err != nil {
				return err
			}
			return operr
		},
	}

	listener, err := config.Listen(context.Background(), "tcp", BindAddress)
	if err != nil {
		fmt.Printf("Fatal: failed to bind socket: %v\\n", err)
		os.Exit(1)
	}
	defer listener.Close()
	fmt.Printf("[KERNEL] Socket bound to %s (somaxconn queue active)\\n", BindAddress)

	// Step 2: Handle OS interrupt signals for graceful drain
	shutdownCtx, stop := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
	defer stop()

	connLimiter := make(chan struct{}, MaxConnections)

	go func() {
		for {
			conn, err := listener.Accept()
			if err != nil {
				select {
				case <-shutdownCtx.Done():
					return // Normal shutdown
				default:
					continue
				}
			}

			// Acquire slot from concurrency limiter
			connLimiter <- struct{}{}
			go func(c net.Conn) {
				defer func() { <-connLimiter }()
				handleClient(c)
			}(conn)
		}
	}()

	<-shutdownCtx.Done()
	fmt.Println("\\n[SHUTDOWN] Draining active TCP connections gracefully...")
}

func handleClient(conn net.Conn) {
	defer conn.Close()

	// Enforce kernel TCP read and write deadlines to prevent Slowloris resource exhaustion
	_ = conn.SetReadDeadline(time.Now().Add(ReadTimeout))
	_ = conn.SetWriteDeadline(time.Now().Add(WriteTimeout))

	reader := bufio.NewReader(conn)
	for {
		msg, err := reader.ReadString('\\n')
		if err != nil {
			return // Connection closed by client or timed out
		}

		// Echo back with protocol ACK header
		_ = conn.SetWriteDeadline(time.Now().Add(WriteTimeout))
		response := fmt.Sprintf("ACK [LEN=%d]: %s", len(msg), msg)
		if _, err := conn.Write([]byte(response)); err != nil {
			return
		}
		// Reset read deadline for subsequent request in keep-alive session
		_ = conn.SetReadDeadline(time.Now().Add(ReadTimeout))
	}
}
""",
        "disasterStudy": """
<div class="space-y-4 text-xs text-slate-300">
  <div class="p-3 rounded-lg bg-rose-950/30 border border-rose-500/30 text-rose-300">
    <div class="font-bold font-mono text-sm text-rose-400">The 2016 Dyn DNS Cyberattack (Mirai Botnet Outage)</div>
    <div class="text-[11px] text-rose-200 mt-1">Impact: Twitter, Spotify, Netflix, Reddit, GitHub, and Amazon vanished for tens of millions of users across the US East Coast.</div>
  </div>

  <div class="space-y-2">
    <div class="text-white font-bold font-mono text-xs uppercase tracking-wider">1. The Trigger &amp; Cascading Failure</div>
    <p>
      On October 21, 2016, approximately 100,000 IoT devices (DVRs, IP cameras) infected by the Mirai botnet launched a 1.2 Terabit/sec distributed reflection denial of service (DDoS) attack against Dyn's authoritative nameservers.
      The flood targeted UDP Port 53 with randomized subdomain lookups (e.g., <code>q8a92z.twitter.com</code>).
    </p>
    <p>
      Because these subdomains did not exist, recursive resolvers like Google DNS (<code>8.8.8.8</code>) and Comcast could not serve answers from cache and were forced to continuously hammer Dyn's authoritative servers.
      When Dyn's Anycast BGP routes dropped under switch buffer exhaustion, client browsers failed to resolve domain names to IP addresses.
      <strong>The application servers at Twitter and Netflix were completely healthy and 100% idle, but zero users could connect!</strong>
    </p>
  </div>

  <div class="space-y-2 border-t border-slate-800 pt-3">
    <div class="text-white font-bold font-mono text-xs uppercase tracking-wider">2. Staff Engineer Architectural Remediation</div>
    <ul class="list-disc list-inside space-y-1 text-slate-300">
      <li><strong class="text-white">Dual-DNS Active-Active Architecture:</strong> Never depend on a single DNS vendor. Production tier-0 systems delegate NS records across two independent DNS providers (e.g. AWS Route53 + Cloudflare DNS) using BGP Anycast.</li>
      <li><strong class="text-white">Aggressive Negative Caching (RFC 2308):</strong> Set realistic TTLs on SOA records (NXDOMAIN responses) so recursive resolvers cache domain misses for 300 seconds rather than flooding origin authoritative servers.</li>
      <li><strong class="text-white">DNS Anycast Scrubbing Centers:</strong> Route UDP 53 ingress traffic through automated eBPF/XDP packet scrubbers that drop unverified SYN/UDP queries directly at the network interface card before Linux kernel socket buffers are allocated.</li>
    </ul>
  </div>
</div>
""",
        "interviewDefense": """
<div class="space-y-4 text-xs font-mono">
  <div class="p-3 rounded-lg bg-amber-950/20 border border-amber-500/30 text-amber-300">
    <div class="text-[10px] text-amber-500 uppercase font-bold">FAANG Staff Interview Trap Question</div>
    <div class="text-sm font-bold text-white mt-1">
      "Why does DNS traditionally operate over UDP rather than TCP, when does it automatically fallback to TCP, and what prevents DNS spoofing?"
    </div>
  </div>

  <div class="space-y-2">
    <div class="text-emerald-400 font-bold">Staff Architect Verbal Answer Script:</div>
    <p class="text-slate-300 font-sans leading-relaxed">
      "DNS lookups are single-packet request/response exchanges. UDP avoids the 1-RTT TCP handshake overhead and requires zero connection state in server memory, allowing a single recursive resolver to serve 250,000 queries per second.
      <br><br>
      However, classic RFC 1035 UDP DNS payloads are strictly limited to <strong>512 bytes</strong>. When a DNS response exceeds 512 bytes—such as when returning large IPv6 (AAAA) records or cryptographic DNSSEC keys—the server sets the <strong>Truncation Bit (TC=1)</strong> in the DNS header. The client OS receives <code>TC=1</code>, immediately discards the partial UDP response, and opens a reliable <strong>TCP connection on Port 53</strong> to stream the complete payload.
      <br><br>
      To prevent DNS cache poisoning (Kaminsky attacks), modern architectures enforce <strong>Source Port Randomization</strong> across 16-bit ephemeral ports combined with 16-bit Query IDs (creating $2^{32}$ entropy) and <strong>DNSSEC (RFC 4033)</strong>, which signs resource record sets using public-key cryptography."
    </p>
  </div>

  <div class="p-3 rounded-lg bg-slate-950 border border-slate-800 space-y-1.5 font-sans">
    <div class="text-slate-400 font-mono text-[10px] uppercase font-bold">Staff Whiteboard Rubric</div>
    <div class="flex items-center gap-2 text-emerald-400 text-xs">
      <span>&#10003; Mentioning EDNS0 (RFC 6891) buffer expansion to 4096 bytes</span>
    </div>
    <div class="flex items-center gap-2 text-emerald-400 text-xs">
      <span>&#10003; Explaining the TC=1 truncation bit and TCP fallback mechanics</span>
    </div>
    <div class="flex items-center gap-2 text-rose-400 text-xs">
      <span>&#10007; Red Flag: Claiming DNS always runs on TCP or confusing authoritative with recursive resolvers</span>
    </div>
  </div>
</div>
"""
    },
    {
        "id": "c-02-http-rest",
        "stageId": "stage-1",
        "stageNum": "STAGE 01",
        "badge": "Day 1 Scratch",
        "color": "emerald",
        "title": "1.2 HTTP Protocols, REST APIs & Idempotency Keys",
        "difficulty": "Beginner",
        "readTime": "20 min read",
        "simulatorKey": "tracer",
        "summary": "Protocol evolution: HTTP/1.1 vs HTTP/2 binary framing vs HTTP/3 QUIC. Safe vs Idempotent verbs, and atomic distributed idempotency keys in Redis.",
        "guidebook": """
<div class="space-y-6 text-sm text-slate-300 leading-relaxed">
  <div class="p-4 rounded-xl bg-emerald-950/20 border border-emerald-500/20 text-emerald-300">
    <div class="font-bold text-xs uppercase font-mono tracking-wider text-emerald-400 mb-1">First-Principles Intuition</div>
    Imagine calling an elevator. Pressing the "Up" button once lights up the indicator. Pressing it 10 more times does NOT summon 10 separate elevators; the building remains in the exact same state. That is <strong>Idempotency</strong>.
    <br><br>
    In distributed systems, networks are inherently unreliable. Packets get delayed, dropped, or timed out. If your credit card charge request times out, did the bank deduct your money or not?
    Without idempotency, retrying that request charges you twice.
  </div>

  <h4 class="text-base font-bold text-white flex items-center gap-2">
    <span class="w-2 h-2 rounded-full bg-emerald-400"></span> 1. The Generational HTTP Evolution
  </h4>
  <div class="overflow-x-auto">
    <table class="w-full text-xs text-left border border-slate-800 rounded-lg overflow-hidden font-mono">
      <thead class="bg-slate-900 text-slate-400">
        <tr>
          <th class="p-2.5">Protocol</th>
          <th class="p-2.5">Transport</th>
          <th class="p-2.5">Multiplexing</th>
          <th class="p-2.5">Head-of-Line (HoL) Blocking</th>
          <th class="p-2.5">Header Compression</th>
        </tr>
      </thead>
      <tbody class="divide-y divide-slate-800/60 text-slate-300 bg-slate-950">
        <tr>
          <td class="p-2.5 text-cyan-400 font-bold">HTTP/1.1 (1997)</td>
          <td class="p-2.5">TCP</td>
          <td class="p-2.5 text-rose-400">None (1 req per conn)</td>
          <td class="p-2.5 text-rose-400">Severe (App-level HoL)</td>
          <td class="p-2.5 text-slate-500">None (Plaintext headers)</td>
        </tr>
        <tr>
          <td class="p-2.5 text-emerald-400 font-bold">HTTP/2 (2015)</td>
          <td class="p-2.5">TCP</td>
          <td class="p-2.5 text-emerald-400">Binary Framing (Streams)</td>
          <td class="p-2.5 text-amber-400">TCP-level HoL (Dropped packet stalls all streams)</td>
          <td class="p-2.5 text-emerald-400">HPACK (Static/Dynamic tables)</td>
        </tr>
        <tr>
          <td class="p-2.5 text-fuchsia-400 font-bold">HTTP/3 (2022)</td>
          <td class="p-2.5">QUIC (UDP)</td>
          <td class="p-2.5 text-emerald-400">True Independent Streams</td>
          <td class="p-2.5 text-emerald-400">Zero HoL Blocking!</td>
          <td class="p-2.5 text-emerald-400">QPACK (Out-of-order header decompression)</td>
        </tr>
      </tbody>
    </table>
  </div>

  <h4 class="text-base font-bold text-white flex items-center gap-2 mt-6">
    <span class="w-2 h-2 rounded-full bg-emerald-400"></span> 2. REST HTTP Verbs: Safe vs Idempotent Matrix
  </h4>
  <p>
    An operation is <strong>Safe</strong> if it does not mutate server state. An operation is <strong>Idempotent</strong> if executing it $N$ times produces the identical side-effect as executing it once: $f(f(x)) = f(x)$.
  </p>
  <div class="grid grid-cols-2 sm:grid-cols-4 gap-2.5 text-xs font-mono">
    <div class="p-3 rounded-lg bg-slate-950 border border-slate-800">
      <div class="text-cyan-400 font-bold">GET / HEAD</div>
      <div class="text-emerald-400 text-[10px] mt-1">Safe: YES</div>
      <div class="text-emerald-400 text-[10px]">Idempotent: YES</div>
      <div class="text-slate-400 text-[10px] mt-1 font-sans">Read-only retrieval. Never mutates.</div>
    </div>
    <div class="p-3 rounded-lg bg-slate-950 border border-slate-800">
      <div class="text-amber-400 font-bold">PUT</div>
      <div class="text-rose-400 text-[10px] mt-1">Safe: NO</div>
      <div class="text-emerald-400 text-[10px]">Idempotent: YES</div>
      <div class="text-slate-400 text-[10px] mt-1 font-sans">Full replacement of resource.</div>
    </div>
    <div class="p-3 rounded-lg bg-slate-950 border border-slate-800">
      <div class="text-rose-400 font-bold">DELETE</div>
      <div class="text-rose-400 text-[10px] mt-1">Safe: NO</div>
      <div class="text-emerald-400 text-[10px]">Idempotent: YES</div>
      <div class="text-slate-400 text-[10px] mt-1 font-sans">Deleting 10 times yields deleted state.</div>
    </div>
    <div class="p-3 rounded-lg bg-slate-950 border border-slate-800">
      <div class="text-fuchsia-400 font-bold">POST</div>
      <div class="text-rose-400 text-[10px] mt-1">Safe: NO</div>
      <div class="text-rose-400 text-[10px]">Idempotent: NO</div>
      <div class="text-slate-400 text-[10px] mt-1 font-sans">Creates child resource. Requires key!</div>
    </div>
  </div>

  <h4 class="text-base font-bold text-white flex items-center gap-2 mt-6">
    <span class="w-2 h-2 rounded-full bg-emerald-400"></span> 3. The Idempotency Key Architecture
  </h4>
  <p>
    When a mobile client sends a payment request, it generates a unique UUIDv4 token:
    <code>Idempotency-Key: 9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d</code>.
    The API Gateway orchestrates a 3-state atomic machine:
  </p>
  <div class="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-2 font-mono text-xs">
    <div>State 1: <code>SET key "PROCESSING" NX EX 120</code> &rarr; Atomically acquires lock. If key exists, return cached response immediately!</div>
    <div>State 2: Execute banking transaction against payment core.</div>
    <div>State 3: <code>SET key "{\"status\":\"SUCCEEDED\",\"charge_id\":\"ch_102\"}" EX 86400</code> &rarr; Cache completed response for 24 hours.</div>
  </div>
</div>
""",
        "topologySvg": """
<svg viewBox="0 0 960 360" class="w-full h-auto bg-slate-950 rounded-2xl border border-slate-800 p-4" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="g-c" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#0284c7"/><stop offset="100%" stop-color="#0369a1"/></linearGradient>
    <linearGradient id="g-gw" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#059669"/><stop offset="100%" stop-color="#047857"/></linearGradient>
    <linearGradient id="g-red" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#dc2626"/><stop offset="100%" stop-color="#991b1b"/></linearGradient>
    <linearGradient id="g-pay" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#7c3aed"/><stop offset="100%" stop-color="#6d28d9"/></linearGradient>
    <marker id="arr-b" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 1 L 10 5 L 0 9 z" fill="#38bdf8"/></marker>
    <marker id="arr-g" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 1 L 10 5 L 0 9 z" fill="#34d399"/></marker>
    <marker id="arr-r" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 1 L 10 5 L 0 9 z" fill="#f87171"/></marker>
  </defs>

  <rect width="100%" height="100%" fill="#07090e" rx="12"/>

  <!-- CLIENT -->
  <g transform="translate(30, 110)">
    <rect width="180" height="130" rx="10" fill="url(#g-c)" stroke="#38bdf8" stroke-width="1.5"/>
    <text x="16" y="28" fill="#ffffff" font-size="12" font-family="sans-serif" font-weight="bold">Mobile Banking Client</text>
    <text x="16" y="48" fill="#bae6fd" font-size="9" font-family="monospace">POST /v1/charges</text>
    <text x="16" y="66" fill="#e0f2fe" font-size="8" font-family="monospace">Idempotency-Key: uuid-v4</text>
    <rect x="16" y="80" width="148" height="34" rx="4" fill="#0c4a6e"/>
    <text x="22" y="94" fill="#38bdf8" font-size="8" font-family="monospace">Network Timeout Retry:</text>
    <text x="22" y="106" fill="#facc15" font-size="8" font-family="monospace">Safe 3x Exponential Backoff</text>
  </g>

  <!-- API GATEWAY -->
  <g transform="translate(290, 110)">
    <rect width="200" height="130" rx="10" fill="url(#g-gw)" stroke="#34d399" stroke-width="1.5"/>
    <text x="16" y="28" fill="#ffffff" font-size="12" font-family="sans-serif" font-weight="bold">API Gateway (Envoy)</text>
    <text x="16" y="48" fill="#a7f3d0" font-size="9" font-family="monospace">Idempotency Interceptor</text>
    <text x="16" y="66" fill="#d1fae5" font-size="8" font-family="sans-serif">Checks Redis Atomic Lock</text>
    <rect x="16" y="80" width="168" height="34" rx="4" fill="#064e3b"/>
    <text x="22" y="94" fill="#34d399" font-size="8" font-family="monospace">If key present: Return Cache</text>
    <text x="22" y="106" fill="#a7f3d0" font-size="8" font-family="monospace">If key absent: Forward Req</text>
  </g>

  <!-- REDIS DISTRIBUTED LOCK CLUSTER -->
  <g transform="translate(570, 20)">
    <rect width="200" height="110" rx="10" fill="url(#g-red)" stroke="#f87171" stroke-width="1.5"/>
    <text x="16" y="26" fill="#ffffff" font-size="11" font-family="sans-serif" font-weight="bold">Redis Lock Cluster</text>
    <text x="16" y="44" fill="#fecaca" font-size="9" font-family="monospace">Atomic Lua Scripts</text>
    <text x="16" y="62" fill="#fee2e2" font-size="8" font-family="sans-serif">Key: idem_lock:{uuid}</text>
    <text x="16" y="78" fill="#fca5a5" font-size="8" font-family="monospace">State: PROCESSING &rarr; DONE</text>
    <text x="16" y="94" fill="#fef08a" font-size="8" font-family="monospace">TTL: 86400s (24 Hours)</text>
  </g>

  <!-- PAYMENT CORE ENGINE -->
  <g transform="translate(570, 180)">
    <rect width="200" height="120" rx="10" fill="url(#g-pay)" stroke="#c084fc" stroke-width="1.5"/>
    <text x="16" y="28" fill="#ffffff" font-size="12" font-family="sans-serif" font-weight="bold">Payment Ledger Core</text>
    <text x="16" y="48" fill="#e9d5ff" font-size="9" font-family="monospace">Double-Entry SQL Ledger</text>
    <text x="16" y="66" fill="#f3e8ff" font-size="8" font-family="sans-serif">Card Network Settlement</text>
    <rect x="16" y="80" width="168" height="24" rx="4" fill="#4c1d95"/>
    <text x="22" y="96" fill="#c084fc" font-size="8" font-family="monospace">Executes EXACTLY ONCE</text>
  </g>

  <!-- PATHS -->
  <path d="M 210 160 L 290 160" fill="none" stroke="#38bdf8" stroke-width="2" marker-end="url(#arr-b)"/>
  <path d="M 490 140 L 570 80" fill="none" stroke="#f87171" stroke-width="2" marker-end="url(#arr-r)"/>
  <path d="M 490 180 L 570 230" fill="none" stroke="#34d399" stroke-width="2" marker-end="url(#arr-g)"/>
</svg>
""",
        "codeSnippet": """-- Production Redis Lua Script for Atomic HTTP Idempotency Key Handling
-- Keys: KEYS[1] = idem_key:{uuid}
-- Args: ARGV[1] = payload_hash, ARGV[2] = response_json, ARGV[3] = lock_ttl_sec, ARGV[4] = cache_ttl_sec

local key = KEYS[1]
local req_hash = ARGV[1]
local lock_ttl = tonumber(ARGV[3]) or 120

-- Step 1: Check existing key state
local current_val = redis.call('GET', key)

if current_val then
    -- Decode JSON representation
    local record = cjson.decode(current_val)
    
    -- Verify request body hash matches to prevent key hijacking
    if record.hash ~= req_hash then
        return cjson.encode({status = 'MISMATCH_ERROR', message = 'Idempotency key reused with different payload'})
    end

    if record.status == 'PROCESSING' then
        return cjson.encode({status = 'IN_FLIGHT', message = 'Concurrent request currently being processed'})
    end

    -- Return cached response; bypass backend entirely!
    return cjson.encode({status = 'REPLAY', body = record.body, code = record.code})
end

-- Step 2: Atomic lock acquisition
local lock_payload = cjson.encode({
    status = 'PROCESSING',
    hash = req_hash,
    created_at = redis.call('TIME')[1]
})

redis.call('SET', key, lock_payload, 'EX', lock_ttl)
return cjson.encode({status = 'ACQUIRED'})
""",
        "disasterStudy": """
<div class="space-y-4 text-xs text-slate-300">
  <div class="p-3 rounded-lg bg-rose-950/30 border border-rose-500/30 text-rose-300">
    <div class="font-bold font-mono text-sm text-rose-400">The Uber Double Billing Outage (New Year's Eve)</div>
    <div class="text-[11px] text-rose-200 mt-1">Impact: Riders were charged 3 to 7 times for individual trips, exhausting credit card limits and sparking regulatory fines.</div>
  </div>

  <div class="space-y-2">
    <div class="text-white font-bold font-mono text-xs uppercase tracking-wider">1. The Trigger &amp; Cascading Failure</div>
    <p>
      During peak New Year's Eve midnight surge, cellular network congestion caused high latency between rider mobile phones and Uber's ingress proxies.
      Riders tapped "Confirm Ride", waited 10 seconds with no UI feedback, and tapped repeatedly.
      Simultaneously, the mobile client SDK had a default HTTP retry policy: on a <code>504 Gateway Timeout</code>, it retried the POST request every 2 seconds.
    </p>
    <p>
      At the payment backend, requests were actually queued and executing successfully in Postgres, but the response packets could not reach the client before the mobile timeout expired.
      <strong>Because the POST endpoints lacked atomic server-side idempotency keys, each retry created a brand new bank authorization!</strong>
    </p>
  </div>

  <div class="space-y-2 border-t border-slate-800 pt-3">
    <div class="text-white font-bold font-mono text-xs uppercase tracking-wider">2. Staff Engineer Architectural Remediation</div>
    <ul class="list-disc list-inside space-y-1 text-slate-300">
      <li><strong class="text-white">Client-Side Deterministic UUIDs:</strong> The mobile client generates the <code>Idempotency-Key</code> at the moment the user initiates the action, persisting it in SQLite locally before sending over the wire.</li>
      <li><strong class="text-white">Two-Phase Redis Gate:</strong> The API Gateway locks the idempotency key with a 120-second lease before dispatching to the payment microservice. If a retry arrives while status is <code>PROCESSING</code>, the gateway returns <code>409 Conflict</code> or blocks until complete.</li>
      <li><strong class="text-white">Payload Hashing Invariant:</strong> The server stores a SHA-256 hash of the request body alongside the key. If an attacker or buggy client sends the same key with different amounts, it is rejected instantly with <code>422 Unprocessable Entity</code>.</li>
    </ul>
  </div>
</div>
""",
        "interviewDefense": """
<div class="space-y-4 text-xs font-mono">
  <div class="p-3 rounded-lg bg-amber-950/20 border border-amber-500/30 text-amber-300">
    <div class="text-[10px] text-amber-500 uppercase font-bold">FAANG Staff Interview Trap Question</div>
    <div class="text-sm font-bold text-white mt-1">
      "What is the difference between a 502 Bad Gateway and a 504 Gateway Timeout, and why is an automated client retry policy disastrous on a 504?"
    </div>
  </div>

  <div class="space-y-2">
    <div class="text-emerald-400 font-bold">Staff Architect Verbal Answer Script:</div>
    <p class="text-slate-300 font-sans leading-relaxed">
      "A <strong>502 Bad Gateway</strong> indicates that an intermediate reverse proxy (e.g. Envoy, NGINX) received an invalid response or a TCP connection reset (RST) from the upstream service. This typically means the upstream process crashed or refused the connection.
      <br><br>
      A <strong>504 Gateway Timeout</strong> means the proxy forwarded the request, but the upstream service failed to respond within the allocated timeout budget. The critical distinction is that on a 504, <em>the backend may still be executing the transaction</em> in the database.
      <br><br>
      If a client blindly retries a non-idempotent POST request upon receiving a 504, it triggers two catastrophic failure modes: (1) <strong>Duplicate Execution:</strong> Charging the customer or mutating database records multiple times, and (2) <strong>Retry Storm / Thundering Herd:</strong> Adding new load to an already overloaded backend that is struggling under slow database queries, transforming a minor transient slowdown into a total cascading outage."
    </p>
  </div>
</div>
"""
    },
    {
        "id": "c-03-monolith-vs-micro",
        "stageId": "stage-1",
        "stageNum": "STAGE 01",
        "badge": "Day 1 Scratch",
        "color": "emerald",
        "title": "1.3 Monoliths vs Microservices: When to Split & Service Mesh",
        "difficulty": "Beginner to Intermediate",
        "readTime": "22 min read",
        "simulatorKey": "interview",
        "summary": "Conway's Law, when to stay monolith vs when to split. The distributed systems tax, gRPC vs REST, and Envoy sidecar service meshes.",
        "guidebook": """
<div class="space-y-6 text-sm text-slate-300 leading-relaxed">
  <div class="p-4 rounded-xl bg-emerald-950/20 border border-emerald-500/20 text-emerald-300">
    <div class="font-bold text-xs uppercase font-mono tracking-wider text-emerald-400 mb-1">First-Principles Intuition</div>
    Imagine a small artisan bakery where 3 bakers share a single kitchen. They communicate instantly by speaking out loud, share bowls and ovens, and make decisions in real time. That is a <strong>Modular Monolith</strong>.
    <br><br>
    Now imagine splitting that bakery into 20 separate food trucks parked around the city. To bake a single cake, Truck A must radio Truck B for flour, Truck B radios Truck C for eggs, and Truck C's battery dies mid-conversation.
    That is the <strong>Microservices Tax</strong>. You traded simple in-memory function calls for network latency, partial failures, distributed transactions, and serialization overhead!
  </div>

  <h4 class="text-base font-bold text-white flex items-center gap-2">
    <span class="w-2 h-2 rounded-full bg-emerald-400"></span> 1. The Architectural Trade-Off Spectrum
  </h4>
  <div class="overflow-x-auto">
    <table class="w-full text-xs text-left border border-slate-800 rounded-lg overflow-hidden font-mono">
      <thead class="bg-slate-900 text-slate-400">
        <tr>
          <th class="p-2.5">Dimension</th>
          <th class="p-2.5">Modular Monolith</th>
          <th class="p-2.5">Microservices Architecture</th>
        </tr>
      </thead>
      <tbody class="divide-y divide-slate-800/60 text-slate-300 bg-slate-950">
        <tr>
          <td class="p-2.5 text-cyan-400 font-bold">Inter-Service Latency</td>
          <td class="p-2.5 text-emerald-400">&lt; 10 nanoseconds (Memory pointer dereference)</td>
          <td class="p-2.5 text-rose-400">2 - 30 milliseconds (TCP/TLS network hop)</td>
        </tr>
        <tr>
          <td class="p-2.5 text-cyan-400 font-bold">Data Consistency</td>
          <td class="p-2.5 text-emerald-400">ACID Transactions across tables (BEGIN / COMMIT)</td>
          <td class="p-2.5 text-amber-400">Eventual Consistency (Sagas, compensating transactions)</td>
        </tr>
        <tr>
          <td class="p-2.5 text-cyan-400 font-bold">Deployment Coupling</td>
          <td class="p-2.5 text-amber-400">Single deployment artifact (All or nothing)</td>
          <td class="p-2.5 text-emerald-400">Independent CI/CD pipelines per team</td>
        </tr>
        <tr>
          <td class="p-2.5 text-cyan-400 font-bold">Failure Blast Radius</td>
          <td class="p-2.5 text-rose-400">High: Memory leak or crash takes down entire app</td>
          <td class="p-2.5 text-emerald-400">Low: Isolated failure domains with circuit breakers</td>
        </tr>
      </tbody>
    </table>
  </div>

  <h4 class="text-base font-bold text-white flex items-center gap-2 mt-6">
    <span class="w-2 h-2 rounded-full bg-emerald-400"></span> 2. The 3 Legitimate Triggers to Split
  </h4>
  <p>
    Staff Engineers never adopt microservices because they are trendy. They only split when at least one of these three physical boundaries is breached:
  </p>
  <ul class="list-disc list-inside space-y-1.5 text-xs text-slate-300 ml-2">
    <li><strong class="text-white">Conway's Law &amp; Team Scalability:</strong> When engineering expands beyond 100+ developers, git merge conflicts, test suite durations (45+ minutes), and release coordination meetings cripple velocity.</li>
    <li><strong class="text-white">Asymmetric Resource Requirements:</strong> A video transcoding service requires high-GPU machines, while a notification service requires high-IOPS network sockets. Running both in one binary forces expensive oversized hardware.</li>
    <li><strong class="text-white">Strict Compliance &amp; Isolation:</strong> PCI-DSS credit card processing requires strict security audits and isolated network subnets that should never touch social feed or recommendation code.</li>
  </ul>
</div>
""",
        "topologySvg": """
<svg viewBox="0 0 960 360" class="w-full h-auto bg-slate-950 rounded-2xl border border-slate-800 p-4" xmlns="http://www.w3.org/2000/svg">
  <rect width="100%" height="100%" fill="#07090e" rx="12"/>

  <!-- SIDE A: MODULAR MONOLITH -->
  <g transform="translate(40, 40)">
    <rect width="400" height="280" rx="12" fill="#0f172a" stroke="#0284c7" stroke-width="1.5"/>
    <text x="20" y="32" fill="#38bdf8" font-size="14" font-family="sans-serif" font-weight="bold">Modular Monolith</text>
    <text x="20" y="52" fill="#94a3b8" font-size="10" font-family="monospace">Single Process Memory Space (In-Proc Calls)</text>

    <!-- Modules inside Monolith -->
    <rect x="20" y="70" width="170" height="80" rx="8" fill="#1e293b" stroke="#334155"/>
    <text x="32" y="94" fill="#f8fafc" font-size="11" font-weight="bold">Order Module</text>
    <text x="32" y="112" fill="#38bdf8" font-size="8" font-family="monospace">orderService.create()</text>
    <text x="32" y="128" fill="#34d399" font-size="8" font-family="monospace">Latency: 5 nanoseconds</text>

    <rect x="210" y="70" width="170" height="80" rx="8" fill="#1e293b" stroke="#334155"/>
    <text x="222" y="94" fill="#f8fafc" font-size="11" font-weight="bold">Payment Module</text>
    <text x="222" y="112" fill="#38bdf8" font-size="8" font-family="monospace">paymentService.charge()</text>
    <text x="222" y="128" fill="#34d399" font-size="8" font-family="monospace">Memory pointer pass</text>

    <!-- Single DB -->
    <rect x="20" y="180" width="360" height="70" rx="8" fill="#0c4a6e" stroke="#0284c7"/>
    <text x="32" y="206" fill="#ffffff" font-size="11" font-weight="bold">Single Shared Relational Database (PostgreSQL)</text>
    <text x="32" y="224" fill="#7dd3fc" font-size="9" font-family="monospace">ACID Transactions &bull; Foreign Keys &bull; Zero Network Overhead</text>
  </g>

  <!-- SIDE B: MICROSERVICES WITH SERVICE MESH -->
  <g transform="translate(500, 40)">
    <rect width="420" height="280" rx="12" fill="#0f172a" stroke="#7c3aed" stroke-width="1.5"/>
    <text x="20" y="32" fill="#c084fc" font-size="14" font-family="sans-serif" font-weight="bold">Microservices + Envoy Mesh</text>
    <text x="20" y="52" fill="#94a3b8" font-size="10" font-family="monospace">Distributed Network Boundaries (gRPC/mTLS)</text>

    <!-- Service Pod 1 -->
    <rect x="20" y="70" width="180" height="90" rx="8" fill="#1e1b4b" stroke="#6d28d9"/>
    <text x="30" y="92" fill="#ffffff" font-size="10" font-weight="bold">Order Service Pod</text>
    <rect x="30" y="105" width="160" height="24" rx="4" fill="#312e81"/>
    <text x="38" y="121" fill="#c084fc" font-size="8" font-family="monospace">Envoy Sidecar (mTLS)</text>
    <text x="30" y="148" fill="#f43f5e" font-size="8" font-family="monospace">Latency: 4.5ms (Wire)</text>

    <!-- Service Pod 2 -->
    <rect x="220" y="70" width="180" height="90" rx="8" fill="#1e1b4b" stroke="#6d28d9"/>
    <text x="230" y="92" fill="#ffffff" font-size="10" font-weight="bold">Payment Service Pod</text>
    <rect x="230" y="105" width="160" height="24" rx="4" fill="#312e81"/>
    <text x="238" y="121" fill="#c084fc" font-size="8" font-family="monospace">Envoy Sidecar (mTLS)</text>
    <text x="230" y="148" fill="#a7f3d0" font-size="8" font-family="monospace">Independent Scale</text>

    <!-- Independent DBs -->
    <rect x="20" y="180" width="180" height="70" rx="8" fill="#431407" stroke="#ea580c"/>
    <text x="28" y="204" fill="#ffffff" font-size="9" font-weight="bold">Order DB (Postgres)</text>
    <text x="28" y="222" fill="#fed7aa" font-size="8" font-family="monospace">Private Datastore</text>

    <rect x="220" y="180" width="180" height="70" rx="8" fill="#431407" stroke="#ea580c"/>
    <text x="228" y="204" fill="#ffffff" font-size="9" font-weight="bold">Payment DB (Postgres)</text>
    <text x="228" y="222" fill="#fed7aa" font-size="8" font-family="monospace">Saga Event Broker</text>
  </g>
</svg>
""",
        "codeSnippet": """// Production Go gRPC Client with Circuit Breaking & OpenTelemetry Tracing
package client

import (
	"context"
	"time"

	"github.com/sony/gobreaker"
	"go.opentelemetry.io/otel"
	"go.opentelemetry.io/otel/trace"
	"google.golang.org/grpc"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
)

type PaymentServiceClient struct {
	cb     *gobreaker.CircuitBreaker
	client PaymentRpcClient
	tracer trace.Tracer
}

func NewPaymentClient(cc grpc.ClientConnInterface) *PaymentServiceClient {
	cbSettings := gobreaker.Settings{
		Name:        "PaymentServiceCircuitBreaker",
		MaxRequests: 5,               // Requests allowed in half-open state
		Interval:    10 * time.Second, // Clearing interval for failure counter
		Timeout:     5 * time.Second,  // Duration breaker stays open before test
		ReadyToTrip: func(counts gobreaker.Counts) bool {
			// Trip open if failure ratio exceeds 40% with minimum 10 requests
			failureRatio := float64(counts.TotalFailures) / float64(counts.Requests)
			return counts.Requests >= 10 && failureRatio >= 0.40
		},
	}

	return &PaymentServiceClient{
		cb:     gobreaker.NewCircuitBreaker(cbSettings),
		client: NewPaymentRpcClient(cc),
		tracer: otel.Tracer("order-payment-client"),
	}
}

func (c *PaymentServiceClient) ProcessPaymentWithProtection(ctx context.Context, req *PaymentRequest) (*PaymentResponse, error) {
	ctx, span := c.tracer.Start(ctx, "PaymentClient.ProcessPayment")
	defer span.End()

	// Enforce strict 1200ms deadline across network hop
	ctx, cancel := context.WithTimeout(ctx, 1200*time.Millisecond)
	defer cancel()

	result, err := c.cb.Execute(func() (interface{}, error) {
		res, rpcErr := c.client.ExecuteCharge(ctx, req)
		if rpcErr != nil {
			st, _ := status.FromError(rpcErr)
			// Don't trip circuit breaker for user errors (e.g. InvalidCard)
			if st.Code() == codes.InvalidArgument {
				return res, nil
			}
			return nil, rpcErr
		}
		return res, nil
	})

	if err != nil {
		span.RecordError(err)
		return nil, err // Fast-fail when circuit breaker is OPEN
	}

	return result.(*PaymentResponse), nil
}
""",
        "disasterStudy": """
<div class="space-y-4 text-xs text-slate-300">
  <div class="p-3 rounded-lg bg-rose-950/30 border border-rose-500/30 text-rose-300">
    <div class="font-bold font-mono text-sm text-rose-400">The Segment Microservices Regret &amp; Monolith Migration</div>
    <div class="text-[11px] text-rose-200 mt-1">Impact: After decomposing their pipeline into 140+ microservices, engineering velocity collapsed and AWS bills exploded.</div>
  </div>

  <div class="space-y-2">
    <div class="text-white font-bold font-mono text-xs uppercase tracking-wider">1. The Trigger &amp; Cascading Failure</div>
    <p>
      Segment initially broke their destination ingestion pipeline into individual microservices for each destination (Google Analytics, Salesforce, Mixpanel).
      With over 140 destinations, each had its own Git repository, ECS auto-scaling group, and queuing tier.
    </p>
    <p>
      When an API schema change occurred, engineers had to submit 140 pull requests.
      Cascading network timeouts between microservices overwhelmed SQS queues, causing queue backlog lag of over 4 hours.
      <strong>The operational overhead of managing 140 microservices consumed 70% of engineering bandwidth!</strong>
    </p>
  </div>

  <div class="space-y-2 border-t border-slate-800 pt-3">
    <div class="text-white font-bold font-mono text-xs uppercase tracking-wider">2. Staff Engineer Architectural Remediation</div>
    <ul class="list-disc list-inside space-y-1 text-slate-300">
      <li><strong class="text-white">Consolidation into a Modular Monolith:</strong> Segment collapsed the 140 destination services into a single Go codebase using dynamic plugin interfaces.</li>
      <li><strong class="text-white">3x Throughput Improvement:</strong> Eliminating inter-service HTTP serialization and intermediate network hops tripled throughput and slashed AWS infrastructure costs by 50%.</li>
      <li><strong class="text-white">The Golden Staff Rule:</strong> Start with a well-structured modular monolith. Only decompose into microservices along true organizational and team velocity lines, never technical lines.</li>
    </ul>
  </div>
</div>
""",
        "interviewDefense": """
<div class="space-y-4 text-xs font-mono">
  <div class="p-3 rounded-lg bg-amber-950/20 border border-amber-500/30 text-amber-300">
    <div class="text-[10px] text-amber-500 uppercase font-bold">FAANG Staff Interview Trap Question</div>
    <div class="text-sm font-bold text-white mt-1">
      "When designing a greenfield system, an interviewer asks: 'Should we build this as microservices from Day 1 to ensure scale?' How do you answer?"
    </div>
  </div>

  <div class="space-y-2">
    <div class="text-emerald-400 font-bold">Staff Architect Verbal Answer Script:</div>
    <p class="text-slate-300 font-sans leading-relaxed">
      "No. Recommending microservices for a greenfield system is an immediate red flag.
      <br><br>
      In early-stage systems, the domain boundaries and business models are still evolving. If you draw microservice boundaries prematurely, you inevitably draw them in the wrong place, resulting in the worst possible architecture: a <strong>Distributed Monolith</strong>, where services are tightly coupled over high-latency network calls without transactional guarantees.
      <br><br>
      The Staff approach is to build a <strong>Modular Monolith</strong> with strict interface encapsulation and separate domain directories. In a modular monolith, refactoring domain boundaries is as simple as moving a package.
      Once team size exceeds 50 engineers or specific components exhibit radically asymmetric scaling needs (e.g. CPU vs IOPS), we peel off those specific modules into isolated microservices along proven domain boundaries."
    </p>
  </div>
</div>
"""
    }
]

print(f"Stage 1 loaded with {len(STAGE_1_CHAPTERS)} comprehensive chapters.")
