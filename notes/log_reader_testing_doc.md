# log_reader.py — Testing Documentation

## 1. Objective

The objective of this exercise was to create a basic Python script that can read a log file, print each line, count the total number of lines, and identify lines containing a specific keyword.

---

## 2. Environment

* Operating System: Kali Linux
* Python version: [record the output of `python3 --version`]
* Script location: `~/cyberlab/scripts/log_reader.py`
* Initial test file: `sample_log.log`

---

## 3. Test File

A small artificial log file was created to safely test the script before using a real system log.

The test file contained 7 lines.

The entries included examples of:

* Informational events
* A warning
* 2 errors
* User activity

---

## 4. Commands Used

```bash
pwd
ls
cd
mkdir
nano
cat
python3
python3 --version
```

### Purpose of important commands

* `pwd` — Displays the working directory
* `ls` — List of files and directories
* `cd` — Helps change the directory
* `mkdir` — Make a new directory
* `nano` — Creates the file if it doesn't exist and opens it while allowing us to edit (write)
* `cat` — Displays and creates text files
* `python3` — Invokes the python3 interpreter

---

## 5. Python Concepts Used

### Variables

Example:

```python
log_file = "sample_log.log"
```

Observation:

The variable stores the path of the file mentioned.

### File opening

```python
with open(log_file, "r") as file:
```

Observation:

Opens the file stored in log_file in read mode; 'with' lets us close the file without explicitly mentioning it. 'as file' is another variable that stores the opened file.

### For loop

```python
for line in file:
```

Observation:

Allows us to loop through every line in the file

### Counter

```python
line_count += 1
```

Observation:

The for loop executes for every line; hence, += 1 adds 1 to the counter every time the for loop loops through a line.

### Conditional check

```python
if "ERROR" in line:
```

Observation:

Checks if the string "ERROR" exists in 'line'.

---

## 6. Initial Test

The script was first tested against `sample_log.log`.

Command used:

```bash
python3 log_reader.py
```

Expected result:

The script should print every line in the test file and display the total number of lines.

Actual result:

INFO User logged in

INFO Network connection established

WARNING Failed login attempt

INFO User opened terminal

ERROR Connection failed

INFO User logged out

ERROR Authentication failed

Total lines: 7

---

## 7. Error Keyword Test

The script was then modified to count lines containing `ERROR`.

Test performed:

Added logs with 'ERROR'

Expected result:

Total error: 2

Actual result:

Total error: 2

---

## 8. Real Log Test

After confirming that the script worked on the artificial test file, a copy of a real Kali log was created for analysis.

Original log:

```text
/var/log/boot.log
```

Analysis copy:

```text
/root/cyberlab/logs/boot.log
```

Command used to create the copy:

```bash
cp /var/log/boot.log ~/cyberlab/logs
```

The Python script was then changed so that `log_file` pointed to the analysis copy instead of `sample.log`.

---

## 9. Real Log Results

Log analyzed:

boot.log

Total lines:

338

Lines containing `ERROR`:

0

---

## 10. Observations

1. The log structure, including the wording, was very different.

2. Since it was a boot.log file, it contained logs related to booting the system. Every log has different kinds of data.

3. Not all logs have errors; an error doesn't mean that the log is suspicious, and a successful log doesn't mean that it's not suspicious

---

## 11. Limitations

The current script only reads text and performs a basic keyword search.

It does not yet:

* Understand the meaning of individual log events
* Determine whether an event is malicious
* Correlate multiple events
* Extract structured fields automatically
* Distinguish normal activity from suspicious activity

---

## 12. Security Relevance

This exercise demonstrated how a simple Python script can automate basic processing of log evidence.

A SOC analyst may need to process large amounts of log data, so scripting can help with repetitive tasks such as searching, counting, filtering, and extracting information.

The current script is only a starting point and should not be treated as a complete detection or investigation tool.

---

## 13. Questions for Further Investigation

* How could the script identify timestamps?
* How could it identify usernames?
* How could it extract Event IDs?
* How could it search for multiple keywords?
* How could it distinguish different types of log entries?
* How could it correlate related events?
