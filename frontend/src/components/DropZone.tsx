import { useCallback, useState } from 'react'
import { useDropzone, FileRejection } from 'react-dropzone'

interface DropZoneProps {
  onFilesAccepted: (files: File[]) => void
  onFilesRejected?: (rejections: FileRejection[]) => void
  maxFiles?: number
  disabled?: boolean
}

const ACCEPTED_TYPES = {
  'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
  'application/vnd.ms-excel': ['.xls'],
  'text/csv': ['.csv'],
  'application/json': ['.json'],
}

export function DropZone({
  onFilesAccepted,
  onFilesRejected,
  maxFiles = 2,
  disabled = false,
}: DropZoneProps) {
  const [isDragActive, setIsDragActive] = useState(false)

  const onDrop = useCallback(
    (acceptedFiles: File[], rejectedFiles: FileRejection[]) => {
      if (acceptedFiles.length > 0) {
        onFilesAccepted(acceptedFiles)
      }
      if (rejectedFiles.length > 0 && onFilesRejected) {
        onFilesRejected(rejectedFiles)
      }
    },
    [onFilesAccepted, onFilesRejected]
  )

  const { getRootProps, getInputProps, open } = useDropzone({
    onDrop,
    accept: ACCEPTED_TYPES,
    maxFiles,
    disabled,
    onDragEnter: () => setIsDragActive(true),
    onDragLeave: () => setIsDragActive(false),
    noClick: false,
    noKeyboard: false,
  })

  return (
    <div
      {...getRootProps()}
      role="button"
      aria-label="Zone de depot de fichiers. Glissez-deposez ou cliquez pour selectionner."
      tabIndex={0}
      className={`
        relative p-8 border-2 border-dashed rounded-xl
        transition-all duration-200 ease-in-out
        cursor-pointer
        focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 focus-visible:ring-offset-2
        ${isDragActive
          ? 'border-primary-500 bg-primary-50 scale-[1.02]'
          : 'border-gray-300 hover:border-primary-400 hover:bg-gray-50'
        }
        ${disabled ? 'opacity-50 cursor-not-allowed' : ''}
      `}
    >
      <input {...getInputProps()} aria-hidden="true" />

      <div className="flex flex-col items-center justify-center gap-4 text-center">
        {/* Upload Icon */}
        <div className={`
          w-16 h-16 rounded-full flex items-center justify-center
          ${isDragActive ? 'bg-primary-100' : 'bg-gray-100'}
        `}>
          <svg
            className={`w-8 h-8 ${isDragActive ? 'text-primary-600' : 'text-gray-400'}`}
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            aria-hidden="true"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
            />
          </svg>
        </div>

        {/* Instructions */}
        <div>
          <p className="text-lg font-medium text-gray-700">
            {isDragActive
              ? 'Deposez vos fichiers ici...'
              : 'Glissez-deposez vos fichiers ici'
            }
          </p>
          <p className="mt-1 text-sm text-gray-500">
            ou cliquez pour selectionner
          </p>
        </div>

        {/* File type hint */}
        <p className="text-xs text-gray-400">
          Formats acceptes: Excel (.xlsx, .xls), CSV, JSON (baseline)
        </p>

        {/* Alternative button for accessibility (FR31) */}
        <button
          type="button"
          onClick={(e) => {
            e.stopPropagation()
            open()
          }}
          disabled={disabled}
          className="
            mt-2 px-4 py-2 text-sm font-medium
            text-primary-600 bg-primary-50 rounded-lg
            hover:bg-primary-100
            focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500
            disabled:opacity-50 disabled:cursor-not-allowed
            min-w-[44px] min-h-[44px]
          "
          aria-label="Choisir fichier(s) depuis votre ordinateur"
        >
          Choisir fichier(s)
        </button>
      </div>
    </div>
  )
}
