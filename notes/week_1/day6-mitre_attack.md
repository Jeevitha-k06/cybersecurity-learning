# Day 6 — MITRE ATT&CK

## 1. Objective

The objective of this investigation is to understand how MITRE ATT&CK can be used by a SOC analyst to understand attacker behavior and connect observed Windows activity with possible attack techniques.

The main technique studied today is:

**T1078 — Valid Accounts**

The focus is not on memorizing MITRE ATT&CK techniques, but on understanding:

* Why attackers perform certain actions
* How those actions are carried out
* What evidence those actions can leave behind
* How a SOC analyst can investigate that evidence
* Why one event alone should not automatically be considered malicious

---

# 2. What is MITRE ATT&CK?

MITRE ATT&CK is a knowledge base that organizes known adversary behaviors and techniques used during cyber attacks.

It helps analysts understand how attackers may operate throughout an intrusion.

Instead of only asking:

> "What malware was used?"

an analyst can ask:

> "What behavior did the attacker perform?"

> "What was the attacker trying to achieve?"

> "How was the action carried out?"

> "What evidence could this behavior leave behind?"

This makes ATT&CK useful for threat detection, investigation, threat intelligence, and understanding how different actions can be chained together during an attack.

---

# 3. Tactics

## What question does a tactic answer?

A tactic primarily answers:

> **Why is the attacker performing this action?**

A tactic represents the attacker's objective or goal at a particular stage of an intrusion.

Examples of objectives include:

* Gaining initial access
* Obtaining credentials
* Executing commands
* Escalating privileges
* Maintaining persistence
* Avoiding detection
* Obtaining valuable information

For example, if an attacker wants to obtain higher privileges, the activity may fall under the **Privilege Escalation** tactic.

### Why are tactics useful to a SOC analyst?

Understanding the attacker's objective helps an analyst reason about what the attacker may do next.

If evidence suggests that an attacker has obtained credentials, the analyst should consider:

> What could the attacker do with those credentials?

> Could they use them to access another system?

> Could they attempt privilege escalation?

> Could they disable security controls?

Therefore, understanding the "why" helps an analyst understand the possible progression of an attack.

---

# 4. Techniques

## What question does a technique answer?

A technique describes:

> **How does the attacker achieve an objective?**

A technique represents a specific adversary behavior used to accomplish a tactical goal.

For example, an attacker may use **Valid Accounts** to obtain or maintain access to a system using legitimate credentials.

### Important distinction

A tool is not automatically a technique.

For example:

**Wireshark** is a network analysis and packet-capture tool.

Using Wireshark to capture packets is not itself a MITRE ATT&CK technique.

A technique describes **attacker behavior**, while a tool is something that can be used to perform an action.

Therefore, an analyst should ask:

> What is the attacker actually doing?

rather than:

> What tool did they use?

---

# 5. Sub-techniques

A sub-technique provides a more specific classification within a broader technique.

It answers:

> **What specific form or implementation of this technique is being used?**

For example, T1078 — Valid Accounts has different sub-techniques based on the type of account being abused.

These include:

| Sub-technique | Area             |
| ------------- | ---------------- |
| T1078.001     | Default Accounts |
| T1078.002     | Domain Accounts  |
| T1078.003     | Local Accounts   |
| T1078.004     | Cloud Accounts   |

This provides more precision than simply saying that valid credentials were used.

---

# 6. Procedure Examples

A procedure example shows how a particular technique has been used by a known threat actor, malware family, or intrusion campaign.

It connects the abstract ATT&CK technique to an observed real-world implementation.

The useful question is:

> **How has this behavior actually been carried out in a real attack?**

A procedure example is therefore evidence of how a technique has been implemented in practice rather than simply being a generic step-by-step attack tutorial.

---

# 7. Behavior, Techniques and Tools

An attacker may have a particular objective, such as gaining access to a system.

The behavior describes the action being performed.

The technique categorizes that behavior according to ATT&CK.

A tool may be used to perform the action.

A simplified relationship can therefore be understood as:

```text
Attacker Objective
       ↓
     Tactic
       ↓
    Behavior
       ↓
   Technique
       ↓
Tool / Method used to perform it
       ↓
Evidence left on the system/network
```

For example:

```text
Goal: Gain or maintain access
        ↓
Tactic: Credential / Access-related objective
        ↓
Behavior: Use legitimate credentials
        ↓
Technique: T1078 — Valid Accounts
        ↓
Possible evidence:
Windows authentication events
process activity
network connections
account activity
```

The exact classification depends on what actually occurred.

---

# 8. Why Does a SOC Analyst Need MITRE ATT&CK?

A SOC analyst needs to understand attacks not only as isolated events but as a chain of behaviors.

