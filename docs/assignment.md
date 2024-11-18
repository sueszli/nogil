assignment: https://www.complang.tuwien.ac.at/anton/lvas/effizienz-aufgabe24/

prof anmerkungen:

- also ich glaub wir können es so machen wie wir wollen
- es geht im vor allem dass er sieht dass wir was gelernt und verstanden haben
- es muss nicht C sein
- wir können auch seine Aufgabe in Python mit den tools optimieren
- wir sollten nur considern auch wenn wir unser eigenes problem machen, optimierungen die er gezeigt hat zu machen
- haben aber den Freiraum uns auszutoben solange wir es erklären können was wir gemacht haben
- als metrics sollten wir jedoch auf das was in der angabe ist setzen, also cycles und so
- und unsere präsi muss etwas kompakter sein, weil wir den algo erklären müssen und die benotung ist eig solely based auf die präsi haha

proposal:

- Wir möchten einen parallelisierbaren Algorithmus im GIL-freien Python (seit kurzem via PEP 703 @ Python3.13)[^pep] implementieren.
- Diese möchten wir zusätzlich mit Multiprocessing, C-Python Interopt sowie C-Python Extensions vergleichen und die Programme mit verschiedenen GCC-optimization-Flags kompilieren.
- Wir haben noch keinen konkreten algorithmus aber mal experimente ausgeführt[^snek].

[^ws23]: https://www.complang.tuwien.ac.at/anton/lvas/effizienz-aufgabe23/
[^pep]: https://peps.python.org/pep-0703/
[^snek]: https://github.com/sueszli/fast-snek
