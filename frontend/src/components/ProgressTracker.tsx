import { ProgressData } from '@/types'

interface ProgressTrackerProps {
  progress: ProgressData
}

const STEPS = [
  { name: 'Validation', icon: '1' },
  { name: 'Pass 1', icon: '2' },
  { name: 'Pass 2', icon: '3' },
  { name: 'Rapport', icon: '4' },
  { name: 'Termine', icon: '5' },
]

export function ProgressTracker({ progress }: ProgressTrackerProps) {
  const currentStep = progress.step

  return (
    <div
      className="p-6 bg-white rounded-xl shadow-sm"
      role="progressbar"
      aria-valuenow={progress.progress * 100}
      aria-valuemin={0}
      aria-valuemax={100}
      aria-label={`Progression: ${progress.stepName}`}
    >
      {/* Step indicators */}
      <div className="flex items-center justify-between mb-6">
        {STEPS.map((step, index) => {
          const stepNum = index + 1
          const isActive = stepNum === currentStep
          const isComplete = stepNum < currentStep
          const isPending = stepNum > currentStep

          return (
            <div key={step.name} className="flex flex-col items-center">
              <div
                className={`
                  w-10 h-10 rounded-full flex items-center justify-center
                  text-sm font-medium transition-all duration-300
                  ${isComplete ? 'bg-success-500 text-white' : ''}
                  ${isActive ? 'bg-primary-500 text-white animate-pulse' : ''}
                  ${isPending ? 'bg-gray-200 text-gray-500' : ''}
                `}
              >
                {isComplete ? (
                  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
                    <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                  </svg>
                ) : (
                  step.icon
                )}
              </div>
              <span className={`
                mt-2 text-xs
                ${isActive ? 'text-primary-600 font-medium' : 'text-gray-500'}
              `}>
                {step.name}
              </span>
            </div>
          )
        })}
      </div>

      {/* Progress bar */}
      <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
        <div
          className="h-full bg-primary-500 transition-all duration-500 ease-out"
          style={{ width: `${progress.progress * 100}%` }}
        />
      </div>

      {/* Current step info */}
      <div className="mt-4 flex items-center justify-between text-sm">
        <span className="text-gray-600">{progress.stepName}</span>
        <span className="font-medium text-primary-600">
          {Math.round(progress.progress * 100)}%
        </span>
      </div>

      {/* Anomaly counter */}
      {progress.anomaliesFound > 0 && (
        <div
          className="mt-4 p-3 bg-warning-50 rounded-lg flex items-center gap-2"
          aria-live="polite"
        >
          <svg className="w-5 h-5 text-warning-500" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
            <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
          </svg>
          <span className="text-warning-700">
            <strong className="text-lg">{progress.anomaliesFound}</strong> anomalie{progress.anomaliesFound > 1 ? 's' : ''} detectee{progress.anomaliesFound > 1 ? 's' : ''}
          </span>
        </div>
      )}
    </div>
  )
}