An analyst should be able to ask:

> What happened?

> Why might the attacker have done it?

> How could they have performed it?

> What evidence should exist?

> What could they do next?

> Which other events could be related?

Understanding ATT&CK helps analysts connect individual observations to broader attacker behavior.

For example:

```text
Credential access
       ↓
Valid account obtained
       ↓
Login using valid account
       ↓
Command execution
       ↓
Privilege escalation
       ↓
Defense evasion
       ↓
Access to sensitive information
```

The presence of one event does not prove that the entire chain occurred.

The analyst must collect and correlate evidence.

---

# 9. Enterprise ATT&CK Matrix

The Enterprise ATT&CK matrix organizes adversary behaviors according to tactics and techniques relevant to enterprise environments.

It allows an analyst to consider different stages and objectives of an attack.

Examples of areas represented in the Enterprise matrix include:

* Initial Access
* Execution
* Persistence
* Privilege Escalation
* Defense Evasion
* Credential Access
* Discovery
* Lateral Movement
* Collection
* Command and Control
* Exfiltration
* Impact

### Questions to ask when looking at the matrix

> If an attacker gains access, what could they attempt next?

> Could they execute commands?

> Could they obtain credentials?

> Could they escalate privileges?

> Could they disable or bypass security controls?

> Could they move to another system?

The matrix is therefore useful for understanding possible attack paths rather than treating every event as an isolated incident.

---

# 10. T1078 — Valid Accounts

## What is a valid account?

A valid account is a legitimate account that can be used to authenticate to a system, service, application, or resource.

The account may already have legitimate permissions and access.

An attacker who obtains or abuses valid credentials can therefore potentially use the account without needing to create an obviously suspicious new account.

---

# 11. Why Would an Attacker Use a Valid Account?

An attacker may prefer a legitimate account because it can already possess useful permissions.

The account may allow access to:

* Systems
* Files
* Services
* Applications
* Network resources
* Other accounts or systems

This can make malicious activity harder to distinguish from legitimate activity.

The important idea is:

> **The account itself may be legitimate while the activity performed through it may not be.**

---

# 12. Does Using a Legitimate Account Mean Malicious Activity?

**No.**

A legitimate account being used does not automatically indicate an attack.

The analyst must examine the activity performed by that account.

For example, a legitimate administrator may:

* Log in
* Access sensitive files
* Start services
* Run administrative processes
* Access another computer
* Perform security-related actions

These actions may all be completely legitimate depending on the situation.

The question should therefore be:

> **Does the observed activity make sense for this account, system, time, and situation?**

---

# 13. What Could Make Valid Account Usage Suspicious?

Potential indicators include:

* Login at an unusual time
* Login from an unusual system
* Login from an unexpected network address
* Unexpected logon type
* Unusual processes being executed
* Unexpected files being accessed
* Unexpected services being started
* Multiple accounts being used unexpectedly
* Security controls being disabled
* Repeated failed logons followed by a successful login
* Activity inconsistent with the normal role of the account

However:

> **One unusual characteristic is not automatically proof of malicious activity.**

The analyst should correlate multiple pieces of evidence.

---

# 14. Why Is T1078 Difficult to Detect?

Valid account abuse can be difficult to identify because the credentials may belong to a legitimate user.

From a superficial perspective:

```text
Legitimate account
        ↓
Valid credentials
        ↓
Successful authentication
```

may look normal.

If an attacker instead created a new account and immediately performed suspicious actions, the activity could be much easier to notice.

With valid accounts, the analyst must investigate the **context and behavior** associated with the account.

---

# 15. Evidence Relevant to Valid Account Investigation

When investigating a potentially suspicious login, what should be examined?

| Evidence                   | Question to Ask                                         |
| -------------------------- | ------------------------------------------------------- |
| Account name               | Who is the account?                                     |
| Logon type                 | How was the authentication performed?                   |
| Timestamp                  | When did the activity occur?                            |
| Computer                   | Which system recorded or was involved in the activity?  |
| Source/network information | Where did the authentication originate, if available?   |
| Process                    | What process was associated with the activity?          |
| Authentication information | How was authentication performed?                       |
| Failed logons              | Were there failed attempts before the successful login? |
| Subsequent activity        | What happened after authentication?                     |
| Services                   | Were unexpected services started?                       |
| Files                      | Were unusual or sensitive files accessed?               |
| Network activity           | Were unexpected connections established?                |

The goal is not to investigate each field independently.

The goal is to ask:

> **Does the complete sequence of activity make sense?**

---

# 16. Connecting T1078 to Windows Events

Windows authentication events can provide useful evidence when investigating potential valid-account abuse.

