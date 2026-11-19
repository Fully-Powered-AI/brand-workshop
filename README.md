# Brand strategy workshop with AI: purpose, positioning and voice

FullyPowered Workflow Templates for owners shaping their brand turn the AI your company already pays for into a team that knows how the work is done: an owner with the company purpose and positioning drafted in their own words, a founder with a brand strategy and a record of every choice made, a team lead with a customer validation kit ready to take into real conversations. Workflow templates, made to be customized and deployed. All plain Markdown, all free, MIT license.

We are FullyPowered AI. We build AI workflows for companies, and these are the templates we start from. We publish them because a good starting point should be open to everyone. Copy one. Change it. Make it yours.

> [!TIP]
> **Missing a template that is not listed here, or want these customized for your organization? Reach out to us.** These are templates, made to be customized and deployed. FullyPowered AI customizes and builds AI workflows, connects them to your business systems, installs them in your agents and puts them in the hands of the people who own the work. [See more examples for owners shaping their brand](https://fullypowered.ai/functions/marketing-and-content/brand/?utm_source=github&utm_medium=referral&utm_campaign=workflow-collections&utm_content=brand-workshop-readme&from=gh-brand-workshop-readme) · [Have one built for your team](https://fullypowered.ai/pricing/?utm_source=github&utm_medium=referral&utm_campaign=workflow-collections&utm_content=brand-workshop-readme&from=gh-brand-workshop-readme). Not sure where to start? Email hello@fullypowered.ai and a person will answer.

**Who this is for**

- Owners and founders who want a clear brand strategy that sounds like their company and no one else.
- Marketing and operations leads who want a repeatable way to settle purpose, positioning and personality.
- The person running the workshop, who supplies the facts, makes every wording choice and tests it with real customers.

**What these are for**

- **Your best way of doing it, for the whole team.** One piece of work, written down precisely enough that an assistant prepares it the same way every time.
- **Work you can check.** Every template says what it needs, what it produces, what it checked and what it could not.
- **A person decides.** Anything that sends, posts, pays or changes a record waits for someone to approve it.
- **Tied into your business systems.** A workflow can be designed to pull from the systems your company already runs, and even push data back into them, with guardrails and a person approving. [Browse the Connectors Directory](https://fullypowered.ai/connectors/?utm_source=github&utm_medium=referral&utm_campaign=workflow-collections&utm_content=brand-workshop-readme&from=gh-brand-workshop-readme).
- **Free, open and portable.** MIT-licensed plain instructions that run in the assistant or agent your team already uses: ChatGPT, Claude, Claude Code, Claude Cowork, Codex, Copilot, Gemini, Grok, Perplexity.

**Quick start**

1. **Try the first step now.** Copy this into ChatGPT, Claude, Copilot or Gemini. Replace the three bracketed lines with your own answers and send it. This is the purpose step of the workshop, shortened so it fits in a single message.

   ```text
   You are helping me run a brand workshop for my company. Work one step at
   a time. Never invent facts about my company. If something is missing,
   ask me.

   What we sell, and to whom: [your answer]
   How customers handle this problem today: [your answer]
   Why we started the company: [your answer]

   Step 1. List eight tensions my customers live with. A tension is a place
   where two pressures pull against each other, including assumptions they
   hold without noticing.
   Step 2. List five things we deliver when we are at our best, as short
   plain summaries of what customers get.
   Step 3. Draft three purpose lines that differ in substance, each
   starting "We exist to". Under each one, add a line starting "Commits the
   company to:" that says who it turns away or what we would have to live
   up to.
   Step 4. Tell me which one you recommend and why. Then stop and wait for
   me to choose.
   ```

2. Read what comes back. It marks what it checked and what is left for you. What a result looks like, for a tutoring company:

   ```text
   Tensions (3 of 8 shown)
   - Families have more tutoring choices than ever and less idea which one will last.
   - Parents want results they can measure and a person their child trusts.
   - Learning apps are cheap and always there, and children stop opening them.

   At our best (2 of 5 shown)
   - A child who dreaded maths asks for an extra session.
   - A parent gets two clear sentences from the tutor after every session.

   Purpose lines
   1. We exist to give every child who is behind at school a tutor who knows them by name.
      Commits the company to: one tutor per child for the whole school year, and no drop-in sessions with whoever is free.
   2. We exist to turn a worrying school report into a plan a family can follow.
      Commits the company to: a written plan after the first session, and turning away families who only want last-minute exam cramming.
   3. We exist to make help with schoolwork feel ordinary for every family in our part of town.
      Commits the company to: staying local, and evening sessions close to home.

   My recommendation: line 1. It gives you a rule you can act on tomorrow, because it rules out drop-in sessions. The choice is yours.
   ```

3. Stop there. You will know if this is for you. When you want it fitted to your company, or built into your agents, [that is what we do](https://fullypowered.ai/pricing/?utm_source=github&utm_medium=referral&utm_campaign=workflow-collections&utm_content=brand-workshop-readme&from=gh-brand-workshop-readme).

The owner starts the workshop, supplies the company's facts and customers' words, and makes every choice. The workflow drafts the options, records each choice and checks the finished document. It sends nothing anywhere.

Everything here is a sample to adapt. Change the steps, the wording and the documents until they match how your company works. A workflow can be one step or many, and FullyPowered AI builds workflows around a company's own way of doing the work.

An owner-led skill for drafting a company's purpose, positioning and personality. It produces a brand strategy, a record of the owner's choices and a validation kit. The owner chooses the wording and runs the real-world validation.

## Included

- `skill/brand-workshop/SKILL.md`: the workshop procedure.
- `assets/` inside that skill: four document and worksheet templates.
- `references/` inside that skill: terms, frameworks and checks.
- `scripts/` inside that skill: two Python checks and their offline fixtures.
- [SOURCES.md](SOURCES.md): source acknowledgments and provenance limits.

## Install and run locally

Clone the public package:

```sh
git clone https://github.com/Fully-Powered-AI/brand-workshop.git
cd brand-workshop
```

Keep `skill/brand-workshop/` intact. Point your agent's skill loader at that folder, or copy the complete folder to the skill location your host supports. With a file-aware agent, you can also ask it to read `skill/brand-workshop/SKILL.md` directly and run the workshop with you, writing outputs into a separate `workspace/` folder.

The agent needs file access and Python 3 execution for the checks; no connector or network service is required. Supply the company facts and customers' words requested by the skill, and stay present for the choices. No specific model is required by this package. Cross-host conversational behavior has not been validated; offline fixture results cover only the deterministic checks. Without code execution, record that the checks were not run.

After the workshop, run from the package root:

```sh
python3 -I skill/brand-workshop/scripts/check_brand_document.py workspace/brand-strategy.md
python3 -I skill/brand-workshop/scripts/check_choices.py workspace/choices-record.md workspace/brand-strategy.md
```

## Offline tests

Requires Bash and Python 3, with no third-party Python dependencies:

```sh
bash skill/brand-workshop/scripts/fixtures/run_fixtures.sh
```

The fixtures exercise valid, partial and invalid documents and choice consistency. Passing them does not validate a company's positioning or audience response.

## Releases and license

This is the public release edition of a private authoring project. Updates are prepared in that project and released here explicitly; the two editions are not automatically merged. Keep local store or company work in a separate workspace.

[MIT](LICENSE), copyright 2026 FullyPowered AI. Third-party source acknowledgments and recorded upstream license terms remain in [SOURCES.md](SOURCES.md); this license does not relicense the cited source materials.
