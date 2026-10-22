
````markdown
# Week 1 — Day 3: Windows Administration

## Objective

Learn the basics of Windows administration and understand how users, groups, services, processes, the Registry, NTFS permissions, and system information can be relevant during a SOC investigation.

---

# 1. Windows Users

I explored the local users on the Windows system.

## Administrator

- Description: Built-in account to administrate the domain/computer.
- This is a privileged account.

## Default Account

- Description: A user account managed by the system.
- It is a system-managed account rather than a normal everyday user account.

## Guest

- Description: Built-in account for guest login.
- A Guest account is intended to provide limited access to a computer for users who do not need a normal personal account.

## Jeevitha

- Personal user account currently being used on the system.

## WDAGUtilityAccount

- Description: A user account managed and used by the system for Windows Defender Application Guard scenarios.
- This is a system-managed account rather than a normal personal user account.

---

# 2. Guest Account vs Default Account

## Guest Account

The Guest account exists to provide limited access to the computer for someone who does not have their own normal user account.

Its purpose is temporary or restricted access.

It has significantly fewer privileges than an administrator account.

## Default Account

The Default Account is a system-managed account created and maintained by Windows.

It is different from the Guest account because the Guest account is intended for restricted guest access, while the Default Account is associated with Windows account management.

| Account | Purpose |
|---|---|
| Guest | Provides limited access for a guest user |
| Default Account | Managed by Windows for system/account-management purposes |

---

# 3. Administrators Group

The Administrators group contains:

- Administrator
- Jeevitha

Membership in this group gives an account elevated administrative privileges.

## Why an unfamiliar account in Administrators is suspicious

If an unfamiliar account were discovered inside the Administrators group, it could indicate unauthorized access or a change made after an intrusion.

Administrators have privileged access to the system.

Examples of administrative capabilities include:

- Creating, modifying, and deleting user accounts
- Adding users to privileged groups
- Changing system configuration
- Installing software
- Managing Windows services
- Accessing and modifying protected files
- Changing security-related settings
- Managing permissions
- Starting or stopping services
- Making system-wide configuration changes

An unfamiliar administrator account is not automatically proof of an intrusion. It would need to be correlated with other evidence such as account activity, Windows event logs, process activity, and network activity.

---

# 4. Windows Services

I explored several Windows services using `services.msc`.

| Service | Status | Startup Type | Observation |
|---|---|---|---|
| Claude | Running | Automatic | Runs Claude |
| Cryptographic Services | Running | Automatic | Provides secure messaging or data transfer mechanisms across applications |
| IP Translation Configuration | Stopped | Manual | Provides IPv4 to IPv6 translation |
| Local Session Manager | Running | Automatic | Manages Windows sessions of different users |
| Microsoft Account Sign-in Assistant | Running | Manual | Assists user sign-ins |

## Security Observation

A malicious program could potentially use a Windows service to maintain access to a system.

Therefore, during an investigation, an analyst could examine:

- Service name
- Service description
- Status
- Startup type
- Executable path
- Whether the service is expected on the system
- Whether the service was recently created or modified

A suspicious service could have an unusual name or an executable path that does not make sense for the service.

The description alone should not be treated as proof that a service is legitimate or malicious.

---

# 5. Windows Registry

I explored the Windows Registry using `regedit`, but I did not initially understand its structure clearly.

The main Registry root keys observed were:

- HKEY_CLASSES_ROOT
- HKEY_CURRENT_USER
- HKEY_LOCAL_MACHINE
- HKEY_USERS
- HKEY_CURRENT_CONFIG

## Current Understanding

The Registry is a hierarchical database used by Windows to store configuration information.

The basic structure can be viewed as:

