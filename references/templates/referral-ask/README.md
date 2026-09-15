# Referral Ask Templates

_Voice-faithful starter templates per ask type. Edit to match your firm's voice. Setup pulls from `<config-root>/memory/me/voice.md` to populate sign-off and apply banned-phrase rules._

These are starting points. Each `/draft-touchpoint` referral-ask invocation tailors based on the specific contact and recent context.

---

## A. Post-positive-touch ask

When: They just did something positive — replied warmly, sent a glowing note, mentioned you publicly, made an intro.

```
[Greeting per voice — "Hey [name]," or "[name],"]

[Acknowledge specific positive thing — 1 sentence, specific, not flattery]

While I have you — I'm working with [ICP type orgs] on [type of work] and looking to talk to a couple more like them. If anyone in your network is wrestling with [problem you solve], I'd love a forwardable intro. Happy to send a 1-paragraph blurb you can pass along if helpful.

[Sign-off per voice]
```

## B. Post-project ask

When: A project just closed — theirs or another they referred.

```
[Greeting]

[Specific outcome from the project — 1-2 sentences. Reference what landed, what shifted, what they cared about.]

Curious if anyone in your network is wrestling with [related problem]. I have capacity opening up in [month] and would love to do another one of these. Easy intro from your end if you have someone in mind — happy to do the heavy lift on the conversation.

[Sign-off]
```

## C. Re-warm + ask

When: They've gone quiet (60+ days) but were warm before. Lead with value, ask softly.

```
[Greeting]

Saw [specific thing in their world or industry] and thought of [their initiative or your last conversation]. [1-2 sentences sharing something genuinely useful — article / framework / intro / observation. The value should be the reason for reaching out, not a wrapper for the ask.]

On my end, [1-line update on what you're up to — must connect to what they care about].

Anyone in your network come to mind worth a conversation? No pressure — happy to keep the door open either way.

[Sign-off]
```

## D. Trigger-based ask

When: Fiscal year flip, conference, budget cycle approaching for them.

```
[Greeting]

[Specific trigger reference — "FY ends for you in March" / "[Conference] is coming up" / "Heard you're in budget planning mode" — make it specific to them, not generic to industry.]

If you're hearing from peers wrestling with [your problem space] as they plan, I'd love to be a resource — even a 15-min sounding-board conversation, no pitch. Forward this if useful.

[Sign-off]
```

---

## Customizing these templates

- **Voice descriptors** — these starters lean toward "warm, direct, low-jargon." If your voice is "sharp, contrarian, plainspoken" the same shape works but the language tightens. The plugin reads `<config-root>/memory/me/voice.md` and adjusts.
- **Length** — defaults are 3-5 sentences. If your voice prefers shorter, the plugin tightens.
- **Sign-off** — pulled from voice file, not hardcoded here.
- **Asks specific to your offering** — the bracketed `[type of work]` gets filled per-call from your ICP definition. The plugin won't ship without one.

---

## Common variations to add

- **"I'd return the favor" exchange asks** — for connectors who you also refer to. Frame as bilateral.
- **Curiosity-only asks** (no commitment) — "Anyone come to mind?" with no follow-on action implied. Lower friction; lower yield.
- **Specific-target asks** — "Looking specifically for [exact title at exact org type]." Higher precision; only use when you really know.

Add these as Section E, F, G as your firm's pattern library grows.
