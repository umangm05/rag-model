"use client";

import React, { useState } from 'react';
import { FileUpload } from '@/components/file-upload';
import { ChatInterface } from '@/components/chat-interface';
import { type UploadedFile } from '@/lib/api';

export default function Home() {
  const [uploadedFiles, setUploadedFiles] = useState<UploadedFile[]>([]);

  const handleFilesChange = (files: UploadedFile[]) => {
    setUploadedFiles(files);
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold">RAG Document Assistant</h1>
              <p className="text-sm text-muted-foreground">
                Upload documents and chat with your content
              </p>
            </div>
            <div className="text-sm text-muted-foreground">
              {uploadedFiles.length > 0 && (
                <span>{uploadedFiles.length} file{uploadedFiles.length !== 1 ? 's' : ''} uploaded</span>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-6 h-[calc(100vh-88px)] overflow-hidden">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 h-full">
          {/* Left Column - File Upload */}
          <div className="h-full overflow-hidden">
            <FileUpload onFilesChange={handleFilesChange} />
          </div>

          {/* Right Column - Chat Interface */}
          <div className="h-full overflow-hidden">
            <ChatInterface />
          </div>
        </div>
      </main>
    </div>
  );
}