Important information may include:

### Account

Does the account name match an expected user or system account?

### Logon Type

Does the logon type make sense for the situation?

For example, a different logon type from what is normally observed may deserve further investigation.

### Time

Did the authentication occur during expected working activity?

An unusual time does not automatically mean malicious activity because legitimate automated processes can also occur outside normal working hours.

### Computer

Which computer generated or recorded the event?

If the activity involves remote authentication, additional evidence may be required to determine where the request originated.

### Source / Network Information

If network information such as an IP address is available:

> Is the address expected for the environment?

An unexpected source address may require investigation.

However, the absence of an IP address does not automatically make an event suspicious.

### Process

What process was associated with the activity?

If an unexpected or unusual executable is involved, the analyst should investigate it further.

### Authentication Information

What authentication mechanism or information is recorded?

If the authentication involves a different or unexpected path, the analyst should investigate how and why the authentication occurred.

---

# 17. Previous Windows Investigation — JEEVITHA$

A previously investigated Windows event involved:

```text
Account: JEEVITHA$
Computer: JEEVITHA
Logon Type: 5
Process information: Available
Network/IP information: Not available
```

The event occurred at:

```text
02-09-2026 19:02
```

The `$` at the end of the account name indicates that it is a machine/computer account naming convention rather than an ordinary human username.

### Could this event be suspicious?

The event should **not** automatically be classified as suspicious.

Questions to investigate would include:

> Is Logon Type 5 expected for this account?

> What process generated the event?

> Is the process associated with a legitimate Windows service?

> Was there any unusual activity immediately before or after the event?

> Were there failed authentication attempts?

> Were there other successful authentication events?

> Did any unexpected processes start?

> Were services created or started?

> Was there unusual network activity?

> Does the event fit normal system activity?

The event becomes more meaningful when correlated with other evidence.

---

# 18. Windows Logon Types

| Logon Type | Meaning            | Investigation Question                                                        |
| ---------- | ------------------ | ----------------------------------------------------------------------------- |
| **2**      | Interactive logon  | Was someone physically using the computer, or is there another explanation?   |
| **3**      | Network logon      | What resource or service was accessed over the network?                       |
| **4**      | Batch logon        | Was a scheduled or automated task responsible?                                |
| **5**      | Service logon      | Which service caused the authentication, and is that service expected?        |
| **7**      | Unlock             | Who or what unlocked the existing session?                                    |
| **10**     | Remote Interactive | Was remote access expected, and what happened after the remote session began? |

---

# 19. Logon Type 2 — Interactive

Logon Type 2 represents an interactive logon.

A typical example is a person physically interacting with the computer and authenticating to the system.

### Investigation questions

> Was the user expected to be logging in at this time?

> Does the account normally use this computer?

> Were there failed attempts beforehand?

> What processes or activity occurred after the login?

---

# 20. Logon Type 3 — Network

Logon Type 3 represents a network logon.

It can occur when an account accesses resources over a network, such as:

* Shared folders
* Network resources
* Printers
* Other network-accessible services

### Investigation questions

> What network resource was accessed?

> Which system initiated the connection?

> Was the source system expected?

> What files, services, or processes were accessed afterward?

> Was the account normally expected to access that resource?

---

# 21. Logon Type 4 — Batch

Logon Type 4 is associated with batch processing and automated activity.

For example, a scheduled task or automated process may require authentication.

### Investigation questions

> Was a scheduled task responsible?

> Is the task legitimate?

> Was the task already configured on the system?

> Did the task execute an expected program?

> Could an attacker have created or modified the task?

The presence of an automated logon is therefore not automatically malicious.

---

# 22. Logon Type 5 — Service

Logon Type 5 is associated with a service logon.

A Windows service may need to authenticate automatically when it starts.

### Investigation questions

> Which service caused the logon?

> Is the service legitimate?

> Is the service expected to start automatically?

> What executable does the service use?

> Was the service recently created or modified?

> Did the service perform unusual activity afterward?

A service-related login can therefore be completely normal, but unexpected service activity can require investigation.

---

# 23. Logon Type 7 — Unlock

Logon Type 7 represents an existing session being unlocked.

The computer was previously locked and was subsequently unlocked.

### Investigation questions

> Who was expected to unlock the system?

> Was the workstation expected to be in use at this time?

> Are there other authentication events around the same time?

---

# 24. Logon Type 10 — Remote Interactive

Logon Type 10 represents a remote interactive logon.

It is commonly associated with remote desktop-style interactive access.

### Investigation questions

> Was remote access expected?

> Who initiated the remote session?

> From which system did the connection originate?

> Was the source address expected?

> What happened after the remote login?

> Which processes were started?

