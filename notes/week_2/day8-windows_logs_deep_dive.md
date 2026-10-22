# Week 2 — Day 1: Windows Event Logs Deep Dive

## Objective

Understand important Windows Security events and their fields, then use basic correlation to reason about what happened, which account or process was involved, what evidence supports the interpretation, and what additional evidence would be needed.

---

## Part 1 — Basic Timeline Correlation

I investigated a different event from the one used earlier and looked for other relevant Security events within approximately one minute before and after it.

### Finding

I did not find another clearly related event within the selected time window.

This means there was not enough nearby evidence to establish a relationship with another event.

---

# Part 2 — Event ID Understanding

## Q1. What do the event IDs represent?

### 4624 — Successful Logon

A 4624 event indicates that a logon was successful.

The context of the logon depends on the Logon Type. For example, a Type 5 logon represents a service logon, while a Type 2 logon represents an interactive logon.

A successful logon does not necessarily mean that a human user physically logged into the computer.

### 4625 — Failed Logon

A 4625 event indicates that a logon attempt failed.

### 4688 — Process Creation

A 4688 event records the creation of a new process.

It can provide information such as the newly created process, its path, and the creator/parent process. This information can help an analyst understand process activity and correlate it with other events when appropriate.

---

## Q2. Difference between 4624 and 4688

A 4624 event is concerned with a **successful logon** and provides information about the account and context of that logon.

A 4688 event is concerned with **process creation** and provides information about a process that was created.

A 4688 should not automatically be described as something that occurred during a particular logon session. It can be correlated with logon activity when other evidence supports the connection.

---

## Q3. Logon Types

### Logon Type 2 — Interactive

An interactive logon occurs when a user directly interacts with the computer to log in, such as entering their credentials at the Windows login screen.

### Logon Type 5 — Service

A service logon occurs when a Windows service logs on using an account so that the service can run with that account's security context.

---

## Q4. Why isn't one event enough?

One event usually does not provide enough evidence to determine whether activity is malicious.

Useful information to examine includes:

* Network information, when available
* The process path
* The parent/creator process
* The authenticity or legitimacy of the file
* The account involved
* The timing and relationship with other events

These pieces of evidence provide context before making a conclusion.

---

# Part 3 — SOC Analyst Thinking

## Q5. Investigating an unfamiliar executable in a temporary directory

If a 4688 event showed:

`C:\Users\User\AppData\Local\Temp\something.exe`

I would investigate it rather than immediately declaring it malicious.

My investigation would include:

1. Check the process path and filename.
2. Check the parent/creator process.
3. Check the account associated with the activity.
4. Check whether other relevant events occurred around the same time.
5. Check the authenticity/legitimacy of the file.
6. Examine available network information if present.
7. Determine whether the available evidence is consistent with normal activity or requires further investigation.

---

## Q6. Comparing two process paths

### Case A

`C:\Windows\System32\lsass.exe`

### Case B

`C:\Users\User\AppData\Local\Temp\lsass.exe`

I would not investigate them in exactly the same way.

The first path is the normal Windows System32 location for `lsass.exe` and is consistent with a legitimate Windows process based on the available evidence.

The second has the same filename but is located in a user's local temporary directory. Because the location is unusual for `lsass.exe`, I would investigate it further.

However, the unusual path alone does not prove that the file is malicious.

I would look for additional evidence such as:

* Other failed or successful logons
* Other process-creation events
* Timing relationships between events
* The parent/creator process
* File authenticity
* Other available telemetry

---

# Part 4 — Final Day 1 Reflection

## Q7. Useful fields when investigating Windows Security events

Important fields include:

* Process path
* Network information, when available
* Event time
* Account involved
* Logon Type
* Logon ID
* Creator/parent process
* New process name

For logon events, the account, Logon Type, Logon ID, time, and available network/process information can provide useful context.

For process-creation events, the process path, new process, creator process, time, and available user information are useful.

---

## Q8. Something I initially misunderstood

I initially thought that a service was requesting to create a session for an account and that this was what a successful logon event represented.

I now understand that **4624 means a logon was successfully completed**, while the Logon Type provides the context of that logon.

For example, the 4624 event I investigated had Logon Type 5, which indicates a service logon.

---

## Q9. Basic thought process for investigating a Windows event

My basic process would be:

**Event → Time → What happened → Account/process involved → Relevant fields → Correlate with nearby evidence → Determine whether the activity is consistent with normal behavior or requires further investigation**

For a logon event, I would examine:

* User/account
* Logon Type
* Logon ID
* Time
* Available network information
* Relevant process information

For a process-creation event, I would examine:

* New process
* Process path
* Creator/parent process
* Account/user, if available
* Time
* Other nearby events

---

# Day 1 Key Takeaways

* **4624 = successful logon**
* **4625 = failed logon**
* **4688 = process creation**
* Logon Type provides context for a 4624 event.
* **Type 2 = Interactive logon**
* **Type 5 = Service logon**
* A process path provides useful context, but a path alone does not establish whether something is malicious.
* A process name such as `lsass.exe` should be considered together with its path and other available evidence.
* Nearby events can help establish context, but temporal proximity alone does not prove that events are related.
* Missing network or command-line information is a telemetry limitation, not automatically evidence of malicious activity.
* A single isolated event generally should not be used to declare activity malicious.
* Investigation should move from **what happened → who/what was involved → what evidence supports it → what additional evidence is needed**.

