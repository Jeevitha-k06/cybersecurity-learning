# Day 4 — PowerShell Logging & Investigation

## Objective

Investigate what evidence is generated when PowerShell is used to execute normal commands and understand how different telemetry sources can be correlated.

The main question for this investigation was:

> If I execute normal PowerShell commands, what evidence is created, where is that evidence stored, and can I correlate the same activity across different sources?

---

## Environment

**Investigation:** Original Windows OS

**Documentation:** Kali VM → `/root/cyberlab/notes`

---

## Part 1 — Initial Understanding

A normal PowerShell activity can lead to Windows telemetry being generated.

For example, if PowerShell launches `notepad.exe`, the process creation telemetry can show information about the newly created process, including its image, command line, parent process and other identifying information.

However, not every PowerShell command creates a separate process.

For example, `whoami.exe` is an executable and therefore creates a process, while commands such as PowerShell cmdlets may execute within the existing PowerShell process.

This distinction became clear during the investigation.

---

## PowerShell Activity Generated

The following commands were executed during the investigation:

```powershell
whoami
hostname
Get-Process
Get-Service
```

I was able to find process-related evidence for `whoami` and `hostname`.

I could not find separate process-creation evidence for `Get-Process` and `Get-Service`.

This is an important observation because PowerShell commands and separately launched executable processes do not necessarily produce the same type of process telemetry.

---

# Evidence Sources

## PowerShell History

PowerShell history focuses on commands that were executed in the PowerShell session and provides a record of previous commands.

It is different from process-creation telemetry because seeing a command in PowerShell history does not by itself provide all the process-level information that Sysmon can provide.

---

## PowerShell Event Logs

I checked the available PowerShell-related logs and found evidence related to the PowerShell activity.

I found:

* A log associated with process ID `14000`
* A log showing the launching of PowerShell

The timestamps I observed for the PowerShell launch were:

```text
2026-09-21T05:15:56.4642359Z
2026-09-21T05:15:56.5311028Z
```

The presence of the same process ID in related evidence helped me connect the events.

---

## Sysmon Event ID 1

I found a Sysmon process-creation event for `whoami.exe`.

### Observed event

```text
Timestamp:
2026-09-21T05:19:39.1185213Z

Process ID:
14000

Image:
C:\WINDOWS\system32\whoami.exe

Parent Image:
C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe

User:
JEEVITHA\JEEVITHA

Process ID:
15440

Process GUID:
{04d20fda-be6a-6ab0-3302-00000000da01}

Hash:
SHA256=23240EF9F8B0A9A324110B1C2331DE31DC1B0E08F5359CB707E51A939AF56CD3
```

### Important observation

The event shows that `whoami.exe` was created as a child process of PowerShell.

Therefore:

```text
PowerShell
    ↓
whoami.exe
```

The process information gives evidence about the process that was actually launched, including its parent, user, process ID, GUID and hash.

---

# Part 7 — Evidence Comparison

| Evidence source       | What I found                                                                                                                         | What does it prove?                                                                  |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------ |
| PowerShell History    | Commands executed in the PowerShell session                                                                                          | Shows commands that were entered/executed in the session                             |
| PowerShell Event Logs | Evidence related to PowerShell activity, including a log associated with process ID `14000` and logs related to PowerShell launching | Provides PowerShell-related telemetry that can be correlated with other evidence     |
| Sysmon Event ID 1     | `whoami.exe` with PowerShell as the parent process, user `JEEVITHA\JEEVITHA`, process information and SHA256 hash                    | Proves that `whoami.exe` was created as a process and provides process-level context |

---

# Correlation

I attempted to correlate the PowerShell activity across different evidence sources.

The Sysmon event showed:

```text
PowerShell
    ↓
whoami.exe
```

The `whoami.exe` process had:

```text
Process ID: 14000
Parent Image: C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe
User: JEEVITHA\JEEVITHA
```

I also found PowerShell-related log evidence associated with process ID `14000`.

This allowed me to connect the process-level evidence from Sysmon with the PowerShell-related evidence.

---

# PowerShell Process Launch

I found evidence showing the launching of PowerShell at approximately:

```text
2026-09-21T05:15:56.4642359Z
2026-09-21T05:15:56.5311028Z
```

The later `whoami.exe` process creation occurred at:

```text
2026-09-21T05:19:39.1185213Z
```

This gives a basic timeline:

```text
05:15:56
    ↓
PowerShell launched
    ↓
PowerShell session used
    ↓
05:19:39
    ↓
whoami.exe created
    ↓
Parent: powershell.exe
```

---

# What I Could Prove

From the available evidence, I could establish that:

1. PowerShell was launched.
2. `whoami.exe` was subsequently created.
3. `whoami.exe` had `powershell.exe` as its parent process.
4. The process was associated with the user `JEEVITHA\JEEVITHA`.
5. The process had a specific process ID and Process GUID.
6. A SHA256 hash was available for the process.
7. The different logs could be correlated using process information and timing.

---

# What I Could Not Prove

I could not conclude that PowerShell activity was suspicious simply because PowerShell was present.

I also could not conclude that every command typed into PowerShell created a separate process.

For example, I found process evidence for `whoami.exe`, but I did not find equivalent process-creation evidence for `Get-Process` and `Get-Service`.

I also should not assume that the presence of `powershell.exe` tells me exactly what was executed inside the session.

