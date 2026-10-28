# Choices record: {{company name}}

Run: {{who ran it, where, date}}
Document: {{path of the brand document this record belongs to}}

One block per decision the owner made. The skill fills a block the moment the owner chooses and never
edits a filled block; a later choice on the same decision is a new block with a later date. The six
decision names below are fixed, because `scripts/check_choices.py` reads them; a run that stops before
a decision leaves its block out.

## Decision: pair
Step: 5
Recorded: {{YYYY-MM-DD}}
Candidates offered:
- A: "{{tension}} / {{best-self line}}", commits the company to {{who it turns away, what it must live up to, what it can no longer say}}
- B: "{{...}}", commits the company to {{...}}
- C: "{{...}}", commits the company to {{...}}
Recommendation: {{the skill's, named as the skill's, with its one-line reason}}
Chosen: {{tension}}
Chosen: {{best-self line}}
Owner's words: {{what the owner said when choosing, or "accepted the recommendation"}}

## Decision: purpose line
Step: 8
Recorded: {{YYYY-MM-DD}}
Candidates offered:
- A: "We exist to {{...}}", commits the company to {{...}}
- B: "We exist to {{...}}", commits the company to {{...}}
- C: "We exist to {{...}}", commits the company to {{...}}
Recommendation: {{...}}
Chosen: We exist to {{...}}
Owner's words: {{...}}

## Decision: category
Step: 14
Recorded: {{YYYY-MM-DD}}
Candidates offered:
- A: "{{existing option}}" (existing), commits the company to {{winning it someday, against ...}}
- B: "{{modified option}}" (modified existing), commits the company to {{...}}
- C: "{{new option}}" (new), commits the company to {{repeating it for years, claiming first, only or best}}
Recommendation: {{...}}
Chosen: {{the category}}
Owner's words: {{...}}

## Decision: positioning statement
Step: 19
Recorded: {{YYYY-MM-DD}}
Candidates offered:
- A: "For ... Who ... is a ... That ... Unlike ... {{...}}", commits the company to {{...}}
- B: "{{...}}", commits the company to {{...}}
- C: "{{...}}", commits the company to {{...}}
Recommendation: {{...}}
Chosen: Who: {{the chosen Who line}}
Chosen: That: {{the chosen benefit}}
Chosen: Unlike: {{the chosen foil}}
Chosen: Because of: {{the chosen differentiator}}
Owner's words: {{...}}

## Decision: dimensions
Step: 23
Recorded: {{YYYY-MM-DD}}
Candidates offered:
- A: "{{dimension}} and {{dimension}}", commits the company to {{...}}
- B: "{{...}}", commits the company to {{...}}
- C: "{{...}}", commits the company to {{...}}
Recommendation: {{...}}
Chosen: {{dimension}}, {{dimension}}
Owner's words: {{...}}

## Decision: adjectives
Step: 27
Recorded: {{YYYY-MM-DD}}
Candidates offered:
- A: "{{five traits, each with its edge in brackets}}", commits the company to {{...}}
- B: "{{...}}", commits the company to {{...}}
- C: "{{...}}", commits the company to {{...}}
Recommendation: {{...}}
Chosen: {{Trait 1}}. {{its sentence or two, with the edge built in, word for word as the document carries it}}
Chosen: {{Trait 2}}. {{...}}
Chosen: {{Trait 3}}. {{...}}
Chosen: {{Trait 4}}. {{...}}
Chosen: {{Trait 5}}. {{...}}
Owner's words: {{...}}
