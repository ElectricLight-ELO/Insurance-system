"""Мини-парсер C4-PlantUML для проверки правил проекта ИС ОСАГО."""
import re

DECL_KINDS = ("Person|Person_Ext|System|System_Ext|SystemDb|SystemDb_Ext|SystemQueue|SystemQueue_Ext|"
              "Container|ContainerDb|ContainerQueue|Container_Ext|ContainerDb_Ext|ContainerQueue_Ext|"
              "Component|ComponentDb|ComponentQueue|Component_Ext|ComponentDb_Ext|"
              "Enterprise_Boundary|System_Boundary|Container_Boundary|Boundary|"
              "Deployment_Node|Deployment_Node_L|Deployment_Node_R|Node|Node_L|Node_R")
DECL_RE = re.compile(r"^\s*(" + DECL_KINDS + r")\((.*)\)\s*\{?\s*$", re.M)
REL_RE = re.compile(r"^\s*(Rel|BiRel|Rel_Back|RelIndex|Rel_\w+|RelIndex_\w+|BiRel_\w+)\((.*)\)\s*$")
GLOBAL_KINDS = re.compile(r"^(Person|System|Container|Enterprise_Boundary|Boundary)")


def split_args(s):
    """Разбить аргументы макроса с учётом кавычек и скобок."""
    out, cur, dep, inq, i = [], "", 0, False, 0
    while i < len(s):
        c = s[i]
        if c == "\\" and inq and i + 1 < len(s):
            cur += s[i:i + 2]; i += 2; continue
        if c == '"': inq = not inq
        elif not inq and c == "(": dep += 1
        elif not inq and c == ")": dep -= 1
        if c == "," and not inq and dep == 0:
            out.append(cur.strip()); cur = ""
        else:
            cur += c
        i += 1
    if cur.strip(): out.append(cur.strip())
    return out


def strip_strings(line):
    return re.sub(r'"(?:[^"\\]|\\.)*"', '""', line)
