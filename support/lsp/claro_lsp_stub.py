#!/usr/bin/env python3
"""Tiny Claro IDE helper stub for v1.17.26.
It prints completion words. A real Language Server Protocol service can build on this.
"""
KEYWORDS = [
    "SAY", "ASK", "SET", "IF", "ELSE", "END", "REPEAT", "TEACH", "DO",
    "CLASS", "NEW", "START TASK", "WAIT TASK", "HTTP GET", "OPEN WINDOW",
    "CLEAR SCREEN", "DRAW TEXT", "UPDATE SCREEN", "CLOSE WINDOW",
    "TYPE OF", "CHECK TYPE",
]
TYPES = ["NUMBER", "TEXT", "YESNO", "LIST", "MAP", "OBJECT", "ANY"]
for word in KEYWORDS + TYPES:
    print(word)
