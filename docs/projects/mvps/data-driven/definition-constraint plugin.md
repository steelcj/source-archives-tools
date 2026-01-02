# definition-constraint plugin

## The Question

How can we us a plugin to configure allowable archive.definition.yml fields and values and/or enforce formatting...

## The Answer

This is a natural next move and this is the right way to frame it.

> Short answer: **yes, a plugin could do that**, and it fits *perfectly* with what you’ve just built **without changing the MVP engine**.
>
> Let me keep this grounded and non-theoretical.
>
> ------
>
> ## What you’re really asking
>
> You’re not asking for “rules everywhere”.
>
> You’re asking:
>
> > *Can we make the engine remain neutral, while letting optional plugins describe what is considered valid, allowed, or well-formed for a given kind of archive definition?*
>
> That’s a good instinct.
>
> ------
>
> ## The key idea (one sentence)
>
> **The engine interprets.
>Plugins constrain.**
> 
> Not the other way around.
>
> ------
>
> ## How this fits your current MVP (important)
>
> Right now you have:
>
> - a neutral interpreter
>- a free-form `archive.definition.yml`
> - one hard guard: `schema_version` must exist
> 
> That’s perfect.
>
> A **plugin for constraints or formatting** would:
>
> - run *before* interpretation
>- look only at the definition file
> - either:
>   - approve it
>   - or explain what doesn’t fit expectations
> 
> Crucially:
>
> - it would **not change how interpretation works**
>- it would **not add behavior**
> - it would **not run unless explicitly enabled**
> 
> So nothing about your MVP is invalidated.
>
> ------
>
> ## What such a plugin could do (concretely)
>
> Examples of *reasonable* responsibilities:
>
> - Declare **allowed top-level keys**
>  - e.g. `archive`, `structure`, `schema_version`
> - Declare **expected shapes**
>   - `archive.id` must be a string
>   - `structure.languages` must be a list of objects
> - Enforce **naming conventions**
>   - language IDs like `en-ca`, `fr-qc`
> - Enforce **formatting norms**
>   - required keys present
>   - no unknown keys
> - Enforce **version compatibility**
>   - “this plugin supports schema_version 1.x”
> 
> All of this is *about the definition*, not behavior.
>
> ------
>
> ## What it should *not* do
>
> A plugin like this should **not**:
>
> - create directories
>- change the filesystem
> - infer intent
> - modify the definition
> - affect interpretation logic
> 
> It’s a **gatekeeper**, not an actor.
>
> ------
>
> ## Why a plugin (instead of hard-coding)?
>
> Because this keeps your core promise intact:
>
> - different archives can have different expectations
>- different communities can enforce different norms
> - the engine stays boring and trustworthy
> 
> Think of it as:
>
> > *“This definition is valid **for this kind of archive**.”*
>
> Not:
>
> > *“This is how SAT works.”*
>
> ------
>
> ## A very light mental model
>
> Without committing to design yet:
>
> ```
>definition
>    ↓
> (optional) definition plugin(s)
>    ↓
> interpreter
>    ↓
> output
> ```
> 
> If no plugin is present:
>
> - freestyle is allowed (like now)
>
> If a plugin is present:
>
> - expectations are explicit and inspectable
>
> ------
>
> ## Why this is not premature (and also not required yet)
>
> You’re not saying *“we must do this now”*.
>
> You’re noticing:
>
> - once people write real definitions
>- they will ask “what’s allowed?”
> - and different answers will exist
> 
> That’s exactly the right time to think:
>
> > *“This belongs outside the engine.”*
>
> ------
>
> ## Where I’d pause (intentionally)
>
> Right now:
>
> - you’ve proven the engine
>- you’ve proven interpretation
> - you’ve proven schema_version as ingress metadata
> 
> The **next signal** to add a plugin like this is:
>
> - when *you* feel friction writing definitions
>- not because it feels architecturally nice
> 
> So yes — you’re thinking in the right direction.
>And no — you don’t need to act on it yet.
> 
> If you want, the next time we touch this we can:
>
> - sketch what a **definition-constraint plugin** *would look like* (no code)
>- or wait until a real definition makes you say “ugh, this should be checked”
> 
> Both are valid.