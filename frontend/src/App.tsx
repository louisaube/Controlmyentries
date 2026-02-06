import { DropZone, FileCard, StatusMessage } from '@/components'
import { useFileUpload } from '@/hooks'
import { useState } from 'react'
import { FileRejection } from 'react-dropzone'

function App() {
  const { files, addFiles, removeFile, updateFileStatus, clearFiles } = useFileUpload()
  const [error, setError] = useState<string | null>(null)

  const handleFilesAccepted = async (acceptedFiles: File[]) => {
    setError(null)
    addFiles(acceptedFiles)

    // Simulate validation (will be replaced with API call)
    for (const file of acceptedFiles) {
      const fileId = files.find(f => f.name === file.name)?.id
      if (fileId) {
        // Simulate async validation
        setTimeout(() => {
          updateFileStatus(fileId, 'validated')
        }, 500)
      }
    }
  }

  const handleFilesRejected = (rejections: FileRejection[]) => {
    const messages = rejections.map(r =>
      `${r.file.name}: ${r.errors.map(e => e.message).join(', ')}`
    )
    setError(messages.join('; '))
  }

  const hasFiles = files.length > 0
  const allValidated = files.length > 0 && files.every(f => f.status === 'validated')
  const hasGL = files.some(f => f.type === 'gl')

  return (
    <main className="min-h-screen bg-gray-50 py-12 px-4">
      <div className="max-w-2xl mx-auto">
        {/* Header */}
        <header className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Controlmyentries
          </h1>
          <p className="text-gray-600">
            Outil de detection d'anomalies budgetaires
          </p>
        </header>

        {/* Instructions */}
        <div className="mb-6 p-4 bg-white rounded-lg shadow-sm">
          <h2 className="text-sm font-medium text-gray-700 mb-2">
            Comment utiliser cet outil :
          </h2>
          <ol className="text-sm text-gray-600 list-decimal list-inside space-y-1">
            <li>Deposez votre fichier Grand Livre (GL) au format Excel ou CSV</li>
            <li>Optionnel : ajoutez un fichier baseline.json pour une analyse statistique complete</li>
            <li>Cliquez sur "Analyser" pour lancer la detection d'anomalies</li>
          </ol>
        </div>

        {/* Error Message */}
        {error && (
          <div className="mb-6">
            <StatusMessage
              type="error"
              title="Erreur lors du depot de fichier"
              message={error}
              onDismiss={() => setError(null)}
            />
          </div>
        )}

        {/* Drop Zone */}
        <div className="mb-6">
          <DropZone
            onFilesAccepted={handleFilesAccepted}
            onFilesRejected={handleFilesRejected}
            maxFiles={2}
            disabled={files.length >= 2}
          />
        </div>

        {/* File List */}
        {hasFiles && (
          <div className="mb-6 space-y-3" role="list" aria-label="Fichiers selectionnes">
            {files.map((file) => (
              <FileCard
                key={file.id}
                file={file}
                onRemove={removeFile}
              />
            ))}
          </div>
        )}

        {/* Action Buttons */}
        {hasFiles && (
          <div className="flex gap-3 justify-center">
            <button
              type="button"
              onClick={clearFiles}
              className="
                px-6 py-3 text-sm font-medium
                text-gray-700 bg-white border border-gray-300 rounded-lg
                hover:bg-gray-50
                focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500
                min-w-[44px] min-h-[44px]
              "
            >
              Effacer
            </button>
            <button
              type="button"
              disabled={!allValidated || !hasGL}
              className="
                px-6 py-3 text-sm font-medium
                text-white bg-primary-600 rounded-lg
                hover:bg-primary-700
                focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500
                disabled:opacity-50 disabled:cursor-not-allowed
                min-w-[44px] min-h-[44px]
              "
            >
              Analyser
            </button>
          </div>
        )}

        {/* Disclaimer (FR25) */}
        <footer className="mt-12 text-center text-xs text-gray-500">
          <p>
            Aide a la detection, pas certificat d'absence d'anomalie.
          </p>
        </footer>
      </div>
    </main>
  )
}

export default App
