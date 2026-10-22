# Investigation 01 — Windows Activity Timeline

## Objective

Reconstruct a sequence of normal Windows activity using Sysmon telemetry, examine process relationships, correlate available evidence, and identify gaps without assuming that ordinary activity is malicious.

## Investigation Environment

- **Investigation machine:** Original Windows OS
- **Documentation environment:** Kali Linux VM
- **Documentation location:** `/root/cyberlab/notes/Investigation-01-Windows-Timeline.md`
- **Primary evidence source:** Sysmon Operational log, Event ID 1 (Process Creation)
- **Account observed:** `JEEVITHA\\JEEVITHA`
- **Investigation scope:** Windows Terminal, PowerShell, `whoami.exe`, `hostname.exe`, Notepad, and Microsoft Edge
- **Activity date:** 2026-10-15, based on the supplied event timestamps
- **Time zone:** To be verified against the original event fields; Sysmon `UtcTime` is UTC.

## Investigation Activity

I generated normal activity on my Windows machine, including running `whoami`, `hostname`, `Get-Process`, and `Get-Service` in PowerShell, creating and manipulating a test file, launching Notepad, and visiting a website in Edge. I then searched the available Sysmon telemetry to reconstruct the activity. Not every expected action had a matching event in the records I examined.

## Evidence Sources

### Sysmon

The supplied records are from Sysmon Event ID 1, Process Creation. They provide process image, command line, account, process identifiers, parent-process details and hashes where available.

### Windows Security Logs

No specific Security event records were supplied for this investigation. I therefore cannot claim that Security logs independently corroborated the observed activity. A future investigation should check relevant logon events and correlate them using available identifiers and timestamps.

### PowerShell Logging

A PowerShell-related process event was found, with `explorer.exe` as its parent and the account `JEEVITHA\\JEEVITHA`. The complete process-creation record, including its exact timestamp, PID, Process GUID and command line, still needs to be collected. No PowerShell Script Block Logging event was supplied.

## Timeline

| Timestamp (as supplied) | Evidence | Event | Account | Process | Interpretation |
|---|---|---|---|---|---|
| 2026-10-15 02:42:46.187 | Sysmon Event ID 1 | Process creation | `JEEVITHA\\JEEVITHA` | `WindowsTerminal.exe`, PID 12752 | Windows Terminal was running under the observed account. Its parent was `svchost.exe`. The `-Embedding` argument alone does not establish which commands were run in the terminal. |
| 2026-10-15 02:43:12.188 | Sysmon Event ID 1 | Process creation | `JEEVITHA\\JEEVITHA` | `whoami.exe` | The command is consistent with querying the current account identity. The supplied event lists PowerShell as the parent image. Its Process GUID and PID unexpectedly match the supplied Terminal event and must be verified in the raw XML. |
| 2026-10-15 02:43:15.329 | Sysmon Event ID 1 | Process creation | `JEEVITHA\\JEEVITHA` | `HOSTNAME.EXE`, PID 8056 | The command is consistent with retrieving the computer hostname. PowerShell is listed as the parent image. The supplied parent Process GUID and PID need comparison with the PowerShell event. |
| 2026-10-15 02:44:38.764 | Sysmon Event ID 1 | Process creation | `JEEVITHA\\JEEVITHA` | `Notepad.exe`, PID 14316 | Notepad was created with PowerShell listed as its parent. Confirm the parent PID and Process GUID against the PowerShell process-creation record. |
| 2026-10-15 02:45:11.378 | Sysmon Event ID 1 | Process creation | `JEEVITHA\\JEEVITHA` | `msedge.exe`, PID 4200 | This is an Edge renderer process, as indicated by `--type=renderer`. Its parent is another Edge process. This event does not establish how the main browser process was initially launched. |

**Timeline limitations:** These timestamps establish the ordering of the supplied records, subject to verifying their time fields. They do not independently prove that every event belonged to one uninterrupted execution chain or that the missing activities occurred between the listed events.

## Detailed Process Evidence

### 1. Windows Terminal

