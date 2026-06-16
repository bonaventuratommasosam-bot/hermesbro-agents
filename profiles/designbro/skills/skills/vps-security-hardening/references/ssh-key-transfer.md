# Trasferimento Sicuro della Chiave Privata SSH dal VPS al PC Locale

Questa guida descrive come trasferire in modo sicuro la chiave privata SSH generata sul VPS (`/home/[REDACTED — dati personali rimossi]/.ssh/id_rsa`) al tuo PC locale, **senza mai esporre la chiave in chat o su canali non sicuri**.

## Passaggi da Eseguire sul TUO PC Locale

1.  **Apri un terminale sul tuo PC locale.** (Non sul VPS, ma sul tuo computer.)

2.  **Esegui il comando `scp` per copiare la chiave.** Ti verrà chiesta la password di root del VPS.

    ```bash
    scp root@TUO_IP_VPS:/home/[REDACTED — dati personali rimossi]/.ssh/id_rsa ~/.ssh/id_rsa_[REDACTED — dati personali rimossi]_vps
    ```
    *   **SOSTITUISCI** `TUO_IP_VPS` con l'indirizzo IP effettivo del tuo server (es. `194.146.12.219`).
    *   Questo comando copierà la chiave privata (`id_rsa`) dal VPS nella tua directory `~/.ssh/` sul PC locale, salvandola come `id_rsa_[REDACTED — dati personali rimossi]_vps`.

3.  **Imposta i permessi corretti per la chiave privata scaricata.** È CRITICO che solo tu possa leggere questa chiave.

    ```bash
    chmod 600 ~/.ssh/id_rsa_[REDACTED — dati personali rimossi]_vps
    ```

4.  **Verifica la connessione SSH utilizzando la nuova chiave.**

    ```bash
    ssh -i ~/.ssh/id_rsa_[REDACTED — dati personali rimossi]_vps [REDACTED — dati personali rimossi]@TUO_IP_VPS
    ```
    *   **SOSTITUISCI** `TUO_IP_VPS` con l'indirizzo IP del tuo server.
    *   Dovresti essere in grado di accedere al VPS come utente `[REDACTED — dati personali rimossi]` senza password.

## Cosa fare dopo aver trasferito la chiave (Informami sul VPS)

Una volta che avrai trasferito e verificato la chiave privata sul tuo PC locale, **avvisami qui in chat**.

Potrò quindi:
1.  **Cancellare la chiave privata (`/home/[REDACTED — dati personali rimossi]/.ssh/id_rsa`) dal VPS** per eliminare la sua presenza dal server.
2.  Disabilitare l'autenticazione tramite password.
3.  Disabilitare il login dell'utente `root` via SSH.

Questi passaggi aumenteranno drasticamente la sicurezza del tuo VPS.
