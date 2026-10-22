Absolutely. I’ve kept this as **your actual investigation**, not turned it into an idealized example. I’ve also kept the distinction between what you **observed**, what you **inferred**, and what you **could not establish**.

````markdown
# Day 7 — First Mini Investigation

## 1. Objective

### Investigation Question

What happened on my Windows system during the period of my login and subsequent network activity, and can the Windows Event Viewer evidence be correlated with the Wireshark network capture?

### Secondary Questions

- What Windows events were generated during the activity?
- What network activity occurred while I browsed websites?
- Can the Windows events be directly connected to the network activity?
- Were any of the observed activities genuinely suspicious?
- What evidence would make an activity more suspicious?

---

# 2. Investigation Methodology

Two sources of evidence were used:

1. **Windows Event Viewer**
2. **Wireshark**

Windows Event Viewer was used to examine system-level activity such as:

- Logons
- Logoffs/session termination
- Special privileges
- Local group membership enumeration
- Other Security events

Wireshark was used to examine network-level activity such as:

- DNS queries
- IP addresses
- TCP connections
- TCP sequence and acknowledgement numbers
- TCP flags
- HTTPS/TLS traffic
- Connection termination

The investigation attempted to correlate the two sources using timestamps.

---

# 3. Investigation Window

## Windows activity

The initial activity began at approximately:

**09:59:25**

A Wireshark capture was later started at:

**10:01:04**

The Wireshark capture ended at:

**10:01:56**

Therefore, the network investigation window was:

```text
10:01:04 → 10:01:56
````

---

# 4. Initial Windows Authentication Activity

## 4.1 Event ID 4634

At approximately:

**09:59:25**

Event ID:

**4634**

was observed.

The event indicated that a logon session had been terminated.

This occurred around the time I locked my laptop.

### Investigation question

Does the 4634 event actually correspond to the user session being affected by the lock operation?

To establish this conclusively, the event's account and Logon ID would need to be correlated with the relevant authentication events.

---

# 5. Successful Interactive Logon

At:

**09:59:40**

the following event was observed:

```text
Event ID: 4624
Logon Type: 2
```

The activity occurred after I physically interacted with the laptop and entered my password.

## Interpretation

Logon Type 2 represents an **interactive logon**.

This is consistent with a user directly interacting with the local computer to authenticate.

### Investigation questions

* Was this login expected?
* Does the account correspond to my account?
* Is the timestamp consistent with my activity?
* Were there failed logon attempts immediately before it?
* What activity occurred after the successful login?

In this investigation, the successful Type 2 logon was consistent with my own activity.

---

# 6. Special Privileges — Event ID 4672

Following the successful logon, Event ID:

**4672 — Special privileges assigned to new logon**

was observed.

This event was interesting because it indicates that the new logon was associated with special privileges.

The event also contains a list of privileges associated with the logon.

### Investigation Questions

* Which account received the special privileges?
* What Logon ID does the event contain?
* Does that Logon ID correspond to the preceding 4624?
* Which privileges are listed?
* Is the account expected to have these privileges?
* Is the account an administrator/system-related account?
* Was the activity consistent with normal use of the machine?

The presence of Event ID 4672 alone does not demonstrate malicious activity.

It becomes more interesting if the account is not expected to possess those privileges or if unusual activity follows the privileged logon.

---

# 7. Wireshark Capture

After the Windows authentication activity, I started a Wireshark capture.

### Capture period

```text
Start: 10:01:04
End:   10:01:56
```

During the capture I:

* Opened Microsoft Edge
* Already had ChatGPT open
* Opened ISEA
* Accessed Hashnode
* Observed the resulting network traffic

The websites were not closed during the capture.

---

# 8. Time Correlation Problem

One of the first challenges was correlating Windows Event Viewer timestamps with Wireshark timestamps.

The two tools were initially displaying time differently.

To make correlation easier, Wireshark was changed to display **absolute time**.

This allowed timestamps from the two sources to be compared more directly.

### Investigation lesson

When correlating evidence from multiple sources:

> Are the timestamps being displayed using compatible formats and time references?

If the timestamps cannot be compared reliably, apparent correlations may be misleading.

---

# 9. Windows Events During the Wireshark Capture

During the Wireshark capture period:

```text
10:01:04 → 10:01:56
```

the Security log showed **4798 events**.

## Event ID 4798

The event represents:

> A user's local group membership being enumerated.

The activity can occur when information about a user's local group membership is queried.

This can provide information about the user's membership in local groups.

### Investigation questions

* Which account was involved?
* What process generated the event?
* Why was the local group membership being queried?
* Was this caused by normal Windows/application activity?
* Did the event occur repeatedly?
* Did anything suspicious happen immediately afterward?

The presence of Event ID 4798 alone does not indicate malicious activity.

---

# 10. Network Investigation — DNS

One observed DNS query occurred at approximately:

**10:01:23**

The queried domain was:

```text
www.isea.gov.in
```

The DNS request was sent to:

```text
8.8.8.8
```

This is a Google Public DNS resolver.

The query requested the IPv4 address of the domain.

The DNS response contained an:

```text
A record
```

which returned an IP address in the form:

```text
164.100.xx.x
```

## DNS sequence

```text
My computer
      ↓
