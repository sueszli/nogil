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

# Motivation


# Experiments


Target hash: `aaa`

Warmup: 3 runs

Docker with Python 3.13t experimental build

| command                                  | mean                | stddev                | median              | user                | system               | min                 | max                 |
|------------------------------------------|---------------------|-----------------------|---------------------|---------------------|----------------------|---------------------|---------------------|
| plain: itertools.py                      | 0.5674692401200001  | 0.01198827824756599   | 0.57006548532       | 0.55990282          | 0.0074184            | 0.5496379653200001  | 0.5865690483200001  |
| plain: lib.py                            | 0.10036984857259255 | 0.002601799874962498  | 0.09955924698       | 0.09509880296296297 | 0.005150482962962963 | 0.09760924698000001 | 0.10862874698000001 |
| plain: plain.py                          | 0.56311819686       | 0.008546263909006254  | 0.5607432801600001  | 0.5574100199999998  | 0.005616299999999999 | 0.55641523866       | 0.58636586266       |
| multiprocessing: imap_unordered.py       | 0.22580185960615384 | 0.008596599653744735  | 0.22358803876       | 0.5456729907692307  | 0.16619102307692304  | 0.21843099776       | 0.24496916376       |
| multiprocessing: imap.py                 | 0.23283159617000002 | 0.006563159786685698  | 0.23060927992000002 | 0.5554529199999999  | 0.16251065           | 0.22356723842       | 0.24263732142000002 |
| multiprocessing: map_async.py            | 0.45283322936000003 | 0.02485797469878736   | 0.44856494596       | 1.0100399599999998  | 0.1108107            | 0.43147434096000004 | 0.51678821696       |
| multiprocessing: map.py                  | 0.44007464079999997 | 0.004331471810503806  | 0.4405771448        | 0.98536284          | 0.10843393999999999  | 0.4329375193        | 0.4467715203        |
| PYTHON_GIL=1 multithreading: executor.py | 0.36965916640000007 | 0.010379827255109443  | 0.3658508374        | 0.35979243999999994 | 0.009223819999999999 | 0.36210054540000003 | 0.3968615454        |
| PYTHON_GIL=0 multithreading: executor.py | 0.21027037247846156 | 0.010426702772034552  | 0.21210451994       | 0.4389796446153846  | 0.010509364615384615 | 0.19627872794       | 0.23218535394000003 |
| PYTHON_GIL=1 multithreading: workers.py  | 0.13046479691       | 0.007172575609842329  | 0.12926548436000002 | 0.11783973          | 0.008177489999999999 | 0.12422606786000001 | 0.15823290086       |
| PYTHON_GIL=0 multithreading: workers.py  | 0.16773493366000006 | 0.007683925116868945  | 0.16856328266000004 | 0.193100225         | 0.020285272499999996 | 0.14299638666000003 | 0.17602834466000003 |
| ctypes: invoke_hashcat.py                | 0.09349466670000002 | 0.0031415585053035443 | 0.0929726247        | 0.08824959857142858 | 0.004916421428571427 | 0.0891826667        | 0.0996272077        |
| ctypes: invoke_hashcat.py                | 0.10213379513846156 | 0.005637809432670206  | 0.1003630886        | 0.09869431076923077 | 0.008382755384615385 | 0.09760121360000001 | 0.1269725466        |
| cpython: invoke_hashcat.py               | 0.10060564948857142 | 0.004357923062152972  | 0.09976227606       | 0.09504387999999998 | 0.005231015714285715 | 0.09432969256       | 0.10817944256       |

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
