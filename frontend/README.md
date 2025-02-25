# HandScanAI Frontend

## Table of Contents

- [Prerequisites](#prerequisites)
- [Environment Setup](#environment-setup)
- [Installation](#installation)
- [Building for Production](#building-for-production)
- [Code Quality](#code-quality)
  - [Linting](#linting)
  - [Formatting](#formatting)
  - [Project Scripts](#project-scripts)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Common Tasks](#common-tasks)

## Prerequisites

- **Node.js**: The project requires Node.js to be installed on your machine. You can download the latest version of Node.js from the [official website](https://nodejs.org/).
- **Package Manager**: Any Node.js package manager can be used to install the dependencies.

## Environment Setup

1. Copy `.env.example` to `.env`.
2. Fill in the `VITE_GRAPHQL_ENDPOINT` in `.env` with the appropriate value.

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

## Building for Production

To build the project for production:

### Using npm

```bash
npm run build
```

### Using yarn

```bash
yarn build
```

### Using pnpm

```bash
pnpm build
```
The optimized output will be in the `dist/` directory.

## Code Quality

### Linting

To lint the project using ESLint:

#### Using npm

```bash
npm run lint
```

#### Using yarn

```bash
yarn lint
```

#### Using pnpm
```bash
pnpm lint
```

### Formatting

To format the project using Prettier:

#### Using npm

```bash
npm run format
```

#### Using yarn

```bash
yarn format
```

#### Using pnpm
```bash
pnpm format
```

### Project Scripts

A complete list of all available CLI commands can be found in `package.json`.

## Tech Stack

HandScanAI's frontend is a web application built with modern web technologies. The application is developed using **React with TypeScript**, optimized with **Vite**, and styled with **Material UI** and **Emotion**. It interacts with a GraphQL backend using **Apollo** and uses **Zustand** for state management.

### Core Technologies
- **[React](https://react.dev/)**: A JavaScript framework for building user interfaces.
- **[TypeScript](https://www.typescriptlang.org/)**: A typed superset of JavaScript for improved developer experience.
- **[Vite](https://vitejs.dev/)**: A fast build tool optimized for modern frontend development.

### State Management
- **[Zustand](https://github.com/pmndrs/zustand)**: A lightweight state management solution for managing application-wide states.

### Styling & UI
- **[Material UI (MUI)](https://mui.com/)**: A popular UI library with ready-to-use React components.
- **[Emotion](https://emotion.sh/docs/introduction)**: A performant CSS-in-JS library used with MUI for custom styling.
- **[Framer Motion](https://www.framer.com/motion/)**: A library used for animated transitions between pages.

### API Communication
- **[Apollo Client](https://www.apollographql.com/docs/react/)**: A GraphQL client used for efficient data fetching and caching.
- **[WebSocket](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)**: WebSocket used for real-time server communication when capturing the hand images.

### Development & Tooling
- **[pnpm](https://pnpm.io/)**: A fast, efficient package manager. Alternatively, npm or yarn are also supported.
- **[ESLint](https://eslint.org/)**: A static code analysis tool for identifying ploblems in JavaScript and TypeScript code.
- **[Prettier](https://prettier.io/)**: A code formatter for consistent styling.

## Project structure

The HandScanAI frontend follows a structured file organization:
```
frontend/
├── eslint.config.js       # ESLint configuration
├── index.html             # Main HTML template
├── package.json           # Project dependencies and scripts
├── pnpm-lock.yaml         # Lockfile for package versions
├── public/                # Public assets such as logos and other images
├── README.md              # Project documentation
├── src/                   # Source code directory
│   ├── App.css            # Global styles
│   ├── App.tsx            # Root React component
│   ├── assets/            # Fonts and other static resources
│   ├── components/        # Reusable UI components
│   │   ├── buttons/
│   │   ├── cards/
│   │   ├── custom/
│   │   ├── headings/
│   │   ├── layout/
│   │   ├── navigation/
│   │   └── text/
│   ├── hooks/             # Custom React hooks
│   ├── index.css          # Base styles
│   ├── Layout.tsx         # Layout wrapper component
│   ├── main.tsx           # Application entry point
│   ├── pages/             # Page-level components (views)
│   │   ├── Explanation.tsx
│   │   ├── Home.tsx
│   │   ├── ImageCapture.tsx
│   │   ├── ImagePostCapture.tsx
│   │   ├── PrivacyNotice.tsx
│   │   ├── Processing.tsx
│   │   ├── Result_1.tsx
│   │   ├── Result_2.tsx
│   │   ├── Setup.tsx
│   │   └── SubmissionComplete.tsx
│   ├── services/          # API service handlers for GraphQL
│   │   ├── api.ts
│   │   ├── graphqlTypes.ts
│   │   ├── mutations.ts
│   │   └── queries.ts
│   ├── store/             # Zustand state management
│   │   └── appStore.ts
│   └── vite-env.d.ts      # TypeScript environment definitions
├── tsconfig.app.json      # TypeScript configuration
├── tsconfig.json          # TypeScript base configuration
├── tsconfig.node.json     # Node-specific TypeScript config
├── vite.config.ts         # Vite configuration
└── Dockerfile             # Docker configuration for deployment
```

### Global files

The `/src` folder contains the global files that apply to all pages, such as the layout.

### Pages

Individual pages are located in the `/pages` folder. The pages represent the accessible pages of the website.

### Components

The pages access components that are located in the `src/components/` folder. The components are building blocks that can be accessed by all pages and thus standardize the styles. By using components, the styles are consistent between the pages and only need to be changed in one place if necessary.

The components are organized thematically by category. The file names in turn supplement the folder name to specify what kind of component it is. For example, `/components/cards/WithText.tsx` contains a text card, i.e. a CardWithText.

## Common Tasks

This section provides guidance on common tasks such as adding a new page, component, or GraphQL query.

### Adding a new page

TODO

### Adding a New Component

TODO

### Adding GraphQL Queries or Mutations

TODO