DNS query
www.isea.gov.in
      ↓
8.8.8.8
      ↓
DNS response
      ↓
A record
      ↓
164.100.xx.x
```

### Questions answered by this evidence

**What domain was queried?**

`www.isea.gov.in`

**What type of record was requested?**

An IPv4 address / A record.

**What address was returned?**

`164.100.xx.x`

---

# 11. TCP Connection

After resolving the domain, network traffic was observed involving:

```text
Source:
My computer / local IP

Destination:
164.100.xx.x
```

The connection used:

```text
Source port:      29777
Destination port: 443
```

Port 443 is commonly used for HTTPS/TLS traffic.

---

# 12. TCP Three-Way Handshake

The capture contained TCP packets showing sequence and acknowledgement information.

The connection establishment followed the general TCP sequence:

```text
Client → Server
SYN
       ↓
Server → Client
SYN + ACK
       ↓
Client → Server
ACK
```

## Interpretation

The sequence indicates that my system initiated a TCP connection.

The destination responded by acknowledging the request and providing its own synchronization information.

The final ACK from my system completed the TCP three-way handshake.

### Questions

* Which system initiated the connection?
* Which system responded?
* What source port was used?
* What destination port was used?
* Did the SYN → SYN/ACK → ACK sequence occur?

In this capture, the observed traffic was consistent with my system initiating the connection to the destination.

---

# 13. HTTPS / TLS Traffic

The connection to port 443 involved encrypted HTTPS/TLS communication.

Because the application data is encrypted, the contents of the communication cannot normally be read directly as ordinary webpage data from the packet capture.

However, network metadata can still be observed.

Examples include:

* Source IP address
* Destination IP address
* Source port
* Destination port
* Packet timing
* TCP flags
* TCP sequence/acknowledgement information
* TLS-related information

### Observed

```text
Source IP:
My system

Destination IP:
164.100.xx.x

Source port:
29777

