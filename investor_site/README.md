# HIVEMIND Architecture Whitepaper Site

Dark-theme architecture whitepaper site for HIVEMIND, built from `docs/architecture.md` as the source of truth.

The site is meant to be a deep investor and technical read: product thesis, terminal surfaces, cross-asset market mesh, swarm runtime, research jobs, knowledge memory, evidence layers, situation engines, agent operating model, token efficiency, validation, build sequence, moat, and glossary.

## Local Preview

Open `index.html` directly in a browser, or serve this folder with any static server.

## Vercel Deploy

Preferred deployment is from the repository root. The root `vercel.json` rewrites `/` to this site, so Vercel import stays one-click and does not require choosing this folder manually.

- Root directory: repository root
- Framework preset: `Other`
- Build command: leave blank
- Output directory: leave blank

```powershell
npx vercel@latest --prod
```

Run the command from the repository root after logging in to the Vercel CLI.
