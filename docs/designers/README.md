# The three standing designers

So the direction never resets between chats, the same three designers advise
every chat: `designer-d` (craft), `designer-e` (the scroll) and `designer-f`
(the destinations; its design won). They are agent definitions in
`.claude/agents/`, so any chat on this repository can call them by name (the
Agent tool, `subagent_type: "designer-d"`). Their memory is in this folder:
`direction.md` (the brief and the owner's decisions, kept by the chats) and
each one's notebook (`D.md`, `E.md`, `F.md`, kept by the designer). A chat
asks them, shows the owner at most two options with one preview, then writes
the owner's answer into `direction.md`.