Destination port:
443
```

The connection duration was not directly determined during this investigation.

---

# 14. TCP Connection Termination

FIN packets were observed in the capture.

A TCP FIN indicates that a TCP connection is being terminated.

The presence of FIN does **not** necessarily mean that the website or browser tab was closed.

A browser can establish multiple individual connections during a browsing session, and individual connections can terminate while the webpage or browser remains open.

Therefore:

```text
FIN
≠
Browser tab closed
```

Instead:

```text
FIN
=
The particular TCP connection is being terminated
```

---

# 15. Other Network Activity

The capture contained DNS and TCP activity associated with websites that I accessed.

There were also DNS queries for domains that I did not intentionally open during the investigation.

Examples included domains associated with services such as:

* Facebook
* Spotify

### Initial interpretation

These queries were not directly initiated by me during the investigation.

Possible explanations include:

* Background browser activity
* Existing open pages
* Embedded website content
* Browser services
* Applications running in the background
* System activity

Further investigation would be required before treating these queries as suspicious.

---

# 16. Evidence Table

| Time              | Evidence Source      | Evidence                                                | Interpretation                                            |
| ----------------- | -------------------- | ------------------------------------------------------- | --------------------------------------------------------- |
| 09:59:25          | Windows Event Viewer | Event ID 4634                                           | A logon session was terminated                            |
| 09:59:40          | Windows Event Viewer | Event ID 4624                                           | Successful logon                                          |
| 09:59:40+         | Windows Event Viewer | Logon Type 2                                            | Interactive logon consistent with direct user interaction |
| After 4624        | Windows Event Viewer | Event ID 4672                                           | Special privileges associated with the new logon          |
| 10:01:04          | Wireshark            | Capture begins                                          | Network activity monitoring begins                        |
| 10:01:23          | Wireshark            | DNS query for [www.isea.gov.in](http://www.isea.gov.in) | Domain resolution requested                               |
| 10:01:23+         | Wireshark            | DNS response / A record                                 | IPv4 address returned                                     |
| 10:01:23+         | Wireshark            | TCP traffic to 164.100.xx.x:443                         | Connection to HTTPS service                               |
| 10:01:23+         | Wireshark            | SYN / SYN-ACK / ACK                                     | TCP connection established                                |
| 10:01:04–10:01:56 | Windows Event Viewer | Event ID 4798                                           | Local group membership enumeration                        |
| During capture    | Wireshark            | FIN packets                                             | Individual TCP connections terminated                     |
| 10:01:56          | Wireshark            | Capture ends                                            | Network monitoring stops                                  |

---

# 17. Windows vs. Network Evidence

The two tools provided different types of evidence.

## Windows Event Viewer

Focused primarily on system-level activity, such as:

```text
Users
Logons
Logoff/session activity
Privileges
Processes
System activity
Security events
```

## Wireshark

Focused on network-level activity, such as:

```text
Packets
DNS
IP addresses
Ports
TCP connections
TCP flags
TLS/HTTPS traffic
```

Therefore, the two sources complement each other.

```text
Windows
   ↓
What was happening on the system?

Wireshark
   ↓
What was happening on the network?

       ↓

Correlation
       ↓