Additional PowerShell-specific evidence would be needed to determine what happened inside the session.

---

# Investigation Questions and Answers

## Q1. What is the difference between PowerShell history and PowerShell logging?

PowerShell history focuses on commands that were executed in the PowerShell session and provides a record of previous commands.

PowerShell logging refers to telemetry generated by PowerShell-related logging mechanisms. It can provide information about PowerShell activity, but it should not be treated as one single source containing every process, parent, command and timing detail.

Different pieces of evidence may come from different logs.

---

## Q2. If Sysmon Event ID 1 shows `Image = powershell.exe`, what can I conclude?

I can conclude that a PowerShell process was created.

It shows that `powershell.exe` was launched as a process.

It does not, by itself, tell me everything that happened inside that PowerShell session.

---

## Q3. Does the presence of `powershell.exe` automatically mean malicious activity?

No.

PowerShell is a normal Windows administration and scripting tool and can be used for legitimate activity.

Additional context would be needed, such as:

* Path
* User
* Parent process
* Command line
* Timing
* Other related activity
* Network or file activity where relevant

An unusual value in one of these fields may justify further investigation, but one field alone does not automatically establish malicious activity.

---

## Q4. Which field in Sysmon Event ID 1 would help me understand how PowerShell was launched?

The **Command Line** field is particularly useful for understanding how the process was invoked and what arguments were supplied.

---

## Q5. Which field would help identify the process that launched PowerShell?

The **Parent Image** field identifies the parent process image.

Other parent-process fields can provide additional context.

---

## Q6. Why is the parent process useful when investigating PowerShell activity?

The parent process helps establish how PowerShell was launched.

For example:

```text
explorer.exe
    ↓
powershell.exe
```

shows that Explorer was the parent of PowerShell.

The parent relationship provides context, but it does not by itself determine whether the activity was suspicious.

---

## Q7. If I find `explorer.exe → powershell.exe`, what does this tell me and what doesn't it tell me?

It tells me that PowerShell was launched as a child of Explorer.

It does not tell me:

* What commands were executed inside PowerShell
* Whether the activity was malicious
* What files or network connections were subsequently involved
* Whether the user performed any suspicious activity

Additional evidence is required.

---

## Q8. If I execute `whoami` but Sysmon Event ID 1 only shows that `powershell.exe` was created, can I conclude that `whoami` was recorded by Sysmon?

No.

Sysmon Event ID 1 is process-creation telemetry.

If `whoami.exe` itself appears as a process-creation event, that provides evidence that the executable was launched. But the creation of `powershell.exe` alone does not prove that `whoami` was executed.

---

## Q9. If I cannot find `whoami` in the logs I checked, what should an analyst record?

The analyst should record that the expected evidence was not found in the logs that were checked.

For example:

> I could not find evidence of `whoami` in the PowerShell logs examined.

The analyst should not invent evidence or assume that an event occurred simply because the command was expected to be there.

---

## Q10. Why is it useful to correlate PowerShell-specific evidence with Sysmon?

The sources provide different types of information.

Sysmon can provide process-level information such as:

* Process creation
* Parent process
* Process ID
* Process GUID
* Image
* Command line
* Hash

PowerShell-specific telemetry can provide additional information about activity occurring within PowerShell.

Correlating them gives a more complete picture than relying on only one source.

---

# Part 10 — Mini Investigation

Given:

```text
Image:
C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe

Parent Image:
C:\Windows\explorer.exe

User:
JEEVITHA\JEEVITHA

Command Line:
powershell.exe
```

## A. What happened?

PowerShell was launched using `explorer.exe` as its parent process, under the user `JEEVITHA\JEEVITHA`.

## B. What evidence supports this?

The evidence is provided by:

* Image: `powershell.exe`
* Parent Image: `explorer.exe`
* User: `JEEVITHA\JEEVITHA`
* Command Line: `powershell.exe`

## C. What looks normal here?

The PowerShell executable is located at the standard Windows PowerShell path:

```text
C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe
```

The user is the expected local user account, and PowerShell being launched from Explorer can occur during normal interactive use.

## D. Is there enough evidence to call this suspicious?

No.

There is not enough evidence from this event alone to determine that the activity is suspicious.

## E. What additional evidence would I want?

I would want to examine:

* Command line and arguments
* Parent process context
* User/account context
* PowerShell-specific logging
* Timing and surrounding events
* Any related file activity
* Any related network activity
* Whether the executable path is expected

---

# Key Takeaways

1. **PowerShell being present does not automatically mean suspicious activity.**

2. **Sysmon Event ID 1 records process creation.**

3. `whoami.exe` appearing in Sysmon means an actual `whoami.exe` process was created.

4. PowerShell cmdlets such as `Get-Process` and `Get-Service` should not automatically be expected to appear as separate process-creation events.

5. **Parent-child relationships provide context**, but they do not determine maliciousness by themselves.

6. **PowerShell history, PowerShell logging and Sysmon are different evidence sources.**

7. Correlation is important because one source may show that a process was launched while another source can provide additional information about activity within the PowerShell environment.

8. **Missing evidence should be documented rather than assumed.**

9. A useful investigation asks:

```text
What happened?
     ↓
What evidence proves it?
     ↓
What does the evidence NOT prove?
     ↓
What additional evidence should I check?
```

10. The overall goal is to reconstruct activity from evidence rather than label individual events as suspicious in isolation.
