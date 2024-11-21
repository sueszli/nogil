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

|    | type            | command           |      mean |     stddev |    median |      user |     system |       min |       max |
|---:|:----------------|:------------------|----------:|-----------:|----------:|----------:|-----------:|----------:|----------:|
|  0 | plain           | itertools.py      | 0.567469  | 0.0119883  | 0.570065  | 0.559903  | 0.0074184  | 0.549638  | 0.586569  |
|  1 | plain           | lib.py            | 0.10037   | 0.0026018  | 0.0995592 | 0.0950988 | 0.00515048 | 0.0976092 | 0.108629  |
|  2 | plain           | plain.py          | 0.563118  | 0.00854626 | 0.560743  | 0.55741   | 0.0056163  | 0.556415  | 0.586366  |
|  3 | multiprocessing | imap_unordered.py | 0.225802  | 0.0085966  | 0.223588  | 0.545673  | 0.166191   | 0.218431  | 0.244969  |
|  4 | multiprocessing | imap.py           | 0.232832  | 0.00656316 | 0.230609  | 0.555453  | 0.162511   | 0.223567  | 0.242637  |
|  5 | multiprocessing | map_async.py      | 0.452833  | 0.024858   | 0.448565  | 1.01004   | 0.110811   | 0.431474  | 0.516788  |
|  6 | multiprocessing | map.py            | 0.440075  | 0.00433147 | 0.440577  | 0.985363  | 0.108434   | 0.432938  | 0.446772  |
|  7 | multithreading  | GIL=1 executor.py | 0.369659  | 0.0103798  | 0.365851  | 0.359792  | 0.00922382 | 0.362101  | 0.396862  |
|  8 | multithreading  | GIL=0 executor.py | 0.21027   | 0.0104267  | 0.212105  | 0.43898   | 0.0105094  | 0.196279  | 0.232185  |
|  9 | multithreading  | GIL=1 workers.py  | 0.130465  | 0.00717258 | 0.129265  | 0.11784   | 0.00817749 | 0.124226  | 0.158233  |
| 10 | multithreading  | GIL=0 workers.py  | 0.167735  | 0.00768393 | 0.168563  | 0.1931    | 0.0202853  | 0.142996  | 0.176028  |
| 11 | ctypes          | invoke_hashcat.py | 0.0934947 | 0.00314156 | 0.0929726 | 0.0882496 | 0.00491642 | 0.0891827 | 0.0996272 |
| 12 | ctypes          | invoke_hashcat.py | 0.102134  | 0.00563781 | 0.100363  | 0.0986943 | 0.00838276 | 0.0976012 | 0.126973  |
| 13 | cpython         | invoke_hashcat.py | 0.100606  | 0.00435792 | 0.0997623 | 0.0950439 | 0.00523102 | 0.0943297 | 0.108179  |

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
