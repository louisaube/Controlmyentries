import { UploadedFile } from '@/types'

interface FileCardProps {
  file: UploadedFile
  onRemove?: (id: string) => void
}

function formatFileSize(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
}

function getFileTypeLabel(type: 'gl' | 'baseline'): string {
  return type === 'gl' ? 'Grand Livre' : 'Baseline'
}

function getFileTypeIcon(type: 'gl' | 'baseline'): string {
  return type === 'gl' ? 'table' : 'chart'
}

export function FileCard({ file, onRemove }: FileCardProps) {
  const isValidated = file.status === 'validated'
  const isError = file.status === 'error'
  const isPending = file.status === 'pending'

  return (
    <div
      className={`
        relative flex items-center gap-4 p-4 rounded-lg border
        ${isValidated ? 'border-success-500 bg-success-50' : ''}
        ${isError ? 'border-error-500 bg-error-50' : ''}
        ${isPending ? 'border-gray-200 bg-gray-50' : ''}
      `}
      role="listitem"
      aria-label={`Fichier ${file.name}, type ${getFileTypeLabel(file.type)}, statut ${file.status}`}
    >
      {/* File Type Icon */}
      <div className={`
        w-12 h-12 rounded-lg flex items-center justify-center
        ${isValidated ? 'bg-success-100' : ''}
        ${isError ? 'bg-error-100' : ''}
        ${isPending ? 'bg-gray-100' : ''}
      `}>
        {getFileTypeIcon(file.type) === 'table' ? (
          <svg className="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 10h18M3 14h18m-9-4v8m-7 0h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
          </svg>
        ) : (
          <svg className="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
        )}
      </div>

      {/* File Info */}
      <div className="flex-1 min-w-0">
        <p className="text-sm font-medium text-gray-900 truncate">
          {file.name}
        </p>
        <p className="text-xs text-gray-500">
          {getFileTypeLabel(file.type)} - {formatFileSize(file.size)}
        </p>
        {isError && file.errorMessage && (
          <p
            className="mt-1 text-xs text-error-600"
            role="alert"
          >
            {file.errorMessage}
          </p>
        )}
      </div>

      {/* Status Indicator */}
      <div className="flex items-center gap-2">
        {isPending && (
          <div className="w-5 h-5 border-2 border-gray-300 border-t-primary-500 rounded-full animate-spin" aria-label="Validation en cours" />
        )}
        {isValidated && (
          <svg className="w-5 h-5 text-success-500" fill="currentColor" viewBox="0 0 20 20" aria-label="Valide">
            <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
          </svg>
        )}
        {isError && (
          <svg className="w-5 h-5 text-error-500" fill="currentColor" viewBox="0 0 20 20" aria-label="Erreur">
            <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
          </svg>
        )}

        {/* Remove Button */}
        {onRemove && (
          <button
            type="button"
            onClick={() => onRemove(file.id)}
            className="
              p-1 rounded-full text-gray-400 hover:text-gray-600 hover:bg-gray-200
              focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500
              min-w-[24px] min-h-[24px]
            "
            aria-label={`Supprimer ${file.name}`}
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        )}
      </div>
    </div>
  )
}
