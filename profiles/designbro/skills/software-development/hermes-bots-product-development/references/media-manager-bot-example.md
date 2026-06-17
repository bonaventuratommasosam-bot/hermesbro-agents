# Media Manager Bot — Example Reference (Wannabe Bot)

Concrete example of bot product development pattern.

## Chosen Name: Wannabe Bot

[REDACTED — dati personali rimossi] chose "Wannabe Bot" — outside Italian-pun convention. "Wannabe" = wanting to grow. Suggested alternatives (AdVinci, MadMan, Brandino) not chosen.

## Personality: Gary Vaynerchuk + David Ogilvy + Seth Godin

- **Gary Vee** (executor): Direct, engagement-first, no-BS social media execution
- **Ogilvy** (strategist): Copywriting mastery, brand building, long-term thinking
- **Godin** (philosopher): Permission marketing, storytelling, Purple Cow

## Tools Built (13)

1. generate_post, 2. create_weekly_plan, 3. record_analytics, 4. get_analytics_report, 5. update_strategy, 6. get_strategy, 7. save_template, 8. get_templates, 9. get_calendar, 10. add_competitor, 11. get_competitors, 12. get_stats, 13. list_posts

## Cron Jobs (4)

- 08:00 morning_check, 20:00 evening_analytics, Monday 09:00 weekly_report, 1st monthly monthly_report

## Deployment

- Port: 8093, Service: wannabe.service
- Webhook: https://YOUR_VPS_HOST/wannabe/webhook/{token}

## Key Lessons

1. [REDACTED — dati personali rimossi] corrected architecture 3 times before settling on FastAPI
2. Nginx config requires Python script via terminal (patch tool refuses /etc/ paths)
3. [REDACTED — dati personali rimossi] chose name himself — don't push naming conventions
