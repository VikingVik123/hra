# Interview Gen Frontend

A Vue 3 frontend for the HRA (Hiring Resource Assistant) API. Generate AI-powered interview questions with support for light and dark modes.

## Features

- ✨ **AI-Powered**: Generate interview questions using Gemini or Groq AI models
- 🌙 **Dark Mode**: Full dark mode support with persistent theme preference
- ⚡ **Vue 3**: Built with Vue 3 Composition API and Vite
- 🎨 **Tailwind CSS**: Beautiful, responsive UI with Tailwind CSS
- 📱 **Responsive**: Works perfectly on desktop, tablet, and mobile

## Prerequisites

- Node.js (v16 or higher)
- npm or yarn
- Backend API running on `http://localhost:8000`

## Installation

1. Navigate to the frontend directory:
```bash
cd frontend/clitheme
```

2. Install dependencies:
```bash
npm install
```

## Development

Start the development server:

```bash
npm run dev
```

The application will be available at `http://localhost:5173`

## Building for Production

Build the application:

```bash
npm run build
```

Preview the production build:

```bash
npm run preview
```

## Project Structure

```
clitheme/
├── src/
│   ├── App.vue           # Main application component
│   ├── main.js           # Entry point
│   └── style.css         # Global styles
├── index.html            # HTML template
├── package.json          # Dependencies
├── vite.config.js        # Vite configuration
├── tailwind.config.js    # Tailwind CSS configuration
└── postcss.config.js     # PostCSS configuration
```

## Usage

1. Enter a job title (e.g., "Senior Software Engineer")
2. Select an AI model (Gemini or Groq)
3. Click "Generate Questions"
4. View the generated interview questions
5. Toggle between dark and light modes using the theme button in the header

## Theme Preference

The application saves your theme preference in localStorage. The default mode is dark.

## Configuration

### API URL

To change the API URL, modify the `API_BASE_URL` constant in `src/App.vue`:

```javascript
const API_BASE_URL = 'http://localhost:8000'
```

## License

MIT
