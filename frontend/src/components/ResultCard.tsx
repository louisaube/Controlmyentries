import { AnalysisResult } from '@/types'

interface ResultCardProps {
  result: AnalysisResult
  onDownload: () => void
  onNewAnalysis: () => void
}

export function ResultCard({ result, onDownload, onNewAnalysis }: ResultCardProps) {
  const formatTime = (ms: number): string => {
    if (ms < 1000) return `${ms}ms`
    const seconds = Math.round(ms / 1000)
    return `${seconds}s`
  }

  return (
    <div className="p-6 bg-white rounded-xl shadow-sm">
      {/* Success header */}
      <div className="flex items-center gap-3 mb-6">
        <div className="w-12 h-12 bg-success-100 rounded-full flex items-center justify-center">
          <svg className="w-6 h-6 text-success-500" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
          </svg>
        </div>
        <div>
          <h2 className="text-lg font-semibold text-gray-900">
            Analyse terminee
          </h2>
          <p className="text-sm text-gray-500">
            en {formatTime(result.processingTime)}
          </p>
        </div>
      </div>

      {/* Metrics grid */}
      <div className="grid grid-cols-2 gap-4 mb-6">
        <div className="p-4 bg-gray-50 rounded-lg">
          <p className="text-2xl font-bold text-gray-900">{result.anomalyCount}</p>
          <p className="text-sm text-gray-600">Anomalies detectees</p>
        </div>
        <div className="p-4 bg-gray-50 rounded-lg">
          <p className="text-2xl font-bold text-gray-900">{result.confidence}%</p>
          <p className="text-sm text-gray-600">Indice de confiance</p>
        </div>
      </div>

      {/* Confidence warning if low */}
      {result.confidence < 50 && (
        <div className="mb-6 p-4 bg-warning-50 rounded-lg">
          <div className="flex items-start gap-3">
            <svg className="w-5 h-5 text-warning-500 mt-0.5" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
              <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
            <div>
              <p className="text-sm font-medium text-warning-800">Confiance limitee</p>
              <p className="text-sm text-warning-700">
                Fournissez une baseline avec plus de donnees historiques pour une analyse plus fiable.
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Action buttons */}
      <div className="flex gap-3">
        <button
          type="button"
          onClick={onDownload}
          className="
            flex-1 px-6 py-3 text-sm font-medium
            text-white bg-primary-600 rounded-lg
            hover:bg-primary-700
            focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500
            flex items-center justify-center gap-2
            min-h-[44px]
          "
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
          </svg>
          Telecharger le rapport
        </button>
        <button
          type="button"
          onClick={onNewAnalysis}
          className="
            px-6 py-3 text-sm font-medium
            text-gray-700 bg-gray-100 rounded-lg
            hover:bg-gray-200
            focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500
            min-h-[44px]
          "
        >
          Nouvelle analyse
        </button>
      </div>

      {/* Disclaimer */}
      <p className="mt-6 text-xs text-gray-500 text-center">
        Aide a la detection, pas certificat d'absence d'anomalie.
      </p>
    </div>
  )
}
