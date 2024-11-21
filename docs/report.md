---
title: "Group 7: GIL-free Python"
subtitle: "Code: [`github.com/sueszli/nogil`](https://github.com/sueszli/nogil)"
output: pdf_document
documentclass: article
papersize: a4
pagestyle: empty
geometry:
    - top=5mm
    - bottom=5mm
    - left=5mm
    - right=5mm
header-includes:
    # title
    - \usepackage{titling}
    - \setlength{\droptitle}{-15pt}
    - \pretitle{\vspace{-30pt}\begin{center}\LARGE}
    - \posttitle{\end{center}\vspace{-70pt}}    
    # content
    - \usepackage{scrextend}
    - \changefontsizes[8pt]{8pt}
    # code
    - \usepackage{fancyvrb}
    - \fvset{fontsize=\fontsize{6pt}{6pt}\selectfont}
    - \usepackage{listings}
    - \lstset{basicstyle=\fontsize{6pt}{6pt}\selectfont\ttfamily}
    # code output
    - \DefineVerbatimEnvironment{verbatim}{Verbatim}{fontsize=\fontsize{6pt}{6pt}}
---

<!--

assignment: https://www.complang.tuwien.ac.at/anton/lvas/effizienz-aufgabe24/

based on: https://github.com/sueszli/fast-snek

prof anmerkungen:

- also ich glaub wir können es so machen wie wir wollen, es geht im vor allem dass er sieht dass wir was gelernt und verstanden haben und seine optimierungen umgesetzt haben
- es muss nicht C sein
- haben aber den Freiraum uns auszutoben solange wir es erklären können was wir gemacht haben
- als metrics sollten wir jedoch auf das was in der angabe ist setzen, also cycles und so
- und unsere präsi muss etwas kompakter sein, weil wir den algo erklären müssen und die benotung ist eig solely based auf die präsi haha
-->

Motivation:

- Memory/Network-bound tasks: Asynchronous I/O with `asyncio`, very competitive.
- Compute-bound tasks: Very slow interpreter, hard to parallelize with GIL. → recently removed in PEP 703

Research question:

- How useful is GIL-free Python for compute-bound tasks?
- How does it compare to alternatives (multiprocessing, C-Python interopt, C-Python extensions)?

Chosen algorithm: hashcat

- on password storage: https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html
- we use a simpler one
- no algorithmic optimizations (e.g. rainbow tables, bloom filters, etc.) just brute-force

Cpython dependency `Python.h`: https://github.com/python/cpython/blob/main/Include/Python.h

# Addendum

### System Specifications

```
$ system_profiler SPSoftwareDataType SPHardwareDataType

Software:

    System Software Overview:

      System Version: macOS 14.6.1 (23G93)
      Kernel Version: Darwin 23.6.0
      Boot Volume: Macintosh HD
      Boot Mode: Normal
      Computer Name: Yahya’s MacBook Pro
      User Name: Yahya Jabary (sueszli)
      Secure Virtual Memory: Enabled
      System Integrity Protection: Enabled
      Time since boot: 79 days, 22 hours, 26 minutes

Hardware:

    Hardware Overview:

      Model Name: MacBook Pro
      Model Identifier: Mac14,10
      Model Number: Z174001ABD/A
      Chip: Apple M2 Pro
      Total Number of Cores: 12 (8 performance and 4 efficiency)
      Memory: 16 GB
      System Firmware Version: 10151.140.19
      OS Loader Version: 10151.140.19
      Serial Number (system): VCYQD0HH0G
      Hardware UUID: BEA4D09D-6651-54E1-A3F7-7FB78A7BF1AB
      Provisioning UDID: 00006020-001A284901E8C01E
      Activation Lock Status: Disabled
```

```
$ docker compose exec main lscpu
Architecture:                         x86_64
CPU op-mode(s):                       32-bit
Byte Order:                           Little Endian
CPU(s):                               12
On-line CPU(s) list:                  0-11
Thread(s) per core:                   1
Core(s) per socket:                   12
Socket(s):                            1
Vendor ID:                            0x61
Model:                                0
Stepping:                             0x0
BogoMIPS:                             48.00
Vulnerability Gather data sampling:   Not affected
Vulnerability Itlb multihit:          Not affected
Vulnerability L1tf:                   Not affected
Vulnerability Mds:                    Not affected
Vulnerability Meltdown:               Not affected
Vulnerability Mmio stale data:        Not affected
Vulnerability Reg file data sampling: Not affected
Vulnerability Retbleed:               Not affected
Vulnerability Spec rstack overflow:   Not affected
Vulnerability Spec store bypass:      Mitigation; Speculative Store Bypass disabled via prctl
Vulnerability Spectre v1:             Mitigation; __user pointer sanitization
Vulnerability Spectre v2:             Not affected
Vulnerability Srbds:                  Not affected
Vulnerability Tsx async abort:        Not affected
Flags:                                fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics fphp asimdhp cpuid asimdrdm jscvt fcma lrcpc dcpop sha3 asimddp sha512 asimdfhm dit uscat
                                       ilrcpc flagm ssbs sb paca pacg dcpodp flagm2 frint
```
