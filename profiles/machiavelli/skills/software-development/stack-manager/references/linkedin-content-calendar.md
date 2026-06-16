# LinkedIn Content Calendar

**Location:** `<SHARED_DIR>/marketing/brand/content-calendar.md`
**Cron:** `linkedin-content-calendar` (3x/day: 09:00, 12:00, 18:00 CET)

## 7-Day Topic Rotation (including weekends)

- **Mon:** AI automation / efficienza PMI
- **Tue:** Tips rapidi / life hacks AI
- **Wed:** Case study / numeri
- **Thu:** Behind the scenes / tech deep dive
- **Fri:** Tendenze AI / thought leadership
- **Sat:** Storytelling / storie imprenditori
- **Sun:** Domanda aperta / engagement / community

**Note:** the owner richiede copertura weekend. Se il prompt del cron job ha solo 3 giorni, espandere a 7/7.

## Workflow
1. Cron triggers → Wannabe loads calendar + brand voice
2. Identifies day → picks topic from rotation
3. Generates post → publishes via LinkedIn API
4. Reports to Hub (chat <THREAD_ID>)