```text
Registry
    ↓
Key
    ↓
Subkey
    ↓
Value
````

I still need more practice with the exact contents and purposes of the different Registry locations.

## Security Relevance

An unfamiliar program referenced in the Registry could be worth investigating because programs can use Registry entries for configuration and other purposes.

A Registry entry by itself does not prove that malware is present.

## Persistence Observation

A program configured in the Registry to start automatically could be significant during an investigation.

Automatic execution could allow a program to run without requiring a user to manually start it.

An attacker could potentially use such mechanisms to maintain access to a compromised system.

---

# 6. NTFS Permissions

I created a test directory and file to examine Windows file permissions.

The accounts/groups displayed by `icacls` included:

* Administrators
* Builtin/Users
* System users
* Authenticated Users

Administrators and the System account were observed to have full control.

I also observed permission indicators such as `R`.

I understood `R` as representing read access.

I did not confidently identify all of the permission abbreviations during this exercise.

## Security Relevance

File permissions are important during investigations because unexpected access to sensitive files could provide useful evidence.

For example, if a user who normally does not have access to a sensitive file suddenly had permission to modify it, this could be suspicious.

However, unusual permissions alone are not proof of malicious activity. They should be correlated with other evidence.

---

# 7. PowerShell Investigation

## `whoami`

Command:

```powershell
whoami
```

Output:

```text
jeevitha\jeevitha
```

### Observation

The command identifies the account currently being used.

This is useful during an investigation because the account being used determines the permissions and access available to the user.

---

## `hostname`

Command:

```powershell
hostname
```

Output:

```text
JEEVITHA
```

### Observation

The command identifies the hostname of the computer.

This can help identify which computer generated particular evidence during an investigation.

---

## `ipconfig /all`

Command:

```powershell
ipconfig /all
```

### Observation

The command provides network-related information such as:

* IP addresses
* MAC addresses
* Network adapter information
* Other network configuration information

This can help identify and understand the system's network configuration.

---

## `systeminfo`

Command:

```powershell
systeminfo
```

### Observation

The command provides general system information.

Information observed included:

* Number of processors
* Installation information
* BIOS information
* System specifications
* Network-related information

This provides an overall view of the system and its configuration.

---

## `net user`

Command:

```powershell
net user
```

### Observation

The command provided information about local user accounts.

Accounts observed included:

* Administrator
* Default Account
* Guest
* Jeevitha
* System-managed accounts

This can help identify accounts that exist on the system and can be useful for investigating suspicious or unexpected users.

---

## `Get-Process`

Command:

```powershell
Get-Process
```

### Observation

`Get-Process` provides process-related information such as:

* Process name
* Process ID
* CPU-related information

It is similar in purpose to the Linux `ps` command because it allows currently running processes to be examined.

---

## `Get-Service`

Command:

```powershell
Get-Service
```

### Observation

`Get-Service` lists Windows services and provides information such as:

* Service name
* Status
* Display name

It can be used to investigate which services are running or stopped.

---

# 8. Basic System Investigation

I performed a basic investigation of my Windows system.

## System Information

### Hostname

```text
JEEVITHA
```

### Username

```text
jeevitha\jeevitha
```

### Windows Version

```text
Windows 11 Pro
```

### System Architecture

```text
x64-based PC
```

---

## Local Users

During the investigation, I identified two visible local users:

* Administrator
* Default Account

### Interesting Account

The Administrator account was considered interesting because it has administrative privileges and therefore has access to multiple privileged system functions.

---

# 9. Process Investigation

I used `Get-Process` to examine running processes.

## Processes I Recognized

* Acrobat
* Adobe
* OneNote

## Processes I Did Not Immediately Recognize

### conhost

* PID: `6852`
* CPU observed: `0.03`

### dashost

* PID: `3320`
* CPU: Unavailable

I did not immediately recognize these processes.

I did not classify them as malicious simply because I did not recognize them.

The next step in an actual investigation would be to establish what the processes are, where their executables are located, and whether their behavior is expected.

---

# 10. Process Investigation Reasoning

For an unfamiliar process, useful information to investigate includes:

* Process name
* PID
* Executable path
* Parent process
* Digital signature
* Network connections
* Start/creation information
* Related Windows events

An unusual executable location could make an otherwise normal-looking process worth investigating further.

An unfamiliar process is not automatically malware.

---

# 11. Windows Investigation Thinking

Several areas investigated during this exercise can provide useful evidence during a SOC investigation.

## Unfamiliar Administrator Account

An unexpected account inside the Administrators group could indicate unauthorized activity because administrators have elevated privileges.

## Unfamiliar Service

An unexpected service, particularly one with an unusual name, unexpected executable path, or unusual configuration, could require further investigation.

## Unfamiliar Process

An unfamiliar process should be investigated rather than immediately classified as malicious.

## NTFS Permissions

Unexpected access to sensitive files or unexpected permission changes could be relevant evidence.

## Registry

Registry entries can contain configuration information and can potentially be relevant when investigating persistence or other suspicious activity.

---

# 12. Investigation Questions

The following questions remain areas for further learning:

* How can Registry keys, subkeys, and values be investigated in more depth?
* Which Registry locations are particularly relevant to security investigations?
* How can Registry activity reveal persistence?
* How can Windows event logs be correlated with suspicious account, service, process, or Registry activity?
* What are the normal executable locations for important Windows processes?

---

# 13. What I Learned

* Windows has different types of user accounts with different purposes.
* Administrator accounts have elevated privileges.
* Group membership can determine what privileges a user has.
* Windows services can run automatically or manually.
* Processes represent programs currently running on the system.
* PowerShell can be used to collect system information from the command line.
* `whoami` identifies the current user.
* `hostname` identifies the computer.
* `ipconfig /all` provides network configuration information.
* `systeminfo` provides general system information.
* `net user` can be used to examine local user accounts.
* `Get-Process` can be used to examine running processes.
* `Get-Service` can be used to examine Windows services.
* NTFS permissions control access to files and directories.
* Unfamiliar accounts, services, processes, and permissions should be investigated rather than immediately classified as malicious.
* The Windows Registry stores configuration information and can be relevant to security investigations.

---


````