- **Image:** `C:\\Program Files\\WindowsApps\\Microsoft.WindowsTerminal_1.24.12741.0_x64__8wekyb3d8bbwe\\WindowsTerminal.exe`
- **Command line:** `"C:\\Program Files\\WindowsApps\\Microsoft.WindowsTerminal_1.24.12741.0_x64__8wekyb3d8bbwe\\WindowsTerminal.exe" -Embedding`
- **User:** `JEEVITHA\\JEEVITHA`
- **Process ID:** 12752
- **Process GUID:** `{04d20fda-3dc0-6ad0-1802-00000000fc01}`
- **Parent image:** `C:\\Windows\\System32\\svchost.exe`
- **Parent PID:** 1300
- **SHA-256:** `4AD317D9DACEDCA1E68DCC2405D6D364A20599B646B8205FEAE829CF18EF4958`

**Interpretation:** This is evidence of Windows Terminal process activity under the observed account. The record alone does not identify the commands executed within the terminal.

### 2. whoami.exe

- **Timestamp:** 2026-10-15 02:43:12.188
- **Image:** `C:\\Windows\\System32\\whoami.exe`
- **Command line:** `"C:\\WINDOWS\\system32\\whoami.exe"`
- **User:** `JEEVITHA\\JEEVITHA`
- **Process ID:** 12752 (as supplied; verify)
- **Process GUID:** `{04d20fda-3dc0-6ad0-1802-00000000fc01}` (as supplied; verify)
- **Parent image:** `C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe`
- **SHA-256:** `23240EF9F8B0A9A324110B1C2331DE31DC1B0E08F5359CB707E51A939AF56CD3`

**Interpretation:** The image and command line are consistent with querying the current account identity. The supplied PID and Process GUID match those of the Terminal event, which is unexpected for two separate process-creation records. I must verify the raw event before relying on these identifiers for correlation.

### 3. hostname.exe

- **Timestamp:** 2026-10-15 02:43:15.329
- **Image:** `C:\\Windows\\System32\\HOSTNAME.EXE`
- **Command line:** `"C:\\WINDOWS\\system32\\HOSTNAME.EXE"`
- **User:** `JEEVITHA\\JEEVITHA`
- **Process ID:** 8056
- **Process GUID:** `{04d20fda-3dc3-6ad0-1902-00000000fc01}`
- **Parent image:** `C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe`
- **Parent process GUID:** `{04d20fda-3da4-6ad0-1002-00000000fc01}`
- **Parent PID:** 4352
- **SHA-256:** `F8B207720D8673FEB5839DF1E52360F72C2AD2CE9917D5F3DA4F30368DC747C9`

**Interpretation:** The executable is consistent with retrieving the machine's hostname. The parent fields support PowerShell as the immediate parent. I need the corresponding PowerShell event to validate the relationship and identify the process chain.

### 4. PowerShell process

The PowerShell-related record I found contained:

- **User:** `JEEVITHA\\JEEVITHA`
- **Logon GUID:** `{04d20fda-3c03-6ad0-38f0-0d0000000000}`
- **Logon ID:** `0xDF038`
- **Terminal session ID:** 1
- **Integrity level:** Medium
- **Parent image:** `C:\\Windows\\explorer.exe`
- **Parent PID:** 9096
- **Parent Process GUID:** `{04d20fda-3c06-6ad0-9e00-00000000fc01}`
- **Parent command line:** `C:\\WINDOWS\\Explorer.EXE`
- **Parent user:** `JEEVITHA\\JEEVITHA`
- **SHA-256:** `60C9B29843624DD8AF6B6A7B26147753BE6AEEF65098B9A503CC50850AFE410F`

**Interpretation:** The record is consistent with a PowerShell process started by Explorer under the observed account. However, its exact timestamp, own Process GUID, PID, image and command line were not included in the supplied details. I need those fields before connecting this process to the Terminal, `whoami`, `hostname` and Notepad events.

### 5. Notepad.exe

- **Timestamp:** 2026-10-15 02:44:38.764
- **Image:** `C:\\Program Files\\WindowsApps\\Microsoft.WindowsNotepad_11.2607.14.0_x64__8wekyb3d8bbwe\\Notepad\\Notepad.exe`
- **Command line:** `"C:\\WINDOWS\\system32\\notepad.exe"`
- **User:** `JEEVITHA\\JEEVITHA`
- **Process ID:** 14316
- **Process GUID:** `{04d20fda-3e16-6ad0-3d02-00000000fc01}`
- **Parent image:** `C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe`
- **Parent PID:** 4352
- **Parent command line:** `"C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe"`
- **SHA-256:** `03745E9E21684C0E6D9FDC50D91CAA0935F4BAF50F626C11987AB7D6991D58D1`

