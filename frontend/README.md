# RAG Document Assistant - Frontend

A modern React/Next.js frontend application for uploading documents and chatting with AI about their content.

## Features

- **File Upload**: Drag and drop or click to upload documents with progress tracking
- **Chat Interface**: Real-time chat with AI assistant about uploaded documents
- **Responsive Design**: Two-column layout that adapts to different screen sizes
- **Modern UI**: Built with shadcn/ui components and Tailwind CSS
- **Mock APIs**: Complete mock implementation for development

## Tech Stack

- **Framework**: Next.js 15 with React 19
- **Styling**: Tailwind CSS v4
- **UI Components**: shadcn/ui v4
- **Icons**: Lucide React
- **TypeScript**: Full type safety

## Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn

### Installation

1. Install dependencies:
```bash
npm install
```

2. Set up environment variables:
```bash
cp env.example .env.local
```

Edit `.env.local` with your configuration:
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_API_VERSION=v1
```

3. Start the development server:
```bash
npm run dev
```

4. Open [http://localhost:3000](http://localhost:3000) in your browser.

## Project Structure

```
src/
├── app/                    # Next.js app directory
│   ├── globals.css        # Global styles
│   ├── layout.tsx         # Root layout
│   └── page.tsx           # Home page
├── components/            # React components
│   ├── ui/               # shadcn/ui components
│   ├── file-upload.tsx   # File upload component
│   └── chat-interface.tsx # Chat interface component
└── lib/                  # Utilities and API
    ├── api.ts           # Mock API functions
    ├── constants.ts     # API endpoints and constants
    └── utils.ts         # Utility functions
```

## API Integration

The application is designed to work with a backend API. Currently, it uses mock implementations:

### File Upload API
- `POST /api/v1/files/upload` - Upload files
- `GET /api/v1/files` - List uploaded files
- `DELETE /api/v1/files/:id` - Delete a file

### Chat API
- `POST /api/v1/chat/message` - Send a message
- `GET /api/v1/chat/messages` - Get chat history

### Replacing Mock APIs

To integrate with a real backend:

1. Update the API base URL in your environment variables
2. Replace the mock functions in `src/lib/api.ts` with actual HTTP requests
3. Update types if needed based on your backend response format

## File Upload Configuration

Supported file types:
- PDF documents
- Text files (.txt)
- Word documents (.doc, .docx)
- CSV files
- JSON files

Maximum file size: 10MB

## Development

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint

### Code Standards

- TypeScript for type safety
- ESLint for code quality
- Tailwind CSS for styling
- Component-based architecture
- Proper error handling and loading states

## Deployment

1. Build the application:
```bash
npm run build
```

2. Start the production server:
```bash
npm start
```

Or deploy to platforms like Vercel, Netlify, or any Node.js hosting service.

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_BASE_URL` | Backend API base URL | `http://localhost:8000` |
| `NEXT_PUBLIC_API_VERSION` | API version | `v1` |

## Contributing

1. Follow the existing code style
2. Add TypeScript types for new features
3. Test components thoroughly
4. Update documentation as needed

## License

This project is part of the RAG Model application.