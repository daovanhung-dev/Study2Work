# Study Web

Study Web is an Angular 22 standalone SPA scaffold. Feature routes, authentication,
and Study API integration have not been implemented.

## Run locally

```bash
npm install
npm start
```

Open `http://localhost:4200/`. The root page is a temporary scaffold status
message; it is not the SH-01 product screen.

## Build

```bash
npm run build
```

## Test

```bash
npm test
```

## Architecture

See [`gui/architech.md`](gui/architech.md) for folder responsibilities, feature
boundaries, Study design rules, and source/API constraints. Screen designs and
DDs remain under `docs/` and are not runtime route evidence.
