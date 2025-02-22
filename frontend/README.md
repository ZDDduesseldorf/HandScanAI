# HandScanAI Frontend

## Environment Setup

1. Copy `.env.example` to `.env`.
2. Fill in the `VITE_GRAPHQL_ENDPOINT` with the appropriate value.

## Installation

You can use `npm`, `yarn`, or `pnpm` to install the dependencies and run the development server.

### Using npm

```bash
npm install
npm run dev
```

### Using yarn

```bash
yarn install
yarn dev
```

### Using pnpm

```bash
pnpm install
pnpm dev
```

## Console commands

A complete list of all console commands can be found in the `package.json`.

## Project structure

### Global files

The `/src` folder contains the global files that apply to all pages, such as the layout.

### Pages

Individual pages are located in the `/pages` folder. The pages represent the accessible pages of the website.

### Components

The pages access components that are located in the `src/components/` folder. The components are building blocks that can be accessed by all pages and thus standardize the styles. By using components, the styles are consistent between the pages and only need to be changed in one place if necessary.

The components are organized thematically by category. The file names in turn supplement the folder name to specify what kind of component it is. For example, `/components/cards/WithText.tsx` contains a text card, i.e. a CardWithText.