Can the two sources explain the same activity?
```

---

# 18. Correlation Attempt

The investigation attempted to determine whether the Windows Security events observed during the Wireshark capture could be directly associated with the browsing activity.

The network capture clearly showed activity associated with DNS resolution and subsequent TCP/TLS connections.

However, the Windows Security events observed during the same period were primarily Event ID 4798.

No Windows Security event was identified that directly stated:

> "The user opened ISEA."

or:

> "The user opened Hashnode."

Therefore, a direct one-to-one correlation between the 4798 events and the specific website visits could not be established from the available evidence.

This is important because temporal proximity alone does not prove causation.

---

# 19. Investigation Findings

## Finding 1 — Successful interactive logon

A successful Event ID 4624 with Logon Type 2 was observed at approximately 09:59:40.

This was consistent with the user's direct interaction with the laptop.

---

## Finding 2 — Special privileges

Event ID 4672 was observed following the successful logon.

The event indicates that the new logon was associated with special privileges.

The event should be interpreted in the context of the account and the privileges listed rather than being automatically classified as suspicious.

---

## Finding 3 — Local group membership enumeration

Event ID 4798 was repeatedly observed during the investigation.

This indicates local group membership enumeration.

No evidence from this investigation was sufficient to establish that the enumeration was malicious.

---

## Finding 4 — DNS activity

A DNS query for:

```text
www.isea.gov.in
```

was observed at approximately 10:01:23.

The request was sent to:

```text
8.8.8.8
```

and an IPv4 address was returned through an A record.

---

## Finding 5 — HTTPS connection

A TCP connection was observed from my system to:

```text
164.100.xx.x:443
```

The capture contained TCP sequence/acknowledgement information and the expected connection establishment process.

The traffic was consistent with HTTPS/TLS communication.

---

## Finding 6 — TCP connection termination

FIN packets were observed.

These indicated termination of individual TCP connections.

They were not interpreted as evidence that the browser tabs themselves were closed.

---

## Finding 7 — Unexpected DNS queries

Some DNS queries were observed for services that I did not intentionally access during the capture.

These were not immediately classified as suspicious because background activity, browser behavior, embedded content, or other applications could explain them.

Additional evidence would be required before determining whether they were unusual.

---

# 20. Suspicious Indicators

No activity observed during this investigation was sufficient to classify the system as compromised.

However, the following patterns would make a login or account activity more interesting for further investigation:

| Indicator                                             | Why investigate?                                                              |
| ----------------------------------------------------- | ----------------------------------------------------------------------------- |
| Multiple failed logons followed by a successful logon | Could indicate attempted credential guessing or other authentication activity |
| Unexpected logon type                                 | May indicate an authentication method that requires explanation               |
| Unexpected source address                             | Could indicate an unusual origin of authentication                            |
| Login at an unusual time                              | May require contextual investigation                                          |
| Unexpected process after login                        | Could indicate unusual execution                                              |
| Unexpected files being executed                       | May indicate suspicious program activity                                      |
| Unexpected service creation/start                     | Could indicate persistence or other unauthorized activity                     |
| Unexpected privilege assignment                       | Requires checking whether the account should have those privileges            |
| Unexpected network connections                        | Could indicate communication with an unfamiliar system                        |
| Activity inconsistent with the account's normal role  | Could indicate account misuse                                                 |

No single indicator should automatically be treated as proof of compromise.

---

# 21. Limitations

The investigation had several limitations.

* The Wireshark capture covered only 10:01:04–10:01:56.
* Windows events before and during the capture were examined, but not every possible Windows log was correlated.
* No direct Windows Security event identifying the individual website visit was found.
* The connection duration was not determined.
* The contents of HTTPS traffic could not be directly inspected because the application data was encrypted.
* Some unexpected DNS queries could not be conclusively attributed to a particular application.
* The investigation was conducted on my own system during normal activity rather than during a known attack scenario.

---

# 22. What Would I Investigate Next?

If this were a real SOC investigation, I would investigate:

### Authentication

* Are there failed 4625 events before the successful 4624?
* Do the account and source details match?
* Is the logon type expected?

### Privileges

* Which privileges were listed in Event ID 4672?
* Is the account expected to receive them?
* Does the Logon ID correlate with the preceding 4624?

### Processes

* What process generated the 4798 events?
* Were unusual processes created after authentication?
* Were any unusual executables launched?

### Services

* Were any services started or created?
* Are those services expected?

### Network

* Which process generated the unexpected DNS requests?
* What destinations did the system communicate with?
* Were the destinations expected?
* Did any suspicious connections occur after authentication?

### Timeline

* What happened immediately before the login?
* What happened immediately after it?
* What happened before and after the network connections?

---

# 23. Conclusion

The investigation demonstrated how Windows Event Viewer and Wireshark can provide different but complementary views of activity on a computer.

The Windows logs showed authentication, privilege-related activity, and local group membership enumeration.

Wireshark showed DNS resolution followed by TCP and encrypted HTTPS/TLS communication.

The timestamps allowed the two sources to be compared, but the available evidence did not establish a direct relationship between the Windows 4798 events and the individual website visits.

No genuinely suspicious activity was identified during the investigation.

Some unexpected DNS queries were observed, but they could not be classified as malicious without additional evidence.

The main lesson from the investigation was:

> **An event occurring at the same time as another event does not automatically mean that the two events are related.**

A SOC analyst needs to correlate evidence, examine context, and build a timeline before reaching a conclusion.

---

# 24. Investigation Flow

```text
User locks / interacts with system
            ↓
Windows authentication events
            ↓
4624 — Successful logon
            ↓
4672 — Special privileges
            ↓
Wireshark capture begins
            ↓
DNS query
            ↓
DNS response
            ↓
TCP connection
            ↓
TLS / HTTPS communication
            ↓
TCP connection termination
            ↓
Windows 4798 events observed
            ↓
Compare timestamps
            ↓
Attempt correlation
            ↓
Evaluate evidence
            ↓
No confirmed malicious activity
```

---

# 25. Key Lessons

### Windows

> What happened on the system?

### Wireshark

> What happened on the network?

### MITRE ATT&CK

> What attacker behavior could this evidence potentially represent?

### Investigation

> Does the evidence actually support that interpretation?

The objective is not to find an attack in every investigation.

The objective is to determine what happened based on available evidence.