**Interpretation:** PowerShell is listed as Notepad's parent, supporting the hypothesis that Notepad was launched from PowerShell. Confirm this using the parent PID and Process GUID of the actual PowerShell process.

### 6. Microsoft Edge renderer

- **Timestamp:** 2026-10-15 02:45:11.378
- **Image:** `C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe`
- **Original file name:** `msedge.exe`
- **Command line:** Includes `--type=renderer` and browser-specific arguments
- **Current directory:** `C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\155.0.4283.45\\`
- **User:** `JEEVITHA\\JEEVITHA`
- **Process ID:** 4200
- **Process GUID:** `{04d20fda-3e37-6ad0-4002-00000000fc01}`
- **Parent image:** `C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe`
- **Parent PID:** 14152
- **Parent Process GUID:** `{04d20fda-3c36-6ad0-2801-00000000fc01}`
- **SHA-256:** `4BB4545B4AB80A3CF463A588CE570CA42DE38FE6DB16E3BAEB0798AC75B4648B`

**Interpretation:** The command line and parent image are consistent with an Edge renderer process created within Edge's multi-process architecture. This record does not establish the initial launch mechanism of the main browser process or which website was accessed.

## File Activity

I searched for Sysmon Event ID 11 (FileCreate) related to the test filename and found zero matching records in the search I performed.

This does not prove that no file activity occurred. Event ID 11 records file creation, not every rename or deletion. The relevant event may also be absent because of configuration, search scope or other collection limitations.

**Next checks:**

1. Verify that Sysmon Event ID 11 is enabled in the active configuration.
2. Search the Sysmon Operational log over a wider time range.
3. Search for the exact test filename and its full path.
4. Record any matching events, including their Image and TargetFilename fields.
5. If no event exists, document the absence without claiming that creation, rename and deletion were all logged or all failed.

## Network and DNS Activity

I found no matching Sysmon Event ID 3 (NetworkConnect) or Event ID 22 (DNS query) records in the search I performed.

This means I currently lack Sysmon evidence linking the observed browser activity to a network connection or DNS query. It does not prove that Edge made no network connections or DNS queries.

**Next checks:**

1. Verify whether Event IDs 3 and 22 are enabled by the active Sysmon configuration.
2. Search the appropriate time window and identify the main Edge process and its child processes.
3. Check the destination address, destination port and protocol if a network event exists.
4. Check the queried domain if a DNS event exists.
5. Use additional available telemetry if necessary, and explicitly distinguish observed evidence from inferred activity.

## Process Relationships

### Relationships supported by supplied fields

- `whoami.exe` lists PowerShell as its parent image.
- `hostname.exe` lists PowerShell as its parent image.
- Notepad lists PowerShell as its parent image.
- The Edge renderer lists another Edge process as its parent.
- The PowerShell-related record lists Explorer as its parent.

### Relationships requiring verification

The exact process chain connecting Windows Terminal to PowerShell and the commands is not fully established. The supplied `whoami.exe` PID and Process GUID unexpectedly match the Terminal event, so the original event XML must be checked.

For each proposed parent-child relationship, compare the child's `ParentProcessId` and `ParentProcessGuid` with the parent's `ProcessId` and `ProcessGuid`. Do not rely on a shared parent image alone to establish that several children belong to the same specific parent process.

## Correlation Attempts

### Correlation 1 — PowerShell and whoami.exe

- **Evidence:** `whoami.exe` lists PowerShell as its parent image; both events show `JEEVITHA\\JEEVITHA`.
- **Supporting context:** Their timestamps are close enough to be consistent with the observed command sequence.
- **Limitation:** The supplied PID and Process GUID for `whoami.exe` match the Terminal event unexpectedly.
- **Assessment:** The parent-image evidence supports the relationship, but the process identifiers need verification before treating the chain as fully confirmed.

### Correlation 2 — PowerShell and hostname.exe

- **Evidence:** The hostname event lists PowerShell as the parent image and includes a parent PID and parent Process GUID.
- **Supporting context:** The event follows the `whoami.exe` event by approximately 3.1 seconds.
- **Limitation:** The matching PowerShell process record needs to be retrieved to verify its identifiers.
- **Assessment:** Consistent with PowerShell launching `hostname.exe`, pending identifier verification.

