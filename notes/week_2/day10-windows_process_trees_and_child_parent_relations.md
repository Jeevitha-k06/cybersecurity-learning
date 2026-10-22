# Day 3 — Process Trees & Parent/Child Relationships

## Objective

Understand how parent and child processes are represented in Sysmon Event ID 1 and use their relationships to reconstruct normal process execution.

---

## Key Concepts

### Parent Process

The parent process is the process that creates or launches another process.

For example:

```text
explorer.exe
     ↓
notepad.exe
```

Here, `explorer.exe` is the parent and `notepad.exe` is the child.

### Child Process

The child process is the process that was created by another process.

In the example above, `notepad.exe` is the child process.

### Process ID (PID)

A PID is an identifier assigned to a running process. It helps distinguish processes while they are running.

A PID should not be treated as a permanent identifier for an application because Windows can reuse PIDs.

### Process GUID

Sysmon also records a Process GUID. This provides a more specific identifier for a particular process instance and can be useful when correlating Sysmon events.

---

# Process Tree 1 — Existing Explorer → Notepad Activity

This was an existing Sysmon Event ID 1 observed during the previous investigation.

### Evidence

**Parent process:**

```text
explorer.exe
```

**Parent image:**

```text
C:\Windows\explorer.exe
```

**Parent Process ID:**

```text
9152
```

**Command line:**

```text
C:\WINDOWS\Explorer.EXE
```

**Child process:**

```text
notepad.exe
```

**User:**

```text
JEEVITHA\JEEVITHA
```

**Process GUID:**

```text
{04d20fda-7415-6aae-6b06-00000000d501}
```

### Process tree

```text
explorer.exe
     ↓
notepad.exe
```

### Interpretation

This is a plausible normal parent-child relationship. Windows Explorer can be involved in launching applications through normal user interaction.

The existence of this relationship alone does not indicate malicious activity.

---

# Process Tree 2 — PowerShell → Notepad

I opened PowerShell and launched Notepad using:

```powershell
notepad.exe
```

Sysmon recorded the resulting process creation.

### Evidence

**Parent image:**

```text
C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe
```

**Parent PID:**

```text
4644
```

**Child image:**

```text
C:\Program Files\WindowsApps\Microsoft.WindowsNotepad_11
```

**Child PID:**

```text
6992
```

**Command line:**

```text
C:\WINDOWS\system32\notepad.exe
```

**User:**

```text
JEEVITHA\JEEVITHA
```

### Process tree

```text
powershell.exe
     ↓
notepad.exe
```

### Interpretation

This relationship was expected because I explicitly launched Notepad from PowerShell.

This demonstrates why parent-child relationships provide useful context. Instead of only seeing that `notepad.exe` was created, Sysmon allows the analyst to see that PowerShell was responsible for creating it.

The presence of PowerShell does not automatically make the activity malicious. PowerShell is a legitimate Windows administration and scripting tool.

---

# Process Tree 3 — WPS PhotoLaunch

A third process creation event involved WPS Office.

### Evidence

**Parent image:**

```text
C:\Users\JEEVITHA\AppData\Local\Kingsoft\WPS Office\12.1.0.28485\office6\photolaunch.exe
```

**Parent PID:**

```text
16868
```

**Child image:**

```text
C:\Users\JEEVITHA\AppData\Local\Kingsoft\WPS Office\12.1.0.28485\office6\photolaunch.exe
```

**Child PID:**

```text
12092
```

**User:**

```text
JEEVITHA\JEEVITHA
```

**Command line:**

```text
C:\Users\JEEVITHA\AppData\Local\Kingsoft\WPS Office\12.1.0.28485\office6\photolaunch.exe" Run "C:\Users\JEEVITHA\AppData\Local\Kingsoft\WPS Office\12.1.0.28485\office6\addons\photoeditlite\photoeditlite.dll" /photo /edit -starttime=7003099 -defaultmainpage=1 -hostwid=461200 -savehostwid=657742 -skin=dark -imageprotocol=filepath
```

### Process tree

```text
photolaunch.exe
     ↓
photolaunch.exe
```

### Interpretation

The parent and child have the same executable name and path.

This does not automatically mean that the process is malicious. Applications can legitimately create another instance of the same executable.

However, this is a relationship worth understanding because the analyst should be able to explain why the application created another instance.

The command line provides additional context because it shows WPS PhotoLaunch loading its `photoeditlite.dll` component and passing arguments related to photo editing.

The important lesson is:

