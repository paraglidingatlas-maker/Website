# The three standing designers

So the direction never resets between chats, the same three designers advise
every chat: Trim (`designer-d`, craft), Cloudbase (`designer-e`, the scroll)
and Turnpoint (`designer-f`, the destinations; its design won). The owner named
them on 24 Oct 2026: Trim for a wing's clean hands-off glide, Cloudbase for the
cloud fly-through, Turnpoint for the places a route flies through. They are agent definitions in
`.claude/agents/`, so any chat on this repository can call them by name (the
Agent tool, `subagent_type: "designer-d"`). Their memory is in this folder:
`direction.md` (the brief and the owner's decisions, kept by the chats) and
each one's notebook (`D.md`, `E.md`, `F.md`, kept by the designer). A chat
asks them, shows the owner at most two options with one preview, then writes
the owner's answer into `direction.md`.
