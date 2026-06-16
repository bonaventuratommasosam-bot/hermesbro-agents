# llms.txt — Machine-Readable Site Summary

Emerging standard for making websites discoverable by AI agents. Place at `/.well-known/llms.txt` or `/llms.txt`.

## Format

```markdown
# Site Name

> One-line description of the site

## Overview
Brief description of what the site offers and who it's for.

## Key Pages
- [Page Name](https://example.com/page): What this page does
- [Another Page](https://example.com/other): Description

## API / Tools
- `POST /api/action`: Description of what it does
- `GET /api/data`: Description

## Authentication
- OAuth2 required for write operations
- API key via header: `Authorization: Bearer <token>`

## Rate Limits
- 100 requests/minute per API key
- 1000 requests/hour for anonymous

## Notes for AI Agents
- Preferred interaction method: REST API over HTML scraping
- WebMCP tools available at /api/mcp
- Structured data available via JSON-LD on all pages
```

## Real-World Examples

### Minimal
```
# My Restaurant

> Italian restaurant in Turin, online ordering available

## Menu
- [/menu](https://example.com/menu): Full menu with prices
- [/order](https://example.com/order): Place an order

## Contact
- [/reservations](https://example.com/reservations): Book a table
```

### API-First
```
# ContAIbile API

> Financial assistant for Italian small businesses

## Endpoints
- POST /api/expenses: Log an expense
- GET /api/reports/monthly: Monthly financial report
- GET /api/invoices: List invoices

## Auth
- Bearer token required for all endpoints
- Register at /auth/register

## Notes
- All amounts in EUR
- Dates in ISO 8601
- Pagination: ?page=1&limit=50
```

## Tools

- [llms.txt validator](https://llmstxt.org/) — check your file
- [Firecrawl llms-txt](https://github.com/mendableai/firecrawl/tree/main/examples/llms-txt) — auto-generate from sitemap
- [WordPress plugin](https://wordpress.org/plugins/llms-txt/) — auto-generate for WP sites

## Why It Matters

Without llms.txt, AI agents have to:
1. Scrape the homepage
2. Guess what the site does
3. Navigate blindly through links
4. Hope they find the right API endpoints

With llms.txt, agents get a structured map immediately. 1 file, 5 minutes to create, huge impact for agent interaction.