### Correlation 3 — PowerShell and Notepad

- **Evidence:** The Notepad event lists PowerShell as the parent image and gives parent PID 4352.
- **Supporting context:** The observed account matches the other supplied events.
- **Limitation:** The corresponding PowerShell process event must be checked for PID and Process GUID agreement.
- **Assessment:** The supplied fields support PowerShell as Notepad's parent. The complete process chain remains to be validated.

### Edge correlation

The Edge renderer has another Edge process as its parent. This supports a relationship within Edge's process tree, not a direct relationship with PowerShell or the other activities. The main Edge process event would be needed to investigate its initial launch.

## Analyst Assessment

### What happened?

The supplied Sysmon Event ID 1 records show Windows Terminal, PowerShell-related activity, `whoami.exe`, `hostname.exe`, Notepad and an Edge renderer process running under the account `JEEVITHA\\JEEVITHA`.

The command lines for `whoami.exe` and `hostname.exe` are consistent with querying account identity and machine hostname. The Notepad event lists PowerShell as its parent, and the Edge renderer event lists another Edge process as its parent.

The available evidence is consistent with ordinary user activity. However, the complete chain connecting all events has not yet been established, and the supplied `whoami.exe` process identifiers need verification.

### What evidence supports the timeline?

- Sysmon Event ID 1 timestamps establish the chronological order of the supplied records, subject to confirming their time fields.
- Image and command-line fields identify the recorded executables and arguments.
- Parent-image and parent-process fields provide evidence for proposed execution relationships.
- User fields show the account recorded for the events.
- Process GUIDs and PIDs can establish specific process relationships when their values agree across the relevant events.

### What was normal?

The recorded activity is consistent with normal user actions: querying identity and hostname, launching Notepad and running Microsoft Edge. The account is consistent across the supplied records, and the displayed executable paths are consistent with expected Windows application locations.

These observations support a benign interpretation but do not independently establish that the entire system or session was safe. Expected paths and account names alone are not proof of legitimacy.

### What could require further investigation?

- An unexpected parent process or process chain.
- An unusual or obfuscated command line.
- Execution from an unexpected directory.
- Unexpected privilege changes or activity inconsistent with the account's normal use.
- Unexpected child processes or file activity.
- Network connections or DNS queries to destinations that warrant investigation.
- Inconsistent or unexplained process identifiers across related events.

These are investigation triggers, not proof of malicious activity.

### What evidence is missing?

- The complete PowerShell Event ID 1 record, including its timestamp, PID, Process GUID and command line.
- Verified raw event XML for the Terminal and `whoami.exe` records because their supplied identifiers unexpectedly match.
- Matching Sysmon Event ID 11 file-creation records.
- Matching Sysmon Event ID 3 network-connection records.
- Matching Sysmon Event ID 22 DNS-query records.
- Independent Security log evidence for relevant logon/session context.
- PowerShell history or PowerShell logging evidence confirming which commands were executed.
- The main Edge process event establishing the browser's initial launch.

### What would I collect next?

1. Retrieve the raw Sysmon XML for the Terminal and `whoami.exe` events and verify all process identifiers.
2. Retrieve the full PowerShell Event ID 1 record and compare its PID and Process GUID with the child events.
3. Check the active Sysmon configuration for Event IDs 11, 3 and 22.
4. Search the relevant logs over a wider timestamp range for the test filename and Edge network/DNS activity.
5. Inspect available PowerShell history and logging evidence without assuming that every command will appear in process-creation logs.
6. Check relevant Windows Security events for logon context and correlate them using available identifiers.
7. Update the timeline only when the supporting evidence is available, preserving any unresolved links as uncertain.

## Answers to Investigation Questions

### Q1. What was the earliest useful piece of evidence?

The Windows Terminal Event ID 1 record at 02:42:46.187 is the earliest supplied event. It establishes that Windows Terminal was running under the observed account. It does not, by itself, establish which commands were subsequently executed.

### Q2. What was the most useful event for understanding process execution?

Sysmon Event ID 1 is the most useful event type in this dataset because it records process creation, image, command line and parent-process information. The individual Notepad and command events become more useful when their parent identifiers can be validated against the PowerShell process event.

### Q3. Which event gave the strongest evidence about the process that performed an action?

