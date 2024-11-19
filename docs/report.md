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

benchmarking:

- https://github.com/sharkdp/hyperfine (very nice)
- https://github.com/sosy-lab/benchexec
- https://github.com/softdevteam/krun/