> Which files or systems were accessed?

A Type 10 event is not automatically a hacking event. Its significance depends on the surrounding evidence and whether the remote access was authorized.

---

# 25. How Should a SOC Analyst Investigate a Suspicious Login?

A useful investigation chain is:

```text
Successful Login
       ↓
Check Failed Logons
       ↓
Check Account
       ↓
Check Logon Type
       ↓
Check Time
       ↓
Check Source / Network Information
       ↓
Check Process Activity
       ↓
Check Services
       ↓
Check Files / System Changes
       ↓
Check Network Activity
       ↓
Correlate Events
       ↓
Determine Whether Activity Makes Sense
```

The successful login itself should not be treated as the conclusion.

It should be treated as the **starting point for investigation**.

---

# 26. Correlating 4624 and 4625

A successful logon event can become more meaningful when compared with failed logon events.

For example:

```text
Multiple failed attempts
        ↓
Successful authentication
        ↓
Unexpected process
        ↓
Unexpected network connection
```

This sequence may require much more investigation than an isolated successful login.

Questions to ask:

> Did failed logons occur before the successful login?

> Do the account details match?

> Are the timestamps close together?

> Does the source information match?

> Did unusual activity occur after the successful authentication?

> Does the complete sequence suggest normal activity or something unusual?

---

# 27. Evidence Correlation

A SOC analyst should avoid making conclusions from one field or one event whenever possible.

For example:

```text
Unusual login time
```

by itself may not mean much.

But:

```text
Unusual login time
        +
Unexpected source
        +
Failed authentication attempts
        +
Unexpected process
        +
Unexpected network connection
```

creates a much stronger reason for investigation.

Therefore:

> **Context and correlation are more important than isolated events.**

---

# 28. What Evidence Would I Look For?

When investigating possible valid-account abuse, I would look for:

### Authentication

* Successful logons
* Failed logons
* Logon type
* Account involved
* Authentication information

### Process Activity

* Processes created after authentication
* Unexpected executables
* Unusual command execution

### Services

* New services
* Modified services
* Unexpected service execution

### Files

* Sensitive files accessed
* Unexpected files created
* Unusual modifications

### Network

* Source and destination addresses
* Unexpected connections
* Remote systems accessed
* Connections outside the expected environment

### Timeline

* What happened before authentication?
* What happened during authentication?
* What happened immediately afterward?

---

# 29. What Would Make the JEEVITHA$ Event More Interesting?

The previously investigated JEEVITHA$ event would require more attention if additional evidence showed something such as:

```text
JEEVITHA$ authentication
        ↓
Unexpected logon behavior
        ↓
Unexpected process
        ↓
Unexpected service
        ↓
Unusual network activity
```

However, the event should still be investigated rather than immediately declared malicious.

The correct approach is:

> **Find evidence that either supports or weakens the suspicious hypothesis.**

---

# 30. Key Investigation Principle

A SOC analyst should not ask only:

> "Is this suspicious?"

Instead, the investigation should progress through:

```text
What happened?
      ↓
Why might it have happened?
      ↓
How did it happen?
      ↓
What evidence supports this?
      ↓
What evidence contradicts this?
      ↓
What happened before?
      ↓
What happened after?
      ↓
Does the complete sequence make sense?
```

This prevents individual unusual events from being incorrectly classified as attacks.

---

# 31. Questions I Still Have

* How can I determine whether a particular Windows service is legitimate?
* How can I identify the exact source of a remote authentication?
* Which Windows events should be correlated with Event ID 4624?
* Which events can show that a service was created or modified?
* How can process creation events help connect a login to subsequent activity?
* How can network evidence be correlated with Windows authentication events?
* How can I determine what is normal for a particular account?
* How can MITRE ATT&CK techniques be mapped automatically from SIEM alerts?

---

# 32. Key Takeaways

### MITRE ATT&CK

* **Tactic** → Why / objective
* **Technique** → How / adversary behavior
* **Sub-technique** → More specific form of the behavior
* **Procedure example** → Real-world example of how a technique was implemented
* **Tool** → Software or mechanism used to perform an action

### T1078 — Valid Accounts

* A legitimate account can be abused by an attacker.
* Valid-account use is not automatically malicious.
* The behavior performed by the account is what requires investigation.
* Context is essential.
* Authentication events should be correlated with process, service, file, and network activity.

### SOC Investigation

```text
Event
 ↓
Context
 ↓
Correlation
 ↓
Timeline
 ↓
Evidence
 ↓
Analysis
 ↓
Conclusion
```

The objective is not to label every unusual event as an attack.

The objective is to determine:

> **What happened, whether it makes sense, and what evidence supports the conclusion.**
