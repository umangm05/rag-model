"use client";

import React, { useState, useCallback, useRef } from 'react';
import { Upload, Trash2, AlertCircle, CheckCircle, Clock, Loader2, FileText, Database } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { ScrollArea } from '@/components/ui/scroll-area';
import { uploadFile, getUploadedFiles, deleteFile, type UploadedFile, type UploadProgress } from '@/lib/api';
import { FILE_UPLOAD } from '@/lib/constants';

interface FileUploadProps {
  onFilesChange?: (files: UploadedFile[]) => void;
}

export function FileUpload({ onFilesChange }: FileUploadProps) {
  const [files, setFiles] = useState<UploadedFile[]>([]);
  const [uploadingFiles, setUploadingFiles] = useState<Map<string, number>>(new Map());
  const [isDragOver, setIsDragOver] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const pollingIntervalRef = useRef<NodeJS.Timeout | null>(null);

  const loadFiles = useCallback(async () => {
    try {
      const uploadedFiles = await getUploadedFiles();
      setFiles(uploadedFiles);
      onFilesChange?.(uploadedFiles);
    } catch (error) {
      console.error('Failed to load files:', error);
    }
  }, [onFilesChange]);

  // Load files on component mount
  React.useEffect(() => {
    loadFiles();
  }, [loadFiles]);

  // Poll for status updates for files that are not completed
  React.useEffect(() => {
    const hasProcessingFiles = files.some(file => 
      ['uploaded', 'queued', 'processing', 'parsing', 'embedding'].includes(file.status)
    );

    if (hasProcessingFiles) {
      pollingIntervalRef.current = setInterval(() => {
        loadFiles();
      }, 2000); // Poll every 2 seconds
    } else {
      if (pollingIntervalRef.current) {
        clearInterval(pollingIntervalRef.current);
        pollingIntervalRef.current = null;
      }
    }

    return () => {
      if (pollingIntervalRef.current) {
        clearInterval(pollingIntervalRef.current);
      }
    };
  }, [files, loadFiles]);

  const handleFileSelect = useCallback((selectedFiles: FileList | null) => {
    if (!selectedFiles) return;

    Array.from(selectedFiles).forEach(async (file) => {
      try {
        await uploadFile(file, (progress: UploadProgress) => {
          setUploadingFiles(prev => new Map(prev.set(progress.fileId, progress.progress)));
          
          if (progress.status === 'completed') {
            setUploadingFiles(prev => {
              const newMap = new Map(prev);
              newMap.delete(progress.fileId);
              return newMap;
            });
            loadFiles(); // Refresh the file list
          }
        });
      } catch (error) {
        console.error('Upload failed:', error);
        setUploadingFiles(prev => {
          const newMap = new Map(prev);
          newMap.delete(file.name);
          return newMap;
        });
      }
    });
  }, [loadFiles]);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
    handleFileSelect(e.dataTransfer.files);
  }, [handleFileSelect]);

  const handleDeleteFile = async (fileId: string) => {
    try {
      await deleteFile(fileId);
      loadFiles(); // Refresh the file list
    } catch (error) {
      console.error('Failed to delete file:', error);
    }
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const getFileIcon = (type: string) => {
    if (type.includes('pdf')) return '📄';
    if (type.includes('word') || type.includes('document')) return '📝';
    if (type.includes('text')) return '📄';
    if (type.includes('csv')) return '📊';
    if (type.includes('json')) return '🔧';
    return '📄';
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="h-4 w-4 text-green-500" />;
      case 'failed':
        return <AlertCircle className="h-4 w-4 text-red-500" />;
      case 'uploaded':
        return <Upload className="h-4 w-4 text-blue-500" />;
      case 'queued':
        return <Clock className="h-4 w-4 text-yellow-500" />;
      case 'processing':
        return <Loader2 className="h-4 w-4 text-blue-500 animate-spin" />;
      case 'parsing':
        return <FileText className="h-4 w-4 text-orange-500" />;
      case 'embedding':
        return <Database className="h-4 w-4 text-purple-500" />;
      default:
        return null;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'text-green-600';
      case 'failed':
        return 'text-red-600';
      case 'uploaded':
        return 'text-blue-600';
      case 'queued':
        return 'text-yellow-600';
      case 'processing':
        return 'text-blue-600';
      case 'parsing':
        return 'text-orange-600';
      case 'embedding':
        return 'text-purple-600';
      default:
        return 'text-gray-600';
    }
  };

  return (
    <Card className="h-full">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Upload className="h-5 w-5" />
          File Upload
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {/* Upload Area */}
        <div
          className={`border-2 border-dashed rounded-lg p-6 text-center transition-colors ${
            isDragOver
              ? 'border-primary bg-primary/5'
              : 'border-muted-foreground/25 hover:border-primary/50'
          }`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
        >
          <Upload className="h-8 w-8 mx-auto mb-2 text-muted-foreground" />
          <p className="text-sm text-muted-foreground mb-2">
            Drag and drop files here, or click to select
          </p>
          <Button
            variant="outline"
            onClick={() => fileInputRef.current?.click()}
          >
            Select Files
          </Button>
          <input
            ref={fileInputRef}
            type="file"
            multiple
            className="hidden"
            accept={FILE_UPLOAD.ALLOWED_TYPES.join(',')}
            onChange={(e) => handleFileSelect(e.target.files)}
          />
          <p className="text-xs text-muted-foreground mt-2">
            Max size: {FILE_UPLOAD.MAX_SIZE / (1024 * 1024)}MB
          </p>
        </div>

        {/* Uploading Files */}
        {uploadingFiles.size > 0 && (
          <div className="space-y-2">
            <h4 className="text-sm font-medium">Uploading...</h4>
            {Array.from(uploadingFiles.entries()).map(([fileId, progress]) => (
              <div key={fileId} className="space-y-1">
                <div className="flex items-center justify-between text-sm">
                  <span className="truncate">{fileId}</span>
                  <span>{Math.round(progress)}%</span>
                </div>
                <Progress value={progress} className="h-2" />
              </div>
            ))}
          </div>
        )}

        {/* Uploaded Files List */}
        <div className="space-y-2">
          <h4 className="text-sm font-medium">
            Uploaded Files ({files.length})
          </h4>
          <ScrollArea className="h-64">
            <div className="space-y-2">
              {files.length === 0 ? (
                <p className="text-sm text-muted-foreground text-center py-4">
                  No files uploaded yet
                </p>
              ) : (
                files.map((file) => (
                  <div
                    key={file.id}
                    className="flex items-center justify-between p-3 border rounded-lg hover:bg-accent/50 transition-colors"
                  >
                    <div className="flex items-center gap-3 min-w-0 flex-1">
                      <span className="text-lg">{getFileIcon(file.type)}</span>
                      <div className="min-w-0 flex-1">
                        <p className="text-sm font-medium truncate">
                          {file.name}
                        </p>
                        <p className="text-xs text-muted-foreground">
                          {formatFileSize(file.size)} • {file.uploadedAt.toLocaleDateString()}
                        </p>
                        {file.message && (
                          <p className={`text-xs ${getStatusColor(file.status)}`}>
                            {file.message}
                          </p>
                        )}
                        {file.error && (
                          <p className="text-xs text-red-600">
                            Error: {file.error}
                          </p>
                        )}
                        {['uploaded', 'queued', 'processing', 'parsing', 'embedding'].includes(file.status) && (
                          <div className="mt-1">
                            <Progress value={file.progress} className="h-1" />
                            <p className="text-xs text-muted-foreground mt-1">
                              {file.progress}% complete
                            </p>
                          </div>
                        )}
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      {getStatusIcon(file.status)}
                      <Button
                        variant="ghost"
                        size="icon"
                        onClick={() => handleDeleteFile(file.id)}
                        className="h-8 w-8 text-muted-foreground hover:text-destructive"
                      >
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                ))
              )}
            </div>
          </ScrollArea>
        </div>
      </CardContent>
    </Card>
  );
}