The Notepad Event ID 1 record gives useful evidence about the process that launched Notepad because it includes the executable and parent-image fields. The `whoami.exe` event identifies an executable consistent with querying the current account identity. No single one of these events establishes every part of the execution chain.

### Q4. Can the full sequence be reconstructed?

Not yet with complete confidence. The supplied timestamps allow a provisional ordering, and the parent-image fields support some proposed relationships. The process-identifier discrepancy and missing file/network records leave gaps in the reconstruction.

### Q5. Which evidence sources were used?

The supplied records were Sysmon Event ID 1 events. No specific Windows Security event or PowerShell Script Block Logging record was supplied. The PowerShell-related process event was also described, but its complete fields are still needed.

### Q6. Which events can be correlated?

The parent-image fields support the proposed PowerShell relationships with `whoami.exe`, `hostname.exe` and Notepad. PID and Process GUID comparisons are needed to validate those relationships. Timestamps establish chronology. A shared user alone does not prove that events belong to the same process chain. The Edge renderer is correlated with its parent Edge process, not with PowerShell based on the supplied evidence.

### Q7. What makes the observed activity look normal?

The executables and command lines are consistent with ordinary account/hostname queries and normal application use. The recorded account is consistent across the supplied events, and the available paths look expected. This supports a benign interpretation but does not prove that all activity was safe.

### Q8. What could make similar activity worth investigating?

Unexpected parent processes, unusual command lines, unexpected execution locations, privilege changes, unusual child processes, unexpected file activity and network/DNS destinations that warrant investigation. These indicators need context and corroboration before drawing conclusions.

### Q9. Which scenario is the strongest investigation lead?

Option D: PowerShell with an unusual command line and an unexpected child process. Multiple contextual indicators make it more useful to investigate than PowerShell's mere presence. It is still not proof of malicious activity.

### Q10. What evidence was expected but not found?

No matching Sysmon Event ID 11, Event ID 3 or Event ID 22 records were found in the searches performed. I do not yet know whether the cause was configuration, search scope or an event that was not generated or captured.

### Q11. What additional telemetry would help?

The active Sysmon configuration, a wider search of the Sysmon Operational log, the complete PowerShell process event, relevant Windows Security events, and available PowerShell history/logging records. These sources can help establish whether the activity was recorded elsewhere and clarify the execution chain.

### Q12. What can be concluded from the whoami event?

The executable and command line are consistent with running `whoami.exe` to query account identity. The event's user field records `JEEVITHA\\JEEVITHA`, and the parent-image field lists PowerShell. The supplied process identifiers need verification before relying on them for correlation.

### Q13. What cannot be concluded from that event alone?

It cannot establish that the activity was malicious or benign, that the user had administrative privileges, that every event belonged to the same session, or that the full process chain has been reconstructed. It also does not establish the user's authorization or whether the activity was expected in the environment.

### Q14. What would be investigated next?

I would verify the process identifiers and parent relationships, retrieve the complete PowerShell process event, examine relevant logon/session context, check available PowerShell logging, and search for associated file and network activity. I would then update the timeline using the additional evidence.

## Conclusion

This investigation provided practical experience using Sysmon Event ID 1 to reconstruct a provisional sequence of Windows activity. The available records are consistent with normal user activity involving Windows Terminal, PowerShell, identity/hostname queries, Notepad and Microsoft Edge.

However, the complete execution chain is not yet verified. The supplied `whoami.exe` process identifiers unexpectedly match the Windows Terminal event, and no matching Sysmon Event ID 11, 3 or 22 records were found in the searches performed. These gaps should remain explicitly documented until the underlying records and configuration are checked.

The main lesson is that timestamps, process images, parent relationships, user fields and process identifiers provide different kinds of evidence. A defensible investigation uses them together, identifies inconsistencies, and separates confirmed observations from hypotheses.

## Questions / Uncertainties

- Why do the supplied Terminal and `whoami.exe` records share a PID and Process GUID?
- What are the complete PID, Process GUID, timestamp and command line of the PowerShell process?
- Is Sysmon configured to collect Event IDs 11, 3 and 22?
- Were file creation, rename and deletion events captured anywhere in the relevant logs?
- Can the Edge renderer be linked to the expected browsing activity using additional browser-process or network telemetry?
- Which Windows Security or PowerShell logs independently corroborate the timeline?