> An unusual-looking process relationship is an investigation clue, not proof of malicious activity.

---

# What Makes a Process Relationship Worth Investigating?

A process relationship should be considered in context.

Useful things to investigate include:

### 1. Command line

Is the command line expected for that application?

A normal process with an unusual command line may require further investigation.

### 2. User

Was the process created by the expected user?

An unexpected account or privilege context can change the interpretation of an event.

### 3. Executable path

Where is the executable located?

For example, an executable running from an unusual temporary or user-writable directory may deserve additional investigation.

However, an unusual path alone does not prove malicious activity.

### 4. Parent process

Does the parent make sense for the child?

For example, an application being launched from Explorer can be normal. A process being launched by an unexpected application may require more investigation.

### 5. Surrounding activity

What happened immediately before and after the process was created?

A single process event provides limited context. Other process creations, logons, network connections, file activity, or other telemetry can help establish a timeline.

---

# Important Investigation Principle

I should not classify a process as suspicious simply because one field looks unusual.

Instead, I should ask:

```text
What happened?
     ↓
Which process created it?
     ↓
Which account was involved?
     ↓
What command was executed?
     ↓
Where is the executable?
     ↓
What happened around the same time?
     ↓
Does the complete activity make sense?
```

This is more useful than treating individual Event IDs or process names as automatically malicious.

---

# Hypothetical Threat-Hunting Examples

## Example 1 — Explorer → Notepad

```text
explorer.exe
     ↓
notepad.exe
```

This relationship alone does not prove malicious activity.

It is a plausible normal relationship and needs to be interpreted in context.

---

## Example 2 — Unexpected Parent → Notepad

```text
unexpected-process.exe
        ↓
notepad.exe
```

This would be worth investigating.

I would check:

* The user account
* The parent process path
* The child process path
* The command line
* The timing
* Other activity surrounding the process creation
* Whether the parent-child relationship is expected for the application

---

## Example 3 — Explorer → PowerShell → Notepad

```text
explorer.exe
     ↓
powershell.exe
     ↓
notepad.exe
```

This chain is not automatically malicious.

Explorer, PowerShell and Notepad are all legitimate software.

The chain should instead be examined using its context:

* Why was PowerShell launched?
* What command line did it use?
* Which user launched it?
* What did PowerShell execute?
* What happened before and after it?
* Were there any unusual network or file activities?

---

# MITRE ATT&CK Connection

## T1059.001 — PowerShell

PowerShell is a legitimate Windows scripting and administration tool, but it can also be used for command and script execution during attacks.

When PowerShell is launched, process creation telemetry such as Sysmon Event ID 1 can provide evidence including:

* The PowerShell executable
* Parent process
* User
* Process ID
* Command line
* Timing

This means PowerShell activity can be investigated together with its parent-child process relationship rather than being treated as automatically malicious.

---

# Questions I Answered

### 1. What is a parent process?

A parent process is the process that creates or launches another process.

### 2. What is a child process?

A child process is the process created by another process.

### 3. Why are parent-child relationships useful?

They help an analyst reconstruct how processes were launched and understand the execution sequence.

### 4. Why is the presence of PowerShell not automatically malicious?

PowerShell is a legitimate Windows tool used for administration and scripting. Its presence becomes meaningful when considered alongside its command line, parent process, user, timing and surrounding activity.

### 5. What additional evidence would I investigate if a process relationship looked unusual?

I would investigate:

* User account
* Parent process
* Parent process path
* Child process path
* Command line
* Timing
* Other process activity
* Related file activity
* Related network activity

---

# My Investigation Approach

If I encounter a process relationship that looks unusual, I would not immediately label it malicious.

I would first investigate:

> Is the user expected?

> Is the command expected?

> Is the executable path expected?

> Is the parent process expected?

> What other activity occurred around the same time?

The combination of these pieces of evidence provides much stronger context than a single process event.

---

# What I Learned

Today I learned that Sysmon Event ID 1 can be used to understand relationships between processes, not just individual process creation events.

I observed:

```text
explorer.exe
     ↓
notepad.exe
```

```text
powershell.exe
     ↓
notepad.exe
```

and:

```text
photolaunch.exe
     ↓
photolaunch.exe
```

The most important lesson was that an unusual process relationship is not automatically malicious. It should be investigated using additional evidence such as the user, command line, executable path, parent process and surrounding activity.

I also understood that PowerShell activity needs to be interpreted in context rather than treated as automatically suspicious.

---


