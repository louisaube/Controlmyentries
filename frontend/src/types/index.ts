/**
 * Shared types for Controlmyentries frontend
 */

export type AppState = 'idle' | 'uploading' | 'processing' | 'complete' | 'error';

export interface UploadedFile {
  id: string;
  name: string;
  size: number;
  type: 'gl' | 'baseline';
  status: 'pending' | 'validated' | 'error';
  errorMessage?: string;
}

export interface ProgressData {
  step: number;
  stepName: string;
  progress: number;
  anomaliesFound: number;
  status: 'processing' | 'complete' | 'error';
}

export interface AnalysisResult {
  success: boolean;
  downloadUrl: string;
  anomalyCount: number;
  processingTime: number;
  confidence: number;
}

export interface ErrorData {
  type: string;
  title: string;
  status: number;
  detail: string;
}
