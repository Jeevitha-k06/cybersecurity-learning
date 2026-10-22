# Day 5 — MITRE ATT&CK + Detection Thinking

## Objective

The objective of Day 5 was to connect the Windows and PowerShell telemetry studied during Days 1–4 with MITRE ATT&CK and begin thinking about how observed behavior can become a detection hypothesis.

The focus was on:

* T1059 — Command and Scripting Interpreter
* T1059.001 — PowerShell
* T1078 — Valid Accounts
* Connecting observed telemetry to attacker behavior
* Beginning to think in terms of detection rather than simply identifying events

---

## 1. T1059 — Command and Scripting Interpreter

T1059 covers the use of command and scripting interpreters to execute commands, scripts, or other programs.

From my understanding, attackers can abuse script interpreters because they provide a way to execute commands and binaries using tools that may already exist on the system.

This makes the interpreter itself important from a defensive perspective, but its presence alone does not establish malicious activity.

---

## 2. T1059.001 — PowerShell

T1059.001 is the PowerShell sub-technique of T1059.

PowerShell is particularly relevant to Windows investigations because it can be used to execute commands and perform system operations. It can also be invoked without the user necessarily opening a visible PowerShell window.

PowerShell can perform actions such as:

* Executing commands
* Running scripts
* Interacting with files and processes
* Downloading or executing other content

Some PowerShell activity can also be performed in ways where the resulting payload does not need to be written to disk in the usual way. This makes understanding the surrounding telemetry important rather than relying only on the presence of a file.

### My observation

From my Day 4 investigation, I observed PowerShell activity such as:

* `whoami`
* `hostname`

I also observed corresponding process/log evidence.

One thing I noticed is that the telemetry can differ depending on what PowerShell actually executes.

For example, a command such as `whoami` results in the execution of `whoami.exe`, while a PowerShell cmdlet is handled differently.

Therefore, when investigating PowerShell activity, I should not only look for the existence of PowerShell. I should also examine what it actually executed and what additional processes or activity resulted from it.

---

## 3. Connecting PowerShell to Telemetry

The investigation work from Days 1–4 gives me several types of evidence that can be useful when examining PowerShell activity.

Examples include:

* Process creation
* Command line
* Parent process
* User
* PowerShell-related logging
* Related processes
* Potential file or network activity

The important idea is that:

```text
PowerShell observed
        ↓
What did PowerShell execute?
        ↓
What evidence was generated?
        ↓
What was the surrounding context?
```

This is more useful than treating every PowerShell execution as suspicious.

---

# 4. T1078 — Valid Accounts

T1078 describes the abuse of legitimate accounts for activities such as gaining access, maintaining access, or obtaining additional privileges.

The important point is that the credentials or account involved may be legitimate. The suspicious part can be **how the account is being used**, rather than whether the account itself is fake.

An attacker could potentially abuse:

* Existing accounts
* Compromised user accounts
* Accounts that are not normally active
* Accounts with higher privileges

### My understanding

An attacker could abuse an existing account to gain access to a system or obtain higher privileges.

An inactive or unusual account becoming active could therefore be worth investigating.

Similarly, activity involving multiple accounts or changes in privilege level may provide useful context when reconstructing what happened.

---

## 5. Possible Evidence for T1078

Some evidence that could be relevant when investigating possible valid-account abuse includes:

* An unusual account logging in
* An account being used at an unusual time or in an unusual context
* Sequential activity involving accounts with different privilege levels
* A large number of failed logins followed by a successful login
* Suspicious activity occurring after a successful authentication

These observations do **not automatically prove** valid-account abuse.

They are signals that would lead to further investigation.

For example:

```text
Multiple failed logins
        ↓
Successful login
        ↓
Account performs unusual activity
        ↓
Investigate authentication + subsequent activity
```

The surrounding evidence is necessary to determine what actually happened.

---

# 6. Detection Thinking

The main change from the earlier days is moving from:

> "What does this event mean?"

toward:

> "What evidence would I expect if a particular behavior occurred?"

For PowerShell, a useful starting hypothesis is:

> If an attacker used PowerShell for execution, I would expect to see evidence of PowerShell execution and potentially additional evidence showing what PowerShell executed and what activity followed.

Relevant evidence could include:

* Process creation
* Command line
* Parent process
* User
* PowerShell logging
* Child processes
* File activity
* Network activity

The important part is the relationship between the evidence.

```text
PowerShell
    ↓
Command / Script
    ↓
Child Process or Other Activity
    ↓
Additional Evidence
```

---

# 7. Detection Hypothesis

A useful detection idea should not simply be:

> "Alert whenever PowerShell runs."

PowerShell is a legitimate Windows administration tool and can be used normally.

A more useful hypothesis is to investigate PowerShell when its **context or behavior is unusual**.

For example:

> Investigate PowerShell execution when it occurs with an unusual parent process, unusual command-line characteristics, an unexpected account, or other activity that provides additional suspicious context.

This gives a starting point for a future detection rule.

At this stage, I am not writing a SIEM query or detection rule. I am first learning how to reason about what evidence a detection should use.

---

# 8. Applying This to My Own Activity

My own PowerShell activity provides a useful example of why context matters.

I generated normal commands such as:

```text
whoami
hostname
```

These produced observable telemetry.

However, simply seeing:

```text
powershell.exe
```

does not tell me whether the activity is malicious.

I would need to examine additional context such as:

* What command was executed?
* Which user executed it?
* What was the parent process?
* What child process was created?
* Was there related file activity?
* Was there related network activity?
* Does the activity make sense for the user's normal behavior?

This reinforces the investigation approach from earlier days:

```text
Event
 ↓
Evidence
 ↓
Context
 ↓
Relationship with other evidence
 ↓
Interpretation
```

---

# 9. Important Distinction

There is an important difference between:

> PowerShell was executed.

and:

> An attacker used PowerShell for malicious execution.

The first is an observation.

The second is an interpretation that requires supporting evidence.

Therefore, I should avoid treating individual events or tools as automatically malicious.

The goal is to determine what happened from the available evidence.

---

# 11. What I Understand

* T1059 represents Command and Scripting Interpreter activity.
* T1059.001 specifically represents PowerShell.
* PowerShell can be used legitimately as well as abused by attackers.
* PowerShell execution can produce different telemetry depending on what is actually executed.
* The existence of PowerShell alone is not enough to establish malicious activity.
* T1078 involves the abuse of legitimate accounts.
* Unusual account activity can provide useful investigation signals.
* Multiple pieces of evidence should be correlated before reaching an interpretation.
* A detection hypothesis should focus on behavior and context rather than simply alerting on the presence of a tool.

---

# 12. What I Still Need to Practice

* Connecting specific PowerShell behaviors to the appropriate MITRE ATT&CK techniques.
* Becoming better at turning observed telemetry into concrete detection hypotheses.
* Understanding how multiple pieces of Windows telemetry can strengthen or weaken an investigation hypothesis.
* Eventually translating detection hypotheses into actual SIEM/detection queries.

---

## Day 5 Takeaway

The main lesson from today is:

> **A tool is not the behavior. The behavior and its context are what I need to investigate.**

PowerShell is a good example. Its presence gives me a starting point, but the useful investigation begins with determining what was executed, by whom, from where, and what happened afterward.
