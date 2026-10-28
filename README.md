# Brand Workshop

Part of **Fully Powered Capability Templates** by [Fully Powered AI](https://fullypowered.ai/).

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

[MIT](LICENSE), copyright 2026 Fully Powered AI. Third-party source acknowledgments and recorded upstream license terms remain in [SOURCES.md](SOURCES.md); this license does not relicense the cited source materials.
