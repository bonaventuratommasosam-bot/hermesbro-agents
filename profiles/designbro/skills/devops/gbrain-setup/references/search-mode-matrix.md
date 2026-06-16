# GBrain Search Mode Cost Matrix

Present this VERBATIM to the user after `gbrain init`. Do NOT silently accept the default.

```
Costo per-query @ 10K queries/mese:

                  Haiku 4.5     Sonnet 4.6    Opus 4.7
                  ($1/M)        ($3/M)        ($5/M)
  conservative    $40/mo        $120/mo       $200/mo
  balanced        $100/mo       $300/mo       $500/mo
  tokenmax        $200/mo       $600/mo       $1,000/mo

(scales linearly: ×10 for 100K/mo, ÷10 for 1K. 25x corner-to-corner spread.)
```

## Modes

| Mode | Token budget | LLM expansion | Chunks | Best for |
|------|-------------|---------------|--------|----------|
| conservative | 4K | OFF | 10 | Haiku-class, cost-sensitive, high-volume loops |
| balanced | 12K | OFF | 25 | Sonnet-tier sweet spot |
| tokenmax | unlimited | ON | 50 | Opus/frontier models, best retrieval quality |

## Application

```bash
gbrain config set search.mode <mode>
gbrain search modes              # verify
```

## Notes

- Cost depends on BOTH mode AND downstream model (see 9-cell matrix above)
- tokenmax is the default since v0.31.x — preserves original retrieval shape
- To get v0.31.x limit=20 instead of 50: `gbrain config set search.searchLimit 20`
