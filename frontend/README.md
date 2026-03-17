# Mitly Frontend - React Application

This directory contains the React frontend for the Mitly URL shortener.

## Tech Stack
- **Framework**: React (Vite)
- **Language**: TypeScript
- **Styling**: TailwindCSS
- **API Client**: Axios
- **Routing**: React Router DOM

## Folder Structure

```shell
frontend/
├── src/
│   ├── components/   # Reusable UI building blocks (Navbar, ResultCard)
│   ├── pages/        # Main application screens (Home, RedirectHandler)
│   ├── services/     # API communication logic (urlService)
│   ├── types/        # TypeScript interfaces matching backend models
│   ├── hooks/        # Custom React hooks (if needed)
│   └── utils/        # Utility functions (if needed)
├── public/           # Static assets (logos, favicons)
└── package.json      # Dependencies & scripts
```

## Key Features

### URL Shortening
Users can input long URLs and set optional expiration days (1-365). The frontend communicates with the FastAPI backend to generate a shortened identifier.

### Redirect Handling
The `RedirectHandler` component captures short identifiers (e.g., `mitly/abc123`) and automatically redirects users to the original destination after checking with the backend for validity and expiration.

### Type Safety
TypeScript interfaces in `src/types/index.ts` are designed to match the Pydantic schemas in the backend, ensuring consistent data handling across the full stack.

## Setup & Development

### 1. Install Dependencies
Ensure you have Node.js and npm installed.
```shell
cd frontend
npm install
```

### 2. Run the Development Server
```shell
npm run dev
```
The application will be available at `http://localhost:5173`.

### 3. Backend Integration
The frontend is configured to talk to the backend at `http://localhost:8003/api/v1`. Ensure the backend is running for full functionality.

## Architectural Notes
- **Decoupled API Logic**: All API calls are isolated in `src/services/urlService.ts`, making UI components cleaner and the application easier to maintain.
- **Component-Based UI**: UI elements are broken down into reusable components in `src/components/` for consistency.
