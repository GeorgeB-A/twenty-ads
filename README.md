# Twenty Ads: a dataset of LLM-generated ad variant sets

**When marketers ask a language model for twenty ad variants to A/B test, how many different ads do they actually get?**

Twenty Ads holds 1,680 sets of 20 social-media ads (33,597 ads) written by two low-cost models under six ways of asking, for 12 product briefs. Each set comes with its effective semantic diversity (k_eff: how many genuinely different ads the set contains) and, for 264 sets, the idea and persuasion strategy of every ad as coded by two judge models.

Use it to measure variant diversity of new models or prompting strategies against a fixed reference, to study near-duplicate creative, or to test deduplication before an A/B test.

## What is in it

| File | Content |
|---|---|
| `data/sets.jsonl` | One set per line: generator, vendor, temperature, brief, category, mode, repetition, the 20 ads (`headline`, `body`), and diversity measures |
| `data/idea_coding.csv` | 10,536 ad-level codings: which idea each ad expresses (ideas numbered within a set) and which persuasion strategy it uses, by two judges (gpt-4.1, claude-sonnet-5-5) |
| `data/briefs_and_prompts.json` | The 12 briefs (brand, product, audience, channel), the 20 persuasion strategies, the system prompt and length limits |
| `runs_meta/` | Full settings of each generation run: prompt templates, sampling route, SDK versions, dates |
| `tools/diversity.py` | k_eff (Vendi score) for any set of texts and any embedding model |

**Generators:** gpt-4.1-mini and claude-haiku-4-5-20251001. **Briefs:** 12 fictional brands across food, home, family and personal care, each for one channel (Instagram, Facebook or TikTok). **Ad format:** headline of 4–8 words, body of 15–25 words.

**Modes** (how the 20 ads were requested):

| Mode | Requests | Instruction |
|---|---|---|
| `independent` | 20 | Write one ad. |
| `independent_slot` | 20 | Write one ad. This is ad i of 20 for the same brief; the other ads are written separately. |
| `independent_strategy` | 20 | Write one ad. It must use this persuasion strategy: strategy i. |
| `batch_plain` | 1 | Write 20 ads. |
| `batch` | 1 | Write 20 different ads. |
| `assigned_strategy` | 1 | Write 20 ads. Ad i must use persuasion strategy i from this list. |

**Runs:**

| Run | Date | Sets | Modes | Temperature |
|---|---|---|---|---|
| `B3` | 5 October 2026 | 360 | independent, batch, assigned_strategy | 1.0 |
| `B3ext` | 7 October 2026 | 360 | the same three | 0.7 |
| `R3` | 11 November 2026 | 240 | batch_plain, independent_strategy | 1.0 |
| `R4` | 14 November 2026 | 720 | all six, in one run on one day | 1.0 |

Use `R4` when comparing modes: all six were generated on the same day with the same settings.

## Diversity measures

`diversity.keff_vendi_q1` is the Vendi score (order 1) of the cosine-similarity matrix of the 20 ads, embedded as "headline — body" with OpenAI `text-embedding-3-small`. It runs from 1 (twenty copies of one ad) to 20 (twenty unrelated ads). `keff_vendi_q2` is the order-2 version; `keff_vendi_q1_head` uses headlines only. Other fields: `distinct_headlines`, `top_headline_count` (copies of the most repeated headline), `mean_cos`, the number of clusters at cosine 0.85 and 0.90, word counts and the share of ads within the length limits.

Mean k_eff (q = 1) and distinct headlines per set of 20, run `R4`:

| Mode | gpt-4.1-mini k_eff | distinct headlines | claude-haiku-4-5 k_eff | distinct headlines |
|---|---|---|---|---|
| independent | 1.67 | 9.2 | 1.90 | 9.3 |
| independent_slot | 1.82 | 11.8 | 2.04 | 9.5 |
| batch_plain | 2.83 | 20.0 | 3.29 | 20.0 |
| batch | 2.88 | 20.0 | 3.19 | 20.0 |
| independent_strategy | 3.18 | 19.9 | 3.84 | 19.6 |
| assigned_strategy | 4.69 | 20.0 | 5.11 | 20.0 |

Twenty separate requests for one ad return sets with an effective diversity below two and repeat about half the headlines; the judge models find about three distinct ideas in such a set. Asking for all twenty at once, or assigning a persuasion strategy to each ad, raises diversity (about ten coded ideas per set with assigned strategies), but no mode comes close to twenty distinct ads.

To score your own sets: `from tools.diversity import keff_from_texts, openai_embed` and pass the 20 texts with the same embedding model.

## Origin

The dataset is the generated material of Bykovskii, G. (2026), "Twenty ads, one idea: modelling near-duplicate AI creative and the winner's curse in A/B testing" (manuscript under review). The full replication package, with the model, simulations, calibration on the Upworthy Research Archive and all analysis code, is at https://doi.org/10.5281/zenodo.24433509.

## Citation

```bibtex
@misc{bykovskii2026twentyads,
  author    = {Bykovskii, George},
  title     = {Twenty Ads: a dataset of LLM-generated ad variant sets},
  year      = {2026},
  publisher = {Zenodo},
  version   = {1.0.0},
  doi       = {10.5281/zenodo.24459422}
}
```

## Licence

Data: CC BY 4.0. Code in `tools/`: MIT. The brands in the briefs are fictional.

Contact: George Bykovskii, Swinburne University of Technology — ORCID [0000-0002-7400-5782](https://orcid.org/0000-0002-7400-5782).
