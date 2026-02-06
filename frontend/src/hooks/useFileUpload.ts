import { useState, useCallback } from 'react'
import { UploadedFile } from '@/types'

interface UseFileUploadReturn {
  files: UploadedFile[]
  addFiles: (newFiles: File[]) => void
  removeFile: (id: string) => void
  updateFileStatus: (id: string, status: UploadedFile['status'], errorMessage?: string) => void
  clearFiles: () => void
  canSubmit: boolean
}

function generateId(): string {
  return Math.random().toString(36).substring(2, 9)
}

function detectFileType(file: File): 'gl' | 'baseline' {
  // JSON files are always baseline
  if (file.name.endsWith('.json')) {
    return 'baseline'
  }
  // Excel/CSV files are GL
  return 'gl'
}

export function useFileUpload(): UseFileUploadReturn {
  const [files, setFiles] = useState<UploadedFile[]>([])

  const addFiles = useCallback((newFiles: File[]) => {
    const uploadedFiles: UploadedFile[] = newFiles.map((file) => ({
      id: generateId(),
      name: file.name,
      size: file.size,
      type: detectFileType(file),
      status: 'pending',
    }))
    setFiles((prev) => [...prev, ...uploadedFiles])
  }, [])

  const removeFile = useCallback((id: string) => {
    setFiles((prev) => prev.filter((f) => f.id !== id))
  }, [])

  const updateFileStatus = useCallback(
    (id: string, status: UploadedFile['status'], errorMessage?: string) => {
      setFiles((prev) =>
        prev.map((f) =>
          f.id === id
            ? { ...f, status, errorMessage }
            : f
        )
      )
    },
    []
  )

  const clearFiles = useCallback(() => {
    setFiles([])
  }, [])

  // Can submit when we have at least one GL file and all files are validated
  const hasGL = files.some((f) => f.type === 'gl')
  const allValidated = files.length > 0 && files.every((f) => f.status === 'validated')
  const canSubmit = hasGL && allValidated

  return {
    files,
    addFiles,
    removeFile,
    updateFileStatus,
    clearFiles,
    canSubmit,
  }
}
